## 类文件结构
> 各种不同的平台的VM与所有平台都统一使用的程序存储格式--字节码(ByteCode)存储格式+VM是构成平台无关性的基石。
#### Class类文件的结构
> Class文件是一组以8个字节为基础单位的二进制流，各个数据项目严格按照顺序紧凑的排列在Class文件中，中间没有添加任何分隔符，这使得整个Class文件中存储的内容几乎全部都是程序运行的必要数据，没有空隙存在。当遇到需要占用8位字节以上的空间的数据项时，则会按照高位在前的方式分割成若干个8位字节进行存储。<p>
根据JVM规范规定，Class文件格式采用一种类似于C语言结构体的伪结构来存储，这种伪结构中只有两种数据类型：**无符号数和表**，后面的解析都要以这两种数据类型为基础。<p>
>> 无符号数属于基本的数据类型，以u1、u2、u4、u8来分别代表1个字节、2个字节、4个字节、8个字节的无符号数，无符号数可以用来描述数字、索引引用、数量值、或者按照UTF-8编码结构成字符串值。<p>
表是由多个无符号数或其他表作为数据项构成的复合数据类型，所有表都习惯性的以"_info"结尾。表用于描述有层次关系的复合结构的数据，整个Class文件本质上就是异常表，由以下数据项构成:

|类型|名称|数量|
|-----|-----|-----|
|u4             |magic|1|
|u2             |minor_version|1|
|u2             |major_version|1|
|u2             |constant_pool_count|1|
|cp_info        |constant_pool|constant_pool_count_1|
|u2             |access_flags|1|
|u2             |this_class|1|
|u2             |super_class|1|
|u2             |interfaces_count|1|
|u2             |interfaces|interfaces_count|
|u2             |fields_count|1|
|field_info     |fields|fields_count|
|u2             |methods_count|1|
|method_info    |methods|methods_count|
|u2             |attributes_count|1|
|attribute_info |attributes|attributes_count|
> 无论是无符号数还是表，当需要描述同一类型但数量不定的多个数据时，经常会使用一个前置的容量计数器加若干个连续的数据项的形式，这时候称这一系列连续的某一类型的数据为某一类型的集合。<p>
* 魔数和Class文件版本
> 每个Class文件的头4个字节称为魔数(Magic Number),唯一作用是用于确定这个文件是否为一个能被虚拟机接受的class文件。用魔数而不是用扩展名来进行身份识别主要是基于安全考虑，扩展名很溶剂可以被改动。<p>
> 紧接着魔数的4个字节存储的是Class文件的版本号:第5和第6个字节是次版本号(Minor Version)，第7和第8个字段是主版本号(Major Version).Java版本号从45开始，JDK1.1之后的每个JDK大版本发布主版本号向上+1,。

* 常量池
> 紧接着主次版本号之后的是常量池入口，常量池是Class文件结构中与其他项目关联最多的数据类型，也是占用Class文件空间最大的数据项目之一，同时它还是在Class文件中第一个出现的表类型数据项目。<p>
由于常量池中常量的数量是不固定的，所以在常量池的入口需要放置一项u2类型的数据(占用两个字节)，代表常量池容量计数值(constant_pool_count)。与Java语言习惯不一样的是这个容量计数是从1开始的。**制定Class文件格式规范时，将第0项常量空出来是由特殊考虑的，这样做是为了满足后面某些指向常量池的索引值的数据在特定情况下需要表达"不引用任何一个常量池项目"的意思，这种情况就可以把索引值置为0来表示。** Class文件结构中只有常量池的容量计数是从1开始的，对于其他集合类型，包括接口索引集合、字段表集合、方法表集合等的容量计数都与一般习惯一致是从0开始的。<p>
> 常量池中主要存放两大类常量:**字面量(Literal)和符号引用(Symbolic References)**。字面量比较接近于Java语言层面的常量概念，如文本字符串、被声明为final的常量值等。符号引用则属于编译原理方面的概念，包括以下几类常量:
>>> 类和接口的全限定名(Fully Qualified Name)<p>
字段的名称和描述符(Descriptor)<p>
方法的名称和描述符<p>
> Java代码在进行javac编译的时候不像C和C++有"连接"这一步骤，而是在VM加载Class文件的时候进行动态链连接，即在Class文件中不会保存各个方法和字段的最终内存布局信息，因此这些字段和方法的符号引用不经过转换的话无法直接被VM使用。当VM运行时，需要从常量池获得对应的符号引用，再在类创建时或运行时解析并翻译到具体的内存地址中。<p>
常量池中的每一项常量都是一个表，多种各不相同的表结构数据，这些表都有一个共同的特点，就是表开始的第一位是一个u1类型的标志位(tag,取值为1-12，缺少标志为2的数据类型)，代表当前这个常量属于那种常量类型。

