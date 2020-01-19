### [Java魔法类——Unsafe应用解析](https://segmentfault.com/a/1190000018161130)
> Unsafe是位于sun.misc包下的一个类，主要提供一些用于执行低级别、不安全操作的方法，如直接访问系统内存资源，自主管理内存资源等，这些方法在提升Java运行效率、增强Java语言底层资源操作能力方面起到了很大作用。但由于Unsafe类使用Java语言 拥有了类似C语言指针一样操作内存空间的能力，这也无疑增加了程序发生相关指针问题的风险。在程序中过度、不正确使用Unsafe类会是的程序出错的概率变大，是的Java这种安全的语言变得不再安全，因此对Unsafe的使用需要慎重。

##### 基本介绍
> Unsafe类为单例实现，提供静态方法getUnsafe获取Unsafe实例，当且仅当调用getUnsafe方法的类为引导类加载器所加载时才合法，否则抛出SecurityException异常。
```java
public final class Unsafe {
    private static final Unsafe theUnsafe;
    
    private Unsafe() {
        
    }
    @CallerSensitive
    public static Unsafe getUnsafe() {
        Class var0 = Reflection.getCallerClass();
        // 仅在引导类加载器BootstrapClassLoader加载时才合法
        if (!VM.usSystemDomainLoader(var0.getClassLoader())) {
            throw new SecurityException("Unsafe");
        } else {
            return theUnsafe;
        }
    }
}
```
*- 获取Unsafe实例方法-*
* 通过getUnsafe方法的使用限制条件出发，通过Java命令行命令 -Xbootclasspath/a把调用Unsafe相关方法的类A所在jar包路径追加到默认的Bootstrap路径中，使得A被引导类加载器加载，从而通过Unsafe.getUnsafe方法安全的获取Unsafe实例
```java
java -Xbootclasspath/a: ${path} // 其中path为调用Unsafe相关方法的类所在jar包路径
```
* 通过反射获取单例对象theUnsafe
```java
private static Unsafe reflectGetUnsafe() {
    try {
        Field field = Unsafe.class.getDeclareField("theUnsafe");
        field.setAccessible(true);
        return (Unsafe)field.get(null);
    } catch (Exception e) {
        log.error(e.getMessage(), e);
        return null;
    }
}
```

##### 功能介绍

|功能|详情|
|------|---|
|数组相关|1、返回数组元素内存大小；2、返回数组首元素偏移地址 |
|内存屏障|禁止load、store重排序|
|系统相关|1、返回内存页大小；2、返回系统指针大小|
|线程调度|1、线程挂起、恢复；2、获取、释放锁|
|内存操作|1、分配、拷贝、扩从、释放堆外内存；2、设置、获得给定地址中的值|
|CAS||
|Class相关|1、动态创建类(普通类&匿名类)；2、获取field的内存地址偏移量；3、检测、确保类初始化|
|对象操作|1、获取对象成员属性在内存偏移量；2、非常规对象实例化；3、存储、获取指定偏移地址的变量值(包含延迟生效、volatile语义)|

