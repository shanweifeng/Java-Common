## 虚拟机性能监控与故障处理工具

> 定位系统问题的时候，知识、经验是关键基础，数据是依据，工具是运用知识处理数据的手段。数据包括:运行日志、异常堆栈、GC日志、线程快照(threadDump/javacore文件)、堆转储快照(heapdump/hprof文件)等。
#### JDK的命令行工具
| 名称 |主要作用|
|------|--------|
|jps   |JVM Process Status Tool,显示指定系统内所有的HotSpot VM进程  |
|jstat |JVM Statistics Monitoring Tool,用于收集HotSpot VM各方面运行数据|
|jinfo |Configuration Info for Java 显示VM配置信息|
|jmap  |Memory Map for Java 生成VM的内存转储快照(heapdump文件)|
|jhat  |JVM Heap Dump Browser 用于分析heapdump文件,它会建立一个HTTP/HTML服务器，让用户可以在浏览器上查看分析结果|
|jstack|Stack Trace for Java 显示虚拟机的线程快照|

* jps:VM进程状况工具（JVM Process Status Tools）
> 可以列出正在运行的虚拟机进程，并显示虚拟机执行朱磊(Main Class, main()函数所在的类)的名称，以及这些进程的本地虚拟机的唯一ID(LVMID, Local Virtual Machine Identifier)。对于本地虚拟机进程来说，LVMID与操作系统的进程id(PID Process Identifier)是一致的。使用Linux的ps命令也可以查询到VM进程的LVMID。<p>
>>jps命令格式:<p>
jps [option] [hostid]

|选项|作用|
|-----|-----|
|-q|只输出LVMID，省略朱磊的名称|
|-m|输出VM进程启动时传递给主类main()函数的参数|
|-l|输出主类的全名，如果进程执行的是Jar包，输出Jar路径|
|-v|输出VM进程启动时JVM参数|

