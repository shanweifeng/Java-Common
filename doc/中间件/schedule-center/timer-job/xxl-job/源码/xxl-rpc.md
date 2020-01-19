### Xxl-RPC源码分析

* xxl-rpc-core
> 核心code

** registry
> ServiceRegistry(abstract)
start stop registry remove discover
** 下面三个registry方式继承了ServiceRegistry抽象类
>> LocalServiceRegistry(本地注册)
>>> 存在一个registryData的Map<String,TreeSet<Stirng>>的实例变量
**** registry(Set<String> keys, String value):将keys中的每个可以放入registryData中，value为其对应添加到TreeSet中的值。
**** remove(Set<String> keys, String value): 从registryData中根据keys中的每一个元素获取到对应的treeSet对象，将value从treeSet对象中删除
**** discover(Set<String> keys)/discover(String key): 根据keys/key从registryData中获取treeSet集合，将集合返回或与可以关联存放到结果集Map中返回。

>> XxlRegistryServiceRegistry(调用xxl-registry注册)
**** start(Map<String, String> param): 设置实例参数registryAddress、AccessToken、biz、env 并获取调用registry的XxlRegistryClient对象
**** stop(): 停止向xxl-registry中注册或删除数据
**** registry(Set<String> keys, String value):将keys中的每个可以与value组装成对象存放到集合中，直接将整个集合注册到xxl-registry中
**** remove(Set<String> keys, String value): 将keys中的每个可以与value组装成对象存放到集合中，直接将整个集合从xxl-registry中删除
**** discover(Set<String> keys)/discover(String key): 根据keys/key从xxl-registry中查询注册数据并返回。

>> ZkServiceRegistry(zk注册)
>>> env(String) zk_address(String) zk_digest(String)   zkBasePath(String)  zkEnvPath(String)  xxlZkClient(XxlZkClient)  refreshThread(Thread)  refreshThreadStop(boolean)    registryData(ConcurrentMap<String, TreeSet<String>) discoveryData(ConcurrentMap<String, TreeSet<String>)
**** keyToPath(String key): 返回zkEnvPath+"/"+key
**** pathToKey(String path): 返回path最后一个字符串
**** start(Map<String, String> param): 获取zkEnvPath，初始化XxlZkClient并监听事件，如果监听事件过期则重新创建zk链接并刷新发现数据，获取监听node如果监听事件节点下面的子节点改变则刷新当前节点的discovery数据。另起一个线程每分钟刷新registry discovery数据。
**** registry(Set<String> keys, String value): 将keys中的每一个key轮询获取TreeSet对象，并将value添加到TreeSet对象中，然后更新zk中对应key节点的子节点,同时更新registryDataMap中的数据。
**** remove(Set<String> keys, String value): 将当前keys中的key对应节点的相应value子节点删除
**** discovery(Set<String> keys)/discovery(String key): 获取discovery中数据并返回

** remoting
*** invoker
**** annotation
>> XxlRpcReference: Rpc reference注解
**** call
******* CallType(enum): SYNC  FUTURE  CALLBACK ONEWAY
******* XxlRpcInvokeCallback<T>: threadInvokerFuture(ThreadLocal<XxlRpcInvokeCallback>)
>> getCallback(): 从threadInvokerFuture获取当前线程对象
>> setCallback(XxlRpcInvokeCallback invokeCallback): 将对象添加到threadInvokerFuture静态变量中。
>> removeCallback(): 删除当前对象的threadInvokerFuture中的变量
****** XxlRpcInvokeFuture:实现Future接口,threadInvokerFuture(ThreadLocal<XxlRpcInvokeFuture>)  futureResponse(XxlRpcFutureResponse)
>> getFuture() serFuture() removeFuture() 三个方法都是操作threadInvokerFuture mapstatic field
>> stop() cancel isCancelled isDone get等方法都是根据futureResponse对象操作其中的方法

**** generic
****** XxlRpcGenericService(I):invoke 接口

**** impl
****** XxlRpcStringInvokerFactory:invoker factory , init service-registry and spring-bean bu annotation for spring
\



