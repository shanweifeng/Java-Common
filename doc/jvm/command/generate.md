### 一般的jvm命令

* 查看当前java进程的启动参数
```text
jcmd pid VM.flags
jinfo -flags pof 
jmap -heap pid
```