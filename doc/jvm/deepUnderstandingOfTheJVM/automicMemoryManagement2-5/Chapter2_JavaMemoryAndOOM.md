## 第二章 Java内存区域与内存溢出异常

> Java虚拟机在执行Java程序的过程中会把它所管理的内存划分为若干个不同的数据区域。这些区域都有各自的用途，以及创建和销毁的时间，有的区域随着虚拟机进程的启动而存在，有的区域则是依赖用户线程的启动和结束而建立和销毁。
#### 运行时数据区域
> ![Java运行时数据区域](/doc/image/java_runtime_data_area.png) 其中虚拟机栈、本地方法栈、程序计数器属于线程私有，方法区、堆为进程所有
* 程序计数器
> 是一块较小的内存空间，它的作用可以看做是当前线程所执行的字节码的行号指示器。在虚拟机的概念模型里(仅是概念模型，各种虚拟机可能会通过一些更高效的方式去实现)，字节码解释器工作时就是通过改变这个计数器的值来选去下一条需要执行的字节码指令，分支、循环、跳转、异常处理、线程恢复等基础功能都需要依赖这个计数器来完成。<p>
由于Java虚拟机的多线程是通过线程轮流切换并分配处理器执行时间的方式来实现的，在任何一个确定的时刻，一个处理器(对于多喝处理器来说是一个内核)只会执行一条线程中的指令。因此为了线程切换后能恢复到正确的执行位置，每条线程都需要有一个独立的程序计数器，各线程之间的计数器互不影响，独立存储，这类内存区域为"线程私有"的内存。<p>
如果线程正在执行的是一个Java方法，这个计数器记录的是正在执行的虚拟机字节码指令的地址；如果正在执行的是native方法，这个计数器值则为空(Undefined)。此内存区域是唯一一个在Java虚拟机规范中没有规定任何OutOfMemoryError情况的区域。<p>
* Java虚拟机栈
> 线程私有，生命周期与线程相同。**描述的是Java方法执行的内存模型：每个方法被执行的时候都会同时创建一个栈帧(Stack Frame)用于存储局部变量、操作栈、动态链接、方法出口等信息。每一个方法被调用直至执行完成的过程，就对应着一个栈帧在虚拟机栈中从入栈到出栈的过程。**<p>
通常所说的Java内存区分为堆内存(Heap)和栈内存(Stack)，这里所说的栈内存指的就是虚拟机栈或者说虚拟机栈中的局部变量表部分。<p>
局部变量表存放了编译期可知的各种基本数据类型(boolean、byte、char、short、int、float、long、double)、对象引用(reference 类型，不是对象本身，根据不同VM实现可能是一个指向对象起始地址的引用指针，也可能指向一个代表对象的句柄或者其他与此对象相关的位置)和returnAddress类型(指向了一条字节码指令的地址)。<p>
其中64位长度的long和double类型的数据会占用2个局部变量空间(Slot)，其余数据类型只占用1个。局部变量表所需的内存空间在编译期间完成分配，当进入一个方法时，这个方法需要在帧中分配多大的局部变量空间是完全确定的，咋爱方法运行期间不会改变局部变量表的大小。<p>
在Java虚拟机规范中，对这个区域规定了两种异常情况：如果线程请求的栈深度大于虚拟机所允许的深度，将抛出StackOverFlowError异常；如果虚拟机栈可以动态扩展(当前大部分的Java虚拟机都可以动态扩展，只不过Java虚拟机规范中也允许固定长度的虚拟机栈),当扩展时无法申请到足够的内存是会抛出OutOfMemoryError异常。<p>
*  本地方法栈
> 与虚拟机栈所发挥的作用是非常相似的，其区别是虚拟机栈执行Java方法(也就是字节码)服务，而本地方法栈则是为虚拟机使用到的Native方法服务。虚拟机规范中对本地方发展中的方法使用的语言、使用方式与数据结构并没有强制规定，因此具体的虚拟机可以自由实现它。部分虚拟机(如Sun HotSpot VM)直接就把本地方法栈和虚拟机栈合二为一。本地方法栈区域也会抛出StackOverFlowError和OutOfMemoryError异常。

>>> 以上三个数据区域是属于线程独有的