|类型|标志|描述|
|----|----|----|
|CONSTANT_Utf8_info|1|UTF-8编码的字符串|
|CONSTANT_Integer_info|3|整型字面量|
|CONSTANT_Float_info|4|浮点型字面量|
|CONSTANT_Long_info|5|长整型字面量|
|CONSTANT_Double_info|6|双精度浮点型字面量|
|CONSTANT_Class_info|7|类或接口的符号引用|
|CONSTANT_String_info|8|字符串类型字面量|
|CONSTANT_Fieldref_info|9|字段的符号引用|
|CONSTANT_Methodref_info|10|类中方法的符号引用|
|CONSTANT_InterfaceMethodref_info|11|接口中方法的符号引用|
|CONSTANT_NameAndType_info|12|字段或方法的部分符号引用|
|CONSTANT_InvokeDynamic|||
|CONSTANT_InvokeDynamicTrans|||
> 使用Javap(jdk中bin目录下的javap.exe)在控制台窗口中输入javap -verbose TestClass即可输出当前字节码文件的常量信息。下面是常量池中数据类型的结构表

|常量|描述(项目、类型、描述)|
|-----|-----|
|CONSTANT_Utf8_info               |tag u1 值为1<p> length u2 UTF-8 编码的字符串占用了字节数<p> bytes u1 长度为了length的UTF-8编码的字符串|
|CONSTANT_Integer_info            |tab u1 值为3<p> bytes u4 按照高位在前存储的int值|
|CONSTANT_Float_info              |tab u1 值为4<p> bytes u4 按照高位在前存储的float值|
|CONSTANT_Long_info               |tab u1 值为5<p> bytes u8 按照高位在前存储的long值|
|CONSTANT_Double_info             |tab u1 值为6<p> bytes u8 按照高位在前存储的double值|
|CONSTANT_Class_info              |tab u1 值为7<p> bytes u2 指向全限定名常量项的索引|
|CONSTANT_String_info             |tab u1 值为8<p> index u2 指向字符串字面量的索引|
|CONSTANT_Fieldref_info           |tab u1 值为9<p> index u2 指向声明字段的类或接口描述符CONSTANT_Class_info的索引项<p> index u2 指向字段描述符CONSTANT_NameAndType的索引项|
|CONSTANT_Methodref_info          |tab u1 值为10<p> index u2 指向声明方法的类描述符CONSTANT_Class_info的索引项<p> index u2 指向名称及类型描述符CONSTANT_NameAndType的索引项|
|CONSTANT_InterfaceMethodref_info |ab u1 值为11<p> index u2 指向声明方法的接口描述符CONSTANT_Class_info的索引项<p> index u2 指向名称及类型描述符CONSTANT_NameAndType的索引项|
|CONSTANT_NameAndType_info        |ab u1 值为12<p> index u2 指向该字段或方法名称常量项的索引<p> index u2 指向该字段或方法描述符常量项的索引|

* 访问标志
> 紧接着常量池结束后的2个字节表示访问标志(access_flags),这个标志用于识别一些类或接口层次的访问信息，包括：**这个Class是类还是接口；是否定义为public类型；是否定义为abstract类型；如果是类的话是否被声明为final等。**

