OSI网络模型（七层、四层）


TCP/IP协议族常用协议：
应用层：TFTP、HTTP、SNMP、FTP、SMTP、DNS、Telnet等

传输层：TCP、UDP

网络层：IP、ICMP、OSPF、EIGRP、IGMP

数据链路层：SLIP、CSLIP、PPP、MTU


重要的 TCP/IP 协议族协议进行简单介绍:

IP(Internet Protocol,网际协议)是网间层的主要协议,任务是在源地址和和目的地址之间传输数据。IP 协议只是尽最大努力来传输数据包,并不保证所有的包都可以传输 到目的地,也不保证数据包的顺序和唯一。

IP 定义了 TCP/IP 的地址,寻址方法,以及路由规则。现在广泛使用的 IP 协议有 IPv4 和 IPv6 两种:IPv4 使用 32 位二进制整数做地址,一般使用点分十进制方式表示,比如 192.168.0.1。
IP 地址由两部分组成,即网络号和主机号。故一个完整的 IPv4 地址往往表示 为 192.168.0.1/24 或192.168.0.1/255.255.255.0 这种形式。
IPv6 是为了解决 IPv4 地址耗尽和其它一些问题而研发的最新版本的 IP。使用 128 位 整数表示地址,通常使用冒号分隔的十六进制来表示,并且可以省略其中一串连续的 0,如:fe80::200:1ff:fe00:1。
目前使用并不多！


ICMP(Internet Control Message Protocol,网络控制消息协议)是 TCP/IP 的 核心协议之一,用于在 IP 网络中发送控制消息,􏰁供通信过程中的各种问题反馈。 ICMP 直接使用 IP 数据包传输,但 ICMP 并不被视为 IP 协议的子协议。常见的联网状态诊断工具比如依赖于 ICMP 协议;
TCP(TransmissionControlProtocol,传输控制协议)是一种面向连接的,可靠的, 基于字节流传输的通信协议。TCP 具有端口号的概念,用来标识同一个地址上的不 同应用。􏰂述 TCP 的标准文档是 RFC793。
UDP(UserDatagramProtocol,用户数据报协议)是一个面向数据报的传输层协 议。UDP 的传输是不可靠的,简单的说就是发了不管,发送者不会知道目标地址 的数据通路是否发生拥塞,也不知道数据是否到达,是否完整以及是否还是原来的 次序。它同 TCP 一样有用来标识本地应用的端口号。所以应用 UDP 的应用,都能 够容忍一定数量的错误和丢包,但是对传输性能敏感的,比如流媒体、DNS 等。
ECHO(EchoProtocol,回声协议)是一个简单的调试和检测工具。服务器器会 原样回发它收到的任何数据,既可以使用 TCP 传输,也可以使用 UDP 传输。使用 端口号 7 。
DHCP(DynamicHostConfigrationProtocol,动态主机配置协议)是用于局域 网自动分配 IP 地址和主机配置的协议。可以使局域网的部署更加简单。
DNS(DomainNameSystem,域名系统)是互联网的一项服务,可以简单的将用“.” 分隔的一般会有意义的域名转换成不易记忆的 IP 地址。一般使用 UDP 协议传输, 也可以使用 TCP,默认服务端口号 53。􏰂
FTP(FileTransferProtocol,文件传输协议)是用来进行文件传输的标准协议。 FTP 基于 TCP 使用端口号 20 来传输数据,21 来传输控制信息。
TFTP(Trivial File Transfer Protocol,简单文件传输协议)是一个简化的文 件传输协议,其设计非常简单,通过少量存储器就能轻松实现,所以一般被用来通 过网络引导计算机过程中传输引导文件等小文件;
SSH(SecureShell,安全Shell),因为传统的网络服务程序比如TELNET本质上都极不安全,明文传说数据和用户信息包括密码,SSH 被开发出来避免这些问题, 它其实是一个协议框架,有大量的扩展冗余能力,并且􏰁供了加密压缩的通道可以 为其他协议使用。
POP(PostOfficeProtocol,邮局协议)是支持通过客户端访问电子邮件的服务, 现在版本是 POP3,也有加密的版本 POP3S。协议使用 TCP,端口 110。
SMTP(Simple Mail Transfer Protocol,简单邮件传输协议)是现在在互联网 上发送电子邮件的事实标准。使用 TCP 协议传输,端口号 25。
HTTP(HyperTextTransferProtocol,超文本传输协议)是现在广为流行的WEB 网络的基础,HTTPS 是 HTTP 的加密安全版本。协议通过 TCP 传输,HTTP 默认 使用端口 80,HTTPS 使用 443。


https://github.com/DeathKing/Learning-SICP  计算机程序的结构和解释

https://github.com/spring-cloud-samples/configserver/blob/master/pom.xml  spring-cloud-samples / configserver

https://docs.spring.io/spring-boot/docs/2.0.9.BUILD-SNAPSHOT/reference/htmlsingle/#boot-features-external-config-vs-value 