* Java 堆
> 被所有线程共享的一块内存区域，在虚拟机启动时创建。此内存区域的唯一目的就是存放对象实例，**几乎所有的对象实例都在这里分配**。这里没有说所有的对象都需要分配在堆上是因为Java虚拟机规范中的描述是:所有的对象实例以及数组都要在堆上分配(规范中国的原文:The heap is the runtime data area from which memory for all class instances and arrays is allocated)，但是随着JIT编译器的发展与逃逸分析技术的逐渐成熟，栈上分配、标量替换(第11章)优化技术将会导致一些微妙的变化发生，所有的对象都分配在对上也渐渐变得不是那么"绝对"了。<p>
Java堆是垃圾收集器管理的主要区域，因此很多时候也被称为"GC堆"(Garbage Collected Heap)。从内存回收的角度看现在收集器基本都是采用分代收集算法，所以java堆中可以细分为:新生代和老年代，在细致一点有Eden空间、From Survivor空间、To Survivor空间等(8:1:1);如果从内存分配角度看，可能划分出多个线程私有的分配缓冲区(Thread Local Allocation Buffer TLAB).无论如何划分存放的还是实例对象。<p>
根据Java虚拟机规范的规定，Java堆可以处于物理上不连续的内存空间中，只要逻辑上是连续的即可。当前主流的虚拟机都是按照可扩展来实现的(通过-Xmx和-Xms控制)。如果在堆中没有内存完成实例分配，并且堆也无法再扩展时，将会抛出OutOfMemoryError异常。
* Java 方法区
> 被各个线程共享的内存区域，用于存储已被虚拟机加载的类信息、常量、静态变量、即时编译器编译后的代码等数据。虽然Java VM规范把方法区描述为堆的一个逻辑部分，但它却有一个别名叫做Non-Heap(非堆)，目的应该是与Java堆区分开来。<p>
在HotSpot VM上，很对人愿意把方法区称为"永久代"(Permanent Generation),本质上两者并不等价，仅仅是因为HotSpot VM的设计团队选择吧GC分代收集扩展至方法区，或者说使用永久代来实现方法区而已。对于其他VM(如BEA JRockit、IBM J9等)来说是不存在永久代的概念的。即使是HotSpot VM本身现在也有放弃永久代并"搬家"至Native Memory来实现方法区的规划了。<p>
Java虚拟机规范对这个区域的限制非常宽松，除了不需要连续的内存和可以选择固定大小或者可扩展外，还可以选择不实现垃圾收集。这个区域的内存回收目标主要是针对常量池的回收和对类型的卸载，一般来说这个区域的回收"成绩"比较难以令人满意，尤其是类型卸载，条件相当苛刻，但是这部分区域的回收确实是有必要的。当方法区无法满足内存分配需求时，将抛出OutOfMemoryError异常<p>
* 运行时常量池
> 是方法区(Method Area)的一部分。Class文件除了有类的版本、字段、方法、接口等描述信息外，还有意向信息是常量池(Constant Pool Table),用于存放编译期生成的各种字面量和符号引用，这部分内容将在类加载后存放到方法区的运行时常量池中。<p>
VM 对于Class文件的每一部分的字节存储数据类型都有要求，这样才会被虚拟机认可、装载和执行。但对于运行时常量VM 规范没有做任何细节要求，不同供应商可以自己实现这个内存区域。一般来说除了保存Class文件中描述的符号引用外，还会把翻译出来的直接引用也存储在运行时常量池中(Class文件类型和符号引用等参见第6章)。<p>
运行时常量池相对于Class文件常量池的另外一个重要特征是具备动态性，苍凉并不要一定只能在编译期产生，也就是并非预置入Class文件中常量池的内容才能进入方法区运行时常量池，运行期间也可能将新的常量放入池中，这种特性被开发人员利用的比较多的便是String类的intern()方法。当常量池无法再申请到内存时会抛出OutOfMemoryError异常。
* 直接内存
> 直接内存并不是虚拟机运行时数据区的一部分，也不是Java虚拟机规范中定义的内存区域，但这部分内存也会被频繁的使用，也可能刀子OutOfMemoryError异常出现。<p>
在JDK1.4中引入的NIO(New Input/Output)类，引入了一种基于通道(Channel)与缓冲区(Buffer)的I/O方式，它可以使用Native函数库直接分配堆外内存，然后通过一个存储在Java堆里面的DirectByteBuffer对象作为这块内存的引用进行操作。这样能在一些场景中显著提高性能，因为避免了在Java堆和Native堆中国来回复制数据。如果各个内存区域的总和大于物理内存限制(包括物理上的和操作系统级的限制)，也会导致动态扩展时出现OutOfMemoryError异常。
### 对象访问
> 对象访问会涉及到Java栈、Java堆、方法区这三个最重要内存区域之间的关联关系。一个对象声明的形式对象会反映到Java栈的本地变量表中，而对象new的部分会反映到Java堆中，长度不固定。在Java堆中还必须包含能查找到此对象类型数据(如对象类型、父类、实现接口、方法等)的地址信息，这些类数据存储在方法区中。<p>
访问VM reference类型的主要两种方式有:使用句柄或直接指针
* 句柄方式:Java堆中将会划分出一块内存来作为句柄池，reference中存储的就是对象的句柄地址，而句柄中包含了对象示例数据和类型数据各自具体地址信息。![句柄方式访问堆对象与类类型信息](/doc/image/java_memory_method_area_handle.png)
* 指针方式：堆对象的布局中必须考虑如何放置访问类型数据的相关信息，reference中直接存储的就是对象地址。![指针方式访问堆对象与类类型信息](/doc/image/java_memory_method_area_pointer.png)
> 这两种方式中，句柄访问方式的最大好处就是reference中存储的是稳定的句柄地址，在对象被移动(垃圾收集时移动对象时非常普遍的行为)时只会改变句柄中的实例数据指针而reference本身不需要被修改。<p>
直接指针访问方式的好处是速度更快，它节省了一次指针定位的时间开销。

