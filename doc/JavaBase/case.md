
* [HashMap多线程操作导致死循环问题](https://coolshell.cn/articles/9606.html)
```text
当HashMap在Rehash的时候，如果存在多线程Rehash，第一个线程已经Rehash完毕，第二个线程在第一个线程Rehash时已经记录了启动位置，等第一个线程执行完不候第二个线程再执行时，有可能出现将已经断掉的指针重新续接而形成环形链表导致死循环
```

* [Hash Collision DOS 问题-hash碰撞的拒绝式服务攻击](https://coolshell.cn/articles/6424.html)
```text
是 Hash Collision DoS （Hash碰撞的拒绝式服务攻击），有恶意的人会通过这个安全弱点会让你的服务器运行巨慢无比。这个安全弱点利用了各语言的Hash算法的“非随机性”可以制造出N多的value不一样，但是key一样数据，然后让你的Hash表成为一张单向链表，而导致你的整个网站或是程序的运行性能以级数下降（可以很轻松的让你的CPU升到100%）
```
* 