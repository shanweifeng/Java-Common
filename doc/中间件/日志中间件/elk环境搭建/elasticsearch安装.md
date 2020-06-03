```text
命令：docker pull docker.elastic.co/elasticsearch/elasticsearch:7.2.0 拉取镜像(这里也可以自己制作镜像或者换其他镜像仓库)
命令：docker run --name es0 -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.2.0 创建elasticsearch容器并简易启动容器
命令：docker restart es 重启docker es
命令：docker exec -it es01[容器名/容器id] bash(或/bin/sh) 进入容器
```
启动容器命令中 discovery.type=single-node代表单节点启动容器服务，如果要设置集群则该配置需要去除。
--name es7将这个容器命名es7 起名之后 docker restart es7  容器的重启通过自定义的命名进行操作
-p 9200:9200 将宿主端口映射到Docker容器中的9200端口 此时可访问容器中的es服务

```text
命令：docker cp es01[容器名/容器id]:/usr/share/elasticsearch/config/ /opt/elasticsearch/   配置 
命令：docker cp es01[容器名/容器id]:/usr/share/elasticsearch/data/ /opt/elasticsearch/     数据
命令：docker cp es01[容器名/容器id]:/usr/share/elasticsearch/logs/ /opt/elasticsearch/     日志
命令：docker cp es01[容器名/容器id]:/usr/share/elasticsearch/plugins/ /opt/elasticsearch/  插件
-- 上面四个命令需要在简易容器启动时操作
命令：docker run --name esMaster1 -p 9201:9200 -p 9301:9300 -v /opt/elasticsearch/master1/config/:/usr/share/elasticsearch/config/ -v /opt/elasticsearch/master1/data/:/usr/share/elasticsearch/data/ -v /opt/elasticsearch/master1/logs/:/usr/share/elasticsearch/logs/ -v /opt/elasticsearch/plugins/:/usr/share/elasticsearch/plugins/ -v /etc/localtime:/etc/localtime   docker.elastic.co/elasticsearch/elasticsearch:7.2.0 启动节点
```

启动节点：
--name esMaster1 指定容器名称
-p 9201:9200 -p 9301:9300 宿主机容器端口映射
-v /opt/elasticsearch/master1/config/:/usr/share/elasticsearch/config/ 以及其他data logs plugins等为宿主机目录映射到容器中指定的相应目录。
docker.elastic.co/elasticsearch/elasticsearch:7.2.0 指定启动容器的镜像。
其他节点启动改变相应的容器名称、映射端口、映射目录即可启动。

* elasticsearch服务的配置：
```java
cluster.name: "elasticsearch_cluster" # 设置集群名称 一定要确保不要在不同的环境中使用相同的集群名称。否则，节点可能会加入错误的集群中。
node.name: "master1"                  # 设置节点名称
node.master: true                     # 是否可竞选master节点
node.data: true                       # 是否存储数据节点
bootstrap.memory_lock: false          #true 如果为true 启动报错 需要修改系统配置 这里先设置为false 由于当jvm开始swapping时es的效率会降低，所以要保证它不swap，这对节点健康极其重要。实现这一目标的一种方法是将 bootstrap.memory_lock 设置为true。
要使此设置有效，首先需要配置其他系统设置。
network.host: 0.0.0.0                 # 网络地址 设置为0.0.0.0为所有网络可访问
transport.tcp.compress: true          # 设置是否压缩tcp传输时的数据
http.cors.enabled: true               # 配置跨域
http.cors.allow-origin: "*"           # 配置跨域
http.cors.allow-headers: X-Requested-With,X-Auth-Token,Content-Type,Content-Length,Authorization  #
http.cors.allow-credentials: true                                                                 #
# minimum_master_nodes need to be explicitly set when bound on a public IP
# # set to 1 to allow single node clusters
# # Details: https://github.com/elastic/elasticsearch/pull/17288
# discovery.type: single-node  # 启动集群时需要注释
discovery.zen.ping.unicast.hosts: ["172.17.0.1:9302", "172.17.0.1:9303"] # 集群其他机器地址
discovery.zen.ping_timeout: 30s                                          # 超时时间设置30s
discovery.zen.minimum_master_nodes: 2                                    # 为了防止数据丢失， discovery.zen.minimum_master_nodes 配置至关重要， 以便每个候选主节点知道为了形成集群而必须可见的最少数量的候选主节点。
cluster.initial_master_nodes: ["master1"]                                # 初始化为master节点的节点名称
gateway.recover_after_nodes: 3                                           # 设置集群中N个节点启动时进行数据恢复
gateway.recover_after_time: 3m                                           # 设置初始化数据恢复进程的超时时间
action.destructive_requires_name: true                                   # 设置之后只限于使用特定名称来删除索引，使用_all 或者通配符来删除索引无效
node.max_local_storage_nodes: 256                                        # 这个配置限制了单节点上可以开启的ES存储实例的个数，我们需要开多个实例，因此需要把这个配置写到配置文件中，并为这个配置赋值为2或者更高。
xpack.security.enabled: false     # 是否开启xpack安全认证
```


* 错误处理
```text
1、max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
解决：/etc/sysctl.conf文件下新增 vm.max_map_count=262144  然后sysctl -p使其生效

2、failed bind service***
解决：给宿主机映射添加777的权限
```

* [elasticsearch config](https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html#path-settings)
* [elasticsearch wiki](https://github.com/13428282016/elasticsearch-CN/wiki/es-setup--elasticsearch)
* [bootstrap.memory_lock](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-configuration-memory.html#mlockall)
* [阿里云elasticsearch](https://help.aliyun.com/product/57736.html)