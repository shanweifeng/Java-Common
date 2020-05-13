## [nginx日志查看](https://www.php.cn/nginx/423530.html)

* 1、通过浏览器查看
> 通过web界面查看时Nginx需要开启status模块，也就是安装Nginx时加上 --with-http_stub_status_module 然后配置Nginx.conf，在server点里面加入如下内容
```text
location /status {
stub_status on;
access_log /usr/local/nginx/logs/status.log;
auth_basic "NginxStatus"; }
```
>解析:
```text
Active connections    //当前 Nginx 正处理的活动连接数。
server accepts handledrequests //总共处理了8 个连接 , 成功创建 8 次握手,总共处理了500个请求。
Reading //nginx 读取到客户端的 Header 信息数。
Writing //nginx 返回给客户端的 Header 信息数。
Waiting //开启 keep-alive 的情况下，这个值等于 active - (reading + writing)，意思就是 Nginx 已经处理完正在等候下一次请求指令的驻留连接
```

* 2、通过命令查看
```text
netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'
```
> 解析：
```text
CLOSED  //无连接是活动的或正在进行
LISTEN  //服务器在等待进入呼叫
SYN_RECV  //一个连接请求已经到达，等待确认
SYN_SENT  //应用已经开始，打开一个连接
ESTABLISHED  //正常数据传输状态/当前并发连接数
FIN_WAIT1  //应用说它已经完成
FIN_WAIT2  //另一边已同意释放
ITMED_WAIT  //等待所有分组死掉
CLOSING  //两边同时尝试关闭
TIME_WAIT  //另一边已初始化一个释放
LAST_ACK  //等待所有分组死掉
```

* 3、nginx 访问量统计
```text
* 1.根据访问IP统计UV
awk '{print $1}'  access.log|sort | uniq -c |wc -l

* 2.统计访问URL统计PV
awk '{print $7}' access.log|wc -l

* 3.查询访问最频繁的URL
awk '{print $7}' access.log|sort | uniq -c |sort -n -k 1 -r|more

* 4.查询访问最频繁的IP
awk '{print $1}' access.log|sort | uniq -c |sort -n -k 1 -r|more

* 5.根据时间段统计查看日志
cat  access.log| sed -n '/14\/Mar\/2015:21/,/14\/Mar\/2015:22/p'|more

* 查找访问频率最高的 URL 和次数：
cat access.log | awk -F ‘^A’ ‘{print $10}’ | sort | uniq -c

* 查找当前日志文件 500 错误的访问：
cat access.log | awk -F ‘^A’ ‘{if（$5 == 500） print $0}’

* 查找当前日志文件 500 错误的数量：
cat access.log | awk -F ‘^A’ ‘{if（$5 == 500） print $0}’ | wc -l

* 查找某一分钟内 500 错误访问的数量：
cat access.log | awk -F ‘^A’ ‘{if（$5 == 500） print $0}’ | grep ’09:00’ | wc-l

* 查找耗时超过 1s 的慢请求：
tail -f access.log | awk -F ‘^A’ ‘{if（$6》1） print $0}’

* 假如只想查看某些位：
tail -f access.log | awk -F ‘^A’ ‘{if（$6》1） print $3″|”$4}’

* 查找 502 错误最多的 URL：
cat access.log | awk -F ‘^A’ ‘{if（$5==502） print $11}’ | sort | uniq -c

* 查找 200 空白页
cat access.log | awk -F ‘^A’ ‘{if（$5==200 && $8 《 100） print $3″|”$4″|”$11″|”$6}’

* 查看实时日志数据流
tail -f access.log | cat -e
或者
tail -f access.log | tr ‘^A’ ‘|’
sed -n '/04\/Dec\/2015:07:30:53/,/04\/Dec\/2015:08:30:55/'p access.log | more  查看一段时间的日志
sed -n '/08\/Dec\/2015:15:48:01/,/08\/Dec\/2015:15:55:59/p' access.log > new.log
```

