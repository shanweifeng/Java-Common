### [理解Java类加载机制](https://blog.csdn.net/javazejian/article/details/73413292#%E7%B1%BB%E5%8A%A0%E8%BD%BD%E7%9A%84%E6%9C%BA%E5%88%B6%E7%9A%84%E5%B1%82%E6%AC%A1%E7%BB%93%E6%9E%84)
** 最终都需要查看源文档

> `Java`文件中都存储着需要执行的程序逻辑，将.java文件通过编译器编译成.class的类文件，.class文件中保存着`Java`代码经过转化后的虚拟机指令，当需要使用某个类时，虚拟机将会加载它的“.class”文件，并创建对应的class对象，**将class文件加载到虚拟机的内存，这个过程称为类加载，**类加载过程如下图:
![类加载过程](doc/image/classLoader.png)
> 加载(装载)、验证、准备、初始化和卸载这五个顺序是固定的类加载过程必须按照这种顺序开始，而解析阶段不一定，它在某些情况下可以在初始化之后在开始，这是为了运行时动态绑定特性(JIT(Just In Time 即时编译)例如接口只在调用时候才知道具体的实现是哪个子类)。值得注意的是：这些阶段通常都是交叉混合式进行的，通常都会在一个阶段执行的过程中调用或激活另一个阶段。

* 加载
> 类加载过程的一个阶段：通过一个类的完全限定查找此类字节码文件，将字节流所代表的的静态存储结构转换成方法去运行时数据结构，并利用字节码文件在java堆创建一个Class对象，作为方法区这些数据的访问入口。<p>
相对于类加载过程的其他阶段，加载阶段是通过类加载器(ClassLoader)来完成的。

* 验证
> 验证阶段是链接阶段的第一步，目的在于确保Class文件的字节流中包含信息符合当前虚拟机要求，不会危害虚拟机自身安全。主要包括四种验证：<p>文件格式验证:验证class文件格式规范<p>元数据验证: 对字节码描述的信息进行语义分析，保证描述的信息符合java语言规范。验证点可能包括：当前类是否有父类(Object除外)、是否继承了不允许被继承的类(final修饰的)、如果该类的父类是抽象类，是否实现了父类或接口中要求实现的方法。 <p>字节码验证: 进行数据流和控制流分析，这个阶段对类的方法体进行校验，保证被校验的方法在运行时不会做出危害虚拟机的行为。<p>符号引用验证：通过字符串描述的全限定名是否能找到对应的类、符号引用类中的类、字段和方法的访问性(private protected public default)能否被当前类访问。

* 准备
> 为类变量(即static修饰的字段变量)分配内存并且设置该类变量的初始值即0(如static int i = 5;这里只将i初始化为0,至于5的值将在初始化时赋值)，这里不包含用final修饰的static，因为final在编译的时候就会分配了，注意这里不会为实力变量分配初始化，类变量会分配在方法区中，而实例变量是会随着对象一起分配到Java堆中。

* 解析
> 主要将常量池中的符号引用替换为直接引用的过程。符号引用就是一组符号来描目标，可以是任何字面量，与虚拟机实现的内存布局无关，目标对象并不一定已经加载到内存中。<p>直接引用就是直接指向目标的指针、相对偏移量或一个间接定位到目标的句柄,直接引用是与虚拟机内存布局实现相关的。<p>有类或接口的解析、字段解析、类方法解析、接口方法解析(这里涉及到字节码变量的引用，如需更详细，参考[深入理解Java虚拟机](doc/PDF/《深入理解Java虚拟机：JVM高级特性与最佳实践》.pdf))

* 初始化
> 类加载最后阶段，若该类具有超类，则对其进行初始化，执行静态初始化器和静态初始化成员变量(如前面只初始化了默认值的static变量将会在这个阶段赋值，成员变量也将会被初始化)。<p>
类构造器<clinit>()方法与类的构造函数(实例构造函数<init>()方法)不同，它不需要显示调用父类构造，虚拟机会保证在子类<clinit>()方法执行之前，父类的<clinit>()方法已经执行完毕。因此虚拟机中的第一个执行的<clinit>()方法类一定是java.lang.Object.<p>
由于父类的<clinit>()方法先执行，也就意味着父类中定义的静态语句块要优先于子类的变量赋值操作。<p>
<clinit>()方法对于类或接口来说并不是必须的，如果一个类中没有静态语句，也没有变量赋值的操作，那么编译器可以不为这个类生成<clinit>()方法。<p>
接口中不能使用静态语句块，但接口与类不同的是：执行接口的<clinit>()方法不需要先执行父接口的<clinit>()方法。只有当父接口中定义的变量被使用时，父接口才会被初始化。另外接口的实现类在初始化时也一样不会执行接口的<clinit>()方法。<p>
虚拟机会保证一个类的<clinit>()方法在多线程环境中被正确加锁和同步，如果多线程同时去初始化一个类，那么只会有一个线程执行这个类的<clinit>()方法，其他线程都需要阻塞等待，直到活动线程执行<clinit>()方法完毕。如果一个的<clinit>()方法中有耗时的操作，则可能造成多个进程阻塞。

