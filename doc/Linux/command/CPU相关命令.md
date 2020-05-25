### 查看CPU相关命令

 
* 1.1 查看CPU个数
 ```text
 # cat /proc/cpuinfo | grep "physical id" | uniq | wc -l
 2 **uniq命令：删除重复行;wc –l命令：统计行数**
```
* 1.2 查看CPU核数
```text
 # cat /proc/cpuinfo | grep "cpu cores" | uniq
 cpu cores : 4
```
& 1.3 查看CPU型号
```text
 # cat /proc/cpuinfo | grep 'model name' |uniq
  model name : Intel(R) Xeon(R) CPU E5630 @ 2.53GHz
```
 总结：该服务器有2个4核CPU，型号Intel(R) Xeon(R) CPU E5630 @ 2.53GHz
 

* 查看CPU信息的linux系统信息命令 
 ```text
 cat /proc/cpuinfo 
 ```