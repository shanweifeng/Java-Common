### [Java四种引用类型](https://www.jianshu.com/p/147793693edc)
[参考](https://gitee.com/brucekankan)
[简书地址](http://www.jianshu.com/u/1f0067e24ff8)
> java.lang.ref是Java类库中比较特殊的一个包，它提供了与Java垃圾回收器密切相关的引用类。StrongReference(强引用)、SoftReference(软引用)、WeakReference(弱引用)、PhantomReference(虚引用)。
#### 引用类型对比

|引用类型|取得目标对象方式|垃圾回收条件|是否可能内存泄漏|
|--------|----------------|------------|----------------|
|StrongReference|直接调用|不回收|可能|
|SoftReference|通过get()方法|视内存情况回收|不可能|
|WeakReference|通过get()方法|永远回收|不可能|
|PhantomReference|无法取得|不回收|可能|

* StrongReference(强引用)
> 如果一个对象具有强引用，垃圾回收器绝不会回收它。当内存空间不足，jvm虚拟机宁愿抛出OutOfMemoryError错误，也不会靠随意回收具有强引用的对象来解决内存不足的问题。
```java
String[] arr = new String[]}{"a","b","c"};
```
* SoftReference(软引用)
> 如果一个对象只具有软引用，则内存空间足够，垃圾回收器就不会回收它，如果内存空间不足了，就会回收这些对象的内存。只要垃圾回收器没有回收它，该对象就可以被程序使用。软引用可用来实现内存敏感的高速缓存。<p>
软引用可以可一个引用队列(ReferenceQueue)联合使用，如果软引用所引用的对像那个被垃圾回收器回收，JVM就会把这个软引用加入到与之关联的引用队列中。
```java
// 示例1
SoftReference<String[]> softBean = new SoftReference<String[]>(new String[]{"a","b","c"});
// 示例2
ReferenceQueue<String[]> referenceQueue = new ReferenceQueue<String[]>();
SoftReference<String[]> softBean = new SoftReference<String[]>(new String[]{"a","b","c"}, referenceQueue);
```
* WeakReference(弱引用)
> 弱引用与软引用的区别在于: 值具有弱引用的对象拥有更短暂的生命周期。在垃圾回收器线程扫描它所管辖的内存区域的过程中，一旦发现了只具有弱引用的对象，不管当前内存空间是否足够，都会回收它的内存。不过，由于垃圾回收器是一个优先级很低的线程，因此不一定会很快发现那些只具有弱引用的对象。<p>
弱引用可以和一个引用队列(ReferenceQueue)联合使用，如果弱引用所引用的对象被垃圾回收，jvm就会把这个弱引用加入到与之关联的引用队列中。
```java
WeakReference<String[]> softBean = new WeakReference<String[]>(new String[]{"a","b","c"});
// 示例2
ReferenceQueue<String[]> referenceQueue = new ReferenceQueue<String[]>();
WeakReference<String[]> softBean = new WeakReference<String[]>(new String[]{"a","b","c"}, referenceQueue);
```
* PhantomReference(虚引用)
> 与其他几种引用不同，虚引用并不会决定对象的生命周期。如果一个对象仅持有虚引用，那么它就和没有引用一样，在任何时候都可能被垃圾回收器回收。<p>
虚引用主要用来跟踪对象被垃圾回收器回收的活动。虚引用与软引用和弱引用的一个区别在于: 虚引用**必须**和引用队列(ReferenceQueue)联合使用。当垃圾回收器准备回收一个对象时，如果发现它还有虚引用，就会在回收对象的内存之前将这个虚引用加入到与之关联的引用队列中
```java
ReferenceQueue<String[]> referenceQueue = new ReferenceQueue<String[]>();
PhantomReference<String[]> softBean = new PhantomReference<String[]>(new String[]{"a","b","c"}, referenceQueue);
```
（引用示例）
##### SoftReference 和 WeakReference的生命周期
* SoftReference生命周期分析
```java
// -Xms10M -Xmx10M -Xmn5M -XX:+PrintGCDetails 执行语句时加上启动参数
public void soft() {
    SoftReference[] softArr = new SoftReference[5];
    softArr[0] = new SoftReference<byte[]>(new byte[1024 * 1024 * 2]);
    System.out.println("GC 前===》" + softArr[0].get());
    System.gc();
    System.out.println("第一次GC 后===》" + softArr[0].get());
    softArr[1] = new SoftReference<byte[]>(new byte[1024 * 1024 * 2]);
    System.gc();
    System.out.println("第二次GC 后===》" + softArr[0].get());
    softArr[2] = new SoftReference<byte[]>(new byte[1024 * 1024 * 2]);
    System.gc();
    System.out.println("第三次GC 后===》" + softArr[0].get());
    softArr[3] = new SoftReference<byte[]>(new byte[1024 * 1024 * 2]);
    //System.gc(); 这里不需要显示执行，堆内存已经满了，jvm会自已执行。
    System.out.println("第四次GC 后===》" + softArr[0].get());
}
```
> 只有内存不足时财货被回收，否则不管GC执行几次都不会被回收
* WeakReference生命周期
```java
// -Xms10M -Xmx10M -Xmn5M -XX:+PrintGCDetails 执行语句时加上启动参数
public void weak() {
        WeakReference<Integer> weak= new WeakReference<Integer>(new Integer[100]);
        System.out.println("GC 前===》" + weak.get());
        System.gc();
        System.out.println("第一次GC 后===》" + weak.get());
}
```
> 只要执行GC,弱引用对象就会被回收，其生命周期是在下一次GC之前。