|标志名称|标志值|含义|
|-----|-----|-----|
|ACC_PUBLIC     |0x0001|是否为public类型|
|ACC_FINAL      |0x0010|是否被声明为final，只有类可设置|
|ACC_SUPER      |0x0020|是否允许使用invokespecial字节码指令，JDK1.2之后编译出来的类的这个标志位真|
|ACC_INTERFACE  |0x0200|标识这是一个接口|
|ACC_ABSTRACT   |0x0400|是否为abstract类型，对于接口或抽象类来说，此标志值为真，其他类值为假|
|ACC_SYNTHETIC  |0x1000|标识这个类并非由用户代码产生|
|ACC_ANNOTATION |0x2000|标识这是一个注解|
|ACC_ENUM       |0x4000|标识这是一个枚举|
> access_flags中一共有32个标志位可以使用，当前只定义了其中8个，没有使用到的标志位要求一律为0。
* 类索引、父类索引与接口索引集合
> 类索引(this_class)和父类索引(super_class)都是一个u2类型的数据，而接口索引集合(interfaces)是一组u2类型的数据的集合，Class文件中由这三项数据来确定这个类的继承关系。
>> 类索引用于确定这个类的全限定名，父类索引用于确定这个类的父类的全限定名。由于Java语言不允许多重继承，所以父类索引只有一个，除java.lang.Object之外所有的Java类都有父类，因此除了Object之外，所有Java类的父类索引都不为0.<p>
接口索引集合就是用来描述这个类实现了哪些接口，这些被实现的接口将按implements语句(如果这个类本身是一个接口则应当是extend是语句)后的接口顺序从左到右排列在接口的索引集合中。<p>
>>>类索引、父类索引和接口索引集合都按顺序排列在访问标志之后，它们各自指向一个类型为CONSTANT_Class_info的类描述符常量。通过CONSTANT_Class_info类型的常量中的索引值可以找到定义在CONSTANT_Utf8_info类型的常量中的全限定名字符串。<p>
接口索引集合入口的第一项u2类型的数据为接口计数器(interfaces_count),表示索引表的容量。如果该类没有实现任何接口，那么该计数器值为0，后面接口的索引表不再占用任何字节。

* 字段表集合
> 字段表(field_info)用于描述接口或类中声明的变量。字段(field)包括了类级变量或实例级变量**但不包括在方法内部声明的变量。** 
>> 描述一个Java字段包括的信息有:字段的作用于(public、private、protected修饰符)。是类级变量还是实例级变量(static修饰符)、可变性(final)、并发可见性(volatile修饰符，是否强制从主内存读写)、是否可序列化(transient修饰符)、字段数据类型(基本类型、对象、数组)、字段名称。各修饰符都是布尔值，而名称、数据类型是无法固定的，只能引用常量池中的常量描述。

|类型|名称|数量|
|-----|-----|-----|
|u2             |access_flags|1|
|u2             |name_index|1|
|u2             |descriptor_index|1|
|u2             |attributes_count|1|
|attribute_info |attributes|attributes_count|
> 字段修饰符放在access_flags项目中，与类的access_flags项目是非常类似的，都是一个u2的数据类型。

|标志名称|标志值|含义|
|-----|-----|-----|
|ACC_PUBLIC     |0x0001|字段是否public|
|ACC_PRIVATE    |0x0002|字段是否private|
|ACC_PROTECTED  |0x0004|字段是否protected
|ACC_STATIC     |0x0008|字段是否static|
|ACC_FINAL      |0x0010|字段是否final|
|ACC_VOLATILE   |0x0040|字段是否volatile|
|ACC_TRANSIENT  |0x0400|字段是否transient|
|ACC_SYNTHETIC  |0x1000|字段是否由编译器自动产生|
|ACC_ENUM       |0x4000|字段是否enum|
> 在实际情况中，ACC_PUBLIC、ACC_PRIVATE、ACC_PROTECTED标志最多只能选其一，ACC_FINAL、ACC_VOLATILE不能同时选择。接口中字段必须有ACC_PUBLIC、ACC_STATIC、ACC_FINAL标志，这些都是Java语言规则规定的。在access_flags标志后面的两项索引值:name_index和descriptor_index都是对常量池的引用，分别代表着字段的简单名称及字段和方法的描述符。
>> 全限定名：如“org//com/TestClass”是这个类的全限定名，仅仅把类全名中的"."替换成了"/"，为了使连续的多个全限定名之间不产生混淆咋使用时最后一般会加入一个";"表示结束。<p>
简单名称:指没有类型和参数修饰的方法和字段名称,如:inc()方法的简单名称为inc.<p>
描述符:是用来描述字段的数据类型、方法的参数列表(包括数量、类型以及顺序)和返回值。根据描述符规则，基本数据类型(byte、char、double、float、int、long、short、boolean)以及代表无返回值的void类型都用一个大写字符来表示.