>> serviceRegistryClass(Class<? extends ServiceRegistry) serviceRegistryParam(Map<String, String>) xxlRpcInvokerFactory
>>> setBeanFactory(BeanFactory beanFactory): implements BeanFactoryAware
>>> destroy(): xxlRpcInvokerFactory.stop() implements DisposableBean
>>> afterPropertiesSet(): new xxlRpcInvokerFactory对象，并调用start()方法 implements InitializingBean
>>> postProcessAfterInstantiation(): 通过ReflectionUtils.doWithFields反射查找bean属性中存在XxlRpcReference注解(只能注解到接口上)的对象，获取其相关注解属性，创建XxlpcReferenceBean对象 然后获取当前服务注册方式对象调用注册discover接口  implements InstantiationAwareBeanPostProcessorAdapter

**** reference
****** XxlRpcReferenceBean
>> 声明XxlRpcReference注解中含有的几个参数对象以及invokeCallback(XxlRpcInvokeCallback) invokerFactory(XxlRpcInvokerFactory),构造器中初始化网络方式net
>> getObject(): 根据线程上下文类加载器给当前指定对象创建一个代理对象， 并调用目标方法
****** XxlRpcSpringReferenceBean
>> 初始化XxlRpcReferenceBean相关属性  serviceRegistryClass(Class<? extends ServiceRegistry>)  serviceRegistryParam(Map<String, String>) stopCallbackList(List<BaseCallback>)  futureResponsePool(ConcurrentMap<String, XxlRpcFutureResponse>)

**** route  load balance
****** LoadBalance: 负载均衡策略 random  round lru(最少使用 时间) lfu(最不常用 频次) consistent_hash
****** XxlRpcLoadBalance(XxlRpcLoadBalance)： route(String serviceKey, Treeset<String> addressSeet)
****** impl: 四种load balance策略

**** XxlRpcInvokerFactory
****** 声明一个volatile类型的静态实例  
****** notifyInvokerFuture 根据请求requestId从futureResponsePool中获取到XxlRpcFutureResponse对象，将XxlRpcFutureResponse对象中的结果同步到response中

*** net
****** ConnectClient:
>> connectClientMap(static volatile ConcurrentHashMap<String, ConnectClient>)  connectClientLockMap(static volatile ConcurrentHashMap<String, Object>)
>>> 当前abstract class中存在init close isValidate  send四个abstract method
>>> asyncSend(): 通过getPool(String address, Class<? extends ConnectClient> coonectClientImpl, final XxlRpcReferenceBean xxlRpcReferenceBean)获取到ConnectClient对象，然后调用send()方法
>>> getPool(String address, Class<? extends ConnectClient> connectClientImpl, final XxlRpcReferenceBean xxlRpcReferenceBean): 如果connectClientMap为空，则将当前xxlRpcReferenceBean对象中获取到的xxlRpcInvokerFactory中的stopCallbackList中添加一个new BaseCallback对象实例(这个时候synchronize的代码块中connectClientMap中可能会有其他线程添加的数据)，baseCallback对象中，如果connectClientMap此时含有数据，则将数据ConnectClient对象获取出来close,然后清空connectClientMap。
如果connectClientMap不为空，则从connectClientMap中根据当前address获取到ConnectClient对象，如果对象存在则直接返回，如果不存在，尝试从connectClientLockMap中后去到clientLock对象，如果clientLock对象不存在，则根据当前地址创建一个new Object对象放入connectClientLockMap中并将刚创建的Object对象赋值给clientLock对象。使用synchronize(clientLock)锁定后续获取ConnectClient对象。从connectClientMap中根据当前address获取ConnectClient，如果存在并且其isValidate()方法返回true，则返回当前ConnectClient对象，否则根据address清除connectClientMap中的对应数据，后续根据参数connectClientImpl创建一个实例，并将实例初始化后存放到connectClientMap中，并返回当前新建实例。

****** impl:存放四种网络请求方式
> JettyClient: extends client
>> jettyHttpClient(HttpClient) client类中的属性
** asyncSend(String address, XxlRpcRequest): 调用postRequestAsync(String address, XxlRpcRequest)方法
** postRequestAsync(String address, XxlRpcRequest): 通过地址和参数，发出http请求，将请求结果存放到invokerFactory中的futureResponsePool中
** getJettyHttpClient(final XxlRpcInvokerFactory xxlRpcInvokerFactory): 获取jettyHttpClient,如果存在直接返回，如果不存在，init jetty http,avoid repeat init(synchronize(HettyClient.class)),获得jettyHttpClient,并将jettyHttpClient添加到invokerFactory中的stopCallbackList集合中。