-- 从虚拟机的角度来说，有两种不同的类加载器：一种是启动类加载器(Bootstrap ClassLoader),该加载器使用C++语言实现，属于虚拟机自身一部分。另一部分就是所有其他的类加载器，这些类加载器是由Java语言实现，独立于JVM外部，并且全部继承抽象类java.lang.ClassLoader.

####启动(Bootstrap)类加载器
> 启动类加载器主要加载的是JVM自身需要的类，这个类加载使用C++语言实现的，是虚拟机自身的一部分，它负责将<JAVA_HOME>/lib路径下的核心类库或-Xbootclasspath参数指定的路径下的jar包加载到内存中，注意由于虚拟机是按照文件名称识别加载jar包的，如rt.jar，如果文件名不被虚拟机识别，即使把jar包丢到lib目录下也是没有作用的(出于安全考虑，Bootstrap启动类加载器只加载包名为java、javax、sun等开头的类)。

#### 扩展(Extension)类加载器
> 扩展类加载器是指sun公司(已被Oracle收购)实现的sun.misc.Launcher$ExtClassLoader类，由Java语言实现的，是Launcher的静态内部类，它负责加载<JAVA_HOME>/lib/ext目录下或者有系统变量-Djava.ext.dir指定位路径中的类库，开发者可以直接使用标准扩展类加载器。
```java
// ExtClassLoader类中获取路径的代码
private static File[] getExtDirs() {
    // 加载<JAVA_HOME>/lib/ext目录中的类库
    String s = System.getProperty("java.ext.dirs");
    File[] dirs;
    if (s != null) {
        StringTokenizer st = new StringTokenizer(s, File.pathSeparator);
        int count = st.countTokens();
        dirs = new File[count];
        for (int i = 0; i < count; i++) {
            dirs[i] = new File(st.nextToken());
        }
    } else {
        dirs = new File[0];
    }
    return dirs;
}
```

#### 系统(System)类加载器（应用程序加载器）
> 是指sun公司实现的sun.misc.Launcher$AppClassLoader。它负责加载系统类路径`java -classpath`或`-Djava.class.path`指定路径下的类库，也就是我们经常用到的classpath路径,开发者可以直接使用系统类加载器，一般情况下该类加载是程序中默认的类加载器，通过ClassLoader#getSystemClassLoader()方法可以获取到该类加载器。<p>
  在Java的日常应用程序开发中，类的加载几乎是由上述3中类加载其相互配合执行的，在必要时，我们还可以自定义类加载器，需要注意的是，Java虚拟机对class文件采用的是按需加载的方式，也就是说当需要使用该类时才会将它的class文件加载到内存生成class对象，而且加载某个类的class文件时，Java虚拟机采用的是双亲委派模式，即把请求交由父类处理，它是一种任务委派模式。
  
#### 双亲委派模式
* 双亲委派模式工作原理
> 双亲委派模式要求除了顶层的启动类加载器外，其余的类加载器都应当有自己的父类加载器，*请注意双亲委派模式中的父子关系并非通常所说的累继承关系，而是采用组合关系来复用父类加载器的相关代码*，类加载器之间的关系图如下：
![双亲委派](doc/image/parent_delegate.png)
> 双亲委派模式是在Java1.2后引入的，其*工作原理*是：如果一个类加载器接收到了类加载请求，它并不会自己先去加载，而是把这个请求委托给父类的加载器去执行，如果父类加载器还存在其父类加载器，则进一步向上委托，依次递归，请求最终将到达顶层的启动类加载器，如果父类加载器可以完成类加载人物，就返回成功，倘若父类加载器无法完成此加载任务，子加载器才会尝试自己去加载。

