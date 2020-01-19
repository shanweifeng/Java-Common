## [《Docker安装及常用命令》](https://www.cnblogs.com/configure/p/6434224.html)

[Docker 创建镜像、修改、上传镜像](https://www.cnblogs.com/lsgxeva/p/8746644.html)

* 修改机器名：hostnamectl set-hostname Docker

* 安装EPEL源：
> yum -y install epel-release <p>
yum clan all<p>
yum makecache

* 安装Docker:
> yum -y install docker <p>
systemctl enable docker <p>
systemctl start docker

### 镜像管理:
* 搜索在线可用的镜像名: docker search centos

* 从官网拉取镜像： docker pull centos

* 查询本地所有的镜像: docker images 

* 删除单个镜像： docker rmi docker.io/centos -f

* 删除所有镜像: docker rmi$(docker images | grep none | awk '{print $3}' | sort -r)

* 创建镜像: docker commit -m="Added Nginx 10.1" -a="Rock Zhao" ef16fea87866 17track/nginx:v1

* 查询镜像详细信息： docker inspect 10888ace4357

### 容器管理
* 创建容器：docker run -it --restart=always --name centos7 -p 80:80 -v /root/docker-centos7:/root/docker-centos7 docker.io/centos:latest /bin.bash

* 查看正在运行的容器： docker ps

* 查看最后退出的容器的ID： docker ps -l

* 查看所有的容器，包括退出的: docker ps -a

* 启动容器： docker start determined_noyce

* 停止容器: docker stop determined_noyce

* 杀掉容器： docker kill determined_noyce

* 删除容器：docker rm determined_noyce

* 删除所有容器： docker rm$(docker ps -a -q)

* 登录容器： docker exec -it determined_noyce /bin/bash
> docker exec -it determined_noyce /bin/sh

* 执行容器内部程序命令： docker exec centos7 /usr/local/nginx/sbin/nginx

* 拷贝文件：docker cp nginx2:/usr/local/nginx /home
> docker cp rootpath-96.sdf.tar.gz nginx:/usr/local/src

* 显示容器内运行的进程: docker top <container>

* 查询某个容器的所有操作记录：docker logs {containerID|容器名称}

* 实时查看容易的操作记录: docker logs -f {containerID|容器名称}