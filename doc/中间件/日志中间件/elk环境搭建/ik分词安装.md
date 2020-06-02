下载分词包：wget https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.2.0/elasticsearch-analysis-ik-7.2.0.zip

解压分词包：unzip elasticsearch-analysis-ik-7.2.0.zip plugins/analysis-ik/

将解压后的分词包放入安装好后的elasticsearch中映射到宿主机上的plugins目录中。多个node可共享一个plugin.



问题解决：
```text
max file descriptors [65535] for elasticsearch process is too low, increase to at least [65536]
编辑 /etc/security/limits.conf，追加以下内容
* soft nofile 65536
* hard nofile 65536

max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
编辑 /etc/sysctl.conf，追加内容vm.max_map_count=655360，然后执行sysctl -p (前面其他安装可能已经操作过这里可以不再操作)
```
