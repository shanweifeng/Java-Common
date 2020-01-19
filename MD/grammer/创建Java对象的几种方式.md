### [java中创建对象的5种方式](https://www.cnblogs.com/wxd0108/p/5685817.html)

|创建方式|注释|
|--------|--------|
|使用new关键字|调用了构造函数|
|使用Class类的newInstance方法|调用了构造函数|
|使用Constructor类的newInstance方法|调用了构造函数|
|使用clone方法|没有调用构造函数|
|使用反序化|没有调用构造函数|

* 使用new关键字创建对象
>> 使用这种方式创建对象可以调用任意形式的构造方法(无参的和带参数的).
```Java
Employee employee = new Employee();
```
  
* 使用Class类的newInstance方法
>> 这个方法只能调用无参数的构造函数
```Java
Employee employee = Class.forName("根路径.Employee").newInstance();
or
Employee employee = Employee.class.newInstance();
```
* 使用Constructor类的newInstance方法
>> 类似class类的newInstance方法，Class类的newInstance方法最终调用的也是Constructor类。可以通过Constructor类的newInstance方法调用有参数的和私有的构造函数。
```java
Constructor<Employee> constructor = Employee.class.getConstructor();
Employee employee = constructor.newInstance();
```
这两种newInstance方法就是所谓的反射。实际上Class类的newInstance方法内部调用的Constructor类的newInstance方法。这也是众多框架，如Spring、hibernate、Struts等使用后者的原因。想了解这两个newInstance方法的区别，请看这篇[Creating objects through Reflection in Java with Example](https://programmingmitra.blogspot.in/2016/05/creating-objects-through-reflection-in-java-with-example.html)
***
* 使用Clone方法
>> 无论何时我们调用一个对象的clone方法，jvm就会创建一个新对象，将前面对象的内容全部拷贝进去。用clone方法创建对象并不会调用任何构造函数。<p>
要实现clone方法，我们需要先实现Cloneable接口并实现其定义的clone方法。clone方法是Object对象的原始方法。在拷贝时如果没有特别标明，则基本都是浅拷贝(如果对象中存在其他对象元素，则拷贝的时候如果是浅拷贝，拷贝前后对象会共用一个对象元素实例导致安全问题).
```java
Employee employee = (Employee) emp3.clone();
```
* 使用反序列化
>> 当我们序列化和反序列化一个对象，jvm会给我们创建一个单独的对象。在反序列化时，jvm创建对象并不会调用任何构造函数。为了反序列化一个对象，我们需要让我们的类实现Serializable接口
```java
ObjectInputStream in = new ObjectInputStream(new FileInputStream("data.obj"));
Employee employee = (Employee) in.readObject();
```

#### [部分区别-摘抄](https://www.cnblogs.com/baizhanshi/p/5896092.html)
* Class类位于Java的lang包中，而而Constructor类类是Java反射机制的一部分。
* Class类的newInstance只能触发无参数的构造方法创建对象，而而Constructor类类的newInstance能触发无参数或者任意参数的构造方法来创建对象。
* Class类的newInstance需要其他构造方法是共有的或者对调用方法可见的，而Constructor类的newInstance方法可以在特定环境下调用私有构造方法来创建对象。
* Class类的newInstance方法抛出类构造函数的异常，而而Constructor类的newInstance包装了一个InvocationTargetException异常。
<p>Class类本质上调用了反射包Constructor类中的无参数的newInstance方法，捕获了InvocationTargetException,将构造器本身的异常抛出.