|标识字符|含义|
|-------|-------|
|B|基本类型byte|
|C|基本类型char|
|D|基本类型double|
|F|基本类型float|
|I|基本类型int|
|J|基本类型long|
|S|基本类型short|
|Z|基本类型boolean|
|V|特殊类型void|
|L|对象类型，如Ljava/lang/Object;|
> d对于数组类型，每一唯独将使用一个前置的"["字符来描述，如"java.lang.String[][]"类型的二维数组将被记录为:"[[Ljava/lang/String;",一个整型数组"int[]"将被记录为"[I"。<p>
>> 用描述符来描述方法时，按照先参数列表后返回值的顺序描述，参数列表按照参数的严格顺序放在一组小括号"()"之内。如方法void inc()描述符为"()V",方法java.lang.String toString()描述符为"()Ljava/lang/String;"，方法int indexOf(char[] source,int sourceOffset,int sourceCount,char[] target,int targetOffset,int targetCount,int fromIndex)描述符为"([CII[CIII)I".
>> 字段表集合第一个u2类型的数据为容量计数器fields_count,第二个u2类型的数据为access_flags标志，然后是name_index和descriptor_index,在之后会跟一个属性表集合的属性表计数器等。
> 字段列表结合中不会列出从超类或父接口中继承的字段，但有可能列出原本java代码之中不存在的字段，譬如在内部类中为了保持对外部类的访问性，会自动添加指向外部类实例的字段。另外在java语言中字段是无法重载(可以继承)，两个字段的数据类型、修饰符不管是否相同，都必须使用不一样的名称，但是对字节码来讲如果两个字段的描述符不一致，那么字段重名就是合法的。

* 方法表集合
> Class文件存储格式中对方法的描述与对字段的描述几乎采用了完全一致的方式，方法表结构如同字段表一样，依次包括了访问标志(access_flags)、名称索引(name_index)、描述符索引(descriptor_index)、属性表集合(attributes)几项。这些数据项目的含义非常类似，仅在访问标志和属性表集合的可选项中有所区别。

|类型|名称|数量|
|-----|-----|-----|
|u2             |access_flags|1|
|u2             |name_index|1|
|u2             |descriptor_index|1|
|u2             |attributes_count|1|
|attribute_info |attributes|attributes_count|
> 方法表标志位

|标志名称|标志值|含义|
|-----|-----|-----|
|ACC_PUBLIC     |0x0001|方法是否为public|
|ACC_PRIVATE    |0x0002|方法是否为private|
|ACC_PROTECTED  |0x0004|方法是否为protected
|ACC_STATIC     |0x0008|方法是否为static|
|ACC_FINAL      |0x0010|方法是否为final|
|ACC_SYNCHRONIZED|0x0020|方法是否为synchronized|
|ACC_BRIDGE     |0x0040|方法是否是由编译器产生的桥接方法|
|ACC_VARARGS    |0x0080|方法是否接受不定参数|
|ACC_NATIVE     |0x0100|方法是否为native|
|ACC_ABSTRACT   |0x0400|方法是否为abstract|
|ACC_STRICT   |0x0800|方法是否为strictfp|
|ACC_SYNTHETIC  |0x1000|方法是否由编译器自动产生|
> 方法里面的Java代码经过编译器编译成字节码指令后存放在方法属性表中一个名为"Code"的属性里面，属性表是Class文件格式中最具扩展性的一种数据项目。与字段表集合相对应的，如果父类方法在子类中没有被重写(Override)，方法表集合中就不会出现来自父类的方法信息。但同样的，有可能会出现由编译器自动添加的方法，最典型的的便是类构造器"<client>"方法额实例构造器"<init>"方法
>> 在Java中重载一个方法，除了要与原方法具有相同的简单名称只亲爱，还要求必须拥有一个与眼方法不同的特征签名，特征签名就是一个方法中各个参数在常量池中的字段符号引用的集合，返回值不包含在特征签名之中。在Class文件中特征签名的范围更大，主要描述符不完全一致的两个方法可以共存。

