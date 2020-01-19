###  CPU高负载排查

* 问题分析：
 1，程序属于CPU密集型，和开发沟通过，排除此类情况。
 2，程序代码有问题，出现死循环，可能性极大。
 
* 解决过程
1. top 命令查看占用CPU高的进程(也可以使用其他命令:ps ux)
2. 将该进程中线程按照占用CPU高低排序  ps -mp pid -o THREAD,tid,time | sort -rn
ps  -Lp pid cu
top -Hp pid
3. 将线程id转换成十六进制 printf "%x\n" pid
4. jstack pid | grep 十六进制线程id -A 30


#### 以下是针对tomcat上的应用的. 其他的java程序, 只要你能触发他的thread dump并且拿到结果, 也是一样.
1. ps -ef | grep java
找到你的java程序的进程id, 定位 pid
2. top -Hp $pid
shift+t 
查看耗cpu时间最多的几个线程, 记录下线程的id
3. 把上诉线程ID转换成16进制小写 比如 : 0x12ef
4. kill -3 $pid 触发tomcat的thread dump
5. 找到tomcat的catalin.out 日志, 把 上面几个线程对应的代码段拿出来.