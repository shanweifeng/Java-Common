## [filebeat配置](https://www.elastic.co/guide/en/beats/filebeat/7.2/filebeat-input-log.html)

* paths：指定要监控的日志，目前按照Go语言的glob函数处理。没有对配置目录做递归处理，比如配置的如果是：
* encoding：指定被监控的文件的编码类型，使用plain和utf-8都是可以处理中文日志的。
* input_type：指定文件的输入类型log(默认)或者stdin。
* exclude_lines：在输入中排除符合正则表达式列表的那些行。
* include_lines：包含输入中符合正则表达式列表的那些行（默认包含所有行），include_lines执行完毕之后会执行exclude_lines。
* exclude_files：忽略掉符合正则表达式列表的文件（默认为每一个符合paths定义的文件都创建一个harvester）。
* fields：向输出的每一条日志添加额外的信息，比如“level:debug”，方便后续对日志进行分组统计。默认情况下，会在输出信息的fields子目录下以指定的新增fields建立子目录，例如fields.level。
* ields_under_root：如果该选项设置为true，则新增fields成为顶级目录，而不是将其放在fields目录下。自定义的field会覆盖filebeat默认的field。例如添加如下配置：
* scan_frequency：Filebeat以多快的频率去prospector指定的目录下面检测文件更新（比如是否有新增文件），如果设置为0s，则Filebeat会尽可能快地感知更新（占用的CPU会变高）。默认是10s。
* harvester_buffer_size：每个harvester监控文件时，使用的buffer的大小。默认是16384.
* max_bytes：日志文件中增加一行算一个日志事件，max_bytes限制在一次日志事件中最多上传的字节数，多出的字节会被丢弃。默认是10M
* backoff：Filebeat检测到某个文件到了EOF之后，每次等待多久再去检测文件是否有更新，默认为1s。
* max_backoff：Filebeat检测到某个文件到了EOF之后，等待检测文件更新的最大时间，默认是10秒。
* backoff_factor：定义到达max_backoff的速度，默认因子是2，到达max_backoff后，变成每次等待max_backoff那么长的时间才backoff一次，直到文件有更新才会重置为backoff。如果设置成1，意味着去使能了退避算法，每隔backoff那么长的时间退避一次。
* multiline：适用于日志中每一条日志占据多行的情况，比如各种语言的报错信息调用栈。这个配置的下面包含如下配置：
```text
pattern：多行日志开始的那一行匹配的pattern
negate：是否需要对pattern条件转置使用，不翻转设为true，反转设置为false
match：匹配pattern后，与前面（before）还是后面（after）的内容合并为一条日志
max_lines：合并的最多行数（包含匹配pattern的那一行）
timeout：到了timeout之后，即使没有匹配一个新的pattern（发生一个新的事件），也把已经匹配的日志事件发送出去
```
* tail_files：如果设置为true，Filebeat从文件尾开始监控文件新增内容，把新增的每一行文件作为一个事件依次发送，而不是从文件开始处重新发送所有内容。
* ignore_older：可以指定Filebeat忽略指定时间段以外修改的日志内容，比如2h（两个小时）或者5m(5分钟)。
* close_inactive：如果一个文件在某个时间段内没有发生过更新，则关闭监控的文件handle。默认5m。
* close_renamed ：启用此选项后，Filebeat会在重命名文件时关闭文件处理程序。 
* close_removed : 启用此选项后，Filebeat会在删除文件时关闭收集器。
* close_timeout：启用此选项后，Filebeat会为每个收集器提供预定义的生命周期。
* clean_inactive ：启用此选项后，Filebeat会在指定的不活动时间段过后删除文件的状态。
* clean_removed ：启用此选项后，如果在最后一个已知名称下无法在磁盘上找到文件，则Filebeat会清除注册表中的文件。 这意味着在harvester完成后重命名的文件也将被删除。默认情况下启用此选项。