* 双亲委派模式优势
> 采用双亲委派模式的好处是Java类随着它的类加载器一起具备了一种带有优先级的层次关系，通过这种层级关系可以避免类的重复加载，当父类加载器已经加载了该类时，子类ClassLoader加载器就没有必要在加载一次。其次考虑到安全因素，Java核心API中定义类型不会被随意替换，假设通过网络传递一个名为java.lang.Integer的类，通过双亲委派模式传递到启动类加载器，而启动类加载器在核心Java API发现这个名字的类，发现该类已被加载，并不会重新加载网络传递过来的java.lang.Integer，而是直接返回已加载过的Integer.class，这样便可以防止核心API库被随意篡改。<p>
 如果在classpath路径下自定义一个名为java.lang.SingleInteger类(该类是自己编的)，该类并不存在于java核心包中，经过双亲委托模式传递到启动类加载器中，由于父类加载器路径下并没有该类，所以不会加载，将反向委托给子类加载器加载，最终会通过系统类加载器加载该类。但是这样做是不允许的，因为java.lang是核心API包，需要访问权限，强制加载将会报出如下异常：
 ```java
java.lang.SecurityException: Prohibited package name: java.lang
```
>所以无论如何都无法加载成功的。从代码层面了解几个Java中定义的类加载器及其双亲委派模式的实现，类图关系如下：
![Java层面定义的类加载器及其双亲委派模式类图](doc/image/class_loader.png)
> 从图中可以看出顶层的类加载器是ClassLoader类，它是一个抽象类，其后所有的类加载器都继承自ClassLoader(不包括启动类加载器)，下面是ClassLoader类中几个比较重要的方法：

#### [ClassLoader API](http://ifeve.com/classloader/)
```java
public Class loadClass(String name);

protected Class defineClass(byte[] b);

public URL getResource(String name);

public Enumeration getResources(String name);

public ClassLoader getParent();
```

* loadClass(String)<p>
该方法加载指定名称(包括包名)的二进制类型，该方法在JDK1.2之后不在建议用户重写但用户可以直接调用该方法，*loadClass()方法是ClassLoader类自己实现的，该方法中的逻辑就是双亲委派模式的实现，*源码如下,loadClass(String name, boolean resolve)是一个重载方法，resolve参数代表是否生成class对象的同时进行解析相关操作：
```java
protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException{
    synchroized (getClassLoadingLock(name)) {
        // First,check if the class has already been loaded
        // 先从缓存查找该class对象，找到就不用重写加载
        Class<?> c = findLoadedClass(name);
        if (c == null) {
            long t0 = System.nanoTime();
            try {
                if (parent != null) {
                    // 如果找不到，则委托给父类加载器去加载
                    c = parent.loadClass(name, false);
                } else {
                    //如果没有父类，则委托给启动加载器去加载
                    c = findBootstrapClassOrNull(name);
                }
            } catch (ClassNotFoundException e) {
                // ClassNotFoundException thrown if class not found
                // from the non-null parent class loader
            }
            
            if (c == null) {
                // if still not found, then invoke findClass in order to find the class
                // 如果都没有找到，则通过自定义实现的findClass去查找并加载
                long t1 = System.nanoTime();
                c = findClass(name);
                // this is the defining class loader;record the stats
                sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0)
                sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                sun.misc.PerfCounter..getFindClasses().increment();
            }
        }
        // 是否需要在加载时进行解析
        if (resolve) {
            resolveClass(c);
        }
        return c;
    }
}
```
> 正如loadClass方法所展示的，当类加载请求到来时，先从缓存中查找该类对象，如果存在直接返回，如果不存在则交给该类加载器的父加载器去加载，倘若没有父加载器则交给顶级启动类加载器去加载，最后倘若人没有找到，则使用findClass()方法去加载。从loadClass是实现也可以知道如果不想重新定义加载类的规则，也没有复杂的逻辑，只想在运行时加载自己指定的类，那么我们可以直接使用this.getClass().getClassLoader.loadClass("className"),这样就可以直接调用ClassLoader的loadClass方法获取到class对象。
* findClass(String)
> 在JDK1.2之前，在自定义类加载时，总会去继承ClassLoader类并重写loadClass方法，从而实现自定义的类加载器，但是在JDK1.2之后已不在建议用户去覆盖loadClass()方法，而是建议把自定义的类加载逻辑写在findClass()方法中，从前面的分析可知，findClass()方法是在loadClass方法中被调用的，当loadClass()方法中父加载器加载失败后，则会调用自己的findClass()方法来完成类加载，这样就可以保证自定义的类加载器也符合双亲委派模式。需要注意的是*ClassLoader类中并没有实现findClass方法的具体代码逻辑，取而代之的是抛出ClassNotFoundException异常*，同时应该知道的是findClass方法通常是和defineClass方法一起使用的，ClassLoader类中findClass()方法源码如下：
```java
protected Class<?> findClass(String name) throws ClassNotFoundException {
    throw new ClassNotException(name);
}
```
* defineClass(byte[] b, int off, int len)
> defineClass()方法是用来将byte字节流解析成JVM能够识别的Class对象(ClassLoader中已实现该方法逻辑)，通过这个方法不仅能够通过class文件实例化class对象，也可以通过其他方式实例化class对象，如通过网络接收一个类的字节码，然后转换成byte字节流创建对应的Class对象，defineClass()方法通常与findClass()方法一起使用，一般情况下，在自定义类加载器时，会直接覆盖ClassLoader的findClass()方法并编写加载规则，取得要加载类的字节码后转换成流，然后调用defineClass()方法生成类的Class对象，简单例子如下：
```java
protected Class<?> findClass(String name) throws ClassNotFoundException {
    //获取类的字节数组
    byte[] classData = getClassData(name);
    if (classData == null) {
        throw new ClassNotFoundException();
    } else {
        //使用defineClass生成class对象
        return defineClass(name, classData, 0, classData.length);
    }
}
```
> 需要注意的是：如果直接调用defineClass()方法生成类的Class对象，这个类的Class对象并没有解析(也可以理解为链接阶段，毕竟解析是链接的最后一步),其解析操作需要等待初始化阶段进行。
* resolveCLas(Class<?> c)
> 使用该方法可以使用类的Class对象创建完成也同时被解析。链接阶段主要是对字节码进行验证，为类变量分配内存并设置初始值同时将字节码文件中的符号引用转换为直接引用。
  