#### OutOfMemoryError异常
* Java堆溢出
> 不断创建对象保证GC Roots到对象之间有可达路径来避免垃圾回收机制清除这些对象，就会在对象数量到达最大堆的容量限制后产生内存溢出异常。<p>
将对的最小值-Xms参数与最大值-Xmx参数设置为一样即可避免堆自动扩展，通过参数-XX:+HeapDumpOnOutOfMemoryError可以让VM在出现内存溢出异常时Dump出当前的内存转储快照以便时候进行分析(关于转储快照文件分析方面参见第4章).代码参见:../oom/HeapOOM.java<p>
```java
/**
 * @author shanweifeng
 * Java堆内存溢出异常测试
 * <com.guique.common.oom>
 *     设置启动时的VM参数为：-Xms20M -Xmx20M -Xmn10M -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=E:\Java\dump -XX:+PrintGCDetails -XX:SurvivorRatio=8
 * @version 1.0
 * @date 2019/4/16 19:45
 **/
public class HeapOOM {

    static class OOMObject {

    }

    public static void main(String[] args) {
        List<OOMObject> list = new ArrayList<>();
        while (true) {
            list.add(new OOMObject());
        }
    }
}
```
> 问题分析过程中，需要确定的是内存泄漏(Memory Leak)还是内存溢出(Memory Overflow).

#### 虚拟机栈和本地方法栈溢出
> 栈容量只由-Xss参数设定。
```java
package com.guique.common.oom;

/**
 * @author shanweifeng
 * 虚拟机栈和本地方法栈OOM测试
 * <com.guique.common.oom>
 *     -Xms20M -Xmx20M -Xmn10M -Xss128K -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=E:\Java\dump -XX:+PrintGCDetails
 * @version 1.0
 * @date 2019/4/16 20:24
 **/
public class JavaVMStackSOF {
    private int stackLength= 1;
    public void stackLeak() {
        stackLength ++;
        stackLeak();
    }

    public static void main(String[] args) throws Throwable {
        JavaVMStackSOF oom = new JavaVMStackSOF();
        try {
            oom.stackLeak();
        } catch (Exception e) {
            System.out.println("stack length:" + oom.stackLength);
            throw e;
        }
    }
}
```
> 需要注意的是如果在多线程情况下，不断地创建线程，如果给每个线程的栈分配的内存越大，则越容易产生内存溢出。在32位的Window中给每个进程分配的内存最大为2GB,虚拟机提供参数来控制Java堆和方法区的这两部分内存的最大值。剩余的内存为操作系统限制内存(2GB)减去Xmx(最大堆内存)，在减去MaxPermSize(最大方法区容量)，程序计数器内存消耗很小忽略不计。如果虚拟机进程本身消耗的内存不计算在内，剩下的内存就由虚拟机栈和本地方法栈"瓜分"了。每个线程分配到的栈容量越大，可以创建的线程数量自然就越少，建立线程时就越容易把剩下的内存耗尽。<p>
如果建立过多线程导致的内存溢出，在不能减少线程数或者更换64位VM的情况下，就只能通过减少最大堆和减少栈容量来换取更多线程。这种通过"减少内存"的手段解决内存溢出的方式比较隐晦。<p>
```java
package com.guique.common.oom;

/**
 * @author shanweifeng
 * 创建线程导致内存溢出异常
 * <com.guique.common.oom>
 *     VM Args:
 * @version 1.0
 * @date 2019/4/17 10:32
 **/
public class JavaVMStackOOM {

    private void donstop() {
        while (true) {

        }
    }

    public void stackLeakByThread() {
        while (true) {
            Thread thread = new Thread(new Runnable() {
                @Override public void run() {
                    donstop();
                }
            });
            thread.start();
        }
    }

    public static void main(String[] args)
        throws Throwable {// 运行时系统会出现假死
        System.out.println("++++++++++++++++++++++++++++++++");
        JavaVMStackOOM oom = new JavaVMStackOOM();
        oom.stackLeakByThread();
    }
}
```
* 运行时常量池溢出
> 向运行时常量池中添加内容，最简单的做法就是使用String.intern()这个Native方法。该方法的作用是:如果池中已经包含一个等于此String对象的字符串，则返回代表池中这个字符串的String对象；否则将此String对象包含的字符串添加到常量池中，并返回此String对象的引用。由于常量池分配在方法区内，可以通过VM 参数-XX:PermSize和-XX:MaxPermSize限制方法区的大小，从而间接限制其中常量池的容量<p>
```java
package com.guique.common.oom;

import java.util.ArrayList;
import java.util.List;

/**
 * @author shanweifeng
 * 运行时常量池导致的内存溢出异常
 * <com.guique.common.oom>
 *     VM Args: -XX:PermSize=10M -XX:MaxPermSize=10M -XX:+PrintGCDetails
 *     64位VM参数为: -Xmx2048m -XX:MetaspaceSize=512m -XX:MaxMetaspaceSize=768m -Xss2m
 * @version 1.0
 * @date 2019/4/17 11:32
 **/
public class RuntimeConstantPoolOOM {
    public static void main(String[] args) {
// 在jdk88中没有复现出常量池内存溢出溢出
        // 使用List保持着常量池引用，避免FullGC回收常量池行为
        List<String> list = new ArrayList<>();
        // 10M的PermSize在integer范围足够产生OOM
        long i = 0;
        while (true) {
            list.add(String.valueOf(i++).intern());
            if (i % 10000000 == 0) {
                System.out.println(i);
            }
        }
    }
}
```

