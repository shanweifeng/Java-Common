### `Java`中`hashCode`和`equals`相关问题阐述

1. 默认情况下hashCode相同是不是意味着equals方法相等？
2. 默认情况下equals方法相等是不是意味着hashCode相同？
3. 重写equals方法是不是需要重写hashCode方法？ 为什么？

* ### 默认情况下hashCode相同是不是意味着equals方法相等？equals方法相等是不是意味着hashCode相同？
> 之所以将这两个问题放在一起，是因为这两个问题可以联系在一起回答，在Object类中的hashCode和equals方法的注释中已经说明了答案。
> 如果两个对象根据equals方法判定相等，那么这两个对象的hashCode方法必定是相同的integer的整型值。<p>
1、equals相等的两个对象，其hashCode必定相等。
2、通过equals判定前，必定有hashCode值比较判断的步骤。
```java
if two objects are equal according to the equals(Object) methos,than calling the hashCode method on each of the two objects must produce the same integer result.
```

> hashCode方法的一种典型实现是将对象在堆内的地址通过某种手段转成一个integer整型值，但是该方法是native修饰的，需要通过查阅openjdk的源码得到。
```java
as much as is reasonably practical, the hashCode method defined by class Object does return distinct integers for distinctObjects.(this is typically implemented by converting the internal address of the object into an integer, but this implementation technique is not required by the java TM programming language.)
```

* 重写equals方法是不是需要重写hashCode方法？为什么？
> 首先该问题的答案仍然在Object中的equals方法注释中有明确。
```java
note that it is generally necessary to override the hashCode method whenever this method is overridden, so as to maintain the general contract for the hashCode method, which states that equal objects must have equal hash codes.
```
> 只要equals方法被重写了就必须重写hashCode方法，此处也解释了“必须”的原因，要维持hashCode方法的contract约定，hashCode方法中申明了相同的对象必须有相同的hash code。


### equals方法的性质
* 自反性(reflexive)
> 对于任意不为null的引用值X,X.equals(X)一定是true

* 对称性(symmetric)
> 对于任意不为null的引用值x和y，当且仅当x.equals(y)是true时，y.equals(x)也是true。

* 传递性(transitive)
> 对于任意不为null的引用值x、y和z,如果x.equals(y)是true，同时y.equals(z)是true，那么x.equals(z)一定是true。

* 一致性(consistent)
> 对于任意不为null的引用值x和y，如果用于equals比价的对象信息没有被修改的话，多次调用时x.equals(y)要么一致的返回true要么一致的返回false。
