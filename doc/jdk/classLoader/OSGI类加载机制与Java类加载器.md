## [OSGI类加载机制](https://blog.csdn.net/runningofsnail/article/details/80757675)
> OSGI类加载机制破坏了双亲委派模型(delegation  model)

#### 类加载器 
> 类加载阶段中"通过一个类的全限定名来获取描述此类的二进制字节流"这个动作放大JVM外部去实现，以便让应用程序自己决定如何去获取所需要的类。实现这个动作的代码模块称为"类加载器".<p>
类加载器可以说是Java语言的一项创新，也是Java语言流行的重要原因之一，在类层次划分、OSGI(Open Service Gateway Initiative)、热部署、代码加密等领域大放异彩。<p>
类加载器虽然只用于实现类的加载动作，但它在Java程序中起到的作用却远不限于类加载阶段。任意一个类都需要**由加载它的类加载器和这个类本身一同确立其在Java虚拟机中的唯一性，每个类都拥有一个独立的类名空间。通俗的讲：比较两个类是否"相等"，只有在这两个类是由同一个类加载器加载的前提下才有意义，否则即使这两个类来源于同一个Class文件被同一个虚拟机加载，只要加载它们的类加载器不同，那么这两个类就必定不相等。**

#### Tomcat的双亲委派模型(delegation model)
> 从Java虚拟机角度来讲，只存在两种不同的类加载器：一种是启动类加载器(Bootstrap ClassLoader),这个类加载器是由C++语言实现的，是虚拟机的一部分；另一种就是所有其他的类加载器，这些类加载器都由Java语言实现，独立于虚拟机外部，并且全部都继承自抽象类java.lang.ClassLoader。<p>
双清委派解决了个各类加载器的基础类的统一问题(越基础的类由越上层的加载器进行加载)，基础类之所以称为"基础",是因为它们总是作为被用户代码调用的API，，但如果基础类又要调用回用户的代码，这样就会打破双亲委派模型。
* 启动类加载器(Bootstrap ClassLoader):

* 扩展类加载器(Extension ClassLoader):

* 应用程序类加载器(Application ClassLoader):
这里类加载的顺序是反转过来的，先加载启动类加载器能够加载的类，然后是扩展类加载器加载，再是系统类加载器加载，如果还有自定义的类加载器则最后加载。

#### 打破双亲委派模型
> 双亲委派模型并不是一个强制性的约束模型，而是Java设计者推荐给开发者的类加载器实现方式，Java中大部分类加载器都遵循这个模型，但也有一些例外。<p>
JNDI(Java Naming and Directory Interface Java命名和目录接口):是Java的标准服务，它的代码由启动类加载器去加载(在JDK1.3时放进去的rt.jar)，但JNDI的目的就是对资源进行集中管理和查找，需要调用独立厂商实现并部署在应用程序的ClassPath下的JNDI接口提供者(SPI service provider interface)的代码。为了搜索到这样的用户代码，设计出了这样一个类加载器:线程上下文类加载器(Thread Context ClassLoader):这个类加载器可以通过java.lang.Thread类的setContextClassLoader()方法进行设置，如果创建线程时还未设置，它将会从父线程中继承一个，**如果在应用程序的全局范围内都没有设置过的话，那这个类加载器默认就是应用程序类加载器(Application ClassLoader).**<p>
有了线程上下文类加载器，JNDI服务使用这个线程上下文磊加载器去加载所需要的SPI代码，也就是父类加载器请求子类加载器去完成类加载的动作，这种行为实际上已经打通了双亲委派模型的层次结构来逆向使用类加载器，实际上已经未被了双亲委派模型的一般性原则。Java中的所有涉及SPI的加载动作基本上都是采用这种方式如：JNDI、JDBC、JCE、JAXB和JBI等。

