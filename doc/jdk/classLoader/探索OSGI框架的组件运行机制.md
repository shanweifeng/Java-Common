### [探索OSGI框架的组件运行机制](https://www.ibm.com/developerworks/cn/java/j-lo-osgi/index.html)
>基于为组件分配独立的类加载器(Class Loader)的思想。

#### OSGI组件框架
> 在框架中，组件被称为Bundle，它是由一些提供Bundle自身功能的资源(如java类文件、配置文件等)、MANIFEST.MF文件和其他资源文件构成。在运行时环境中，每个Bundle都有一个独立的Class Loader，Bundle之间通过不同的类加载器和在MANIFEST.MF文件中定义的包约束条件就可以轻松实现包级别的资源隐藏和共享，从而实现基于组件方式的开发和运行。Class Loader是实现这种运行方式的关键机制，每个Bundle的Class Loader必须在此Bundle得到正确的解析(Resolving)之后，再由框架创建。只有当一个Bundle中所有包约束条件都满足时，它才被正确解析完毕。

* Bundle解析
> Bundle的解析是通过分析定义在MANIFEST.MF文件中的元数据(主要定义了包约束条件)，查找与包约束条件相匹配的Bundle并建立关联关系的过程。MANIFEST.MF文件中的包约束条件主要是通过Import-Package、DynamicImport-Package、Export-Package和Require-Bundle这四种表达方式来实现。<p>
1、Import-Package:定义需要导入的包。默认是所有需导入的包必须都能够找到相应的导出Bundle(Export)，否则解析失败。<p>
2、Export-Package：定义导出的包。在一个Bundle里面，一个包的导出定义并不意味着相应的包导入定义，而是这些类资源会在Bundle自身的类路径里面查找和加载。<p>
3、Require-Bundle：定义依赖的Bundle。<p>
4、DynamicImport-Package：定义需要动态导入的包。这部分定义没有在Bundle接戏过程中使用，而是在运行时动态解析并加载共享包。<p>

> 在Bundle得到正确解析后，OSGI框架将会生成此Bundle的依赖关系表。通过关系表能够找到 Bundle依赖的外部Class Loader从而实现外部类资源的加载和运行。

* Bundle运行
> Bundle的运行主要依靠于OSGI框架为其创建的类加载器(Class Loader)，加载器负责查找和加载Bundle自身 或所依赖的类资源。ClassLoader之间的依赖关系构成了一个有向图![Bundle中ClassLoader之间的依赖关系有向图](/doc/image/OSGI_Bundle_digraph.png)
Bundle 的Class Loader能加载的所有类的集合构成了Bundle的类空间(Class Space).累空间包含的类资源主要来源于以下几个方面:<p>
1、父ClassLoader可加载 的类集合<p>
2、Import-Package定义的依赖的包<p>
3、Require-Bundle定义依赖的Bundle的类集合<p>
4、Bundle自身的类集合，通常在Bundle-Classpath中定义<p>
5、隶属于Bundle的Fragment类集合<p>

> 在实际运行环境中，Bundle的Class Loader根据如下规则去搜索类资源：<p>
1、如类资源属于java.*包，则将加载请求委托给父加载器<p>
2、如类资源定义在OSGI框架中启动委托列表(org.osgi.framework.bootdelegation)中，则将加载请求委托给父加载器<p>
3、如类资源属于在Import-Package中定义的包，则框架通过Class Loader依赖关系图找到导出此包的Bundle的Class Loader，并将加载请求委托给此Class Loader<p>
4、如类资源属于在Require-Bundle中定义的Bundle，则框架通过Class Loader依赖关系图找到此Bundle的class loader，将加载请求委托给此Class Loader<p>
5、Bundle搜索自已的类资源(包括Bundle-Classpath里面定义的类路径和属于Bundle的Fragment的类资源)<p>
6、若类在DynamicImport-Package中定义，则开始尝试在运行环境中寻找符合条件的Bundle<p>
7、若任然没有正确的加载到类资源则OSGI框架会想歪抛出类未发现异常。

#### 确保Bundle类空间的完整性
> 