> JettyServerHandler
>> xxlRpcProviderFactory(XxlRpcProviderFactory)
** 构造方法 赋值xxlRpcProviderFactory
** handl(String target, Request baseRequest, HttpServletRequest, HttpServletResponse response):如果处理target参数为"/services"的请求。将XxlRPCProviderFactory对象中serviceData中数据轮询添加到方法变量stringBuffer中，然后将数据写出去。否则，获取并序列化请求数据为XxlRPCRequest对象，调用XxlRPCProviderFactory的invokeService 方法请求数据，将返回结果序列化为byte数组后写出去。

> JettyServer: extends Server
>> thread(Thread)  
** start(final XxlRpcProviderFactory xxlRpcProviderFactory): 设置一个守护线程运行。 获得指定线程的Server对象，通过Server对象获得ServerConnector对象，设置连接并启动，jetty中线程启动后需要手动停止，否则会在server中循环等待。
** stop(): thread interrupt

** mina:
**** MinaClient:  extends Client  调用asyncSend()方法
**** MinaClientHandler: extends IoHandlerAdapter
>> xxlRpcInvokerFactory(XxlRpcInvokerFactory) 
>> 构造函数赋值xxlRpcInvokerFactory
>> messageReceived(IoSession session, Object message): 调用xxlRpcInvokerFactory.notifyInvokerFuture(requestId, xxlRpcResponse).
>> exceptionCaught(IoSession session, Thrpwable cause): session.closeOnFlush().
>> sessionCreated(IoSession session): session.getConfig().setIdlTime(IdlStatus.BOTH_IDLE, 10*60)
>> sessionIdl(IoSession session, IdleStatus status): status== IdleStatus.BOTH_IDLE -> session.closeOnFlush(). 
**** MinaConnectClient: extends ConnectClient
>> connector(NioSocketConnector)   ioSession(IoSession)
>> init(String address final Serializer serializer, final XxlRpcInvokerFactory xxlRpcInvokerFactory): 拆分address为ip和port，new NioSocketConnector(), 设置连接的编码/解码方式 设置连接参数，根据地址连接，异步连接(mina)
>> isValidate(): connector is active  and session is connected
>> close(): 关闭session 和connector
>> send(XxlRpcRequest xxlRpcRequest): ioSession.write(xxlRpcRequest)
**** MinaDecoder
**** MinaEncoder
**** MinaServer: extends Server
>> thread(Thread)
>> start(final XxlRpcProviderFactory xxlRpcProviderFactory): new Thread();根据类名称获取ThreadPoolExecutor, acceptor = new NioSocketAcceptor;设置acceptor过滤链(ExecutorFilter-> Executors.newCachedThreadPool, codec).设置SocketSessionConfig属性信息，如果当前线程没有中断，设置线程sleep(1),将thread设置为daemon
>> stop(): thread interrupt and callback stop
**** MinaServerHandler: extends IoHandlerAdapter
>> xxlRpcProviderFactory(XxlRpcProviderFactory)  serverHandlerPool(ThreadPoolExecutor)
>> constructor set xxlRpcProviderFactory  serverHandlerPool
>> mesageReceived(final IoSession session, Object message): executor执行线程 调用XxlRPCProviderFactory。invokeService(xxlRpcRquest) session 将XxlRPCResponse write