##### 内存操作
> 主要包括堆外内存的分配、拷贝、释放、给定地址值操作等方法
```java
// 分配内存、相当于C++的malloc函数
public native long allocateMemory(long bytes);
// 扩从内存
public native long reallocateMemory(long address, long bytes);
//释放内存
public native void freeMemory(long adddress);
// 在给定的内存块中设置值
public native void setMemory(Objecto, long offset, long bytes, byte value);
// 内存拷贝
public native void copyMemory(Object srcBase, long srcOffset, Object destBase, long destOffset, long bytes);
//获取给定地址设置值，忽略修饰限定符的访问限制。与此类似操作还有:getInt、getDouble、getLong、getChar等
public native Object getObject(Object o, long offset);
//为给定地址设置值，忽略修饰限定符的访问限制。与此类似操作还有: putInt、putDouble、putLong、putChar等。
public native void putObject(Object o, long offset, Object x);
//获取给定地址的byte类型的值(当且仅当该内存地址为allocateMemory分配时，此方法结果为确定的)
public native byte getByte(long address);
//为给定地址设置byte类型的值(当且仅当该内存地址为allocateMemory分配时，此方法结果才是确定的)
public native void putByte(long address, byte x);
```
> 通常Java中创建的对象都处于对内存中由JVM所管理，且遵循JVM的内存管理机制，JVM会采用垃圾回收机制同意管理内存。与之相对的是堆外存，存在于JVM管控之外的内存区域，Java中对堆外存的操作，依赖于Unsafe提供的操作堆外存的native方法。
* 使用堆外存的原因
> 1、对垃圾回收停顿的改善。由于堆外存是直接受操作系统管理而不是JVM，所以当我们使用堆外存时，即可保持较小的堆内存规模。从而在GC时减少回收停顿对于应用的影响。<p>
2、提升程序I/O操作的性能。通常在I/O通信过程中，会存在堆内存到堆外存数据拷贝操作，对于需要频繁进行内存间数据拷贝且生命周期较短的暂存数据，都建议存储到堆外存中。（零拷贝计术使用的即时堆外存）
* 典型应用
> DirectByteBuffer是Java用于实现堆外内存的一个重要类，通常用在通信过程中做缓冲池，如在netty、MINA等NIO框架中应用广泛。DirectByteBuffer对于堆外内存的创建、使用、销毁等逻辑均由Unsafe提供的堆外内存API来实现。<p>
下图为DirectByteBuffer构造函数，创建DirectByteBufferd的时候，通过Unsafe.allocateMemory分配内存、Unsafe.setMemory进行内存初始化，而后构建Cleaner对象用于跟踪DirectByteBuffer对象的垃圾回收，以实现当DirectByteBuffer被垃圾回收时，分配的堆外存一起被释放。![DirectByteBuffer_Constructor](/doc/image/directByteBuffer_constructor.png)
> Cleaner继承自[Java四大引用类型](/doc/jdk/java_reference.md)之一的虚引用PhantomReference(无法通过PhantomReference获取与之关联的对象实例，发生GC时一定会被回收),通常PhantomReference与引用队列ReferenceQueue结合使用，可以实现虚引用关联对象被垃圾回收时能够进行系统通知、资源清理等功能。如下图所示，当某个被Cleaner引用的对象将被回收时，JVM垃圾收集器会将此对象的引用放入到对象引用中的pending链表中，等待Reference-Handler进行相关处理。其中Reference-Handler为一个拥有最高优先级的守护线程，会循环不断地处理pending链表中的对象引用，执行Cleaner的clean方法进行相关清理工作。![Cleaner清理对象](/doc/image/Cleaner_pending.png)
所以当DirectByteBuffer仅被Cleaner引用时，其可以在任意GC时段被回收。当DirectByteBuffer实例对象被回收时，在Reference-Handler线程操作中，会调用Cleaner的clean方法根据创建Cleaner时传入的Deallocator来进行堆外内存的释放。
![DirectByteBuffer释放内存](/doc/image/directByteBuffer_deallocator.png)![reference执行handlerPending](/doc/image/reference_pending.png)

