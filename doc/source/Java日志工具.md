## [Java中常见的日志工具](https://blog.csdn.net/waitgod/article/details/78750184)
* JUL(java.util.logging.logger): jdk自带的日志系统
* Apache Commons Logging 
* Avalon LogKit
* log4j
* SLF4J
* Logback
* Log4j2

#### 使用场景
* 只使用Apache Commons Logging 
     ```text
     <dependency>
               <groupId>commons-logging</groupId>
               <artifactId>commons-logging</artifactId>
               <version>1.2</version>
           </dependency>
     ```
* Apache Commons Logging和log4j结合使用
```text
<dependency>
          <groupId>commons-logging</groupId>
          <artifactId>commons-logging</artifactId>
          <version>1.2</version>
      </dependency>
      <dependency>
          <groupId>log4j</groupId>
          <artifactId>log4j</artifactId>
          <version>1.2.17</version>
      </dependency>
```
* SLF4J结合Logback
```text
<dependency>
          <groupId>org.slf4j</groupId>
          <artifactId>slf4j-api</artifactId>
          <version>${slf4j.version}</version>
      </dependency>
      <dependency>
          <groupId>ch.qos.logback</groupId>
          <artifactId>logback-core</artifactId>
          <version>${logback.version}</version>
      </dependency>
      <dependency>
          <groupId>ch.qos.logback</groupId>
          <artifactId>logback-classic</artifactId>
          <version>${logback.version}</version>
      </dependency>
```
* 单独使用Log4j2
```text
<dependency>
          <groupId>org.apache.logging.log4j</groupId>
          <artifactId>log4j-api</artifactId>
          <version>2.6.2</version>
      </dependency>
      <dependency>
          <groupId>org.apache.logging.log4j</groupId>
          <artifactId>log4j-core</artifactId>
          <version>2.6.2</version>
      </dependency>
```