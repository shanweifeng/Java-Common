### [多线程并发任务(关注源码)](https://www.cnblogs.com/dennyzhangdd/p/7010972.html)
> Future、FutureTask、CompletionService、CompletableFuture
> 开启线程执行任务，不管使用Runnable(无返回值)还是Callable(有返回值)接口，都可以轻松实现。如果是开启线程池并需要获取结果集的情况下，各种实现方式的优劣如下：
* Future
> 接口中存在cancel()、get()、isCancel()、isDone等5个方法，
![future接口方法](/doc/image/Futrue_method.png)
> futures多线程并发任务结果代码见threadTask包FutureDemo.java<p>
任务并行且按照完成顺序获取结果。*比较耗CPU*

* FutureTask
> 实现了RunnableFuture接口，futureTask类的继承关系图如下![FutureTask类图](/doc/image/futureTask_class_diagram.png)
从类图中可以看出RunnableFuture接口继承自Runnable+Future<V>:<p>
a. Runnable接口可以开启单个线程执行。<p>
b. Future<v>接口可接受Callable接口的返回值，futureTask.get()阻塞获取结果。<p>
FutureTask存在两种构造方法：![FutureTask构造函数](/doc/image/futureTask_constructor.png)![FutureTask构造函数中创建Callable](/doc/image/Executors_Callable.png)![RunnableAdapter创建Callable](/doc/image/RunnableAdapter.png)
从图中可以看出FutureTask两种构造函数最终都是赋值Callable.查看FutureTaskDemo实例代码

* CompletionService
> 内部通过阻塞队列 + FutureTask实现了任务先完成可先获取到，即结果按照完成先后顺序排序CompletionServiceDemo<p>
CompletionService中可以选择添加顺序获取结果也可以选择执行结果先后顺序获取。<p>
建议：使用率也挺高，而且能按照完成先后排序，建议如果有排序需求的优先使用。只是多线程并发执行任务结果归集，也可以使用。

* CompletableFuture(38个方法) 参见CompletableFutureDemo
> jdk1.8添加的并行类,ForkJoinPool中默认的创建线程方式ForkJoinPool.commonPool()，该方法只能在虚拟机中创建一次后一直存在(传说中的daemon线程)，后续如果还是使用默认的创建方式则不会继续创建，如果想要使用non-daemon线程，则需要使用自定义的thread pool 或者executor thread pool.<p>
异步执行任务静态方法:supplyAsync用于返回有值的任务，runAsync用于没有返回值的任务。Executor参数可以手动指定线程，否则默认ForkJoinPool.commonPool()系统级公共线程池(daemon线程，只有退出jvm生命周期才会终止).<p>
组合completableFuture:<p>
a. thenCombine:先完成当前CompletionStage和other 1个CompletionStage任务，然后把结果传参给BiFUN错题欧尼进行结果合并操作。<p>
b.thenCompose:第一个CompletableFuture执行完毕后，传递给下一个CompletionStage作为入参进行操作。<p><p>
allOf是等待所有任务完成，构造后CompletableFuture完成。anyOf是只要有一个任务完成，构造后CompletableFuture就完成。

### 四种并发执行的总结
||Future|FutureTask|CompletionService|CompletableFuture|
|---|---|----------|-----------------|-----------------|
|原理|Future接口|接口RunnableFuture的唯一实现类，RunnableFuture接口继承自Future<V> + Runnable|内部通过阻塞队列+FutureTask接口|JDK8实现；额Future<T>、CompletionStage<T>2个接口|
|多任务并发执行|支持|支持|支持|支持|
|获取任务结果的顺序|支持任务完成先后顺序(即先完成的先获取)|未知|支持任务完成先后顺序|支持任务完成先后顺序|
|异常捕捉|自己捕捉|自己捕捉|自己捕捉|源生API支持，返回每个任务的异常|
|建议|CPU高速轮询，消耗系统资源|并发任务中嵌套层多|推荐使用，没有CompletableFuture之前最好的方案？|API极端丰富，配合流式编程，速度飞快|