https://github.com/iccfish/12306_ticket_helper  

http://www.flickering.cn/ 数学之美 机器学习

https://www.jianshu.com/p/6f1b129442a1 spring security

https://www.zybuluo.com/codeep/note/163962  markdown语法表示数学公式

https://www.kancloud.cn/imnotdown1019/java_core_full/1005824

https://blog.csdn.net/zqz_zqz/article/details/70233767# 

https://blog.csdn.net/lengxiao1993/article/details/81568130

https://www.cnblogs.com/yxx123/p/5227267.html   uml状态机图画图

http://www.xinhuanet.com//tech/2017-02/07/c_1120421682.htm  翻墙

https://zhuanlan.zhihu.com/p/28457897   GitHub 万星推荐：黑客成长技术清单

https://open.youzan.com/v3/apicenter/doc-api-list/1 有赞文档

https://www.showdoc.cc/item/password/200481633019093?page_id=1136959549943167&redirect=%2F200481633019093%3Fpage_id%3D1136959549943167  爱库存
密码:DadacangH5 

https://bookset.me/  
http://einverne.github.io/post/2018/02/free-online-books.html  工具

https://github.com/justjavac/free-programming-books-zh_CN 一些书

https://github.com/Hack-with-Github/Awesome-Hacking  基础hacking English   https://zhuanlan.zhihu.com/p/28457897  https://www.4hou.com/info/news/7061.html

https://www.cnblogs.com/hello1123/p/10214737.html  IT人员应该掌握的30种技能

花生壳 IP穿透 http://service.oray.com/question/1669.html
66.42.32.62
[Sf1J75XeQ$X*Zu.
kunxuan@kunxuan.cn/kunxuan@kunxuan.cn7788
https://www.elastic.co/cn/downloads/elasticsearch
https://c.runoob.com/more/shapefly-diagram/index.html#  画图

https://mp.weixin.qq.com/s/Lb6pjRn7vL-FgMa45qfGJA python scaft

https://blog.csdn.net/feifeidepop/article/details/83281050  es面试问题  这里需要了解es的运行过程
https://blog.csdn.net/jiangjiang_jian/article/details/80834157   推荐系统 这个适合在空余的时间上来完成  作为对自己的一个挑战  必选项 9月份之前完成 

Elasticsearch中有哪些坑。  https://blog.csdn.net/zlh3955649/article/details/53169586   https://blog.csdn.net/opensure/article/details/47617437

Elasticsearch中的脑裂问题及防治措施  
事务日志
Lucene的段
为什么搜索时使用深层分页很危险
计算搜索相关性中困难及权衡
并发控制
为什么Elasticsearch是准实时的
如何确保读和写的一致性
https://segmentfault.com/a/1190000015220491#articleHeader9 
https://www.cnblogs.com/liyafei/p/8543309.html  multi index search
https://blog.csdn.net/u012983826/article/details/52129833   商品ElasticSearch的查询改造

http://www.kgc.cn/java/34988.shtml   基于Elasticsearch技术实现大觅网商品搜索1

https://www.19lou.com/forum-1637-thread-5071558493577967-showthread-10480784-puid-10480784-1-1.html


https://www.runningcheese.com/baiduyun  百度云盘提速方法

https://blog.csdn.net/cuixhao110/article/details/88353308
https://www.cnblogs.com/cs99lzzs/p/7212428.html es 用法
es+spark 用法

https://learnku.com/courses/ecommerce-advance/5.5/stress-testing-part-one/2054  电商系统优化


https://my.oschina.net/xuxueli  许雪里


https://yarn.bootcss.com/docs/usage/

http://www.java1234.com/a/javabook/yun/list_115_2.html



https://www.cnblogs.com/lemon-flm/p/7877898.html queue


http://c.biancheng.net/view/3150.html   docker资源


http://developer.51cto.com/art/201907/599473.htm  微服务框架


跳板机ip：47.94.132.152 账号： 密码：Swf123456@
老跳板机：47.111.13.178 账号： 密码：swf184856

redis: 
解压路径：/opt/redis/redis-5.0.5
安装路径：/mnt/server/redis
password:123456zdt
port: 6379
ip:59.110.173.169

mysql:
安装路径：/usr/local/mysql
username： root
password: 123456zdt
port: 3306
ip: 101.200.41.41

Host is not allowed to connect to this MySQL server解决方法
在装有MySQL的机器上登录MySQL mysql -u root -p密码
执行use mysql;
执行update user set host = '%' where user = 'root';这一句执行完可能会报错，不用管它。
执行FLUSH PRIVILEGES;


mvn deploy:deploy-file -DgroupId=com.sun -DartifactId=jai_core -Dversion=1.1.3 -Dfile=C:\Users\Administrator\Desktop\jai_core\jai_core.jar -Durl=http://47.96.109.118:8081/repository/maven-public/ -DrepositoryId=Snapshots

单点登录CAS使用记（七）：关于服务器超时以及客户端超时的分析
https://www.cnblogs.com/notDog/p/5276643.html