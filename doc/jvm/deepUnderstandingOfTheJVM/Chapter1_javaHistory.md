## Chapter 1 走进Java
>> 一次编写、到处运行的理想；提供了一种相对安全的内存管理和访问机制，避免了绝大部分的内存泄漏和指针越界；实现了热点代码检测和运行时编译及优化。

> 作为一名Java程序员，在编写程序时除了尽情发挥Java的各种优势外，还应该去了解和思考一下Java技术体系中这些技术是如何实现的。认清这些技术的运作本质，是自己思考**"程序这样写好不好"**的基础和前提。当我们在使用一门技术时，如果不再依赖书本和他人就能得到这个问题的答案，那才算升华到了“不惑”的境界。

#### 1.2 Java技术体系
> 从广义上讲，Clojure、JRuby、Groovy等运行于Java虚拟机上的语言及其相关的程序都属于Java技术体系的一员。如果仅从传统意义上来看，Sun官方所定义的Java技术体系包括了一下几个组成部分:
* Java程序设计语言
* 各种硬件平台上的Java虚拟机
* Class文件格式
* Java API类库
* 来自商业机构和开源社区的第三方Java类库
> Java程序设计语言、Java虚拟机、Java API类库这三部分统称为JDK(Java Development Kit)，JDK是用于支持Java程序开发的最小环境。Java API类库中的Java SE API子集和Java虚拟机这两部分统称为JRE(Java Runtime Environment)，JRE是支持Java程序运行的标准环境。![Java技术体系所包含的内容](/doc/image/javaTechnicalSystemjava.png)

> 上图中是按照功能来进行划分的。按照技术所服务的领域或业务领域划分为四个平台:
* Java Card:支持一些Java小程序(Applets)运行在小内存设备(如智能卡)上的平台。
* Java ME(Micro Edition):支持Java程序运行在移动终端(手机、PDA)上的平台，对Java API有所精简，并加入了针对移动终端的支持，这个版本以前称为J2ME.
*Java SE(Standard Edition):支持面向桌面级应用(如Windows下的应用程序)的Java平台，提供了完成的Java核心API，这个版本以前称为J2SE.
* Java EE(Enterprise Edition):支持使用多层架构的企业应用(如ERP、CRM应用)的Java平台，除了提供Java SE API外，还对其做了大量扩充并提供了相关部署支持，这个版本以前称为J2EE.
>> 这些扩展一般以javax.*作为包名，而以java.*为包名的包都是Java SE API的核心包，但由于历史原因，一部分曾经是扩展包的API后来进入了核心包，因此核心包中也包含了不少javax.*的包名.

>>> 模块化、混合语言、多核并行、

#### 获取OPEN JDK源码
* 一种是通过Mercurial代码版本管理工具从Repository中直接取得源码(http://hg.openjdk.java.net/jdk7/jdk7),这是最直接的方式，从版本管理中看变更轨迹比看任何Release Note都来的实在，不过比较太麻烦。
* 可以从Source Release地址(http://download.java.net/openjdk/jdk7/)取得打包好的源码。