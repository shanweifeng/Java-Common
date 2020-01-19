### spring-boot-actuator
> 通过Spring Boot Actuator进行日常的微服务监控治理
#### Actuator监控
> Spring Boot 使用“习惯优于配置的理念”，采用包扫描和自动化配置的机制来加载依赖Jar中的Spring bean,不需要任何xml配置，就可以实现Spring的所有配置。虽然这样做能让我们的代码变得非常简洁，但是整个应用的实例创建和依赖关系等信息都被离散到了各个配置类的注解上，这使得分析整个应用中资源和实例的各种关系变得非常困难。<p>
Actuator是Spring Boot提供的对应用系统的自省和监控的集成功能，可以查看应用配置的详细信息，例如自动化配置信息、创建Spring beans以及一些环境属性等.<p>
为保证actuator暴露的监控接口的安全性，需要添加安全控制的依赖spring-boot-start-security依赖，访问应用监控端点时，都需要输入验证信息。Security依赖，可以选择不加，不进行安全管理，但是不建议这么做。

#### Actuator的REST接口
> Actuator监控分为两类：原生端点和用户自定义端点。自定义端点主要是指扩展性，用户可以根据自己的实际应用，定义一些比较关心的指标，在运行期间进行监控。<p>
原生端点是在应用程序里提供众多Web接口，通过他们了解应用程序运行时的内部状况
* 原生端点可以分为三类：
> 1.应用配置类：可以查看应用在运行期的静态信息：例如自动配置信息、加载的 Spring bean信息、yml文件配置信息、环境信息、请求映射信息；<p>
> 2.度量指标类:主要是运行期的动态信息，例如堆栈、请求链、一些健康指标、metrics信息等；<p>
> 3.操作控制类：主要是指shutdown，用户可以发送一个请求将应用的监控功能关闭。
* Actuator提供了13个接口，具体如下表所示

|HTTP方法|路径|描述|
|--------|----|----|
|GET|/auditevents|显示应用暴露的审计事件(比如认证进入、订单失败)|
|GET|/beans|描述应用程序上下文里全部的Bean以及它们的关系|
|GET|/conditions|就是1.0的/autoconfig,提供一份自动配置生效的条件情况记录哪些自动配置条件通过了，哪些没有通过|
|GET|/configprops|描述配置属性(包涵默认值)如何注入Bean|
|GET|/env|获取全部环境属性|
|GET|/env/{name}|根据名称获取特定的环境属性值|
|GET|/flyway|提供一份Flyway数据库迁移信息|
|GET|/liquidbase|显示Liquibase数据库迁移的纤细信息|
|GET|/health|报告应用程序的健康指标，这些值由HealthIndicator的实现类提供|
|GET|/heapdump|dump一份应用的JVM堆信息|
|GET|/httptrace|显示HTTP足迹，最近100个HTTP request/response|
|GET|/info|获取应用程序的定制信息，这些信息由info打头的属性提供|
|GET|/logfile|返回log file中的内容(如果logging.file或者logging.path被设置)|
|GET|/loggers|显示和修改配置的loggers|
|GET|/metrics|报告各种应用程序度量信息，比如内存用量和HTTP请求计数|
|GET|/metrics/{name}|报告指定名称的应用程序度量值|
|GET|/scheduledtasks|展示应用中的定时任务信息|
|GET|/sessions|如果使用了Spring Session展示应用中的HTTP sessions信息|
|POST|/shutdown|关闭应用程序，要求endpoints.shutdown.enabled设置为true|
|GET|/mappings|描述全部的URI路径以及它们和控制器(包含Actuator端点)的映射关系|
|GET|/threaddump|获取线程活动的快照|

### 快速上手
##### 项目依赖
```java
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
  </dependency>
</dependencies>
```
##### 配置文件
```java
info.app.name=spring-boot-actuator
info.app.version= 1.0.0
info.app.test=test

management.endpoints.web.exposure.include=*
management.endpoint.health.show-details=always
#management.endpoints.web.base-path=/monitor

management.endpoint.shutdown.enabled=true
```
* management.endpoints.web.base-path=/monitor 代表启用单独的URL地址来监控Spring boot应用，为了安全一般都启用独立的端口来访问后端的监控信息
* management.endpoint.shutdown.enable=true启用借口关闭Spring Boot.