#### [Java CompletableFuture 详解](https://colobu.com/2016/02/29/Java-CompletableFuture/)
> Future是Java 5添加的类，用来描述一个异步计算的结果。可以使用isDone方法检查计算是否完成，或者使用get方法阻塞调用线程，直到计算完成返回结果，也可以使用cancel方法停止任务执行。
```java
ExecutorService es = Executors.newFixedThreadPool(10);
Future<Integer> f = es.submit(() ->{
    // 计算 然后返回结果
    return 100;
});
// 主线程轮询判断Future是否完成， 然后通过get方法获取返回结果
f.get();
```
>Future及其相关使用方法虽然提供了异步执行任务的功能，但是获取结果时只能通过阻塞或轮询得到任务的结果。阻塞降低效率，轮询耗费CPU资源且不能及时得到计算结果。使用观察者设计模式当计算结果完成及时通知坚挺者。<p>
java的一些框架中如Netty中扩展了Java的future接口，提供了addListener等多个扩展方法:
```java
ChannelFuture future = bootstrap.connect(new InetSocketAddress(host, port));
future.addListener(new ChannelFutureListener() {
    @Override
    public void operationComplete() throws Exception {
        if (future.isSuccess()) {
            // SUCCESS
        } else {
            // FAILURE
        }
    }
})
```
> Google guava也提供了通用的扩展Future：ListenableFuture、SettableFuture以及辅助类Futures等，方便异步编程：
```java
final String name= "...";
inFlight.add(name);
ListenableFuture<Result> future = service.query(name);
future.addListener(new Runnable() {
    public void run() {
        processedCount.incrementAndGet();
        inFlight.remove(name);
        lastProcessed.set(name);
        logger.info("Done with {0}", name);
    }
}, executor);
```
>Scala提供的简单易用且功能强大的Future/Promise异步编程模式.