> 双亲委派模型的另外一个"被破坏"是由于用户对程序动态性的最求而导致的。这里所说的"动态性" 指的是当前一些热门名称: 代码热替换(HotSwap)、模块热部署(HotDeployment)等。OSGI实现模块化热部署的关键则是它自定义的类加载器机制的实现。每一个程序模块(OSGI中称为Bundle)都有一个自己的类加载器，当需要更换一个
Bundle是，就把Bundle连同类加载器一起换掉以实现代码的热替换.<p>
在OSGI环境下，类加载器不在是双亲委派模型中的树状结构，而是进一步发展为更加复杂的网状结构，当收到类加载器请求时，OSGI将按照下面的顺序进行类搜索：<p>
1、将以java.*开头的类委派给父类加载器。<p>
2、否则将委派列表名单内的类委派给父类加载器<p>
3、否则将Import列表中的类委派给Export这个类的Bundle的类加载器加载<p>
4、否则查找当前Bundle的Class Path，使用自己的类加载器加载<p>
5、否则查找类是否在自己的Fragment Bundle中，如果在则委派为Fragment Bundle的类加载器加载<p>
6、否则查找Dynamic Import列表的Bundle，委派给对应Bundle的类加载器加载<p>
7、否则类查找失败。

> OSGI 对类加载器的使用精髓学习

#### OSGI:灵活的类加载器架构  ？？
> OSGI(Open Service And Gateway Initiative):是OSGI联盟指定的一个基于Java语言的动态模块化规范，这个规范最初是由Sun、IBM、爱立信等发起，目的是使服务提供商通过住宅网管为各种家用智能设备提供各种服务，后来这个规范在Java的其他技术领域的发展使得其成为Java世界的模块化标准，并且已经有了Equinox、Felix等成熟的实现。<p>
OSGI中的每一个模块(称为Bundle)与普通的Java类库区别并不大，两者一般都以Jar格式进行封装，并且内部存储的都是Java Package和Class。但是Bundle可以声明它所依赖的Java Package(通过Import-Package描述)，也可以声明他允许导出发布的Java Package(通过Import-Package描述)。在OSGI里面Bundle之间的依赖关系从传统的上层模块依赖底层模块转变为平级模块之间的依赖(至少外观上如此 ？？)，而且类库的可见性能得到精确的控制，一个模块里只有被Export过的Package才可能由外界访问，其他的Package和Class将会隐藏起来。除了更精确的模块划分和可见性控制外，引入OSGI的另外一个重要理由是，基于OSGI的程序均可能可以实现模块级的热插拔功能。<p>
OSGI的类加载器架构规则:Bundle类加载器之间只有规则，没有固定的委派关系。例如某个Bundle声明了一个它依赖的Package，如果有其他的Bundle声明发布了这个Package，那么所有对这个Package的类加载动作都会为派发给他的Bundle类加载器去完成。不涉及某个具体的Package时，各个Bundle加载器是平级关系，只有具体使用某个Package和Class的时候，才会根据Package导入导出定义来构造Bundle间的委派和依赖。另外，一个Bundle类加载器为其他Bundle提供服务时，会根据Export-Package列表严格控制访问范围。如果一个类存在于Bundle的类库中但是没有被Export，那么 这个Bundle的类加载器能找到这个类但不会提供给其他Bundle使用，而且OSGI平台也不会把其他Bundle的类加载请求分配给这个Bundle来处理。（这里好模糊，需要看原文档）.

