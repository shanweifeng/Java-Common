## [《Docker 创建镜像、修改、上传镜像》](https://www.cnblogs.com/lsgxeva/p/8746644.html)

### 创建镜像
* 可以从Docker Hub获取已有镜像并更新，也可以利用本地文件系统创建

### 修改已有镜像
* 先使用下载的镜像启动容器
> docker run -it training/sinatra /bin/bash
>> 记住容器的ID，后续会用到

* 在容器中添加json和gem两个应用
> gem install json

当结束后，使用exit退出，现容器已经被我们改变，使用docker commit命令来提交更新后的副本
> sudo docker commit -m "Added json gem" -a "Docker Newbee" 0b2616b0e5a8 ouruser/sinatra:v2
>> 其中，-m 来指定提交的说明信息，跟我们使用的版本控制工具一样；-a 可以指定更新的用户信息；之后是用来创建镜像的容器的 ID；最后指定目标镜像的仓库名和 tag 信息。创建成功后会返回这个镜像的 ID 信息。

使用docker images来查看新创建的镜像
> sudo docker images

之后使用新的镜像来启东容器
> sudo docker run -it ouruser/sinatra:v2 /bin/bash

### 利用Dockerfile来创建镜像
* 新建一个目录和一个Dockerfile
> mkdir sinatra    cd sinatra  touch Dockerfile

* Dockerfile 中每一条指令都创建镜像的一层，如
```text
# this is a comment 
FROM ubuntu:14.04
MAINTAINER Docker Newbee <newbee@docker.com>
RUN apt-get -qq update
RUN apt-get -qqy install ruby ruby-dev
RUN gem install sinatra
```
> Dockerfile 基本语法是：使用#来注释，