#### CompletableFuture-主动完成计算
> 实现了CompletionStage和Future接口，依然可以像以前一样通过阻塞或者轮询的方式获得结果。
```java
public T get()
public T get(long timeout, TimeUnit unit)
public T getNow(T valueIfAbsent)
public T join()
```
> getNow如果已经计算完则返货结果或抛出异常，否则返货给定的valueIfAbsent值.<p>
join返回计算的结果或者抛出一个unchecked异常(CompletionException)，它和get对抛出的异常的处理有一些细微的区别。
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    int i = 1 / 0;
    return 100;
});
// future.get()；
future.join();
```
#### CompletableFuture对象创建
> CompletableFuture.completedFuture是一个静态辅助方法，用来返回一个已经计算好的CompletableFuture.
```java
public static <U> CompletableFuture<U> CompletableFuture.completedFuture(U value);
```
> 以下四个静态方法用来为一段异步执行的代码创建CompletableFuture对象:
```java
public static CompletableFuture<Void> runAsync(Runnable runnable);
public static CompletableFuture<Void> runAsync(Runnable runnable, Executor executor);
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier);
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier, Executor executor);
```
> 以Async结尾并且没有指定Executor的方法会使用ForkJoinPool.commonPool()作为它的线程池执行异步代码。<p>
runAsync方法以Runnable函数式接口类型为参数，所以CompletableFuture的计算结果为空。<p>
supplyAsync方法以Supplier<U>函数式接口类型为参数，CompletableFuture的计算结果类型为U.<p>
因为方法的参数类型都是函数式接口，所以可以使用lambda表达式实现异步任务：
```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    //执行异步耗时计算
    return "";
});
```
#### CompletableFuture - 计算结果完成时的处理
> 当CompletableFuture的计算结果完成或者抛出异常的时候，我们可以执行特定的Action：
```java
public CompletableFuture<T> whenComplete(BiConsumer<? super T, ? super super Throwable> action);
public CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T, ? super super Throwable> action);
public CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T, ? super super Throwable> action, Executor executor);
public CompletableFuture<T> exceptionally(Function<Throwable, ? extends T> function);
```
> 上面四个方法中的action类型是BiConsumer<? super T, ? super Throwable>,可以处理正常的计算结果或异常情况。方法不易Async结尾，意味着Action使用相同的线程执行，而Async可能会使用其他的线程去执行(如果使用相同的线程池，也可能或被同一个线程选中执行)。<p>
这几个方法都会返回CompletableFuture，当Action执行完毕后它的结果返回原始的CompletableFuture的计算结果或者返货异常。
```java
public class Main {
    private static Random rand = new Random();
    private static long t = System.currentTimeMillis();
    static int getMoreData() {
        System.out.println("begin to start compute");
        try {
            Thread.sleep(10000);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        System.out/println("end to start compute.passed " + (System.currentTimeMillis() - t) / 1000 + " seconds");
        return rand.nextInt(1000);
    }
    
    public static void main(String[] args) throws Exception {
        CompletableFuture<Integer> future = CompletableFuture.supplyAsync(Main::getMoreData);
        Future<Integer> f = future.whenComplete((v, e) -> {
            System.out.println(v);
            System.out.println(e);
        });
        System.out.println(f.get());
        System.in.read();
    }
}
```
>exceptionally方法返货一个新的CompletableFuture，当原始的CompletableFuture抛出异常的时候，就会触发这个CompletableFuture的计算，调用function个计算值，否则如果原始的CompletableFuture正常计算完后，这个新的CompletableFuture也计算完成，它的值和原始的CompletableFuture的计算的值相同。这个exceptionally方法用来处理异常情况。
> 下面一组方法返回的也是CompletableFuture对象，但对象的值和原来的CompletableFuture计算的值不同。当原先的CompletableFuture的值计算完成或者抛出异常的时候，会触发这个CompletableFuture对象的计算，结果由BiFunction参数计算而得。因此这组方法兼有whenComplete和转换的两个功能:
```java
public <U> CompletableFuture<U> handle(BiFunction<? super t, Throwable, ? extends U> fn);
public <U> CompletableFuture<U> handleAsync(BiFunction<? super t, Throwable, ? extends U> fn);
public <U> CompletableFuture<U> handleAsync(BiFunction<? super t, Throwable, ? extends U> fn, Executor executor);
```
> 不以Async结尾的方法由原来的线程计算，以Async结尾的方法由默认线程池ForkJoinPool.commonPool()或者指定线程池executor运行

#### CompletableFuture - 转换
> CompletableFuture可以作为monad(单子)和functor。由于回调风格的实现，我们不必因为等待一个计算完成而阻塞着调用线程，而是告诉CompletableFuture当计算完成的时候请执行某个function。而且我们还可以将这些操作串联起来或者将CompletableFuture组合起来。
```java
public <U> CompletableFuture<U> thenApply(Function<? supper T, ? extends U> fn);
public <U> CompletableFuture<U> thenApplyAsync(Function<? supper T, ? extends U> fn);
public <U> CompletableFuture<U> thenApplyAsync(Function<? supper T, ? extends U> fn, Executor executor);
```
> 这组函数的功能是当原来的CompletableFuture计算完成后，将结果传递给函数fn，将fn的结果作为新的CompletableFuture计算结果。<p>
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 100;
});
CompletableFuture<String> f = future.thenApplyAsync(i -> i * 10).thenApply(i -> i.toString());
System.out.println(f.get());// "1000"
```
>这里并不是立马执行的，而是在前一个stage完成后继续执行。与handle方法的区别在于handle方法会处理正常计算值和异常，可以屏蔽异常避免异常继续抛出。而thenApply方法只是用来处理正常值，因此一旦有异常就会抛出。

#### CompletableFuture - 纯消费(执行Action)
> 上面的方法是当计算完成的时候，会生成新的计算结果(thenApply、handle),或者返回同样的计算结果whenComplete,CompletableFuture还提供了一种处理结果的方法，只对结果执行action，而不是返回新的计算值，因此计算值为Void
```java
public CompletableFuture<Void> thenAccept(Consumer<? super T> action);
public CompletableFuture<Void> thenAcceptAsync(Consumer<? super T> action);
public CompletableFuture<Void> thenAcceptAsync(Consumer<? super T> action, Executor executor);
```
> 上面一组方法的参数是函数式接口Consumer，这个接口只有输入没有返回值
```java
CompletableFuture<Integer> future = CompletableFuture.supply(() -> {
    return 100;
});
CompletableFuture<Void> f = future.thenAccept(System.out::println);
System.out.println(f.get());
```
> thenAcceptBoth以及相关的方法提供了类似的功能，当两个CompletionStage都正常计算的时候，就会执行提供的action，它用来组合另外一个异步的结果。<p>
runAfterBoth是当两个CompletionStage都正常完成计算的时候，执行一个Runnable,这个Runnable并不使用计算的结果。
```java
public <U> CompletableFuture<Void> thenAcceptBoth(CompletionStage<? extends U> other, BiConsumer<? super T, ? super U> action);
public <U> CompletableFuture<Void> thenAcceptBothAsync(CompletionStage<? extends U> other, BiConsumer<? super T, ? super U> action);
public <U> CompletableFuture<Void> thenAcceptBothAsync(CompletionStage<? extends U> other, BiConsumer<? super T, ? super U> action, Executor executor);
public     CompletableFuture<Void> runAfterBoth(CompletionStage<?> other, Runnable action);
```
```java
CompletableFuture<Integer> future = CompletableFuture.supply(() -> {
    return 100;
});
CompletableFuture<Void> f = future.thenAcceptBoth(CompletableFuture.completedFuture(10), (x, y) -> System.out.println(x * y));
System.out.println(f.get());
```
>下面一组方法当计算完成的时候会执行一个Runnable，与thenAccept不同，Runnable并不适用CompletableFuture计算的结果
```java
public CompletableFuture<Void> thenRun(Runnable action);
public CompletableFuture<Void> thenRunAsync(Runnable action);
public CompletableFuture<Void> thenRunAsync(Runnable action, Executor executor);
```
>先前计算的结果被忽略，这个方法返回CompletableFuture<Void>类型的对象
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 100;
});
CompletableFuture<Void> f = future.thenRun(() -> System.out.println("finished"));
System.out.println(f.get());
```
* >因此可以根据方法的参数类型来记忆。Runnable类型的参数会忽略计算结果，Consumer是纯消费计算结果，BiConsumer会组合另外一个CompletableFuture纯消费，Function会对计算结果做转换，BiFunction会组合另外一个CompletableFuture的计算结果做转换

#### CompletableFuture - 组合（没用过）
> 下面一组方法接受Function作为参数，这个Function的输入时当前的CompletableFuture的计算值，返回结果是一个新的CompletableFuture，这个新的CompletableFuture会组合原来的CompletableFuture和函数返回的CompletableFuture
```java
public <U> CompletableFuture<U> thenCompose(Function<? super T, ? extends CompletionStage<U>> fn);
public <U> CompletableFuture<U> thenComposeAsync(Function<? super T, ? extends CompletionStage<U>> fn);
public <U> CompletableFuture<U> thenComposeAsync(Function<? super T, ? extends CompletionStage<U>> fn, Executor executor);
```
> thenCompose返回的对象并不一定是fn返回的对象，如果原来的CompletableFuture还没有计算出来，它就会生成一个新的组合后的CompletableFuture。
```java
CompletableFuture<Integer> future = CompletableFuture.sypplyAsync(() -> {
    return 100;
});
CompletableFuture<String> f = future.thenCompose(i -> {
    return CompletableFuture.supplyAsync(() -> {
        return (i * 10) + "";
    });
});
System.out.println(f.get());
```
> thenCombine： 两个CompletionStage是并行执行，它们之间没有先后顺序，other并不会等待先前的CompletableFuture执行完毕后在执行。
```java
public <U> CompletableFuture<U> thenCombine(ComletionStage<? extends U> other, BiFunction<? super T, ? super U, ? extends V> fn);
public <U> CompletableFuture<U> thenCombineAsync(ComletionStage<? extends U> other, BiFunction<? super T, ? super U, ? extends V> fn);
public <U> CompletableFuture<U> thenCombineAsync(Function<ComletionStage<? extends U> other, BiFunction<? super T, ? super U, ? extends V> fn, Executor executor);
```
> 从功能上来讲，thenCombine功能更类似thenAcceptBoth，只不过thenAcceptBoth是纯消费，它的函数参数没有返回值，而thenCombine的函数参数fn有返回值。
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 100;
});
CompletableFuture<String> future2 = CompletableFuture.supply(() -> {
    return "abc";
});
CompletableFuture<String> f = future.thenCombine(future2, (x,y) -> y + "-" + x);
System.out.println(f.get());
```

