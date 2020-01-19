## Servlet中的一些问题
* [Servlet](https://www.runoob.com/servlet/servlet-life-cycle.html)

* 1、Servlet的生命周期
```text
Servlet接口中定义了5个方法，其中前三个方法与Servlet生命周期相关：
    void init(ServletConfig config) throws ServletExceptiom;
    void service(ServletRequest req, ServletResponse resp) throws ServletException, java.io.IOException
    void destroy();
    java.lang.String getServletInfo();
    ServletConfig getServletConfig();
生命周期：Web容器加载Servlet并将其实例化后，Servlet生命周期开始
Servlet通过调用init()方法进行初始化
调用service()方法来处理客户端的请求
通过调用destroy()方法终止(结束)
最后由JVM的垃圾回收器进行垃圾回收。
```

* 2、Servlet为什么不是线程安全的？为什么一个Servlet类只能有一个实例？
 ```text
为什么Servlet不是线程安全的？一个Servlet类只有一个实例，当出现多线程访问同一个实例时，如果存在类变量或实例变量，会出现线程安全问题。为什么一个Servlet类只能有一个实例？ 一个是说性能问题，如果每次请求都创建的话，内存开销、时间、回收等都会影响请求速度。为什么不能是多个实例呢？(有限的个数)  这里如果需要深入透彻的了解Tomcat接收HTTP的细节以及与Servlet交互的细节，需要深入了解Tomcat的架构和源码！！！
```
* 3、Servlet和CGI的区别？什么是CGI？
```text
1、什么是CGI(Common gateway interface 通用网关接口)：
    · CGI是外部扩展应用程序与www服务器交互的的一个标准接口。按照CGI标准辨析的外部扩展应用程序可以处理客户端(一般是www浏览器)输入的协同工作数据，完成客户端与服务器的交互操作。如可以编写CGI外部扩展程序来访问外部数据。CGI一般分梁红在那个：标准CGI和缓冲CGI。所有的www服务器均应支持CGI，按标准CGI编写的程序与具体的www服务器无关。而按缓冲CGI编写的程序与www服务器有关。https://www.cnblogs.com/lidabo/p/5756248.html
2、Servlet和CGI的区别：
CGI的不足之处：1、需要为每一个请求启动一个操作CGI程序的系统进程。如果请求频繁，这将会带来很大的开销；2、需要为每个请求加载和运行一个CGI程序，这将带来很大的开销；3、需要重复编写处理网络协议的代码以及编码。
Servlet的优点：1、只需要启动一个操作系统进程以及加载一个JVM，大大降低系统开销；2、如果多个请求需要做同样处理的时候，这时候只需要加载一个类，这也大大降低了开销；3、所有动态加载的类可以实现对网络协议以及请求解码的共享；4、Servlet能直接和Web服务器交互，而普通的CGI程序不能。Servlet还能在各个程序之间共享数据，是数据库连接池之类的功能很容易实现。

补充：Servlet是一个特殊的java程序，一个基于Java的Web应用通常包含一个或多个Servlet类。Servlet不能够自行创建并执行，它是在Servlet容器中运行的，容器将用户的请求传递给Servlet程序，并将Servlet的响应回传给用户。通常一个Servlet会关联一个或多个JSP页面。以前CGI经常因为性能开销上的问题被诟病吗，后来的Fast CGI解决了CGI效率上的问题。

```
* 4、[Get和POST请求的区别，Http请求方式分别有哪些？](https://blog.csdn.net/KUKI123321/article/details/78219252)
```text
Http协议的8中请求：
options:返回服务器针对特定资源所支持的HTML请求方法 或 web服务器发送*测试服务器功能(允许客户端查看服务器性能)
Get:向特定资源发出请求(请求指定页面信息，并返回实例主体)
Post:向指定资源提交数据进行处理请求(提交表单、上传文件)，有可能导致新的资源或原有资源的修改
Put: 向指定资源位置上上传其最新内容(从客户端向服务器传输的数据渠道指定文档的内容)
Head: 与服务器与get请求一致的响应，响应体不会反悔，获取包含在小消息头中的原信息(与Get请求类似，反悔的响应中没有具体内容，用于获取报头)
Delete:请求服务器删除request-url所标示的资源*(请求服务器删除页面)
Trace: 回显服务器收到的请求，用于测试和诊断
Connect: HTTP/1.1协议中能够将连接改为管道方式的代理服务器
http服务器至少能实现get head post方法，其他都是可选的。

Get和POST请求的区别：
get用于获取信息，应该是安全的和幂等的，且最好不使用该方式修改数据。长度有限制最大1024 只接受ASCII字符
post可能修改服务器上的资源，长度理论上没有限制 但是实际上还是有的 不同环境下限制不一样 数据类型的字符没有限制
但是最大的不同是在specification 而不是implementation:specification是RFC(Request For Comments 征求意见稿)，implementation则是所有实现了specification中描述的代码/库/产品等。https://www.zhihu.com/question/28586791

```
* [5、多种方式实现跨域请求](https://blog.csdn.net/qq_36140085/article/details/81606508)
```text
1、图片ping或script标签跨域
2、JSONP跨域
3、cors(Cross-Origin Resource Sharing)跨域
4、window.name+iframe
5、window.postMessage()
6、修改document.domain跨子域
7、WebSocket
8、代理
9、location.hash 跨域
```

* 6、转发(Forward)和重定向(Redirect)的区别
```text
转发是服务器行为，重定向是客户端行为
```

* 7、Servlet与线程安全
```text
Servlet不是线程安全的，多线程并发的读写会导致数据不同步的问题。在使用单实例多线程编码时，尽量不用类变量和实例变量，否则会导致数据不一致问题。
```

* 8、JSO的内置对象
```text
JSP有9个内置对象：
request：封装客户端的请求，其中包含来自GET或POST请求的参数
response：封装服务器对客户端的响应
pageContext：通过该对象可以获取其他对象；
session：封装用户会话的对象
application：封装服务器运行环境的对象
out：输出服务器响应的输出流对象
config：Web应用的配置对象
page：JSP页面本身(相当于Java程序中的this)
exception:封装页面抛出异常的对象
```

* Request对象的主要方法
```text
setAttribute(String name,Object)：设置名字为name的request 的参数值
getAttribute(String name)：返回由name指定的属性值
getAttributeNames()：返回request 对象所有属性的名字集合，结果是一个枚举的实例
getCookies()：返回客户端的所有 Cookie 对象，结果是一个Cookie 数组
getCharacterEncoding() ：返回请求中的字符编码方式 = getContentLength() ：返回请求的 Body的长度
getHeader(String name) ：获得HTTP协议定义的文件头信息
getHeaders(String name) ：返回指定名字的request Header 的所有值，结果是一个枚举的实例
getHeaderNames() ：返回所以request Header 的名字，结果是一个枚举的实例
getInputStream() ：返回请求的输入流，用于获得请求中的数据
getMethod() ：获得客户端向服务器端传送数据的方法
getParameter(String name) ：获得客户端传送给服务器端的有 name指定的参数值
getParameterNames() ：获得客户端传送给服务器端的所有参数的名字，结果是一个枚举的实例
getParameterValues(String name)：获得有name指定的参数的所有值
getProtocol()：获取客户端向服务器端传送数据所依据的协议名称
getQueryString() ：获得查询字符串
getRequestURI() ：获取发出请求字符串的客户端地址
getRemoteAddr()：获取客户端的 IP 地址
getRemoteHost() ：获取客户端的名字
getSession([Boolean create]) ：返回和请求相关 Session
getServerName() ：获取服务器的名字
getServletPath()：获取客户端所请求的脚本文件的路径
getServerPort()：获取服务器的端口号
removeAttribute(String name)：删除请求中的一个属性
```

*