> 上述4个方法是ClassLoader类中比较重要的方法，也是我们可能会经常用到的方法。接着看SercureClassLoader扩展了ClassLoader新增了几个与使用相关的源代码(对源代码的位置及其证书的验证)和权限定义类验证(主要指对class源码的访问权限)的方法，一般我们不会直接跟这个类打交道，更多的是与它的子类URLClassLoader有所关联，前面说过，CLassLoader是一个抽象类，很多方法是空的没有实现，比如findClass（）、findResource()等。而URLClassLoader这个实现类为这些方法提供了具体的实现，并新增了URLClassPath类协助取得Class字节码流等功能，在编写自定义类加载器时，如果没有太过于复杂的需求，可以直接继承URLClassLoader类，这样就可以避免自己去编写findClass()方法及其获取字节码流的方式，使自定义类加载器编写更加简洁：
![UrlClassLoader](doc/image/UrlClassLoader.png)
> URLClassLoader中存在一个URLClassPath类，通过这个类就可以找到要加载的字节码流，也就是说URLClassPath类复杂找到要加载的字节码，再读取成字节流，最后通过defineClass()方法创建类的Class对象。从URLClassLoader类的结构图中可以看出其构造方法都必须有一个必须传递的参数URL[],改参数的元素代表字节码文件的路径，换句话说在创建URLClassLoader对象时必须要指定这个类加载器到哪个目录下找class文件。同时也应该注意URL[]也是URLClassPath类的必传参数，在创建URLClassPath对象时，会根据传递过来的URL数组中的路径判断是问价还是jar包，然后根据不同的路径创建FileLoader或者JarLoader或默认Loader类去加载相应路径下的class文件，而当JVM调用findClass()方法时，就由这3个加载器中的一个将class文件的字节码流加载到内存中，最后利用字节码流创建类的class对象。请记住，如果我们在定义类加载器时选择继承ClassLoader类而非URLClassPath，必须手动编写findClass()方法的加载逻辑以及获取字节码流的逻辑。了解完URLClassLoader后接着看看剩余的两个加载器，即拓展类加载器ExtClassLoader和系统类加载器AppClassLoader,这两个类加载器都继承自URLClassLoader，是sun.misc.Launcher的静态内部类。sun.misc.Launcher主要被系统用于启动主应用程序，ExtClassLoader和APPClassLoader都是有sun.misc.Launcher创建的，其类主要类结构如下：
![UrlClassLoader](doc/image/UrlClassLoaderExtend.png)
> 它们之间的关系正如前面所阐述的那样，同时我们发现ExtClassLoader并没有重写loadClass()方法，这足矣说明其遵循双亲委派模式，而APPClassLoader重载了loadClass方法，但最终调用的还是父类loadClass()方法，因此依然遵循双亲委派模式，重载方法源码如下：
````java
/**
* Overrude loadClass 方法，新增包权限检测功能
*/
public Class loadClass(String name, boolean resolve) throws ClassNotFoundException{
    int i = name.lastIndexOf('.');
    if (i != -1) {
        SecurityManager sm = System.getSecurityManager();
        if (sm != null) {
            sm.checkPackageAccess(name.substring(0,1));
        }
    }
    /**
    * 依然调用父类的方法
*/
    return (super.loadClass(name, resolve));
}
````
> 无论是ExtClassLoader还是AppClassLoader都是继承URLClassLoader类，因此它们都遵守双亲委派模型。到此对于ClassLoader、URLClassLoader、ExtClassLoader、APPClassLoader以及Launcher类之间的关系比较清晰。