* 属性表集合(字段表、方法表都有属性表)
> 在Class文件、字段表、方法表中都可以携带属性表(attribute_info)集合，用于描述某些场景专有的信息。<p>
>> 与Class文件中其他的数据项目要求严格的顺序、长度和内容不同，属性表集合不要求各个属性表具有严格的顺序，并且只要不与已有的属性名重复，可以向属性表中写入自定义的属性信息，JVM运行时会忽略吊不认识的属性。

|属性名称|使用位置|含义|
|---------|---------|---------|
|Code               |方法表|Java代码编译成的字节码指令|
|ConstantValue      |字段表|final关键字定义的常量值|
|Deprecated         |类、方法表、字段表|被声明为Deprecated的方法和字段|
|Exceptions         |方法表|方法抛出的异常|
|InnerClasses       |类文件|内部类列表|
|LineNumberTable    |Code属性|Java源码的行号与字节码指令的对应关系|
|LocalVariableTable |Code属性|方法的局部变量描述|
|SourceFile         |类文件|源文件名称|
|Synthetic          |类、方法表、字段表|标识方法或字段为编译器自动生成的|
> 对于每个属性，它的名称需要从常量池中引用一个CONSTANT_Utf8_info类型的常量来表示，二属性值的结构则是完全自定义的，只需要说明属性值所占用的位数长度即可:

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u2|attribute_length|1|
|u1|info|attribute_length|

* * Code属性
> 方法体重代码经过编译器处理编程字节码指令存储在Code属性内。Code属性出现在方法表属性集合中，但并非所有的方法表都必须存在这个属性，譬如接口或抽象方法就不存在Code属性。

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u4|attribute_length|1|
|u2|max_stack|1|
|u2|max_locals|1|
|u4|code_length|1|
|u1|code|code_length|
|u2|exception_table_length|1|
|exception_info|exception_table|exception_table_length|
|u2|attributes_count|1|
|attribute_info|attributes|attributes_count|

+ attribute_name_index attribute_length:是一项指向CONSTANT_Utf8_info类型常量的索引，常量值固定为"Code",它代表了该属性的属性名称，**attribute_length**指示了属性值的长度，由于属性名称索引与属性长度一共是6个字节，所以属性值的长度固定为真个属性表的长度减去6个字节。
+ max_stack: 代表操作数栈(Operand Stacks)深度的最大值。在方法执行的任意时刻，操作数栈都不会超过这个深度。VM运行时需要根据这个值来分配栈帧(Frame)中的操作栈深度。
+ max_locals: 代表了局部变量表所需要的存储空间。max_locals的单位是Slot，Slot是VM为局部变量分配内存所使用的最小单位。对于byte、char、float、int、short、boolean、reference和returnAddress等长度不超过32位的数据类型，每个局部变量占用1个Slot，double、long需要2个Slot存放。方法参数(包括实例方法中的隐藏参数this)、显示异常处理器的参数(Exception Handler Parameter即try-catch语句中catch块所定义的异常)、方法体中定义的局部变量都需要使用局部变量表来存放。编译器会根据变量的作用于来分类Slot并分配给各个变量使用，然后计算出max_locals的大小（并不是所有局部变量所占Slot之和，一个方法执行完成后其局部变量所占的Slot可以被其他局部变量使用）。
+ code_length code:用来存储Java源程序编译后生成的字节码指令。code_length代表字节码长度，code用于存储字节码指令的一系列字节流。既然名为字节码指令，则每个指令就是一个u1类型的单字节。VM读取到code中的字节码时可以超出其代表的指令、其后是否跟参数以及参数当如何理解。
> 关于code_length，虽然是一个u4类型的长度值，理论上最大可以达到2^3-1，单VM规范中限制了一个方法不允许超过65535条字节码指令，如果超过这个限制，javac编译器就会拒绝编译。<p>
Code属性是Class文件中最重要的一个属性，如果将Java程序中的信息分为代码(Code，方法体里面的代码)和元数据(Metadata,包括类、字段、方法定义及其他信息)两部分，那么真个Class文件里，Code属性用于描述代码，所有其他数据项都用于描述元数据。在任何实例方法中都可以通过"this"关键字访问到此方法所属的对象，因此在实例方法的局部变量表中至少会存在一个指向当前对象实例的局部变量，局部变量表中也会预留出第一个Slot位来存放对象实例的引用，方法参数值从1开始计算。这个处理只对实例方法有效，如果方法被声明为"static"，那么Args_size就会等于0.<p>
>> 在字节码指令之后的是这个方法的显示异常处理表集合，异常表对于Code属性来说不是必须存在的。它包含四个字段：如果字节码从第start_pc行(非源码中的行，而是相对于方法体开始的偏移量)到第end_pc行之间(不含end_pc行)出现了类型为catch_type或其子类的异常(catch_type为指向一个CONSTANT——Class_info类型常量的索引)，则转到handler_pc行继续处理。当catch_type的值为0时，代表任何的异常情况都需要转向到handler_pc处进行处理。<p>
异常表实际上是Java代码的一部分，编译器使用异常表而不是简单的跳转命令来实现Java异常及finally处理机制(1.4.2之前使用jsr、ret指令实现finally语句)。

