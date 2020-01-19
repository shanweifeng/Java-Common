## Queued队列源码
* [reference address](https://www.cnblogs.com/lemon-flm/p/7877898.html)
* Queue:基本上，一个队列就是一个先入先出(FIFO)的数据结构
* Queue:接口与List、Set同一级别，都是继承了Collection接口。LinkedList实现了Deque接口。

#### Queue的实现
* 1、没有实现的阻塞接口的LinkedList：实现了java.util.Queue接口和java.util.AbstractQueue接口
> 内置的不阻塞队列：PriorityQueue和ConcurrentLinkedQueue<p>
PriorityQueue和ConcurrentLinkedQueue类在Collection Framework中加入两个具体集合实现<p>
PriorityQueue类实质上维护了一个有序列表。接入到Queue中的元素根据它们的天然排序(通过其java.util.Comparable实现)或者根据传递给构造函数的java.util.Comparable实现来定位<p>
ConcurrentLinkedQueue是基于链接节点的、线程安全的队列。并发访问不需要同步。因为它在队列的尾部添加元素并从头部删除它们，所以只要不需要知道队列的大小，ConcurrentLinkedQueue对公共集合的共享访问就可以工作的很好。收集关于队列大小的信息会很慢，需要遍历队列。

* 2、实现阻塞接口的：
> java.util.concurrent中加入了BlockingQueue接口和五个阻塞队列类。它实质上就是一种带有一点扭曲的FIFO数据结构。不是立即从队列中添加或者删除元素，线程执行操作阻塞，知道有空间或元素可用。<p>
>> ArrayBlockingQueue:一个由数组支持的有界队列。<p>
LinkedBlockingQueue：一个由链接节点支持的可选有界队列。<p>
PriorityBlockingQueue：一个由优先级堆支持的无界优先级队列。<p>
DelayQueue：一个由优先级堆支持的、基于时间的调度队列。<p>
SynchronousQueue:一个利用BlockingQueue接口的简单聚集(rendezvous)机制。

* jdk1.5中阻塞队列操作：

|method Name| function| remark|
|------------|--------|-------|
|add|增加一个元素|如果队列已满，则抛出一个NoSuchElementException异常|
|remove|移除并返回队列头部的元素|如果队列为空，则抛出一个NoSuchElementException异常|
|element|返回队列头部的元素|如果队列为空，则抛出一个NoSuchElementException异常|
|offer|添加一个元素并返回true|如果队列已满，则返回false|
|poll|移除并返回队列头部的元素|如果队列为空则返回null|
|peek|返回队列头部的元素|如果队列为空，则返回null|
|put|添加一个元素|如果队列满，则阻塞|
|tack|移除并返回队列头部的元素|如果队列为空，则阻塞|

*jdk8中队列操作

|method Name| function | remark | Queue|
|-----------|----------|--------|------|
|add| 增加一个元素|如果队列已满，则抛出一个NoSuchElementException异常||
|remove|移除并返回队列头部的元素|如果队列为空，则抛出一个NoSuchElementException异常||
|element|返回队列头部的元素|如果队列为空，则抛出一个NoSuchElementException异常||
|offer|添加一个元素并返回true|如果队列已满，则返回false||
|poll|移除并返回队列头部的元素|如果队列为空则返回null||
|peek|返回队列头部的元素|如果队列为空，则返回null|
|put|添加一个元素|如果队列满，则阻塞||
|tack|移除并返回队列头部的元素|如果队列为空，则阻塞||

#### 方法详解
> remove、element、offer、poll、peek是属于Queue接口。
>> add 、remove和element操作在试图为一个已满的队列增加元素或从空队列取得元素时抛出异常。在多线程程序中，队列在任何时候都有可能编程满的或空的，所以尽可能在队列中使用offer、poll和peek方法，这些方法在无法完成任务时只是给出出错示意而不会抛出异常。
>>>  **poll和peek方法出错返回的是null，因袭向队列中插入null是非法的。**
> put和take是阻塞操作，put在队列满时阻塞，take在队列空时阻塞。

#### Queue详情
* LinkedBlockingQueue：基于链表的队列

* ArrayBlockingQueue: 基于数组的队列，可以选择是否需要公平性，如果公平参数被设置为true，等待时间最长的线程会优先得到处理(其实就是通过将ReentrantLock设置为true来达到这种公平性的，即等待时间最长的线程会先操作)。通常公平性会是的性能有损。是基于数组的阻塞循环队列。

* PriorityBlockingQueue:是一个带优先级的队列，而不是FIFO，基于堆数据结构的，进入队列的元素要有比较能力。

* DelayQueue:基于PriorityQueue实现的存放Delayed元素的无界阻塞队列。如果延迟期没有满，poll将返回null。