* 设置缓存区大小
git config http.postBuffer 524288000
* 网络下载速度慢
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999

* 浅层clone
git clone --depth=1 http://gitlab.xxx.cn/yyy/zzz.git
git fetch --unshallow

git clone https://github.com/apereo/cas.git --depth 1

env GIT_SSL_NO_VERIFY=true git clone https://github.com/apereo/cas.git
git config http.sslVerify "false"

git config  --global   http.sslVerify "false"

* [多git账号设置](https://www.cnblogs.com/popfisher/p/5731232.html)