##### CAS相关
> CAS相关操作方法
```java
/**
* CAS
* @param o                包含要修改field的对象
* @param offset           对象中某field的偏移量
* @param expected         期望值
* @param update           更新值
* @return                 true| false
*/
public final native boolean compareAndSwapObject(Object o,long offset, Object expected, Object update);

public final native boolean compareAndSwapInt(Object o,long offset, int expected, int update);

public final native boolean compareAndSwapLong(Object o,long offset, long expected, long update);
```
> CAS即比较并替换，是实现并发算法时常用到的一种技术。包含三个操作数-内存位置、预期值以及新值。执行操作的时候将内存位置的值与预期原值比较，如果相匹配处理器会自动将该位置值更新为新值，否则处理器不做任何操作。由于CAS是一条CPU的院子指令(cmpxchg指令)，不会造成数据不一致问题，Unsafe提供的CAS方法(如compareAndSwapXXX)底层实现即为CPU指令cmpxchg.
* 典型应用
> 在java.util.concurrent.atomic相关类、Java AQS、CurrentHashMap等实现上有非常广泛的应用。如下图所示，AtomicInteger的实现中，静态字段valueOffset即为字段value的内存偏移地址，valueOffset的值在AtomicInteger初始化时，在静态代码块中通过Unsafe的objectFieldOffset方法获取。在AtomicInteger中提供的线程安全方法中，通过字段valueOffset的值可以定位到AtomicInteger对象中value的内存地址，从而可以根据CAS实现对value字段的原子操作。![AtomicInteger的valueOffset偏移地址获取](/doc/image/atomicInteger.png)
下图为某个AtomicInteger对象自增操作前后的内存示意图，兑现那个的基地址baseAddress="0x110000",通过baseAddress + valueOffset得到value的内存地址valueAddress="0x11000c"；然后通过CAS进行原子性的更新操作，成功则返回否则基础重试，直到更新成功为止。![atomicInteger_incr内存操作示意图](/doc/image/atomicInteger_incr.png)

##### 线程调度
> 包括线程挂起、恢复、锁机制等方法
```java
// 取消阻塞线程
public native void unpark(Object thread);
// 阻塞线程
public native void park(boolean isAbsolute, long time);
// 获得对象锁(可重入锁)
@Deprecated
public native void monitorEnter(Object o);
//释放对象锁
@Deprecated
public native boolean monitorExit(Object o)
//尝试获取锁对象
@Deprecated
public native boolean tryMonitorEnter(Object o);
```
>方法park、unpark即可实现线程的挂起和恢复，将一个线程进行挂起是通过park方法实现的，调用park方法后，线程将一直阻塞直到超时或者中断等条件出现；unpark可以终止一个挂起的线程使其恢复正常。

>> 线程的生命周期：新建状态、就绪状态、运行状态、阻塞状态及死亡状态。![thread_status](/doc/image/thread_status.jpg)
1、join方法：在A线程中调用B线程的join方法，这时B线程继续运行，A线程停止进入阻塞状态，等B线程运行完毕后A线程继续执行。<p>
2、sleep方法：线程调用sleep方法后本线程停止(进入阻塞状态)，不让出CPU<p>
3、yield方法：线程这种调用yield方法后本线程并不停止，运行权又本线程和优先级不低于本线程的线程来抢<p>
4、wait方法：当前线程转入阻塞状态，让出CPU的控制权，解除锁定<p>
5、notify方法：唤醒因为wait进入阻塞状态的其中一个线程<p>
6、notifyAll方法：唤醒因为wait进入阻塞状态的所有线程<p>
>>> 线程挂起(wait)和睡眠(sleep)是主动的，挂起恢复需要主动完成，睡眠恢复则是自动完成的，睡眠时间一到就会恢复到就绪状态。阻塞是被动的，是在等待某种事件或者资源的表现，一旦获得所需资源或者事件信息就会自动回到就绪状态。<p>
睡眠和挂起是两种行为，阻塞是一种状态。


* 典型应用
> Java锁和同步器框架的核心类AbstractQueuedSynchronizer,就是通过调用LockSupport.park()和LockSupport.unpark()实现线程的阻塞和唤醒的，而LockSupport的park.unpark方法实际调用Unsafe的park、unpark方法来实现。