|类型|名称|数量|
|-----|-----|-----|
|u2|start_pc|1|
|u2|end_pc|1|
|u2|handler_pc|1|
|u2|catch_type|1|
```java
public int inc() {
        int x;
        try {
            x = 1;
            return x;
        } catch (Exception e) {
            x = 2;
            return x;
        } finally {
            x = 3;
        }
    }// 如果代码没有异常输出1 异常输出2 其他则非正常退出 由于finally中结果没有推送到返回值中准备返回。如果finally中存在return x;则会返回3
```

* * Exceptions属性
> 这里的Exceptions属性是在方法表中与Code属性平级的一项属性，不是Code属性中的异常表。Exceptions属性的作用是列举出方法中可能抛出的受查异常(Checked Exceptions),也就是方法描述时在throws关键字后面刘局的异常。

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u4|attribute_length|1|
|u2|number_of_exceptions|1|
|u2|exception_index_table|number_of_exceptions|
>> * number_of_exceptions表示方法可能抛出number_of_exceptions中受查异常，每一种受查异常使用一个Exception_index_table项表示，exception_index_table是一个指向常量池中CONSTANT_Class_info类型常量的索引，代表了该受查异常的类型。

* * LineNumberTable属性
> LineNumberTable属性用于描述Java源码行号和字节码行号(字节码的偏移量)之间的对应关系。并不是运行时必须的属性，但会默认生成到Class文件之中，可以在Javac中使用-g:none或-gLkines选项来取消或要求生成这项信息。如果不生成则在程序宜昌市对战中将不会显示出错的行号，并在调试程序的时候无法按照源码来设置断点。

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u4|attribute_length|1|
|u2|line_number_table_length|1|
|line_number_info|line_number_table|line_number_table_length|
>> line_number_table是一个数量为line_number_table_length、类型为line_number_info的集合，line_number_info表包括start_pc和line_number两个u2类型的数据项，前者是字节码行号，后者是Java源码行号。