** netty
**** NettyClient: extends Client
>> 实现父类Client中abstract void asyncSend（String address, XxlRpcRequest xxlRpcRequest);调用NettyConnectClient中的asyncSend()方法。
**** NettyConnectClient: extends ConnectClient
>> group(EventLoopGroup)  channel(Channel)
>> init(String address, final Serializer serializer, final XxlRpcInvokerFactory xxlRpcInvokerFactory): 根据address拆接触host 和 port，新建NIoEventLoopGroup以及Bootstrap，设置bootstrap属性等connect目标地址。
>> isValidate(): channel is active
>> close():关闭channel eventLoopGroup
>> send(XxlRpcRequest xxlRpcRequest):this.channel.writeAndFlush(xxlRpcRequest).sync();
**** NettyClientHandler: extends SimpleChannelInboundHandler<XxlRpcResponse>
>> xxlRpcInvokerFactory(XxlRpcInvokerFactory)
>> constructor set xxlRpcInvokerFactory
>> channelReadO(ChannelHandlerContext ctx, XxlRpcResonse xxlRpcResponse): xxlRpcInvokerFactory.notifyInvokerFuture(xxlRpcResponse.getRequestId, xxlRpcResponse);
>> exceptionCaught(ChannelHandlerContext ctx, Throwable cause): ctx.close()
>> userEventTriggered(ChannelHandlerContext ctx, Object evt): ctx.channel.close();
**** NettyDecoder/NettyEncoder 解码/编码
**** NettyServer: extends Server
>> thread(Thread)
>> start(final XxlRpcProviderFactory xxlRpcProviderFactory): thread = new Thread();thread中根据NettyServer类名称获取当前ThreadPoolExecutor, new NioEventLoopGroup() new NioEventLoopGroup();
>> stop(): thread interrupt and callback stop
**** NettyServerHandler: extends SimpleChannelInboundHandler<XxlRpcRequest>
>> xxlRpcProviderFactory(XxlRpcProviderFactory) serverHandlerPool(ThreadPoolExecutor)
>> constructor set xxlRpcProviderFactory serverHandlerPool
>> channelRead0(final ChannlelHandlerContext ctx, final XxlRpcRequest xxlRpcRequest): executor.execute()-> xxlRpcProviderFactory.invokeService(xxlRpcRequest)

** netty_http
**** NettyHttpClient extends Client: 实现Client的abstract void asyncSend(String address, XxlRpcRequest xxlRpcRequest);调用NettyHttpConnectClient.asyncSend()方法。

**** NettyHttpClientHandler extends SimpleChannelInboundHandler<FullHttpResponse>
>> xxlRpcInvokerFactory(XxlRpcInvokerFactory)    serializer(Serualizer)
>> constructor set xxlRpcInvokerFactory and serializer
>> channelRead0(ChannelHandlerContext ctx, FullHttpResponse msg):deserialize msg , xxlRpcInvokerFactry.notifyInvokerFuture(xxlRpcResponse.getRequestId(), xx;RpcResponse);
>> exceptionCaught(ChannelHandlerContext ctx, Throwable cause): ctx.close();
>> userEventTriggered(ChannelHandlerContext ctxm Object evt): ctx.channel.close()

**** NettyHttpConnectClient 
>> group(EventLoopGroup)  channel(Channel)  serializer(Serializer)  address host
>> init(String address, final Serializer serializer, final XxlRpcInvokerFactory xxlRpcInvokerFactory): 赋值并获取host和port，new NioEventLoopGroup() new Bootstrap(),设置bootStrap属性以及添加pipeline，获取channel等。
>> isValidate(): return channel is active
>> close(): close channel and group
>> send(XxlRpcRequest xxlRpcRequest):serialize xxlRpcRequest,get DefaultFullHttpRequest and set headers, channel.writeAndFlush(DefaultFullHttpRequest).sync();

**** NettyHttpServer extends Server
>> thread(Thread)
>> start(final XxlRpcProviderFactory xxlRpcProviderFactory): new Thread(); similar netty
>> stop(): thread interrupt

**** NettyHttpServerHandler
>> 添加services方法提供在线服务查询
>> 核心方法：xxlRpcProviderFactory.invokeService(xxlRpcRequest)，将返回结果通过ctx write