##### Class相关
> 这里主要提供Class和其静态字段的操作相关方法，包含静态字段内存丁文、定义类、定义匿名类、检验&确保初始化等
```java
// 获取给定静态字段的内存地址偏移量，这个值对于给定的字段是唯一且固定不变的。
public native long staticFieldOffset(Field f);
// 获取一个静态类中给定字段的对象指针
public native Obhect staticFieldBase(field f);
// 判断是否需要初始化一个类，通常在获取一个类的静态属性的时候(因为一个类如果没有初始化，它的静态属性也不会初始化)使用。当且仅当ensureClassI你天力泽的方法不生效时返回false。
public native boolean shouldBeInitialized(Class<?> c);
//检测给定的类是否已经初始化。通常在获取一个类的静态属性的时候(因为一个类如果没有初始化，它的静态属性也不会初始化)使用。
public native void ensureClassInitialized(Class<?> c);
//定义一个类，此方法会跳过JVM的所有安全检查，默认情况下，ClassLoader(类加载器)和 ProtectionDomain(保护域)实例来源于调用者
private native Class<?> defineClass(String name, byte[] b, int off, int len, ClasLoader loader, ProtectionDomain protectionDomain);
// 定义一个匿名类
private native Class<?> defineAnonymousClass(Class<?> hostClass, byte[] data, Object[] cpPatches);
```

* 典型应用
> 从Java8开始，JDK使用invokedynamic及VM Anonymous Class结合来实现Java语言层面上的Lambda表达式.<p>
1.invokedDynamic: 是java7为了实现在JVM上运行动态语言而引入的一条心的虚拟机指令，可以实现在运行期动态解析出调用点限定符所引用的方法，然后再执行该方法，invokedynamic指令的分派逻辑是由用户设定的引导方法决定。<p>
2、VM Anonymous Class：可以看做是一种模板机制，针对于程序动态生成很多结构相同、仅若干常量不同的类时，可以先创建包含常量占位符的模板类，而后通过Unsafe.defineAnonymousClass方法定义具体类时填充模板的占位符生成具体的匿名类。生成的匿名类不显式挂在任何ClassLoader下面，只要当该类没有存在的实例对象、且没有强引用来引用该类的Class对象时，该类就会被GC回收。故而VM Anonymous Class相比于Java语言层面的匿名内部类无需通过ClassLoader进行类加载且更易回收。

##### 对象操作
> 主要包含对象成员属性相关操作及非常规的对象实例化方式等相关方法
```java
// 返回对象成员属性在内存地址相对于此对象的内存地址的偏移量
public native long objectFieldOffset(Field f);
// 获得给定对象的指定地址偏移量的值，与此类似操作还有: putInt,putDouble,putLong,putChar等
public native Object getObject(Object o, long offset);
// 给定对象的指定地址偏移量设置，与此类事操作还有： putInt,putDouble,putLong,putChar等
public native void putObject(Object o, long offset, Object x);
// 从对象的指定偏移量处获取变量的引用，使用volatile的加载语义
public native Object getObjectVolatile(Object o, long offset);
// 存储变量的引用到对象的指定的偏移量出，使用volatile的存储语义
public native void putObjectVolatile(Object o, long offset, Object x);
// 有序、延迟版本的putObjectVolatile方法，不保证值得改变被其他线程立即看到。只有在field被Volatile修饰符修饰时邮箱
public native void putOrderedObect(Object o, long offset, Object x);
// 绕过构造方法、初始化代码来创建对象
public native Object allocateInstance(Class<?> cls) throws InstantiationException;
```

* 典型应用
> 1、常规对象实例化方式:通常所用到的创建对象的方式，从本质上讲都是通过new机制来实现对象的创建。但是这种方式在：如果类只提供了有参构造函数且无显示声明无参构造韩式时，则必须使用有参构造函数进行对象构造，使用有参构造是必须传递对于的参数才能完成对象实例化。<p>
2、非常规的实例化方式：在Unsafe中提供allocateInstance方法，仅通过Class对象就可以创建此类的实例对象，而且不需要调用其构造函数、初始化代码、JVM安全检查等。它抑制修饰符检测，也就是即使构造器是private修饰的也能通过此方法实例化，只需要提供类对象即可创建相应的对象。由于这种特性，allocateInstance在java.lang.invoke、Objenesis(提供绕过类构造器的对象生成方式)、Gson(反序列化时用到)中都有相应的应用。

