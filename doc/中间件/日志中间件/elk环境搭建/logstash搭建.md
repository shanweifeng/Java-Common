```text
命令：docker pull docker.elastic.co/logstash/logstash:7.2.0 拉取镜像
命令：docker run --name logstash -p 5044:5044 docker.elastic.co/logstash/logstash:7.2.0 创建并启动简易容器


-- 将简易容器中的配置、pipeline、日志和数据目录分别映射到宿主机相关位置
命令：docker cp efaf5cd489f7:/usr/share/logstash/config/ /opt/logstash/node/
命令：docker cp efaf5cd489f7:/usr/share/logstash/pipeline/ /opt/logstash/
#命令：docker cp efaf5cd489f7:/usr/share/logstash/logs/ /opt/logstash/node/
命令：docker cp efaf5cd489f7:/usr/share/logstash/data/ /opt/logstash/node/


-- 启动映射后的容器
命令：docker run --name logstash1 -p 5044:5044 -v /opt/logstash/node1/config/:/usr/share/logstash/config/ -v /opt/logstash/node1/data/:/usr/share/logstash/data/ -v /opt/logstash/node1/logs/:/usr/share/logstash/logs/ -v /opt/logstash/pipeline/:/usr/share/logstash/pipeline/  docker.elastic.co/logstash/logstash:7.2.0
```

```java
input {
  beats {
    port => 5044
    codec => json
  }
}

filter {
  useragent {
    target => "ua"
    source => "useragent"
  }
  mutate {
    remove_field => ["useragent"]
  }

  if ![url] {
    drop{}
  }
  if [domain] != "test.b43.cn" and [domain] != "test.pay.b43.cn" {
    drop{}
  }

  ruby {
    code => "event.set('timestamp', event.get('@timestamp').time.localtime + 8*60*60)"
  }
  ruby {
    code => "event.set('@timestamp',event.get('timestamp'))"
  }
  mutate {
    remove_field => ["timestamp"]
  }
  mutate {
    add_field => {"hostname" => "%{[beat][hostname]}"}
  }
  mutate {
    remove_field => ["tags", "beat", "host", "message", "meta", "@version", "input", "prospector"]
  }
  urldecode {
    field => body
  }
  urldecode {
    field => referer
  }
  if [referer] == "-" {
    mutate {
      update => { "referer" => ""}
    }
  }
  if [body] == "-" {
    mutate {
      update => { "body" => ""}
    }
  }
  if [args] == "-" {
    mutate {
      update => { "args" => ""}
    }
  }

  if [cookie] =~ /SESSION=([A-Z0-9]*)/ {
    grok {
      match => {
        "cookie" => "(?<cookieId>(?<=SESSION=)([a-zA-Z0-9]*))"
      }
    }
  } else {
    mutate {
      add_field => {"cookieId" => ""}
    }
  }

  if [cookie] =~ /UM_distinctid=([a-zA-Z0-9-]*)/ {
    grok {
      match => {
        "cookie" => "(?<umId>(?<=UM_distinctid=)([a-zA-Z0-9-]*))"
      }
    }
  } else {
    mutate {
      add_field => {"umId" => ""}
    }
  }

  mutate {
    remove_field => ["cookie"]
  }

  if [url] =~ /^\/api\/trackView\//{
    mutate {
      replace => { "eventType" => "page" }
    }
  } else if  [url] =~ /^\/api\/trackClick\// {
    mutate {
      replace => { "eventType" => "click" }
    }
  } else if [url] =~ /^\/api\// {
    mutate {
      replace => { "eventType" => "api"}
    }
  } else if [url] =~ /^\/stylesheet\// or [url] =~ /^\/js\// or [url] =~ /^\/css\// or [url] =~ /^\/img\// or [url] =~ /^\/image\// {
    mutate {
      replace => { "eventType" => "resource"}
    }
  } else {
    mutate {
      replace => { "eventType" => "other"}
    }
  }

  mutate {
    split => ["proxy", ","]
  }

  if [proxy][0] =~ /(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)/ {
    mutate {
      update => {"ip" => "%{[proxy][0]}"}
    }
  }
  mutate {
    join => ["proxy", ","]
  }
  geoip {
    source => "ip"
    fields => ["country_name", "region_name", "city_name", "ip", "latitude", "longitude"]
  }
  if [eventType] == "page" {
    if "?" in [referer] {
        grok {
           match => {
            "referer" => "(?<url_temp>(.*)(?=\?)/?)"
           }
         }
    mutate {
        update => { "url" => "%{[url_temp]}"}
      }
    } else {
        mutate {
          update => { "url" => "%{[referer]}"}
        }
    }
  }
  mutate {
      convert => ["responseTime", "float"]
  }
}
output {
  if [from] == "mall" {
    elasticsearch {
      hosts => ["192.168.27.129:9201","192.168.27.129:9202","192.168.27.129:9203",] # logstash数据传输的es地址
      index => "nginx-saas-log-%{+YYYY.MM}"  # 动态索引名称
      document_type => "_doc"  # 索引对应的type名称
      template_overwrite => true # index template是否覆盖
    }
  }
}
```