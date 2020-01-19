### [获取Class字节码对象的方式](https://blog.csdn.net/caidie_huang/article/details/52562757)
> 每个类被加载后，系统就会为该类生成一个对应的字节码对象，通过该字节码对象就可以访问到JVM中的对应类。

* 使用类的class属性获取字节码对象
```java
Class<java.util.Date> clz1 = java.util.Date.class;
``` 
* 通过Class类中的静态方法forName(String className),传入类的全限定名(必须添加完整包名)
```java
Class<?> clz2 = Class.forName("java.util.Date");
```
* 通过对象的getClass方法来实现，其中getClass()是Object类中的方法，所有的对象都可以调用该方法
```java
java.util.Date str = new java.util.Date();
Class<?> clz3 = str.getClass();
```
> 第一种方式和第二种方式都是直接根据类来获取字节码对象，相比之下，第一种方式更加安全，因为在编译时期就可以检查要访问的Class对象是否存在，同时不用调用方法，性能也更好，因此用第一种方式比较多。但是如果只能得一个字符粗串如"java.lang.String"就只能使用第二种方式否则可能会抛出ClassNotFoundException异常。<p>
注意，同一个类在JVM中只存在一份字节码对象，上述三种方式生成的对象都是相等的。

### 九大内置Class实例
> JVM中预先提供好的Class实例: byte short int long float double boolean char void<p>
在8大基本数据类型的包装类中都有一个常量:TYPE，用于返回该包装类对应基本类的字节码对象，因此Integer。TYPE = int.class,但是Integer和int是不同的数据类型。

* 数组的Class实例：数组是引用数据类型
1. 数组类型。class
2. 数组对象.getClass()
> 所有具有相同维数和相同元素类型的数组共享同一份字节码对象，和元素没有关系？