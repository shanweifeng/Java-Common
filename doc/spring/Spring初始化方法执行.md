## spring中的DisposableBean和InitializingBean，ApplicationContextAware、BeanPostProcessor的用法
* https://blog.csdn.net/glory1234work2115/article/details/51815911
* https://www.cnblogs.com/zr520/p/4894554.html

* InitializingBean:
> init-method方法:初始化bean的时候执行，可以针对某个具体的bean进行配置。init-method需要在applicationContext.xml配置文档中bean的定义里头写明。例如：
```java
<bean id="TestBean" class="nju.software.xkxt.util.TestBean" init-method="init"></bean> 
```
这样，当TestBean在初始化的时候会执行TestBean中定义的init方法。<p>
afterPropertiesSet方法，初始化bean的时候执行，可以针对某个具体的bean进行配置。afterPropertiesSet 必须实现 InitializingBean接口。实现 InitializingBean接口必须实现afterPropertiesSet方法。

* BeanPostProcessor:
> 针对所有Spring上下文中所有的bean，可以在配置文档applicationContext.xml中配置一个BeanPostProcessor，然后对所有的bean进行一个初始化之前和之后的代理。BeanPostProcessor接口中有两个方法： postProcessBeforeInitialization和postProcessAfterInitialization。 postProcessBeforeInitialization方法在bean初始化之前执行， postProcessAfterInitialization方法在bean初始化之后执行。

>> 总之，afterPropertiesSet 和init-method之间的执行顺序是afterPropertiesSet 先执行，init-method 后执行。从BeanPostProcessor的作用，可以看出最先执行的是postProcessBeforeInitialization，然后是afterPropertiesSet，然后是init-method，然后是postProcessAfterInitialization。

* DisposableBean:
> destroy方法，在一个bean被销毁的时候，spring容器会帮你自动执行这个方法，估计底层原理也是差不多的，对于一些使用完之后需要释放资源的bean，我们都会实现这个接口，或者是配置destory-method方法。

* ApplicationContextAware：
> 属性注入的，但是这个ApplicationContextAware的不同地方在于，实现了这个接口的bean，当spring容器初始化的时候，会自动的将ApplicationContext注入进来