* 方法区溢出
> 方法区用于存放Class类的相关信息，如类名、访问修饰符、常量池、字段描述、方法描述等。对于方法去溢出的思路是运行时产生大量的类去填满方法区，直到溢出。虽然直接使用Java SE API也可以动态产生类(如反射时的Generated Constructor Accessor和动态代理等)。下面是使用CGLib(开源项目地址:http://cglib.sourceforge.net/)直接操作字节码运行时生成大量动态类。
```java
package com.guique.common.oom;

import net.sf.cglib.proxy.Enhancer;
import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;

import java.lang.reflect.Method;

/**
 * @author shanweifeng
 * 借助CGLib使得方法区出现内存溢出异常
 * <com.guique.common.oom>
 * @version 1.0
 * @date 2019/4/17 14:15
 **/
public class JavaMethodAreaOOM {
    public static void main(String[] args) {
        while (true){
            Enhancer enhancer =new Enhancer();
            enhancer.setSuperclass(OOMObject.class);
            enhancer.setUseCache(false);
            enhancer.setCallback(new MethodInterceptor() {
                @Override public Object intercept(Object o, Method method, Object[] objects, MethodProxy methodProxy)
                    throws Throwable {
                    return methodProxy.invokeSuper(o, objects);
                }
            });
            enhancer.create();
        }
    }
    static class OOMObject{

    }
}
```
> 在经常动态生成大量Class的应用中，需要特别注意类的回收状态，除了上面使用的CGLib字节码增强外，还有JSP或动态产生JSP文件的引用(JSP第一次运行时需要编译为Java类)，基于OSGI的应用、动态代理等。
* 本机直接内存溢出
> DirectMemory容量可通过-XX:MaxDirectMemorySize指定，如果不指定则默认与Java堆的最大值(-Xmax指定)一样。
```java
package com.guique.common.oom;

import sun.misc.Unsafe;

import java.lang.reflect.Field;

/**
 * @author shanweifeng
 * 使用Unsafe分配本机内存
 * <com.guique.common.oom>
 * @version 1.0
 * @date 2019/4/17 15:15
 **/
public class DirectMemoryOOM {
    private static final int _1MB = 1024 * 1024;

    public static void main(String[] args) throws Exception {
        Field unsafeField = Unsafe.class.getDeclaredFields()[0];
        unsafeField.setAccessible(true);
        Unsafe unsafe = (Unsafe) unsafeField.get(null);
        while (true) {
            unsafe.allocateMemory(_1MB);
        }
    }
}
```