#### 类加载器之间的关系
> 进一步了解类加载器之间的关系(并非指继承关系)，主要可以分为以下4点：<p>
1、启动类加载器，由C++实现，没有父类<p>
2、拓展类加载器(ExtClassLoader)，由Java语言实现，父类加载器为null<p>
3、系统类加载器(AppClassLoader)，由Java预言实现，父类加载器是ExtClassLoader<p>
4、自定义类加载器，父类加载器肯定为AppClassLoader<p>
代码中`custom`包中为测试自定义类加载器.
> 在custom包中的代码中定义了一个FileClassLoader，继承了ClassLoader而非URLClassLoader，因此需要自己编写findClass()方法逻辑以及加载字节码的逻辑，这里FileClassLoader是自定义加载器，通过在ClassLoaderTest类中通过ClassLoader.getSystemClassLoader()获取到系统默认类加载器，通过获取其父类加载器及其父类的父类加载器，同时还获取了自定义类加载器的父类加载器，从结果中可知：AppClassLoader的父类加载器为ExtClassLoader，而ExtClassLoader没有父类加载器。如果我们事先自己的类加载器，它的父类加载起只会是APPClassLoader。这里可以查看Launcher的构造器源码：
```java
public Launcher() {
    // 先创建拓展类加载器
    ExtClassLoader extcl;
    try {
        extcl = ExtClassLoader。getExtClassLoader();
    } catch (IOException e) {
        throw new InternalError("Could not create extension class loader");
    }
    // Now create the class loader to use to launch the application
    try {
        // 创建AppClassLoader并把extcl作为父加载器传递给AppClassLoader
        loader = AppClassLoader.getAppClassLoader(extcl);
    } catch (IOException e) {
        throw new InternalError("Could not create application class loader");
    }
    // 设置线程上下文类加载器
    Thread.currentThread().setContextClassLoader(loader);
}
```
> Launcher初始化时首先会创建ExtClassLoader类加载器，然后再创建AppClassLoader并把ExtClassLoader传递给它作为父类加载器，这里还把APPClassLoader默认设置为线程上下文类加载器。在创建ExtClassLoader时强制设置了其父加载器为null：
```java
// Lancher中创建ExtClassLoader
extcl = ExtClassLoader.getExtClassLoader();

// getExtClassLoader方法
public static ExtClassLoader getExtClassLoader() throws IOException {
    // ...
    return new ExtClassLoader(dirs);
}

// 构造方法
public ExtClassLoader(File[] dirs) throws IOException {
    //调用父类构造URLClassLoader传递null作为parent
    super(getExtURLs(dirs), null, factory);
}

// URLClassLoader构造
public URLClassLoader(URL[] urls, ClassLoader parent, URLStreamHandlerFactory factory){
    
}
```
> 可以看出ExtClassLoader的父类加载器为null，而AppClassLoader的父类加载器为ExtClassLoader，所以自定义类加载器其父类加载器只会是APPClassLoader，这里所指的父类并不是Java继承关系中的那种父子关系。

#### 类与类加载器
> 在JVM中表示两个class对象是否为同一个类对象存在的两个必要条件：<p>
1、类的完整类名必须一致，包括包名<p>
2、加载这个类的ClassLoader(指ClassLoader实例对象)必须相同

> 在JVM中，即使两个类对象(class对象)来源于同一个Class文件，被同一个虚拟机加载，但只要加载他们的ClassLoader实例对象不同，这两个对象也是不相等的，因为不同的ClassLoader实例对象都拥有不同的独立的类名称空间，所以加载的class对象也会存在不同的类名空间中，前提是需要重写loadClass()方法,从前面双亲委派模式对loadClass()方法的源分析中可知，在方法第一步会通过Class<?> c = findLoadedClass(name);从缓存查询，类名完成名称相同则不会再次被加载，因此必须绕过缓存查询才能重新加载class对象。当然也可以直接调用findClass()方法：
```java
String rootDir = "rootDir";
// 创建两个不同的自定义类加载器实例
FileClassLoader loader1 = new FileClassLoader(rootDir);
FileClassLoader loader2 = new FileClassLoader(rootDir);
// 通过findClass创建类的class对象
Class<?> object1 = loader1.findClass("com.....DemoObj");
Class<?> object2 = loader2.findClass("com.....DemoObj");

System.out.println("findClass -> obj1:" + object1.hashCode());
System.out.println("findClass -> obj2:" + object2.hashCode());
```
> 这样能看到输出的对象hashCode不一致.如果嗲用父类的loadClass方法，则会发现两个结果相同。<p>
所以如果不存缓存查询相同完全类名的class对象，那么只有ClassLoader的实例对象不同，同一字节码文件创建的class对象自然也不会相同。

