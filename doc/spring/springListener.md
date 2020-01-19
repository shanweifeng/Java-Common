### spring的各种监听器

##### 定义：
>  listener监听器主要是实现了javax.servlet.ServletContextListener接口的服务端程序，它跟过滤器一样随web应用启动而启动，只需要初始化一次，以后都可以进行监听。一般主要用于ServletContext、HttpSession、HttpServletSession这三个对象中的属性变更信息事件监听。

* 使用listener步骤：
> 1、通过实现具体接口创建实现类(可实现多个监听器接口)<p>
2、配置实现类成为监听器，有两种配置方式：<p>
>> a、直接用@WebListener注解修饰实现类<p>
b、通过web.xml方式配置，代码如下：
```java
<listener>
    <listener-class>com.zrgk.listener.MyListener</listener-class>
</listener>
```

* 一、对request进行监听
> 应用实例：实现对javax.servlet.ServletRequestListener接口的监听，也就是HttpRequestServlet进行监听
>> 1、Web.xml中的配置
```java
<listener>
    <description>HttpRequestServlet监听</description>
    <listener-class>com.check.listener.MyRequestContextListener</listener-class>
</listener>
```

> >2、在MyRequestContextListener类中对ServletRequestListener接口的实现
```java
package com.check.listener;
import javax.servlet.ServletRequestEvent;
import javax.servlet.ServletRequestListener;
import javax.servlet.http.HttpSessionEvent;
import javax.servlet.http.HttpSessionListener;

public class MyRequestContextListener implements ServletRequestListener {
    
    @Override
    public void requestDestroyed(ServletRequestEvent event) {
        System.out.println("Request销毁成功" + event.getServletRequest());
    }
    
    public void requestInitialized(ServletRequestEvent event) {
        System.out.println("Request创建成功" + event.getServletRequest());
    }
}
```
>> 这样就可以对request请求进行监听，其中对象的创建和销毁时间为请求发生时候对象创建到响应产生的时候request对象销毁。

* 对session进行监听
> 1、web.xml中的配置
```java
<listener>
    <description>HttpSessionListener监听器</description>
    <listener-class>class pah </listener-class>
</listener>
```
> 实现HttpSessionListener 接口
> 2、session id的创建与销毁 超市设置等

* 实现对servletContext时间的监听
> 1、web.xml配置
2、实现类实现ServletContextListener 接口

* 对其中属性进行一个监听例如ServletContextAttributeListener
> 1、web.xml配置
2、实现类实现ServletContextAttributeListener 接口

* spring常用listener
> 1、IntrospectorCleanupListener
>> 该listener应该注册为web.xml中的第一个listener，确保web应用程序的类加载器以及期价在的类正确的释放资源

> 2、Log4jConfigListener

> 3、WebAppRootListener

> 4、ContextLoaderListener
>> 启动web容器时，自动装配ApplicationContext的配置信息。

> 5、RequestContextListener
>> 