#### CompletableFuture - Either
> thenAcceptBoth和runAfterBoth是当两个CompletableFuture都计算完成，而下面一组方法是当任意一个CompletableFuture计算完成的时候就会执行：
```java
public CompletableFuture<Void> acceptEither(CompletionStage<? extends T> other, Consumer<? super T> action);
public CompletableFuture<Void> acceptEitherAsync(CompletionStage<? extends T> other, Consumer<? super T> action);
public CompletableFuture<Void> acceptEitherAsync(CompletionStage<? extends T> other, Consumer<? super T> action, Executor executor);

public CompletableFuture<U> applyToEither(CompletionStage<? extends T> other, Function<? super T, U> fn);
public CompletableFuture<U> applyToEitherAsync(CompletionStage<? extends T> other, Function<? super T, U> fn);
public CompletableFuture<U> applyToEitherAsync(CompletionStage<? extends T> other, Function<? super T, U> fn， Executor executor);
```
> acceptEither方法是当任意一个CompletionStage完成的时候，action这个消费者就会被执行。这个方法返回CompletableFuture<Void><p>
applyToEither方法是当任意一个CompletionStage完成的时候，fn会被执行，它的返回值会当做新的CompletableFuture<U>的计算结果。
```java
Random rand = new Random();
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    try {
        Thread.sleep(10000 + rand.nextInt(1000));
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 100;
});
CompletableFuture<Integer> future2 = CompletableFuture.supplyAsync(() -> {
    try {
        Thread.sleep(10000 + rand.nextInt(1000));
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 200;
});
CompletableFuture<String> f = future.applyToEither(future2, i -> i.toString());
```
#### CompletableFuture - 辅助方法allOf和anyOf
> 下面一组方法用来组合多个CompletableFuture：
```java
public static CompletableFuture<Void> allOf(CompletableFuture<?>... cfs);
public static CompletableFuture<Void> anyOf(CompletableFuture<?>... cfs);
```
> allOf方法是当所有的CompletableFuture都执行完毕后执行计算<p>
anyOf方法是当任意一个CompletableFuture执行完后就会执行计算，计算的结果相同。
```java
Random rand = new Random();
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    try {
        Thread.sleep(10000 + rand.nextInt(1000));
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 100;
});
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> {
    try {
        Thread.sleep(10000 + rand.nextInt(1000));
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return "abc";
});
// CompletableFuture<Void> f = CompletableFuture.allOf(future2, future);
CompletableFuture<Object> f = CompletableFuture.anyOf(future2, future);
System.out.println(f.get());
```