#### [Tomcat的类加载器架构---很早就应该看这类文章了](https://blog.csdn.net/fuzhongmin05/article/details/57404890)
>主流的Java Web服务器(也就是Web容器)，如Tomcat、Jetty、WebLogic。WebSphere或其他的服务器，都实现了自定义的类加载器(一般都不止一个)。因为一个功能健全的web容器，要解决一下几个问题：
* 部署在同一个web容器上的两个web应用程序所使用的的Java类库可以实现互相隔离。这是最基本的需求，两个不同的应用程序可能会依赖同一个第三方类库的不同版本，不能要求类库在一个服务器中只有一份，服务器应当保证两个应用程序的类库可以相互独立使用。
* 部署在同一个web容器上的两个web应用程序所使用的java类库可以互相共享。类库在使用时都要被加载到web容器的内存，如果类库不能共享，虚拟机的方法去就会很容易出现过度膨胀的风险。
* web容器小尽可能的保证自省的安全不受部署的web应用程序影响。目前许多容器使用的开发语言与应用程序的开发语言相同，基于安全考虑容器所使用的类库应该与应用程序的类库互相独立。
* 支持JSP应用的web容器，大多数都需要支持HotSwap功能。JSP文献最终要编译成java class才能由虚拟机执行，但JSP文件由于其纯文本存储的特性，运行时修改的概率远远大于第三方类库或程序自身的Class文件。而且APS、PHP和JSP这些网页应用也把修改后无需重启作为一个很大的"优势"来看待。主流web容器都会支持网页文件生成类的热替换，但也有不支持的如WEbLogic<p>
由于上述问题，在web应用部署时，就需要提供多个Class Path路径供用户存放第三方类库，这些路径一般都以lib或classes命名。被放置到不同路径中的类库具备不同的访问范围和服务对象，通常每个目录都会有一个相应的自定义类加载器去加载放置的java类库。一下是Tomcat规划用户类库结构和类加载器：<p>
Tomcat中有三组目录结构("/common/*"、"/server/"、"/shared/*")可以存放Java类库，另外还可以加上Web应用程序自身的目录"/WEB-INF/*",把Java类库放置在这些目录中的含义分别如下:<p>
放置/common目录：类库可被Tomcat和所有的Web应用程序共同使用。<p>
/server:类库可被Tomcat使用，对所有的Web应用程序都不可见<p>
/shared:类库可被所有的Web应用程序共同使用，但对Tomcat自己不可见<p>
/Webapp/WEB-INF:类库仅仅可以被此Web应用程序使用，对Tomcat和其他Web应用程序都不可见<p>
为了支持这套目录结构，并对目录里面的类库进行加载和隔离，Tomcat自定义了多个累加载器，这些累加载器按照经典的双亲委派模型来实现，其关系图如：![Tomcat自定义类加载器](/doc/image/tomcat_classloader.png)
其中启动类加载器、扩展类加载器、应用程序类加载器这三个是JDK本身提供的类加载器。而CommonClassLoader、CatalinaClassLoader、SharedClassLoader和WebappClassLoader则是Tomcat自己定义的类加载器，分别加载/common/*、/server/*、/shared/*、/WebApp/WEB_INF/*中的java类库。其中WebApp类加载器和JSP类加载器通常会存在多个实例，每个Web应用程序对应一个WebApp类加载器，每个JSP文件对应一个JSP类加载器。<p>
从图中的委派关系可以看出，CommonClassLoader能加载的类都可以被CatalinaClassLoader和SharedClassLoader使用，而CatAlinaClassLoader和SharedClassLoader自己能加载的类则与对方相互隔离。WebAPPClassLoader可以使用SharedClassLoader加载到的类，但各个WebAPPClassLoader实例之间相互隔离。而JasperLoader的加载范围仅仅是这个JSP文件所编译出来的那个.class文件，它出现的目的就是为了被丢弃：**当Web容器检测到JSP文件被修改时，会替换掉目前的JasperLoader的实例，并通过在建立一个新的Jsp类加载器来实现JSP文件的HotSwap功能。**<p>
对于Tomcat的6.X版本，只有指定了tomcat/conf/catalina.properties配置文件的server.loader和share.loader项后才会真正简历Catalina ClassLoader和SharedClassLoader的实例，否则在用到这两个类加载器的地方都会用CommonClassLoader的实例代替，而默认的配置文件中没有设置这两个loader项，所以Tomcat6.X顺理成章的把/common、/server和/shared三个目录默认合并到一起变成一个/lib目录，这个目录里的类库相当于以前/common目录中类库的作用。如果默认设置不能满足需要，用户可以通过修改配置文件指定server.loader和share.loader的方式重新启用Tomcat5.X的加载器架构。<p>
Tomcat加载器架构实现采用了官方推荐的双亲委派模型。<p>
##### tomcat类加载场景:
> 如果有10个web应用程序都是用Spring来进行组织和管理，可以把Spring放到Common或Shared目录下让这些程序共享。Spring要对用户程序的类进行管理，自然要能访问到用户程序的类，而用户程序显然是放在/WebApp/WEB-INF目录中的，那么被CommonClassLoader或SharedClassLoader加载的Spring如何访问并不在其家在范围内的用户程序呢？<p>
解析：按照主流的双亲委派机制，显然无法做到让父类加载器加载的类去访问子类加载器加载的类。而使用线程上下文类加载器来加载，可以让父类加载器请求子类加载器去完成类加载的动作。（源码部分）Spring源码中可以发现，Spring加载类所用的ClassLoader是通过Thread.currentThread().getContextClassLoader()来获取的，而当线程创建时会默认setContextClassLoaderAPPClassLoader),即线程上下文类加载器被设置为APPClassLoader,spring中始终可以获取到这个APPClassLoader(在Tomcat中就是WebAPPClassLoader)子类加载器来加载Bean，以后任何一个线程都可以通过getContextClassLoader()获取到WebAPPClassLoader来getBean。