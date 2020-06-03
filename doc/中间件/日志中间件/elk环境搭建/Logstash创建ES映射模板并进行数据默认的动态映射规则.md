
* 先拿一个 logstash 的配置文件来看一下
```java
output {
  elasticsearch {
    hosts => “localhost:9200"
    index => "my_index"
    template => "/data1/cloud/logstash-5.5.1/filebeat-template.json"
    template_name => "my_index"
    template_overwrite => true
  }
  stdout { codec => rubydebug }
}
```
* 再看一个ES模板配置文件
```java
{
  "template" : "logstash*",
  "settings" : {
    "index.number_of_shards" : 5,
    "number_of_replicas" : 1,
    "index.refresh_interval" : "60s"
  },
  "mappings" : {
    "_default_" : {
       "_all" : {"enabled" : true},
       "dynamic_templates" : [ {
         "string_fields" : {
           "match" : "*",
           "match_mapping_type" : "string",
           "mapping" : {
             "type" : "string", "index" : "not_analyzed", "omit_norms" : true, "doc_values": true,
               "fields" : {
                 "raw" : {"type": "string", "index" : "not_analyzed", "ignore_above" : 256,"doc_values": true}
               }
           }
         }
       } ],
       "properties" : {
         "@version": { "type": "string", "index": "not_analyzed" },
         "geoip"  : {
           "type" : "object",
             "dynamic": true,
             "path": "full",
             "properties" : {
               "location" : { "type" : "geo_point" }
             }
         }
       }
    }
  }
}
```
```text
这里关注几个属性index、template_name、以及模板文件中的 template。index是索引的名称，我们经常会有诸如 index => "logstash-%{+YYYY.MM
.dd}”这样的索引名称，可以按照日期来分割不同的索引。template_name对应的是模板名称，template这是比较关键的，因为决定了索引是否能够匹
配到模板配置，这里应该与 index相匹配。比如固定的 index 名称，这里就可以是固定名称。对于按日期分隔的，可以使用通配符，例如logstash-*。
```