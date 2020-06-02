命令：docker pull mobz/elasticsearch-head:5 拉取镜像 版本根据需要确定
命令：docker run -d --name es_head -p 9100:9100 -v /etc/localtime:/etc/localtime  mobz/elasticsearch-head:5 运行容器

命令：docker  cp 容器名称或Id:/usr/src/app/_site /opt/elasticsearch/head/_site/
命令：docker run -d --name es_head -p 9100:9100 -v /opt/elasticsearch/head/_site/:/usr/src/app/_site/  -v /etc/localtime:/etc/localtime  mobz/elasticsearch-head:5 重新创建容器并启动

* 问题解决：
elasticsearch配置文件中一定要配置跨域配置
es-head chrome插件请求报错： Content-Type header [application/x-www-form-urlencoded] is not supported: 进入_site中找到vendor.js，修改6886跳转到6886行，把contentType: "application/x-www-form-urlencoded" 改为 contentType: "application/json"