#### 了解class文件的显示加载与隐式加载的概念
> 所谓class文件的显示加载与隐式加载的方式是指JVM加载class文件到内存的方式，*显示加载*指的是在代码中通过调用ClassLoader加载class对象，如直接使用Class.forName(name)或this.getClass.getClassLoader().loadClass加载class对象。*隐式加载*则是不直接在代码中调用ClassLoader的方法加载class对象，而是通过虚拟机自动加载到内存中，如在加载某个类的class文件时，该类的class文件中引用了另外一个类的对象，此时额外引用的类将通过JVM自动加载到内存中。在日常开发以上两种方式一般会混合使用。

####编写自己的类加载器
> 继承ClassLoader实现自定义的特定路径下的文件类加载器并加载编译后的class文件(查看custom/FileClassLoader.java)：

> 通过getClassLoader()方法找到的class文件并转换为字节流，并重写findClass()方法，利用defineClass()方法创建了类的class对象。
在main方法中调用loadClass()方法加载指定路径下的class文件，由于启动类加载器、拓展类加载器一级系统类加载器都无法在其路径下找到该类，因此最终将由自定义类加载器加载，即调用findClass()方法进行加载。如果继承URLClassLoader实现则代码除了需要重写构造器外无需编写findClass()方法及其class文件的字节流转换逻辑(见com.guique.common.custom.FileURLClassLoader.java).

### 自定义网络类加载器
> 自定义网络类加载器，主要用于读取通过网络传递的class文件(这里忽略class文件的解密过程)，并将其转换成字节流生成对于的class对象（详见NetClassLoader.java）。
在网络文件加载器中，ClassLoader类中`protected Class<?> findClass(String name) throws ClassNotFoundException {
                         throw new ClassNotFoundException(name);
                     }`方法没有实现，需要调用者自己实现
> 网络类加载器与文件类加载器主要是在获取字节码流时的区别，从网络直接获取到字节流再转成字节数组然后利用defineClass方法创建class对象，如果继承URLClassLoader类则和文件路径的实现是类似的，无需担心路径是filePath还是URL，URLClassLoader内的URLClassPath对象会根据传递过来的URL数组中的路径判断是文件还是jar包，然后根据不同的路径创建FileLoader或者JarLoader或默认Loader去读取对应的路径或者URL下的class文件。

### 热部署类加载器
> 热部署就是利用同一个class文件不同的类加载器在内存中创建出两个不同的class对象(利用不同的类加载实例)，由于JVM在加载类之前会检测请求的类是否已经加载过(即在loadClass()方法中调用findLoadedClass()方法)，如果被加载过，则直接从缓存获取，不会重新加载。注意同一个类加载器的实例和同一个class文件只能被加载器加载一次，多次加载将报错，因此实现热部署必须让同一个class文件可以根据不同的类加载器重复加载，以实现所谓的热部署。实际上前面实现的FileClassLoader和FileUrlClassLoader已经具备这个功能，单前提是直接调用findClass()方法而不是调用loadClass()方法，因为ClassLoader中loadClass()方法体中调用了findLoadClass()方法进行检测是否已经被加载，因此需要绕过缓存检查直接调用findClass()方法，当然也可以重写新的loadClass()方法(目前不建议在自定义类加载器中重写)。
```java
public static void main(String[] args) throws ClassNotFoundException {
        String rootDir="/Users/zejian/Downloads/Java8_Action/src/main/java/";
        //创建自定义文件类加载器
        FileClassLoader loader = new FileClassLoader(rootDir);
        FileClassLoader loader2 = new FileClassLoader(rootDir);

        try {
            //加载指定的class文件,调用loadClass()
            Class<?> object1=loader.loadClass("com.zejian.classloader.DemoObj");
            Class<?> object2=loader2.loadClass("com.zejian.classloader.DemoObj");

            System.out.println("loadClass->obj1:"+object1.hashCode());
            System.out.println("loadClass->obj2:"+object2.hashCode());

            //加载指定的class文件,直接调用findClass(),绕过检测机制，创建不同class对象。
            Class<?> object3=loader.findClass("com.zejian.classloader.DemoObj");
            Class<?> object4=loader2.findClass("com.zejian.classloader.DemoObj");

            System.out.println("loadClass->obj3:"+object3.hashCode());
            System.out.println("loadClass->obj4:"+object4.hashCode());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
```
> 第一次调用loadClass()方法，该方法没有重写直接调用的ClassLoader类的，该方法先检查缓存findLoadedClass()中是否已经加载过，如果没有使用parent类加载器加载，如果父加载器不能加载则使用启动类加载器加载，如果还不能则直接通过自定义的类加载器加载findClass()。<p>
所以上面两个不同的自定义类加载器实例调用loadClass()方法(该方法内部实现同步)加载类加载器，第二次加载的时候是从缓存中获取的。而第二遍中直接调用的findClass()方法是直接使用自定义类加载器加载。