****** params:
> BaseCallback:  abstract void run
> XxlRpcFutureResponse:  implements Future<XxlRpcResponse>
>> invokerFactory(XxlRpcInvokerFactory)  request(XxlRpcRequest) response(XxlRpcResponse)  done(boolean)  lock(Object) invokeCallback(XxlRpcInvokeCallback)
>>> XxlRpcFutureResponse(final XxlRocInvokerFactory, XxlRpcRequest, XxlRpcInvokeCallback invokeCallback): 赋值给相关变量，调用setInvokerFuture()方法
>>> setInvokerFuture(): 将requestId和当前对象存放到invokerFuture中的futureResponsePool的Map中
>>> removeInvokerFuture(): 根据requestId删除invokerFuture中的futureResponsePool中的数据
>>> setResponse(): 赋值response，并唤醒synchronize(lock)锁的所有其他线程
>>> cancel isCancelled 暂时未实现
>>> get(): 如果没有调用setResponse()则当前线程或wait,直到调用setResponse()方法后被唤醒后返回设置的XxlRPCResponse对象。

> XxlRpcRequest: rpc request param:requestId createMilisTime accessToken className methodName parameterTypes(Class<?>[]) parameters(Object[]) version
> XxlRpcResponse: rpc ressponse param: requestId errorMsg result(Object)
****** Client(abstract): 
>> volatile xxlRpcReferenceBean(XxlRpcReferenceBean)
>>> init(XxlRpcReferenceBean xxlRpcReferenceBean): 赋值xxlRpcReferenceBean
>>> abstract asyncSend(String address, XxlRpcRequest xxlRpcRequest):
****** Server(abstract): 
>> stopedCallback(BaseCallback) startedCallback(BaseCallback)  abstract start(final XxlRpcProviderFactory) abstract void stop()
>>> onStarted(): 运行startedCallback.run()  
>>> onStoped(): 运行stopedCallback.run()  
****** NetEnum(Enum): 四种请求方式类型netty netty_http mina jetty 两个 参数serverClass(Class<? extends Server>) clientClass(Class<？ extends Client)

*** provider
***** XxlRpcService: annotation
***** XxlRpcSpringProviderFactory: extends XxlRpcProviderFactory implements ApplicationContextAware InitializingBean DisposableBean
> netType(default NETTY) serialize(default HESSIAN) ip port accessToken serviceRegistryClass(Class<? extends ServiceRegistry>) serviceRegistryParam(Map<String, String>) 
>>>> prepareConfig(): 获取 netType serialize等信息，调用XxlRpcProviderFactory中的initConfig方法初始化。
>>>> setApplicationContext(ApplicationContextAware): 通过applicationContext获取所有含有XxlRPCService注解的Spring 管理的bean,通过获取到的bean中获取到这些注解的相关配置信息以及bean名称，通过调用XxlRpcProviderFactory中的addService方法添加到serviceData集合中。
>>>> afterPropertiesSet(InitailizingBean): 调用prepareConfig()和XxlRpcProviderFactory中的start方法
>>>> destroy(DisposableBean): 调用XxlRpcProviderFactory中的stop方法

***** XxlRpcProviderFactory:
> serviceRegistryClass(Class<? extends ServiceRegistry>) serviceRegistryParam(Map<String, String>)  netType  serializer ip port accessToken server(Server) serviceRegistry(ServiceRegistry) serviceAddress  serviceData(Map<String,Object>)
>>>> initConfig(): 初始化serviceRegistryClass  serviceRegistryParam netType serializer ip port accessToken 并valid port default 7080 ip默认获取请求方的ip
>>>> start(): 将注册回调的存放到对应server的startedCallback属性上，将 stopCallback设置到server的stopedCallback属性上。启动当前server的start()方法。
>>>> makeServiceKey(String iface, String version): 将iface和version合并成的serviceKey
>>>> addService(String iface, String version, Object serviceBean): 根据makeServiceKey方法获得serviceKey,然后将serviceKey和serviceBean存放到serviceData属性集合中。
>>>> invokeService(XxlRpcRequest xxlRpcRequest): 从serviceData中获取到serviceBean,根据请求serviceRequest中信息，反射调用方法获取结果，返回XxlRPCResponse对象。

** serialize
>>> Hessian1 Hessian  Jackson kryo  protostuff 5中序列化方式

** util



XxlRpcGenericService在哪里被实现过



xxl-rpc源码共读：

registry: 服务注册中心

remoting: 服务通讯模块

serialize: 序列化模块

util: 工具模块

provider: 服务提供方

invoker: 服务消费方

admin: 服务治理、监控中心：管理服务节点信息 统计服务调用次数、QPS和健康状况