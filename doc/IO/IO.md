* [IO](https://segmentfault.com/a/1190000003063859)
```text
IO访问会经历两个阶段：
1、等待数据准备(Waiting for the data to be ready)
2、将数据从内核拷贝到进程中(Copying the data from the kernel to process)
这两个模式使得Linux系统产生了下面五种网络模式的方案：
阻塞I/O(blocking IO)
非阻塞I/O(nonblocking IO)
I/O多路复用(IO multiplexing)
信号驱动I/O(signal driven IO)
异步 I/O(asynchronous IO)

```