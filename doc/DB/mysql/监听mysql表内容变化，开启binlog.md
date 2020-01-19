### [监听mysql二进制日志文件(binlog, binary log)](https://blog.csdn.net/tianyaleixiaowu/article/details/79652903)
> mysql的binlog默认是关闭的，需要修改mysql配置文件来开启
```java
[mysqlId]
server_id = 1
log-bin = mysql-bin
binlog-format = ROW
```
>mysql-bin只是一个名称，后面保存的日志文件名就是mysql-bin.000001,mysql-bin.000002这样的。<p>
注意binlog_format必须设置为ROW，因为在STATEMENT或MIXED模式下，Binlog只会记录和传输sql语句(以减少日志大小)，而不包含具体数据。<p>
然后通过 brew restart mysql 重启mysql 通过mysql -uroot -p命令进入mysql控制台，执行*show variables like '%log_bin%';*<p>
flush logs 刷新binlog日志文件<p>
reset master 情况日志文件<p>
show binlog events 查看第一个binlog文件内容<p>
show binlog events in 'mysql-bin.000004' 查看指定binlog文件内容<p>
show binary logs 获取binlog文件列表

### [canal 监听mysql表内容变化](https://blog.csdn.net/tianyaleixiaowu/article/details/79653829)
[canal github地址](https://github.com/alibaba/canal)
> mysql 本身支持主从(master slave),原理就是master产生的binlog日志记录了所有正删改语句，将binlog发送到slave节点进行执行即可完成数据同步。。
#####原理
1. canal 模拟mysql slave的交互协议，伪装自己为mysql slave，向mysql master发送dump协议
2. master收到dump请求，开始推送binary log给slave(canal)
3. canal 解析binary log对象(原始为byte流)