* * LocalVariableTable属性
> 用于描述栈帧中局部变量表中的变量与Java源码中定义的变量之间的关系，不是运行时必须属性，默认也不会生成到Class文件中，可以在javac中使用-g:none或-g:vars选项来取消或要求生成这项信息。如果没有所有的参数名称都将丢失，IDE可能会使用诸如org0,org1之类的占位符来代替原有的参数名，对程序运行无影响。但编写较不便，而且调试期间无法根据参数名称从上下文中获得参数值。

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u4|attribute_length|1|
|u2|local_variable_table_length|1|
|local_variable_info|local_variable_table|local_variable_table_length|
>> * local_variable项目代表了一个栈帧与源码中局部变量的关联,结构如
|类型|名称|数量|
|-----|-----|-----|
|u2|start_pc|1|
|u2|length|1|
|u2|name_index|1|
|u2|descriptor_index|1|
|u2|index|1|
>>> start_pc和length分别代表这个局部变量的声明周期开始的字节码偏移量及其作用范围覆盖的长度，两种结合起来就是这个局部变量在字节码之中的作用域范围。<p>
name_index和descriptor_index都是指向常量池中CONSTANT_Utf8_info类型常量的索引，分别代表了局部变量的名称及该局部变量的描述符。<p>
index是在栈帧局部变量表中Slot的位置。当这个变量的数据类型是64位类型时(double和long)，占用的Slot为index和index+1两个位置。
>>>> 在JDK1.5中引入泛型后新增了一个**LocalVariableTypeTable属性**，这个属性与其非常像是，仅仅是将descriptor_index替换成了字段的特征签名(Signature),对于非泛型类型来说，描述符和特征签名能描述的信息基本一致，但引入泛型之后由于描述符中泛型的参数化类型被擦出了，描述符就不能准确地描述泛型类型，因此出来了LocalVariableTypeTable属性。

* * SourceFile属性
> 用于记录生成这个Class文件的源码文件名称。该属性也是可选的，可以用Javac的-g:none或-g:source选项来关闭或要求生成这项信息。在一些特殊情况(如内部类)如果不生成该项属性，当抛出异常时，对战中将不会显示出错误代码所属文件名。

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u4|attribute_length|1|
|u2|sourcefile_index|1|
>> sourcefile_index数据项是指向常量池中CONSTANT_Utf8_info类型常量的索引，常量值是源码文件的文件名。

* * ConstantValue属性
> 作用是通知VM自动为静态变量赋值。只有被static关键字修饰的变量(类变量)才可以使用这项属性。对于非static类型的变量(实例变量)的赋值是在实例构造器<init>方法中进行的；而对于类变量，择优两种方式可以选择:赋值在类构造器<clinit>方法中进行，或者使用ConstantValue属性来赋值，由于Class文件格式的常量类型中只有基本属性和字符串相对于的字面量，所有ConstantValue的属性值只限于基本类型和String。

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u4|attribute_length|1|
|u2|constantvalue_index|1|
>> ConstantValue属性是一个定长属性，其attribute_length数据项值必须固定为2.constantvalue_index数据项代表了常量池中一个字面量常量的引用，根据字段类型不同，字面量可以是CONSTANT_Long_info、CONSTANT_Integer_info、CONSTANT_Double_info、CONSTANT_Float_info和CONSTANT_String_info长两种的一种

* * InnerClasses属性
> 用于记录内部类与宿主类之间的关联。如果一个类中定义了内部类，则编译器将会为它及其所包含的内部类生成InnerClasses属性。

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u4|attribute_length|1|
|u2|number_of_classes|1|
|inner_classes_info|inner_classes|number_of_classes|
> number_of_classes表示需要记录多少个内部类信息，每个内部类的信息都由一个inner_classes_info表进行描述。inner_classes_info表结构

|类型|名称|数量|
|-----|-----|-----|
|u2|inner_classes_info_index|1|
|u2|outer_class_info_index|1|
|u2|inner_name_index|1|
|u2|inner_class_access_flags|1|
>> inner_class_info_index和outer_class_info_index都是指向常量池中CONSTANT_Class_info类型常量的索引，分别代表了内部类和宿主类的符号引用。<p>
inner_name_index是指向常量池中CONSTANT_Utf8_info类型常量的索引，代表这个内部类的名称，如果是匿名内部类则改值为0.<p>
inner_class_access_flags是内部类的访问标志，类似类的access_flags。inner_class_access_flags标志取值

|标志名称|标志值|含义|
|-----|-----|-----|
|ACC_PUBLIC     |0x0001|内部类是否为public|
|ACC_PRIVATE    |0x0002|内部类是否为private|
|ACC_PROTECTED  |0x0004|内部类是否为protected
|ACC_STATIC     |0x0008|内部类是否为static|
|ACC_FINAL      |0x0010|内部类是否为final|
|ACC_SYNCHRONIZED|0x0020内部类是否为synchronized|
|ACC_ABSTRACT   |0x0400|内部类是否为abstract|
|ACC_SYNTHETIC  |0x1000|内部类是否由编译器自动产生|
|ACC_ANNOTATION|0x2000|内部类是否是一个注解|
|ACC_ENUM|0x4000|内部类是否是一个枚举|

