## 执行命令(非java的也可以使用)
```text
使用pmap能够查看某一个进程（非java的也能够）的内存使用使用情况，
pman 进程id
```
### 演示样例
```text
pmap 12358
```

#### 结果说明
```text
第一列。内存块起始地址
第二列。占用内存大小
第三列，内存权限
第四列。内存名称。anon表示动态分配的内存，stack表示栈内存
最后一行。占用内存总大小，请注意，此处为虚拟内存大小，占用的物理内存大小能够通过top查看
```