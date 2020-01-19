# Getting Started

### Reference Documentation
For further reference, please consider the following sections:

* [Official Apache Maven documentation](https://maven.apache.org/guides/index.html)

### Java IO
* [参考一](https://segmentfault.com/a/1190000014932357)

##### 按操作方式：
* Reader 字符读取
> * 节点流：FileReader、PipedReader、CharArrayReader

> * 处理流：BufferedReader、InputStreamReader

* Writer 字符写出
> * 节点流：FileWriter、PipedWriter、CharArrayWriter

> * 处理流：BufferedWriter、OutputStreamWriter、printWriter

* InputStream 字节读取
> * 节点流：FileInputStream、PipedInputStream、ByteArrayInputStream

> * 处理流：BufferedInputStream、DataInputStream、ObjectInputStream、SequenceInputStream

* OutputStream 字节写出
> * 节点流：FileOutputStream、PipedOutputStream、ByteArrayOutputStream

> * 处理流：BufferedOutputStream、DataOutputStream、ObjectOutputStream、PrintStream

* 输入/输出流体系中常用的流分类表

|分类|字节输入流|字节输出流|字符输入流|字符输出流|
|-----|----------|----------|----------|---------|
|抽象基类|InputStream|OutputStream|Reader|Writer|
|访问文件|FileInputStream|FileOutputStream|FileReader|FileWriter|
|访问数组|ByteArrayInputStream|ByteArrayOutputStream|CharArrayReader|CharArrayWriter|
|访问管道|PipedInputStream|PipedOutputStream|PipedReader|PipedWriter|
|访问字符串| | |StringReader|StringWriter|
|缓冲流|BufferedInputStream|BufferedOutputStream|BufferedReader| BufferedWriter|
|转换流| | |InputStreamReader|OutputStreamWriter|
|对象流| ObjectInputStream|ObjectOutputStream| | |
|抽象基类|FilterInputStream|FilterOutputStream|FilterReader|FilterWriter|
|打印流| |PrintStream| |PrintWriter|
|推回输入流|PushbackInputStream| |PushbackReader| |
|特殊流|DataInputStream|DataOutputStream| | |

#### 按操作对象：
* 缓冲操作：BufferedInputStream、BufferedOutputStream、BufferedReader、BufferedWriter

* 基本数据类型操作：DataInputStream、DataOutputStream

* 对象序列化操作：ObjectInputStream、ObjectOutputStream

* 转化控制：InputStreamReader、OutputStreamWriter

* 打印控制：printStream、printWriter

* 文件操作：FileInputStream、FileOutputStream、FileReader、FileWriter

* 管道操作：PipedInputStream、PipedOutputStream、PipedRead、PipedWriter

* 数组操作：ByteArrayInputStream、ByteArrayOutputStream、CharArrayReader、CharArrayWriter

>> 上面两种方式中“按操作对象”方式比“按操作方式”少一种SequenceInputStream流操作方式。

* IO流分类：
> * 按照流的流向：可以分为输入流和输出流
> * 按照操作单元：可以分为字节流和字符流
> * 按照流的角色：可以分为节点流和处理流

>> * 节点流：可以从/向一个特定的IO设备(如磁盘、网络)读/写数据的流。也被称为低级流。使用节点流进行输入和输出时，程序直接连接到实际的数据源

>> * 处理流：对一个已经存在的流进行连接和封装，通过封装后的流来实现数据的读/写功能。也被称为高级流。使用处理流进行输入/输出时，程序并不会直接连接到实际的数据源，没有和实际的输入和输出节点连接。这样的好处是如果数据源发生了变化处理流的使用方式可以不改变。

* 流的原理浅析
> InputStream和Reader里面都提供了一些方法来控制记录指针的移动
> * 处理流的功能只要体现在以下两个方面：
>> * 性能的提高：主要以增加缓冲的方式来提供输入和输出的效率
>> * 操作的便捷：处理流可能提供了一系列便捷的方法来依次输入和输出大批量的内容，而不是输入/输出一个或多个水滴。
> 处理流可以“嫁接”在任何已存在的流的基础上，这就允许Java应用程序采用相同的代码，透明的方式来访问不同的输入和输出设备的数据源。


### 常用IO流的用法
##### IO体系的基类
```
字节流和字符流的操作方式基本一致，只是操作的数据单元不同。字节流操作单元市字节，字符流操作单元市字符
```
> InputStream和Reader是所有输入流的抽象基类
* InputStream、Reader里包含以下方法(主要方法)

|方法类型|InputStream方法签名 | 方法简介 |Reader方法签名 |方法简介 |
|----|--------------------|-----------|--------------|---------|
|读取方法|int read()|从输入流中读取单个字节，<p>返回所读取的字节数据(字节数据可直接转换成int类型)| int read()|从数据流中读取单个字符，返回所读取的字符数据(字符数据可直接转成为int类型)|
|读取方法|int read(byte[] b|从输入流中最多读取b.length个字节数据，<p>并将其存储在字节数组b中，返回实际读取字节数|int read(char[]  b)|从输入流中最多读取b.length个字符，并将其存储在字符数组b中，返回实际读取的字符数|
|读取方法|int read(byte[] b,int off,int len)|从输入流中的off位置最多读取len个字节的数据，并将其存储在b数组中，返回实际读取的字节数|int read(char[] b,int off,int len)|从输入流中的off位置开始最多读取len个字符的数据，并将其存储在数组b中，返回实际读取的字符数|
|指针移动|void mark(int readAheadLimit)|在记录指针当前位置记录一个标记(mark)|同前面||
|指针移动|void markSupported()|判断此输入流是否支持mark()操作，即是否支持记录标记|同前面||
|指针移动|void reset()|将此流的记录指针重新定位到上一次记录标记(mark)的位置|同前面||
|指针移动|long skip(long n)|记录指针向前移动n个字节/字符|同前面||

* OutputStream、Writer里包含以下方法(主要方法)

|InputStream方法签名 | 方法简介 |Reader方法签名 |方法简介 |
|--------------------|-----------|--------------|---------|
|void write(int c)|将指定字节输出到流中|void write(int c)|将指定字符输出到流中|
|void write(byte[] buf) |将字节数组中的数据输出到指定流中|void write(char[] buf)|将字符数组中的数据输出到指定流中|
|void write(byte[] buf, int off,int len) |将字节数组从off位置开始长度为len的字节输出到流中|void write(char[] buf, int off,int len)|将字符数组从off位置开始长度为len的字节输出到流中|
| | |void write(String str)|将字符串里包含的字符输出到指定输出流中|
| | |void writer(String str, int off, int len)|将字符串中从off位置开始长度为len的字符输出到指定输出流中|
| | | Writer append(CharSequence csq)|将字符输出到指定流中 |
| | | Writer append(CharSequence csq, int off, int len)|将 字符从off位置开始长度为len的字符输出到指定流中 |
| | | Writer append(char c)|将字符输出到指定流中 |

##### IO体系的基类文件流的使用(FileInputStream/FileReader、FileOutputStream/FileWriter)
 > 具体查看java-io中file package内的几个测试类
 
##### 转换流的使用(InputStreamReader/OutputStreamWriter)
> 具体查看java-io中convert package内的几个测试类
>> BufferedReader具有缓存功能，一次读取一行，如果没有换行标志则程序阻塞

##### 对象流(ObjectInputStream/ObjectOutputStream)
 > 具体查看java-io中object package内的几个测试类
 
 