### 双亲委派模型的破坏者-线程上下文类加载器
> 在Java应用中存在着很多服务提供者接口(Service provider interface, SPI),这些接口允许第三方为它们提供实现，如常见的SPI有JDBC、JNDI等，这些SPI的接口属于Java核心库，一般存在rt.jar包中，有Bootstrap类加载器加载，而SPI的第三方实现代码则是作为Java应用所依赖的jar包被存放在classPath路径下，由于SPI接口中的代码经常需要加载具体的第三方实现类并调用其相关方法，但SPI的核心接口类是由引导类加载器(启动类加载器)来加载的，而Bootstrap类加载器无法直接加载SPI的实现类，同时由于双亲委派模式的存在，Bootstrap类加载器也无法反向委托APPClassLoader加载器加载SPI的实现类。在这种情况下，就需要一种特殊的类加载器来加载第三方的类库，而线程上下文类加载器就是很好的选择。<p>
线程上下文类加载器(contextClassLoader)是从JDK1.2开始引入的，可以通过java.lang.Thread类中的getContextClassLoader()和setContextClassLoader(ClassLoader cl)方法来获取和设置线程上下文类加载器。如果没有手动设置上下文类加载器，线程将继承其父线程的上下文类加载器，初始线程的上下文类加载器是系统类加载器(AppClassLoader),在线程中运行的代码可以通过此类加载器来加载类和资源，以jdbc.jar加载为例:
![双亲委托模型破话-线程上下文类加载器](/doc/image/Patents_delegation_violation-ContextClassLoader.png)
从上图可知rt.jar核心包是有Bootstrap类加载器加载的，其内包含SPI核心接口类，由于SPI中的类经常需要调用外部实现类的方法，而jdbc.jar包含外部实现类(jdbc.jar存在于classPath路径)无法通过Bootstrap类加载器加载，因此只能委派线程上下文类加载器把jdbc.jar中的实现类加载到内存以便SPI相关类使用。显然这种线程上下文类加载器的加载方式破坏了"双亲委派模型"，它在执行过程中抛弃双亲委派加载链模式，使程序可以逆向使用类加载器，当然这也使得Java类加载器变得更加灵活。为了进一步证实这种场景，不妨看看DriverManager类的源码，DriverManager是Java核心rt.jar包中的类，该类用来管理不同数据库的实现驱动即Driver,d都实现了Java核心包中的java.sql.Driver接口，如MySQL驱动包中的com.mysql.jdbc.Driver,这里主要看如何加载外部实现类，在DriverManager初始化时会执行如下代码:
```java
// Drivermanager 是Java核心包rt.jar的类
public class DriverManager {
    // 省略不必要的代码， 为一些处理相关逻辑的代码
    static {
        loadInitialDrivers();// 执行该方法
        println("JDBC DriverManager initialized");
    }
    
    // loadInitialDriver
    private static void loadInitialDrivers() {
        // If the driver is packaged as a Service Provider, load it. Get all the drivers through the classLoader
        // exposed as a java.sq;.Driver.class service. ServiceLoader.load replaces the sun.misc,Providers().
        AccessController.doPrivileged(new PrivilegedAction<Void>() {
            public Void run() {
                // 加载外部的Driver的实现类
                ServiceLoader<Driver> loaderDrivers = ServiceLoader.load(Driver.class);
                // 省略不必要的逻辑代码
            }
        });
    }
}
```
> 在DriverManager类初始化时执行了loadInitialDrivers()方法，在该方法中通过ServiceLoader.load(Driver.class);去加载外部实现的驱动类，ServiceLoader类会读取MySQL的jdbc.jar下META-INF文件的内容:
![加载mysql驱动的外部类路径](/doc/image/mysql-jdbc-driver.png)
![mysql中Driver继承的来自rt.jar中的SPI接口](/doc/image/mysql-driver-extends-rt_Driver.png)
com.mysql.jdbc.Driver继承关系如下：
```java
//Here for backwards compatibility with MM.MySQL
public class Driver extends com.mysql.cj.jdbc.Driver {
    public Driver() throws SQLException {
        super();
    }
    static {
        System.err.println("Loading class `com.mysql.jdbc.Driver'. This is deprecated. The new driver class is `com.mysql.cj.jdbc.Driver'. "
                        + "The driver is automatically registered via the SPI and manual loading of the driver class is generally unnecessary.");
    }
}
```
> 从注释可以看出平常我们使用com.mysql.jdbc.Driver已经被丢弃了(deprecated),取而代之的是com.mysql.cj.jdbc.Driver，也就是说官方不在建议使用如下代码注册mysql驱动:
```java
// 不建议使用该方式注册驱动类
Class.forName("com.mysql.jdbc.Driver");
String url = "jdbc:mysql://localhost:3306/cm-storylocker?characterEncoding=UTF-8";
// 通过java库获取数据库连接
Connection conn = java.sql.DriverManager.getConnection(url, "root", "password");
```
> 而是直接去掉注册步骤:
```java
String url = "jdbc:mysql://localhost:3306/cm-storylocker?characterEncoding=UTF-8";
// 通过java库获取数据库连接
Connection conn = java.sql.DriverManager.getConnection(url, "root", "password");
```
> 这样ServiceLoader会处理好驱动类注册工作，并最终通过load()方法加载，load()方法实现如下:
````java
public static <S> ServiceLoader<S> load(Class<S> service) {
    // 通过线程上下文类加载器加载
    ClassLoader cl = Thread.currentThread().getContextClassLoader();
    return ServiceLoader.load(service, cl);
}
````
> 很明显确实通过线程上下文类加载器加载的，实际上核心包的SPI类对外部实现类的加载都是基于线程上下文类加载器执行的，通过这种方式实现了Java核心代码内部去调用外部实现类。*我们知道线程上下文类加载器默认情况下就是AppClassLoader，为什么不直接通过getSystemClassLoader()获取类加载器来加载classpath路径下的类呢？通常情况下是可行的，但是如果代码部署到不同服务器时，如果这些服务使用的线程上下文类加载器并非AppClassLoader而是应用服务器自家的类加载器，类加载器不同，这样可能会导致不必要的问题。不同的服务器可能默认ClassLoader不同，但是使用线程上下文类加载器总能获取到与当前程序执行相同的ClassLoader，从而避免不必要的问题。*<p>
DriverManager、ServiceLoader(解耦机制)

> 类加载器的委托欣慰动机是为了避免相同的类被加载多次，但事实上，Java在服务器端要求类加载器能够翻转委派原则，即限价在本地的类，如果加载不到，再到parent中加载。这里需要区分委派、反转委派、破坏委派方式<p>
1、委派即支持双清委派模型<p>
2、反转委派即先加载本地的类，如果加载不到才回到parent类加载器中尝试加载<p>
3、破坏委派即打破委派加载模式，如SPI(server provider Interface)这种线程加载器(父类默认是appClassLoader).<p>
在Tomcat中默认行为是先尝试在Bootstrap和ExtensionClassLoader中进行加载，加载不到在在AppClassLoader加载最后到自定义加载器中加载。<p>
ClassNotFoundException、 NoClassDefFoundError、NoSuchMethodError、ClassCastException 判断一个类实例相同的条件是类加载器+全限定名,如果有多个类加载器，**这里需要注意**<p>
linkageError 同一个类被不同加载器加载

#### 委派机制(delegation model)和颠覆委派机制
> 委派机制的典型代表"Tomcat类加载机制"  颠覆委派机制-》"OSGI类加载"<p>
测试类加载顺序，可以先生成一个类的class文件放入到ext加载的位置中，然后在将原来的java文件中的提示修改，启动后能发现扩展类加载器先于系统应用类加载器。

使用Middleware-Detector进行类查找

*参考资料*

[JSR33](http://ifeve.com/wp-content/uploads/2014/03/JSR133%E4%B8%AD%E6%96%87%E7%89%881.pdf)

[深入理解java虚拟机](/doc/PDF/《深入理解Java虚拟机：JVM高级特性与最佳实践》.pdf)
[深入分析Java web技术内幕]:

[ClassLoader加载](http://ifeve.com/classloader/)

[从jdk源码角度理解jvm类加载机制](https://blog.csdn.net/architect0719/article/details/50411545)

[类加载机制中的自定义ClassLoader实现以及exception](https://blog.csdn.net/architect0719/article/details/50411545)