* * Deprecated和Synthetic属性
> 两个属性都属于标志类型的布尔属性，只存在有或没有的区别，没有属性值的概念。
>> Deprecated用于表示某个类、字段、方法已经被程序作者定为不再推荐使用，它可以通过在代码中使用@Deprecated注释进行设置。

>> Synthetic属性代表此字段或方法并不是由Java源码直接产生的，而是由编译器自行添加的，在JDK1.5之后，标识一个类、字段、方法是编译器自动产生的，也可以设置其访问标志中ACC_SYNTHETIC标志位，其中最低那行的例子就是Bridge method。所有非用户代码产生的类、方法和字段都应当至少设置Synthetic属性和ACC_SYNTHETIC标志位中的一项，唯一例外的是实例构造器"<init>"方法和类构造器"<clinit>"方法<p>
>>> Deprecated和Synthetic结构属性

|类型|名称|数量|
|-----|-----|-----|
|u2|attribute_name_index|1|
|u4|attribute_length|1|
>>>> attribute_length数据项值碧玺为0x00000000,没有任何属性值需要设置

#### Class文件结构的发展
> Class文件的主体结构几乎没有变化，改进的都集中在在访问标志、属性表这些可扩展数据结构中。
>> JDK1.5和JDK1.6版本中共增加了10项新属性。

|属性名称|使用位置|含义|
|-----|-----|-----|
|StackMapTable|Code属性|JDK1.6中添加的属性，为了加快Class文件的校验速度，把类型校验时需要用到的相关信息直接写入到Class文件中，以前这些信息都是通过代码数据流分析得到|
|EnclosingMethod|类|JDK1.5中添加的属性，当一个类为局部类或匿名类时，可通过这个属性来声明其访问范围|
|Signature|类、方法表、字段表|JDK1.5中添加的属性，存储类、方法、字段的特征签名。JDK1.5引入引入泛型是Java语言的一个巨大进步，虽然使用了类型擦除手段以避免在字节码级别产生改变，但是元数据中的泛型信息任然需要保留下来，而这种情况下描述符在无法精确的描述泛型信息，因此添加这个特征签名属性|
|SourceDebugExtension|类|JDK1.6中添加的属性，SourceDebugExtension属性用于存储额外的调试信息。譬如在进行JSP文件调试时，无法通过Java堆栈定位到JSP文件的行号，JSR-45规范为这些非Java语言编写，却需要编译成字节码并运行在JVM中的程序提供了一个进行调试的标准机制，使用SourceDebugExtension属性就可以用于存储这个标准锁芯加入的调试信息|
|LocalVariableTypeTable|类|JDK1.5中添加的属性，作用在上文中LocalVariableTable属性类似，使用特征签名代替描述符是为了引入泛型语法之后能描述泛型参数化类型而添加|
|RuntimeInvisibleAnnotations|类、方法表、字段表|JDK1.5中添加的属性，为动态注解提供支持。RuntimeVisibleAn弄他提欧女士属性用于知名哪些注解是运行时(实际上运行时就是进行反射调用)可见的|
|RuntimeInvisibleAnnotations|类、方法表、字段表|JDK1.5中添加的属性，与RuntimeVisibleAnnotations属性作用相反，用于指明哪些注解是运行时不可见|
|RuntimeVisibleParameterAnnotation|方法表|JDK1.5中添加的属性，作用与RuntimeVisibleAnnotations属性类似，只不过作用对象为方法参数|
|RuntimeInvisibleParameterAnnotations|方法表|JDK1.5中添加的属性，作用与RuntimeInvisibleAnnotations属性类似，只不过作用对象为方法参数|
|AnnotationDefault|方法表|JDK1.5中添加的属性，用于记录注解类冤死的默认值|
> 上面这些属性大部分用于支持Java中许多新出现的语言特性，如枚举、变长参数、泛型、动态注解等。还有一些是为了支持性能改进和调试信息，如StackMapTab和SourceDebugExtension