## [Linux内核OOM机制的详细分析](http://blog.chinaunix.net/uid-29242873-id-3942763.html)

> Linux 内核有个机制叫OOM killer(Out-Of-Memory killer),该机制会监控那些占用内存过大，尤其是瞬间很快消耗大量内存的进程，为了防止内存耗尽而内核会把该进程杀掉。典型的情况是: 某天一台机器突然ssh远程登录不了，但能ping同，说明不是网络的故障，原因是sshd进程被OOM killer杀掉了(多次遇到这样的假死状况)。重启机器后查看系统日志/var/log/messages会发现Out of Memory: Kill process1865(sshd)类似的错误信息<p>
防止重要的系统进程触发(OOM)机制而被杀死：可以设置参数/proc/PID/oom_adj为-17，可临时关闭Linux内核的OOM机制。内核会通过特定的算法给每个进程计算一个分数来决定杀死哪个进程，每个进程的OOM分数可以/proc/PID/oom_score中找到。运维过程中保护的一般是sshd和一些管理agent。<p>
* 保护某个进程不被内核杀掉可以这样操作:
```text
echo -17 > /proc/$PID/oom_adj
```
*  如何放置sshd被杀 可以这样操作:
```text
pgrep -f "/usr/sbin/sshd" | while read PID;do echo -17 > /proc/$PID/oom_adj;done
```
>> 可以在计划任务里添加这样一条定时任务，就更安全：
```text
#/etc/cron.d/oom_disable
*/1 * * * * root pgrep -f "/usr/sbin/sshd" | while read PID;do echo -17 > /proc/$PID/oom_adj;done
// 为了避免重启失效，可以写入/etc/rc.d/rc.local
echo -17 > /proc/$(pidof sshd)/oom_adj
```

> 至于为什么用-17而不用其他数字(默认值为0)，这个是由Linux内核定义，查看内核源码可知:以Linux-3.3.6版本的kernel源码为例，路径为linux-3.6.6/include/linux/oom.h,阅读内核源码可知oom_adj的可调值为15到-16，其中15最大-16最小，-17为禁止使用OOM。oom_score为2的n次方计算出来的，其中n就是进程oom_adj值，所以oom_score的分数越高就越会被内核优先杀掉。
```text
#di=efine OOM_DISABLE (-17)
/* inclusive */
#define OOM_ADJUST_MIN (-16)
#define OOM_ADJUST_MAX (15)
```
> 还可以通过修改内核参数禁止OOM机制
```text
# sysctl -w vm.panic_on_oom=1vm.panic_on_oom = 1//1表示关闭，默认为0表示开启OOM
#sysctl -p
```

#### 验证OOM机制
```text
free -m //查看当前系统内存及其使用情况
top // 查看当前进程中系统资源占用情况
```
>

##### 注意：
      
      1.Kernel-2.6.26之前版本的oomkiller算法不够精确，RHEL 6.x版本的2.6.32可以解决这个问题。
      
      2.子进程会继承父进程的oom_adj。
      
      3.OOM不适合于解决内存泄漏(Memory leak)的问题。
      
      4.有时free查看还有充足的内存，但还是会触发OOM，是因为该进程可能占用了特殊的内存地址空间。