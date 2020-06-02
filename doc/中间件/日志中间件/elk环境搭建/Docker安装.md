docker version 或者 docker --version 查看安装版本 如果没有会报错

命令： yun -y install docker 执行安装docker

命令： docker version 查看docker版本
命令： service docker start 启动docker服务
命令： docker info 查看docker存储位置
命令： docker ps 查看是否有docker进程
命令： docker logs -f 容器名 查看日志
命令： docker images  查看镜像文件
命令： docker ps  查看正在运行的容器
命令： docker ps –a  查看所有的容器
命令： docker stop CONTAINER_ID 停止容器
命令： docker container exec -it containerId /bin/bash  进入到容器
命令： exit 退出
命令： docker version  查看版本
命令： docker run -d -p 81:80 nginx 启动nginx容器
命令： docker rmi imgageid 删除镜像
命令： docker rm 容器id 删除容器
命令： docker volumes ls  查看所有volume存储名称
命令： docker volumes inspect volumeName  查看指定存储名称的路径


docker-compose安装问题：
* max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
vm.max_map_count kernel setting needs to be set to at least 262144
解决：/etc/sysctl.conf文件下新增 vm.max_map_count=262144 然后sysctl -p使其生效
