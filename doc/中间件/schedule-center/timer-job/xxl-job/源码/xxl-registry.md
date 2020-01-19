### 关于xxl-registry源码阅读

* xxl-registry-client
** model
> XxlRegistryDataParamVO:key->value

> XxlRegistryParamVO:
>> accessToken、biz、env、keys(List<String>)、registryDataList(List<XxlRegistryDataParamVO>)

** util request and json to Object
> BasicHttpUtil: request methos

** XxlRegistryBaseClient
> adminAddress、accessToken、biz、env
>> method: registry remove discovery monitor

** XxlRegistryClient 
> registryData(Set<XxlRegistryDataParamVO>)、discoveryData(ConcurrentMap<String, TreeSet<String>>)、 registryThread(Thread)、discoveryThread(Thread)、registryThreadStop(boolena default false)、registryBaseClient(XxlRegistryBaseClient)
>>> 通过将操作数据放入列表中，由线程轮询执行 registry 、 remove 、 discover、 stop thread等操作，这些操作最终通过baseClient一HTTP形式请求admin对应的接口


* Xxl-registry-admin:
** 项目涉及三张数据库表:xxl-registry、xxl-registry-data、xxl-registry-message

*** XxlRegistryServiceImpl:
**** pageList: 根据业务标识、环境标识、注册Key分页查询registry ,总记录数和过滤后的总记录数是同一个数
**** delete: 查询registry 并删除registry and registry data记录,同时将删除的registry记录信息存放到registry message中
**** update: 校验并查询更新registry记录，更新成功后将更新后的信息存放到registry message中
**** add: 校验并添加registry记录,添加成功后将更新后的信息存放到registry message中

**** registry: 校验并将biz and env param copy to registry data,将registryDataList参数集合添加到registryQueue阻塞队列中
**** remove: 校验biz and env param copy to registry data,将registryDataList参数集合添加到removeQueue阻塞队列中
**** discover: 校验biz and env param copy to registry data,通过biz和env和key查找到相关注册文件，根据key和文件中的data数据存返回对应map
**** monitor: 校验biz and env param， 通过biz和env和key查找到相关注册文件，通过DeferredResult异步处理生成返回值。将对应的key值相关文件的监控信息放入集合并放入registryDeferredResultMap中
**** checkRegistryDataAndSendMessage： 根据registryData数据查找出符合要求的registryData集合，将集合中对象的value提取出来合并成一个json字符串，根据对应的条件查找出registry，如果不存在，添加registry，否则将前一步获取的json串放到registry的data中更新registry，同时将变更信息记录到message表中。(前提是registry记录钥匙可用的)
**** afterPropertiesSet: 启动10个添加线程(这里为什么启动10个)，从队列registryQueue中获取到registryData数据，更新或添加registryData数据，获取registry对应的文件，检查当前数据是否在registry对应关联的数据中。存在则不做操作，否则更新registry中data数据并将变更记录到message中。
 另起10个删除线程，从removeQueue队列中获取registry数据，删除对应的记录，根据标识获取registry记录，如果registry记录data中存在当前registryData数据，则将registry中data更新并将变更记录添加到message中。
 启动一个清除旧old message线程。将消息中的data数据转换成registry对象，如果registry对象状态是删除的，则将registry对象的data设置为空。然后根据registry对象获取该对象对应的文件，判断文件数据是否相同，如果不相同则将registry对象的数据更新到对应文件中，并根据文件名称获取registryDeferredResultMap中的DeferredResult集合，将变更结果设置setResult中，(DeferredResult是一个异步返回结果的)，同时删除registryDeferredResultMap中对应文件数据。然后将当前文件的目录返回。，每10秒清除一次message
 启动一个清理old registry-data file线程，清除当前时间beatTime*3之前的registrydata记录。获取registry记录，根据registry获取registrydata记录，将每一个registry对应的registryData集合中的value合并成json更新到registry中，更新registry对应的文件，删除当前文件下没有与数据库记录对应的文件。

** controller
*** annotation
**** PermessionLimit: permessionLimit注解
*** interceptor
**** cookieInterceptor: push cookies to model as cookieMap
**** PermissionInterceptor:  登录 登录拦截等
**** WebMvcConfig: 将permessionInterceptor、cookieInterceptor拦截器注册到环境中。
*** resolver
**** MqExceptionResolver: 异常处理

*** ApiController(/api)
**** registry: 
**** remove: 
**** discovery:
**** monitor
*** IndexController
**** index: 列表
**** tologin:登录
**** login:登录
*** RegistryController(/registry)
**** pageList:分页查询注册信息
**** delete：删除注册信息
**** update：
**** addd: 