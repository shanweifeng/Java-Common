## filebeat 安装
wget https://download.elastic.co/beats/filebeat/filebeat-1.3.0-x86_64.tar.gz
tar -zxvf filebeat-1.3.0-x86_64.tar.gz
```text
环境说明：
1）elasticsearch和logstash 在不同的服务器上,只发送数据给logstash
2）监控nginx日志
3）监控支付日志
4）监控订单日志
```
```text
filebeat: 
  prospectors:
  -
      paths:
        - /www/wwwLog/www.lanmps.com_old/*.log
        - /www/wwwLog/www.lanmps.com/*.log
      input_type: log 
      document_type: nginx-access-www.lanmps.com
 -
      paths:
        - /www/wwwRUNTIME/www.lanmps.com/order/*.log
      input_type: log 
      document_type: order-www.lanmps.com
  -
      paths:
        - /www/wwwRUNTIME/www.lanmps.com/pay/*.log
      input_type: log 
      document_type: pay-www.lanmps.com
output:
  #elasticsearch:
  #   hosts: ["localhost:9200"]
   logstash:
    hosts: ["10.1.5.65:5044"]

```

* 启动测试 ./filebeat -e -c filebeat.yml -d "Publish"

* 启动 nohup ./filebeat -e -c filebeat.yml >/dev/null 2>&1 & 转入后台运行