#### 进一步
> 如果使用过Guava的Future类，能发现Futures辅助类提供了很多便利方法用来处理多个Future，而Java CompletableFuture只提供了allOf、anyOf两个方法。比如将多个CompletableFuture组合成一个CompletableFuture，这个组合后的CompletableFuture是一个List包含前面所有的CompletableFuture计算结果，guava的Futures.allAsList可以实现这样的功能，Java CompletableFuture则需要辅助方法:
```java
public static <T> CompletableFuture<List<T>> sequence(List<CompletableFuture<T>> futures) {
    CompletableFuture<Void> allDoneFuture = CompletableFuture.allOf(futures.toArray(new CompletableFuture[futures.size()]));
    return allDoneFuture.thenApply(v -> futures.stream.mapCompletableFutureLLjoin).collect(Collectors.<T>toList());
}

public static <T> CompletableFuture<Stream<T>> sequence(Stream<CompletableFuture<T>> futures) {
    List<CompletableFuture<T>> futureList = futures.filter(f -> f != null).collect(Collectors.toList());
    return sequence(futureList);
}
 ```
 > 或者Java Future转CompletableFuture
 ```java
public static <T> CompletableFuture<T> toCompletable(Future<T> future, Executor executor) {
    return CompletableFuture.supplyAsync(() -> {
        try {
            return future.get();
        } catch( InterruptedException | ExecutionException e) {
            throw new RuntimeException(e);
        }
    }, executor);
}
```
> github上有多个项目可以实现Java CompletableFuture与其他Future(如Guava ListenableFuture)之间的转换，如spotify/futures-extra、future-converter、scala/scala-java8-compat等。

### 参考文档(英文版的看不懂哇 学好英文的重要性)
[Java 8:Definitive guide to CompletableFuture](https://www.nurkiewicz.com/2013/05/java-8-definitive-guide-to.html)
[https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html)
[https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletionStage.html](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletionStage.html)