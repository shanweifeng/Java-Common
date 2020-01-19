## [Linux进程意外退出：OOM-killer](http://hongjiang.info/tomcat-killed-by-oomkiller/)

* 当进程在日志中没有原因的退出系统时，应该考虑进程被系统干掉这个点
> 通过dmesg名称查看系统干掉的OOM-killer
```text
sudo dmesg | grep java | grep -i oom-killer
```
这里OOM可以参考：[Linux内核OOM机制的详细分析](/doc/Linux/系统运维/Linux内核OOM机制的详细分析.md)

