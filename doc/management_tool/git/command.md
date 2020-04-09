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


git clone --depth=1 xxxxxx 这个只能拉取一个分支 没有其他分支信息 下面的为拉取其他分支信息
git remote set-branches origin 'remote_branch_name'
$ git fetch --depth 1 origin remote_branch_name
$ git checkout remote_branch_name