* jstat:VM统计信息监视工具（JVM Statistics Monitoring Tool）
> 用于监视VM各种运行状态信息的命令行工具。可以显示本地或远程(需要远程主机提供RMI支持，Sun提供了jstatd工具可以很方便地建立远程RMI服务器)VM进程中的类装载、内存、垃圾收集、JIT编译等运行数据。在没有GUI图形界面只提供纯文本控制台环境的服务器上，将是运行期定位VM性能问题的首选工具。<p>
>> jstat 命令格式:<p>
jstat [option vmid [interval[s|ms] [count]]]<p>
对于命令格式中的VMID与LVMID需要注意的是:如果是本地虚拟机进程，VMID与LVMID是一致的，如果是远程虚拟机进程，那VMID格式应当是:<p>
[protocal:][//]lvmid[@hostname[:port]/servername]
参数interval和count代表查询间隔和次数， 如果省略这两个参数，说明只查询一次。

|    选项|作用|
|-----|-----|
|-class           |监视类装载、卸载数量、总空间及类装载所耗费时间|
|-gc              |监视Java堆状况，包括Eden区、2个survivor区、老年代、永久代等的容量，已用空间、GC时间合计等信息|
|-gccapacity      |监视内容与-gc基本相同，但输出主要关注Java堆各个区域使用到的最大和最小空间|
|-gcutil          |监视内容与-gc基本相同，但输出主要关注已经使用空间站总空间的百分比|
|-gccause         |与-gcutil功能一样，但会额外输出导致上一次GC产生的原因|
|-gcnew           |监视新生代GC的状况|
|-gcnewcapacity   |监视内容与-gcnew基本相同，输出主要关注使用到 的最大和最小空间|
|-gcold           |监视老年代GC的状况|
|-gcolecapacity   |监视内容与-gcold基本相同，输出主要关注使用到的最大和最小空间|
|-gcpermcapacity  |输出永久代使用到的最大和最小空间(JDK8中已经没有)|
|-compiler        |输出JIT编译器编译过的方法、耗时等信息|
|-printcompilation|输出已经被JIT编译的方法|

* jinfo:Java配置信息工具(Configuration Info for Java)
> 实时查看和调整VM的各项参数。使用jsp -v可查看VM启动时显示指定的参数列表，但如果想知道默认的系统值可以使用 jinfo的-flag选项进行查询。jinfo提供了查询和修改虚拟机参数值功能如：-flag [+|-]name 或-flag name=value<p>
>> jinfo命令格式:<p>
jinfo [option] pid<p>
执行样例:查询CMSInitiatingOccupancyFraction参数值: jinfo -flag CMSInitiatingOccupancyFraction pid

* jmap: Java 内存映像工具(Memory Map for Java)
> 用于生产堆转储快照(一般称为heapdump或dump文件)。如果不用jmap命令获取快照，可以使用JVM参数-XX:+HeapDumpOnOutOfMemoryError让VM在出现OOM异常之后自动转储dump文件，通过-XX:+HeapDumpOnCtrlBreak参数可以使用[Ctrl]+[Break]键让VM生产dump文件，又或者在Linux系统下通过Kill -3命令也能拿到dump文件。<p>
除了获取dump文件外，还可以查询Finalize执行队列、Java堆和永久代的详细信息，如空间使用率、当前使用的收集器等信息。<p>
>>jmap命令格式:<p>
jmap [option] vmid

|    选项|作用|
|-----|-----|
|-dump          |生成Java堆转储快照。格式为: -dump:[live,]format=b,file=<filename>,其中live子参数说明是否只dump出存活的对象|
|-finalizerinfo |显示在F-Queue中等待Finalizer线程执行Finalize方法的对象。只在Linux/Solaris平台下有小|
|-heap          |显示Java堆详细信息，如使用的回收器、参数配置、分代状况等。只在Linux/Solaris平台下有小|
|-histo         |显示堆中对象统计信息，包括类。实例数量和合计容量|
|-permstat      |以ClassLoader为统计口径显示永久代内存状态。只在Linux/Solaris平台下有小|
|-F             |当VM进程堆-dump选项没有响应时，可使用这个选项强制生成dump快照。只在Linux/Solaris平台下有小|

* jhat:VM堆转储快照分析工具(JVM Heap Analysis Tool)
> 与jmap搭配使用，来分析jmap生成的堆转储快照。

* jstack:Java堆栈跟踪工具(Stack Trace for Java)
> 用于生成VM当前时刻的线程快照(一般称为threaddump或javacore文件)。线程快照就是当前VM内每条线程正在执行的方法堆栈的集合，生成线程快照的主要目的是定位当前线程出现长时间停顿的原因，如线程死锁、死循环、请求外部资源导致的长时间等待等都是导致线程长时间停顿的常见原因。
>> jstack 命令格式:<p>
jstack [option] vmid

|    选项|作用|
|-----|-----|
|-F|当正常输出的请求不被响应时，强制输出线程堆栈|
|-l|除堆栈外，显示关于所的附加信息|
|-m|如果调用到本地方法的话，可以显示C/C++的堆栈|

#### JDK可视化工具
##### JConsole(JDK1.5)[Java Monitoring and Management Console]
> 是一款基于JMX(Java Management Extensions)的可视化监视和管理的工具。管理部分的功能是针对JMX MBean进行管理的，MBean可以使用代码、中间件服务器的管理口控制台或所有符合JMX规范的然健进行访问。
* 启动JConsole
* 内存监控
> 相当于可视化的jstat命令，用于监视受收集器管理的VM memory(Java堆和永久代)的变化趋势。
* 线程监控
> 相当于可视化的jstack命令
##### VisualVM(JDK1.6 https://visualvm.dev.java.net/)[All-in-One Java Troubleshooting]
> 运行监视、故障处理、性能分析(Profiling),不需要被监视的程序基于特殊Agent运行，因此对应用程序的实际性能的影响很小，使得可以直接应用在生产环境中。
* VisualVM兼容范围与插件安装
> 基于NetBeans平台开发，因此具备插件扩展功能的特性，通过插件扩展支持，VisualVM可以做到:
>> 显示VM进程及进程的配置和环境信息(jps jinfo)<p>
监视应用程序的CPU、GC、堆、方法区及线程的信息（jstat、jstack）<p>
dump及分析堆转储快照(jmap、jhat)<p>
方法级的程序运行性能分析，找出被调用最多、运行时间最长的方法<p>
离线程序快照：收集程序的运行时配置、线程dump、内存dump等信息简历一个快照，可以将快照发送开发者处进行Bug反馈<p>
其他plugins的无线可能。
>>> VisualVM具备很强的向下兼容的能力,如果早于JDK1.6的平台需要打开-Dcom.sun.management.jmxremote参数才能被VisualVM管理
>>VisualVM主要功能兼容性列表

|特性|JDK1.4.2|JDK1.5|JDK1.6 local|JDK1.6 remote|
|-----|-----|-----|-----|-----|
|运行环境信息|&radic;|&radic;|&radic;|&radic;|
|系统属性| - | - |&radic;| - |
|监视面板|&radic;|&radic;|&radic;|&radic;|
|线程面板| - |&radic;|&radic;|&radic;|
|性能监控| - | - |&radic;| - 
|堆、线程Dump| - | - |&radic;| - |
|MBean管理| - |&radic;|&radic;|&radic;|
|JConsole| - |&radic;|&radic;|&radic;|