##### 数组相关
> 主要介绍与数据操作相关的arrayBaseOffset与arrayIndexScale这两个方法，两者配合起来使用即可定位数组中每个元素在内存中的位置。
```java
// 返回数组中第一个元素的偏移量地址
public native in arrayBaseOffset(Class<?> arrayClass);
// 返回数组中一个元素占用的大小
public native int arrayIndexScale(Class<?> arrayClass);
```
* 典型应用
> 这两个与数据操作相关的方法，在java.util.concurrent.atomic包下的AtomicIntegerArray(可以实现对Integer数组中每个元素的原子性操作)中有典型的应用，通过Unsafe的ArrayBaseOffset、arrayIndexScale分别获取数组首元素的偏移地址base以及单个冤死大小因子scale.后续相关原子性操作均依赖于这两个值进行数字中元素的定位，getAndAdd方法即通过checkedByteOffset方法获取某数组元素的偏移地址，而后通过CAS实现原子性操作。![atomictIntegerArray获取每个元素地址](/doc/image/atomicIntegerArray_first_address.png)![atomictIntegerArray中getAndAdd方法中通过CheckedByteOffset获取元素指定位置偏移地址](/doc/image/atomicIntegerArray_getAndAdd.png)

##### 内存屏障
> 内存屏障(也成为内存栅栏、内存栅障。屏障指令等是一类通过屏障指令，是CPU或编译器在堆内存随机访问的操作中的一个同步点，使得此点之前的所有读写操作都执行后才可以开始执行此点之后的操作)，避免代码重排序。
```java
// 内存屏障，禁止load操作重排序。屏障前的load操作不能被重排序到屏障后，屏障后的load操作不能被重排序到屏障前
public native void loadFence();
// 内存屏障，禁止store操作重排序，前后操作不能重排序
public native void storeFence();
//  内存屏障，禁止load。store操作重排序
public native void fullFence();
```
* 典型应用
> java8中引入了一种锁的新机制--StampedLock，它可以看成是读写锁的一个改进版本。StampedLock提供了一种乐观读锁的实现，这种乐观读锁类似于无锁的操作，完全不会阻塞写线程获取写锁，从而缓解读多写少时写线程"饥饿"现象。由于StampedLock提供的乐观读锁不阻塞写线程获取读锁，当线程共享变量从主内存load到线程工作内存时，会存在数据不一致问题。所以使用StampedLock的乐观读锁，需要确保数据一致性。![StampedLock乐观读锁保证数据一致性](/doc/image/StampedLock_read_write.png)
StampedLock.validate方法通过锁标记与相关常量进行微云思安、比较来校验锁状态，在姜堰逻辑之前，会通过Unsafe的loadFence方法加入一个load内存屏障,目的是避免赋值与校验发生重排序导致所状态校验不准去的问题。![StampedLock中validate方法添加load内存屏障](/doc/image/StampedLock_validate_loadFence.png)

##### 系统相关
> 包含获取系统相关信息
```java
// 返回系统指针的大小。返回值为4(32位系统)或8(64位系统)
public native int addressSize();
// 内存页的大小，此值为2的幂次方
public native int pageSize();
```

* 典型应用
> java.nio下的工具类Bits中计算待申请内存所需内存页数量的静态方法，其依赖于Unsafe中pageSize方法获取系统内存页大小实现后续计算逻辑。![Bits中pageSize操作](/doc/image/Bits_pageSize.png)

参考（英语的重要性）
[open jdk 7 unsafe source](http://hg.openjdk.java.net/jdk7/jdk7/jdk/file/9b8c96f96a0f/src/share/classes/sun/misc/Unsafe.java)

[Java Magic sun.misc.Unsafe](http://mishadoff.com/blog/java-magic-part-4-sun-dot-misc-dot-unsafe/)

[Java crashes at libjvm.so](https://www.zhihu.com/question/51132462)

[Java中神奇的双刃剑--Unsafe 链接中详细介绍的Unsafe中的方法的含义以及部分用法](https://www.cnblogs.com/throwable/p/9139947.html)

[DirectByteBuffer理解]()

[]()