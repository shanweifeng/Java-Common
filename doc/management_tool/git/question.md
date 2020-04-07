*  1、curl 18 transfer closed with outstanding read data remaining
```text
如果出现上面问题可以先设置查看缓冲区大小是否适合，如果缓存设定后还是不行则可以查看网络下载速度，最后在缓存区以及网络下载速度都不能解决下载失败的情况下可是试试浅层clone.
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
-- 刷新分支
git remote update origin --prune

```

