version:2.0.2

JobInfoController: 关于任务管理的相关操作：添加任务、编辑任务、删除任务、手动触发任务、启动任务执行器、停止任务执行器
》 任务地址怎么发现的等问题

JobLogController:关于任务调度相关日志：任务调度器、任务、状态、调度时间查询日志
》 查询时没有具体的管局任务的问题


JobGroupController: 关于执行器

JobCodeGroup：没看到

JobAPIController： 没看明白

IndexController: 运行报表、登录相关接口、格式化绑定

annotation:登录控制注解

interceptor:登录、cookie拦截器

resolver: 异常捕捉

问题点: 触发操作 启动操作 停止排除

RPC:ServletServerHandler  XxlRpcInvokerFactory  XxlRpcProviderFactory  XxlRpcReferenceBean

XxlRpcInvokerFactory.getInstance().stop();  这个在XxlJobExecutor中停止 使用的地方在哪？


RPC  registry : start stop registry remove discovery 