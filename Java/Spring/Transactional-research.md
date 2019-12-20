# 스프링 transactional에 대한 고찰
tag: spring, spring-boot, transaction, transactional, annotation, autocommit, datasource, oracle, jdbc,
 JTA, jtaTransactionManager, atomikos

## 1. Spring Transaction 사용법
참고: 
- http://blog.naver.com/tkstone/50192718268

Spring ​Framework 에서 제공하는 Transaction 을 사용하는 방법은 크게 다음과 같다.
1) Spring context 설정파일에서 Transaction 선언
2) Spring Transaction Annotation 을 사용한 Transaction 선언
3) Spring API 를 사용하여 프로그램 소스 상에 Transaction 구현

위의 3가지 방법 중 1) 과 2)는 Spring AOP 를 사용하는 것이고, 3)은 AOP 가 아닌 순수 Spring API 를 사용하는 방법이다.

<필요 Library>
Maven 을 사용하는 경우 기본적인 Spring Framework 외에 다음 Library 에 대한 Dependency 를 추가로 선언해야 한다.

pom.xml:
```xml
  1 <dependency>
  2     <groupId>org.springframework</groupId>
  3     <artifactId>spring-jdbc</artifactId>
  4     <version>xxxx</version>
  5 </dependency>
  6 <!-- AOP 사용 시 필요>  
  7 <dependency>
  8     <groupId>org.aspectj</groupId>
  9     <artifactId>aspectjrt</artifactId>
 10     <version>xxxx</version>
 11 </dependency>
 12 <dependency>
 13     <groupId>org.aspectj</groupId>
 14     <artifactId>aspectjweaver</artifactId>
 15     <version>xxxx</version>
 16 </dependency>
 17 <dependency>
 18     <groupId>cglib</groupId>
 19     <artifactId>cglib-nodep</artifactId>
 20     <version>xxxx</version>
 21 </dependency>
 22 <dependency>
 23     <groupId>org.springframework</groupId>
 24     <artifactId>spring-aop</artifactId>
 25     <version>xxxx</version>
 26 </dependency>
```
<Transaction 대상 프로그램>
일단 Mybatis 기반의 프로그램을 예제로 설정한다. (여기서는 Mapper interface 를 주입 받는 방식으로 구현)

TransactionInvoker.java:
```java
  1 public class TransactionInvoker {
  2     private Mapper1 mapper1;
  3  
  4     public void setMapper1(Mapper1 mapper1){
  5         this.mapper1 = mapper1;
  6     }
  7  
  8     public void transaction(){
  9         insert1();
 10         insert2();
 11     }
 12 
 13     public void insert1(){
 14         A1 a1 = new A1();
 15         a1.col1 = "col1";
 16         a1.col2 = "col2";
 17         mapper1.insertA1(a1);
 18     }
 19  
 20     public void insert2(){
 21         A2 a2 = new A2();
 22         a2.col1 = "col1";
 23         a2.col2 = "col2";
 24         mapper1.insertA2(a2);  
 25     }
 26  
 27 } // End of TransactionInvoker
 28 
```


### 1) Spring Context 를 이용한 Transaction 선언
```xml
  1 <beans xmlns="http://www.springframework.org/schema/beans"
  2  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  3  xmlns:tx="http://www.springframework.org/schema/tx"
  4  xmlns:aop="http://www.springframework.org/schema/aop"
  5  xsi:schemaLocation="http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-3.1.xsd
  6   http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
  7   http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-3.1.xsd">
  8 
  9  <bean id="dataSource1" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
 10   <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
 11   <property name="url" value="jdbc:mysql://localhost:3306/test"/>
 12   <property name="username" value="test"/>
 13   <property name="password" value="test"/>
 14  </bean>
 15  
 16  <bean id="txManager1" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
 17    <property name="dataSource" ref="dataSource1" />
 18  </bean>
 19  
 20  <tx:advice id="txAdvice" transaction-manager="txManager1">
 21   <tx:attributes>
 22    <tx:method name="transaction" propagation="REQUIRED" read-only="false"/>
 23   </tx:attributes>
 24  </tx:advice>
 25  
 26  <aop:config>
 27   <aop:pointcut id="TOperation" expression="execution(* tkstone.test.transaction.TransactionInvoker.*(..))"/>
 28   <aop:advisor advice-ref="txAdvice" pointcut-ref="TOperation"/>
 29  </aop:config>
 30 
 31 </beans>
```
- AOP 기반의 Transaction 을 사용 하려면 3,4 라인의 tx 및 aop namespace prefix 를 선언하는 것이 필요하다.
- 16 ~ 18 라인에서 TransactionManager 를 선언하였다. Mybatis - Spring 을 사용하는 경우에는 DataSourceTransactionManager 를 사용하나, 사용하는 Persistence 기술에 따라 JpaTransactionManager 나 HibernateTransactionManager 를 쓸 수 있다.
- 20 ~ 24 라인에서는 AOP 에서 사용할 Advisor 를 선언 하였다. tx prefix 를 사용했다는 것은 Spring Tranaction 에서 제공하는 내장 Advisor 를 쓴다는 것을 의미한다.
- Advisor 는 AOP의 advice (어떤 동작을 할 것인가) + pointcut (advice 적용 위치) 의 역할을 하는 Spring Utility 모듈이다.
- <tx:advice> 의 transaction-manager attribute에는 앞에서 선언한 TransactionManager 의 ID 값을 설정한다. 만일 TransactionManager 의 ID 값이 "transactionManager" 인 경우에는 생략해도 된다. 여기서는 이해를 위해 일부러 다른 이름을 설정 하였다.
- 22라인의 <tx:method> 에서는 Transaction 을 적용할 메소드 별 세부 Transaction 속성을 설정한다. 가장 중요한 속성은 propagation 값이다. 여기에 대해서는 별도의 포스팅에서 설명하도록 한다. 
- 26 ~ 29 라인에서는 AOP 설정을 한다. 여기서는 pointcut 및 advisor 를 매핑 한다. 즉 "어디서 어떤 동작을 수행하라"는 선언이다.
- 27 라인의 expression 은 AspectJ 표기법을 따른다. (execution 값에서 * 와 tkstone 사이에 공백이 있다는 것을 주의해야 한다.) 여기서는 TransactionInvoker class 의 모든 method 에 대해서 advisor를 적용한다는 의미이다.
- 28 라인에서는 Advisor 를 지정한다. 여기서는 앞의 20 ~ 24 라인에 선언한 Spring Transaction 내장 Advosor 를 사용한다고 선언한다.
- 참조 관계를 정리하면 다음과 같다.

```
AOP -> Advisor -> TransactionManager -> DataSource
         ↘ 대상 클래스
```

이제 TransactionInvoker.transaction() method 에는 Spring Transaction 기능이 적용 된다. 이것이 적용되기 위해서는 TransactionInvoker 객체를 바로 생성하는 것이 아니라 종속성 주입 (Dependency Injection) 을 받아서 호출해야 한다. 그 이유는 위의 AOP 선언에 대해서 Spring 내부적으로 TransactionInvoker 객체에 대한 Proxy 객체를 생성하고 이것을 주입해 주기 때문이다. 즉 "호출하는 Bean -> Proxy 객체 -> TransactionInvoker 객체" 의 순서로 호출이 이루어진다. 이것은 다음과 같이 확인 가능하다.

```java
System.out.println(transactionInvoker.getClass().getName());
=> TransactioInvoker 객체가 아닌 Proxy 객체 정보가 출력됨
```

### 2) Spring Transaction Annotation 을 사용한 Transaction 선언
위의 Spring context 방식의 Transaction 선언이 좀 복잡하게 느껴진다면 @Transactional Annotation 을 사용한 선언을 고려할 수 있다. (개인적으로는 이 방법을 더 선호한다.)

우선 Spring context 가 약간 바뀐다.
```java
  1 <beans xmlns="http://www.springframework.org/schema/beans"
  2  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  3  xmlns:tx="http://www.springframework.org/schema/tx"
  4  xmlns:aop="http://www.springframework.org/schema/aop"
  5  xsi:schemaLocation="http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-3.1.xsd
  6   http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
  7   http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-3.1.xsd">
  8 
  9  <bean id="dataSource1" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
 10   <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
 11   <property name="url" value="jdbc:mysql://localhost:3306/test"/>
 12   <property name="username" value="test"/>
 13   <property name="password" value="test"/>
 14  </bean>
 15  
 16  <bean id="txManager1" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
 17    <property name="dataSource" ref="dataSource1" />
 18  </bean>
 19 
 20  <tx:annotation-driven transaction-manager="txManager1"/> 
 21 </beans>
```
- 18 라인 까지는 AOP 선언 방법과 동일하다. 하지만 이후는 AOP 선언이 빠지고 20 라인의 <tx:annotation-driven> 으로 대치되었다.
- <tx:annotation-driven> 에서 transaction-manager 속성은 대상 TransactionManager 의 ID 값이다. 만일 TransactionManager 의 ID 가 "transactionManager" 인 경우에는 생략 가능하다.
- 여기에는 AOP 선언이 없지만 내부적으로는 Spring AOP 에 의해서 동작한다.
- Transaction 을 사용할 메소드에는 다음과 같이 Annotation을 설정 한다.

TransactionInvoker.java:
```java
  1 import org.springframework.transaction.annotation.Propagation;
  2 import org.springframework.transaction.annotation.Transactional;
  3 
  4 public class TransactionInvoker {
  5  private Mapper1 mapper1;
  6  
  7  public void setMapper1(Mapper1 mapper1){
  8   this.mapper1 = mapper1;
  9  }
 10  
 11  @Transactional(propagation = Propagation.REQUIRES_NEW)
 12  public void transaction(){
 13   insert1();
 14   insert2();
 15  }
 16 
 17  public void insert1(){
 18   A1 a1 = new A1();
 19   a1.col1 = "col1";
 20   a1.col2 = "col2";
 21   mapper1.insertA1(a1);
 22  }
 23  
 24  public void insert2(){
 25   A2 a2 = new A2();
 26   a2.col1 = "col1";
 27   a2.col2 = "col2";
 28   mapper1.insertA2(a2);  
 29  }
 30 } // End of TransactionInvoker
```

위의 프로그램에서는 11라인의 @Transactional annotation 가 추가 되었다. 이렇게 하면 앞서 설명한 Spring context 방식과 동일한 기능을 수행한다. 물론 TransactionInvoker 를 사용하는 Bean에서는 전혀 변경할 사항이 없다.
Spring API 를 이용하여 프로그램 방식으로 Transaction 을 구현하는 방법은 별도 포스팅에서 설명 하도록 하겠다.

일단 Spring AOP 를 이용한 Transaction 구현의 특징은 다음과 같다.
1) Transaction 단위는 method 이다. (Spring AOP 의 특징)
2) 외부에서 호출하는 method 에 대해서만 Transaction 이 설정 된다. 
    위의 예에서는 
    "호출하는 Bean 에서 TransactionInvoker.transaction() 호출 -> Proxy.transaction() -> TransactionInvoker.tranaction() -> TransactionInvoker.insertA1(), insertA2()" 의 순서로 동작한다.
    
    예를 들면 다음의 경우에는 Transaction 이 적용 되지 않는다.
    ```java
      1 public class TransactionInvoker {
      2  
      3  public void transaction(){
      4   insert1();
      5   insert2();
      6  }
      7 
      8  @Transactional(propagation = Propagation.REQUIRES_NEW)
      9  public void insert1(){
     10   A1 a1 = new A1();
     11   a1.col1 = "col1";
     12   a1.col2 = "col2";
     13   mapper1.insertA1(a1);
     14  }
     15  
     16  @Transactional(propagation = Propagation.REQUIRES_NEW)
     17  public void insert2(){
     18   A2 a2 = new A2();
     19   a2.col1 = "col1";
     20   a2.col2 = "col2";
     21   mapper1.insertA2(a2);  
     22  }
     23 } // End of TransactionInvoker
     24 
     25 ...
     26 
     27 // snippet from Transaction Consumer
     28 public void someMethod(){ 
     29     transactionInvoker.transaction();
     30 }
    ```
3) Transaction 대상 객체 참조는 종속성 주입을 통해서 얻어야 한다. (직접 객체를 생성하면 안된다는 의미임) 


## 2. TransactionTemplate 을 이용한 Spring Transaction 사용
참고: 
- http://blog.naver.com/tkstone/50192724315

앞서 Spring AOP 를 이용한 Transaction 사용법을 설명 하였다. 특히 @Transactional 을 사용한 Transaction 선언이 편리하기는 하나 다음과 같은 경우에는 동작을 하지 않는다.
```java
  1 public class TransactionInvoker2 {
  2  
  3  private A1Dao a1dao;
  4  private A2Dao a2dao;
  5 
  6  public void setA1dao(A1Dao dao){
  7   this.a1dao = dao;
  8  }
  9  
 10  public void setA2dao(A2Dao dao){
 11   this.a2dao = dao;
 12  }
 13  
 14  // 외부에서 호출하는 method
 15  public void invoke() throws Exception{
 16   doInternalTransaction();
 17  }
 18  
 19  @Transactional
 20  public void doInternalTransaction() throws Exception{
 21   a1dao.insertA1();
 22   a2dao.insertA2();
 23  }
 24 }
```
위의 프로그램에 Spring Transaction 이 적용되지 않는 이유는 앞의 포스팅에서 언급 했듯이 Proxy 방식으로 동작하기 때문이다. 여기서 invoke() 가 호출하는 대상 method 는 Proxy 의 doInternalTransaction() 이 아닌 실제 doInternalTransaction() 이다. Proxy 는 클래스 외부에서 호출하는 경우에만 동작 한다.

그러면 invoke() 에 @Transactional 을 설정하는 것을 고려할 수 있으나 다음 문제가 발생한다.

- Spring Transaction 은 method 단위로 동작 한다. 이것은 Method 시작 시점에 DB Connection 객체를 얻고 Method 종료 시점에 commit 후 DB Connection 을 반납한다는 것을 의미한다.
- 따라서 처리 시간이 긴 method 인 경우에는 불필요하게 오랫동안 DB Connection 을 점유하게 된다.
- 또한 DB Lock 이 유지되는 시간이 길어진다. (DBMS 종류에 따라 이 문제가 심각한 경우가 있다)

따라서 위와 같은 유형의 프로그램에서는 개발자가 Transaction 의 시작 및 종료 시점을 결정할 필요가 있다. 이것을 위해서 Spring 에서는 TransactionTemplate을 이용하는 방법을 제공한다.
```java
  1 import org.springframework.transaction.PlatformTransactionManager;
  2 import org.springframework.transaction.support.TransactionTemplate;
  3 import org.springframework.transaction.TransactionDefinition;
  4 import org.springframework.transaction.support.TransactionCallbackWithoutResult;
  5 import org.springframework.transaction.TransactionStatus;
  6 
  7 public class TransactionInvoker2 {
  8  
  9  private A1Dao a1dao;
 10  private A2Dao a2dao;
 11  private TransactionTemplate transactionTemplate;
 12 
 13  public void setA1dao(A1Dao dao){
 14   this.a1dao = dao;
 15  }
 16  
 17  public void setA2dao(A2Dao dao){
 18   this.a2dao = dao;
 19  }
 20  
 21  public void setTransactionManager(PlatformTransactionManager transactionManager){
 22   this.transactionTemplate = new TransactionTemplate(transactionManager);
 23   this.transactionTemplate.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRED);
 24  }
 25  
 26  public void invoke() throws Exception{
 27   doInternalTransaction();
 28  }
 29  
 30  private void doInternalTransaction() throws Exception{
 31   transactionTemplate.execute(new TransactionCallbackWithoutResult(){
 32    public void doInTransactionWithoutResult(TransactionStatus status){
 33     try{
 34      a1dao.insertA1();
 35      a2dao.insertA2();
 36     }
 37     catch(Exception e){
 38      status.setRollbackOnly();
 39     }
 40     return;
 41    }
 42   });
 43  }
 44 }
```
- 21 라인에서 Spring에서 TransactionManager 를 주입 받는다. 이 때 TransactionTemplate 을 생성 및 Transaction 속성을 설정한다. (실제로 Transaction 을 실행하는 부분에서 처리해도 무방하다.)
- 30 ~ 43 라인에서는 TransactionTemplate.execute() 내에서 로직을 실행한다.


위의 Bean 이 동작하기 위해서 Spring context 에 다음과 같이 선언해야 한다.
```xml
  1 <bean id="TransactionInvoker4" class="tkstone.test.transaction.TransactionInvoker4">
  2     <property name="a1dao" ref="a1dao"/>
  3     <property name="a2dao" ref="a2dao"/>
  4     <property name="transactionManager" ref="txManager1"/>
  5 </bean> 
```
여기서 TransactionManager 를 선언하는 방법은 앞의 글 (Spring Transaction) 을 참조하기 바란다.

시중에 나온 Spring 관련 서적에서는 Business Logic 과 Transaction 의 분리 필요성을 언급하고 있다. 대부분의 경우에는 올바른 접근 방법이다. 그러나 DB transaction 이 아주 중요한 서비스에서는 Business logic 구현 시 Transaction을 같이 고려해야 한다. 특히 DBMS 종류에 따른 Lock 지속 시간이나 Read consistency 차이 및 이로 인한 서비스 동시성 문제, 처리 성능이 문제 되는 경우에는 위와 같이 프로그램에 의한 Transaction 조정이 필요하다.




## 3. Spring Transaction 내부 동작 메커니즘 (중요) 
참고:
- http://blog.naver.com/tkstone/50193135886

Mybatis 와 같은 DB 연동 라이브러리를 사용해서 DB에 연동할 때 Spring Transaction 을 사용하는 경우와 개발자가 직접 Transaction 을 관리하는 2가지 경우가 있다. 이 경우 내부적으로 어떻게 동작하는지 차이점을 알면 대용량 트랜젝션 처리에 대비를 할 수 있다. 세부적인 동작을 알기 위해 다음 샘플 프로그램을 실행해 보자.

Spring 및 Mybatis 내부 동작을 파악하기 위한 Log level 설정:
```xml
  1 <?xml version="1.0" encoding="UTF-8"?> 
  2 <!DOCTYPE log4j:configuration PUBLIC "-//APACHE//DTD LOG4J 1.2//EN" "log4j.dtd"> 
  3 <log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/"> 
  4  
  5     <!-- Appenders --> 
  6     <appender name="console" class="org.apache.log4j.ConsoleAppender"> 
  7         <param name="Target" value="System.out" /> 
  8         <layout class="org.apache.log4j.PatternLayout"> 
  9             <param name="ConversionPattern" value="%-5p: %c - %m%n" /> 
 10         </layout> 
 11     </appender> 
 12      
 13     <logger name="org.springframework.jdbc"> 
 14         <level value="debug" /> 
 15     </logger> 
 16  
 17     <logger name="org.springframework.transaction"> 
 18         <level value="debug" /> 
 19     </logger> 
 20      
 21     <logger name="java.sql"> 
 22         <level value="debug" /> 
 23     </logger> 
 24          
 25     <logger name="java.sql.Connection"> 
 26         <level value="debug" /> 
 27     </logger>     
 28      
 29     <logger name="java.sql.Statement"> 
 30         <level value="debug" /> 
 31     </logger>     
 32      
 33     <logger name="org.mybatis"> 
 34         <level value="debug" /> 
 35     </logger>         
 36  
 37     <!-- Root Logger --> 
 38     <root> 
 39         <priority value="info" /> 
 40         <appender-ref ref="console" /> 
 41     </root> 
 42      
 43 </log4j:configuration> 
 44 
```

Mybatis 기반의 DB 연동 프로그램 - **Spring Transaction 을 사용하지 않는 경우**:
```java
  1 package tkstone.test.transaction; 
  2  
  3 public class TransactionInvoker {
  4     private Mapper1 mapper1; 
  5      
  6     public void setMapper1(Mapper1 mapper1){ 
  7         this.mapper1 = mapper1; 
  8     } 
  9      
 10     public String invoke(){ 
 11         System.out.println("*** invoke start"); 
 12         insert1(); 
 13         insert2(); 
 14         System.out.println("*** invoke end"); 
 15         return "transaction invoked"; 
 16     } 
 17  
 18     public void insert1(){ 
 19         A1 a1 = new A1(); 
 20         a1.col1 = "col1"; 
 21         a1.col2 = "col2"; 
 22         mapper1.insertA1(a1); 
 23     } 
 24      
 25     public void insert2(){ 
 26         A2 a2 = new A2(); 
 27         a2.col1 = "col1"; 
 28         a2.col2 = "col2"; 
 29         mapper1.insertA2(a2);         
 30     } 
 31 } // End of TransactionInvoker 
 32 
```

Mybatis 기반의 DB 연동 프로그램 - **Spring Transaction 을 사용하는 경우**:
```java
  1 ... 
  2     @Transactional 
  3     public String invoke(){ 
  4         System.out.println("*** invoke start"); 
  5         insert1(); 
  6         insert2(); 
  7         System.out.println("*** invoke end"); 
  8         return "transaction invoked"; 
  9     } 
 10 ...
```
여기서는 설명의 편의를 위해 Mybatis 나 Spring 설정을 모두 생략 하였다. 위의 2가지 프로그램을 실행했을 경우 출력 로그는 다음과 같다. (설명의 편의를 위해 일부 로그는 생략함)

Spring transaction 을 사용하지 않았을 경우
```
*** invoke start
DEBUG: org.mybatis.spring.SqlSessionUtils - Creating a new SqlSession
DEBUG: org.springframework.jdbc.datasource.DataSourceUtils - Fetching JDBC Connection from DataSource
DEBUG: org.mybatis.spring.transaction.SpringManagedTransaction - JDBC Connection [jdbc:mysql://localhost:3306/test, UserName=test@localhost, MySQL Connector Java] will not be managed by Spring
DEBUG: org.mybatis.spring.SqlSessionUtils - Closing non transactional SqlSession 
DEBUG: org.springframework.jdbc.datasource.DataSourceUtils - Returning JDBC Connection to DataSource
DEBUG: org.mybatis.spring.SqlSessionUtils - Creating a new SqlSession
DEBUG: org.springframework.jdbc.datasource.DataSourceUtils - Fetching JDBC Connection from DataSource
DEBUG: org.mybatis.spring.transaction.SpringManagedTransaction - JDBC Connection [jdbc:mysql://localhost:3306/test, UserName=test@localhost, MySQL Connector Java] will not be managed by Spring
DEBUG: org.mybatis.spring.SqlSessionUtils - Closing non transactional SqlSession 
DEBUG: org.springframework.jdbc.datasource.DataSourceUtils - Returning JDBC Connection to DataSource
*** invoke end
```
위의 로그를 보면 다음과 같은 특징이 있다.

- insert1() 이 호출 될 때 DB connection 을 얻어 와서 SQL을 실행한 후 DB connection 을 반환한다.
- insert2() 이 호출될 때 동일한 동작을 반복한다.
- insert1()과 insert2()는 Mybatis SqlSession 객체 및 DB Transaction을 공유하지 않는다.
- DB connection 은 auto commit mode 이므로 별도의 commit 이 발생하지 않는다.


반면 Spring transaction 을 사용했을 경우에는 로그 출력값이 바뀐다.
```
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Creating new transaction 
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Acquired Connection for JDBC transaction
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Switching JDBC Connection to manual commit

*** invoke start
DEBUG: org.mybatis.spring.SqlSessionUtils - Creating a new SqlSession
DEBUG: org.mybatis.spring.SqlSessionUtils - Registering transaction synchronization for SqlSession
DEBUG: org.mybatis.spring.transaction.SpringManagedTransaction - JDBC Connection will be managed by Spring
DEBUG: org.mybatis.spring.SqlSessionUtils - Releasing transactional SqlSession 
DEBUG: org.mybatis.spring.SqlSessionUtils - Fetched SqlSession from current transaction
DEBUG: org.mybatis.spring.SqlSessionUtils - Releasing transactional SqlSession 
*** invoke end

DEBUG: org.mybatis.spring.SqlSessionUtils - Transaction synchronization committing SqlSession 
DEBUG: org.mybatis.spring.SqlSessionUtils - Transaction synchronization deregistering SqlSession 
DEBUG: org.mybatis.spring.SqlSessionUtils - Transaction synchronization closing SqlSession 
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Initiating transaction commit
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Committing JDBC transaction on Connection 
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Releasing JDBC Connection after transaction
DEBUG: org.springframework.jdbc.datasource.DataSourceUtils - Returning JDBC Connection to DataSource
```
위의 로그를 보면 Spring TransactionManager (DatasSourceTransactionManager)가 Transaction 관리를 하는 것을 알 수 있다. 

여기서 중요한 특징은 다음과 같다. 
- invoke() method 가 시작되기 전에 DB Connection 을 얻어 와서 Autocommit = false 설정을 한다.
- invoke() method 내에서는 하나의 Mybatis SqlSession 객체를 사용해서 insert1() 및 insert2() 를 실행한다. 즉 2개의 insert 가 실행될 때 동일한 DB Connection 을 사용한다.
- invoke() method 가 실행된 이후 Transaction 을 commit 하고 connection 을 반환한다.

여기서 Transaction 이 시작하는 지점은 invoke() 메소드에 대한 Proxy method 내부이다. 따라서 다음과 같이 호출 된다. 

호출 Bean -> Proxy.invoke() 시작 -> Transaction 시작 -> TransactionInvoker.invoke() 처리 완료 -> Transaction commit -> Proxy.invoke() 종료 

위의 로그를 보면 Spring Transaction(AOP 방식인 경우)에 대한 다음과 같은 시사점을 얻을 수 있다.

1. Transaction 은 method 단위로 관리 된다. => method 가 끝날 때까지 commit 또는 connection 반환이 이루어지지 않는다.
2. Transaction 대상 method 내에서 발생하는 SQL 은 동일한 Connection 을 사용한다. (Propagation 정책에 따라 별도 Connection 사용 가능)

따라서 처리 시간이 긴 method 의 경우에는 Transaction 단위를 조정해서 DB Lock 지속시간이 지나치게 길어지거나 DB connection pool 이 모자라지 않도록 해야 한다.


## 4. Spring Transaction propagation mode에 따른 내부 동작 메커니즘 (중요)
출처:
http://blog.naver.com/tkstone/50193141378

Spring transaction 선언 시 propagation mode 를 설정할 수 있다. 예를 들면 다음과 같다.

@Transactional(propagation = Propagation.REQUIRES_NEW)

propagation 을 설정하지 않으면 default 값은 `REQUIRED` 이다.

이 포스팅에서는 설정 가능한 값 중 가장 많이 사용 하는 `REQUIRES_NEW` 와  `REQUIRED` 의 차이점을 설명 한다.

- REQUIRED : 실행 중인 Transaction context 가 있으면 해당 Transaction 내에서 실행하고, 없으면 새로운 Transaction 생성
- REQUIRES_NEW : 기존에 실행 중인 Transaction 유무와 상관 없이 무조건 새로운 Transaction 생성 

대부분의 책에서 위의 수준으로 언급하고 있으나, 실제로 제대로 동작하기 위해서 고려해야 할 내용은 언급하고 있지 않다. 다음은 여기에 대해 시행 착오를 거친 내용이다.

예를 들어 insert1(), insert2() 를 차례대로 실행하는 경우 하나의 transaction 으로 처리하고 싶어서 다음과 같이 설정해 보았다.
```java
  1     @Transactional(propagation = Propagation.REQUIRED) 
  2     public void insert1(){ 
  3         A1 a1 = new A1(); 
  4         a1.col1 = "col1"; 
  5         a1.col2 = "col2"; 
  6         mapper1.insertA1(a1); 
  7     } // End of insert1() 
  8  
  9     @Transactional(propagation = Propagation.REQUIRED) 
 10     public void insert2(){ 
 11         A2 a2 = new A2(); 
 12         a2.col1 = "col1"; 
 13         a2.col2 = "col2"; 
 14         mapper1.insertA2(a2);         
 15     } // End of insert2()
``` 

위의 method를 호출하는 Bean에서는 다음과 같이 호출하도록 구현하였다.
```java
  1 public void someMethod(){ 
  2         targetBean.insert1(); 
  3         targetBean.insert2(); 
  4 }
```

그러나 위와 같이 실행 했을 경우 로그를 살펴 보면 원하는 형태로 실행되지 않았다.
```
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Creating new transaction with name [tkstone.test.transaction.TransactionInvoker.insert1]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT; ''
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Acquired Connection [jdbc:mysql://localhost:3306/test, UserName=test@localhost, MySQL Connector Java] for JDBC transaction
...
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Committing JDBC transaction on Connection 
...
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Creating new transaction with name [tkstone.test.transaction.TransactionInvoker.insert2]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT; ''
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Acquired Connection [jdbc:mysql://localhost:3306/test, UserName=test@localhost, MySQL Connector Java] for JDBC transaction
...
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Committing JDBC transaction on Connection 
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Releasing JDBC Connection [jdbc:mysql://localhost:3306/test, UserName=test@localhost, MySQL Connector Java] after transaction
...
```

위의 로그에서 보면 insert1() 과 insert2()가 별도의 Transaction 으로 실행 되었음을 할 수 있다. 여기에 대한 해법은 다음과 같다.


Transaction context를 관리하는 중간 클래스 추가:
```java
  1 package tkstone.test.transaction; 
  2  
  3 import org.springframework.transaction.annotation.Propagation;
  4 import org.springframework.transaction.annotation.Transactional;
  5  
  6 public class TransactionGateway {
  7     private TransactionInvoker invoker; 
  8      
  9     public void setTransactionInvoker(TransactionInvoker invoker){ 
 10         this.invoker = invoker; 
 11     }     
 12  
 13     @Transactional(propagation = Propagation.REQUIRED)
 14     public void invoke(){ 
 15         this.invoker.insert1(); 
 16         this.invoker.insert2(); 
 17     } 
 18 } 
 19 
```
~~기존 클래스에 Gateway method를 추가하지 않고 새로운 클래스를 생성한 이유는 Spring Transaction 이 Proxy 로 동작하기 때문에 외부에서 호출하는 경우에만 @Transactional 이 동작하기 때문이다.~~ 
(주: 기존 클래스에 Gateway method 를 추가해서 호출해도 된다. 테스트완료, 외부에 호출될 메소드는 @transactional을 붙여줘야 한다.)


호출하는 Bean 수정:
```java
  1 public void someMethod(){ 
  2     this.transactionGateway.invoke(); 
  3 }
```

위와 같이 수정한 후 실행하면 원래 의도한 Propagation 정책이 적용 되었음을 알 수 있다.
```
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Creating new transaction with name [tkstone.test.transaction.TransactionGateway.invoke]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT; ''
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Acquired Connection for JDBC transaction
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Switching JDBC Connection to manual commit
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Participating in existing transaction
DEBUG: org.mybatis.spring.SqlSessionUtils - Creating a new SqlSession
DEBUG: org.mybatis.spring.SqlSessionUtils - Registering transaction synchronization for SqlSession 
DEBUG: org.mybatis.spring.SqlSessionUtils - Releasing transactional SqlSession 
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Participating in existing transaction
DEBUG: org.mybatis.spring.SqlSessionUtils - Fetched SqlSession 
DEBUG: org.mybatis.spring.SqlSessionUtils - Releasing transactional SqlSession 
DEBUG: org.mybatis.spring.SqlSessionUtils - Transaction synchronization committing SqlSession 
DEBUG: org.mybatis.spring.SqlSessionUtils - Transaction synchronization deregistering SqlSession 
DEBUG: org.mybatis.spring.SqlSessionUtils - Transaction synchronization closing SqlSession 
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Initiating transaction commit
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Committing JDBC transaction on Connection 
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Releasing JDBC Connection after transaction
DEBUG: org.springframework.jdbc.datasource.DataSourceUtils - Returning JDBC Connection to DataSource 
```
위에서 보면 TransactionGateway에서 새로운 Transaction이 시작 되고 insert1()과 insert2() 에서는 "Participating in existing transaction"이라는 메세지와 함께 기존 Transaction 내에서 SQL 을 실행하고 있다

여기서 알 수 있는 점은 다음과 같다.

Propagation 정책은 transaction 이 선언된 method 내에서 transaction이 선언된 다른 method를 호출할 때 적용된다.
(주: 기본 @transactional(propagation = Propagation.REQUIRED) 로 선언된다. Aservice.insert() 에서 Bservice.get() 를 
     호출하려면 Bservice.get() 에 명시적으로 `@transactional(propagation = Propagation.REQUIRED_NEW)`로 선언되어있지
     않으면(또는 @Transactional를 선언하지 않았다면) 기본값(Propagation.REQUIRED)으로 동작하는 것으로 보인다.) 

여기서 insert2()의 정책을 REQUIRES_NEW 로 변경 하면 다음과 같이 실행 된다.
```
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Creating new transaction with name [tkstone.test.transaction.TransactionGateway.invoke]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT; ''
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Acquired Connection for JDBC transaction
...
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Suspending current transaction, creating new transaction with name [tkstone.test.transaction.TransactionInvoker.insert2]
...
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Acquired Connection for JDBC transaction
...
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Committing JDBC transaction on Connection 
...
DEBUG: org.springframework.jdbc.datasource.DataSourceTransactionManager - Committing JDBC transaction on Connection 
...
```
위의 로그 내용은 크게 다음과 같이 구성 되어 있다.

1) TransactionGateway 에서 Transaction 시작 (T1)
2) insert1() 에서는 기존 Transaction 내에서 실행
3) insert2() 에서는 새로운 Transaction 시작(T2) (Suspending current transaction, creating new transaction with ~) 이것을 위해 새로운 DB Connection 을 맺음
4) insert2() 에 대해서 commit 수행 (T2)
5) TransactionGateway 실행 완료 시 commit 수행 (T1)

대부분의 경우에는 REQUIRED로 충분하나 간혹 REQUIRES_NEW를 통해 새로운 Transaction 을 생성하고자 하는 경우에는 위와 같이 동작함을 이해해야 한다.


## 5. :star2: 분산 트랜젝션 처리 (multi Transaction)
위에서 하나의 Connection에서(하나의 Database) 안에서 Transaction을 처리하는 로직에 대한 설명을 했다.
그러나 실운영에선 한개의 database를 사용하는 경우는 거의 없다고 봐야한다. 다수의 database를 이용하거나 또는 
서로 다른 Database들을 이용해 비즈니스 로직이 들어가기 때문에 single Transaction은 거의 사용할 일이 없다고 생각한다.


### 그렇다면 Multi Transaction은 어떻게 진행되어야 할까? 
couponServiceImpl: 
```java
  0 @Transactional
  1 public void downloadCoupon() throws Exception{ 
  2         int result1 = userMapper.update();
  3         int result2 = couponMapper.insert();
  4         if(result1+result2 == 2){
  5             throw new RuntimeException();
  6         }
  7 }
```
위 소스에서 우리가 기대하는 결과는 result1=1, result2=1 이 되어 result1+result2=2가 되어 throw new RuntimeException()을 일으키고,
`2라인`, `3라인`이 rollback이 되는 결과를 예상할 것이다. 
하지만 위 셋팅에서 그대로 테스트를 진행했다면 2라인, 3라인 중에 둘중에 하나만 rollback을 진행할 것이다. 

왜 둘중 하나만? 그리고 하나는 왜 rollback이 진행될까? 
이는 위에서 설명한 Spring에서 제공하는 @Transactional 에 대한 이해가 필요하다.

0라인에 선언된 `@Transactional`은 기본적으로 생략된 속성 값이 있다. `transactionManager` 이 값이 생략되어있고 이 값은
`@primary` 로 선언된 "transactionManager" Bean이 자동으로 들어간다.

즉, userMapper, couponMapper 이 사용하는 Datasource config 설정하는 파일중에 `@primary` 로 선언된 `transactionManager` bean이 
자동으로 들어간다.(그렇기 때문에 Spring-boot에서 다중 DataSouce config 셋팅할때 어느 한쪽에 반드시 `@primary` 값을 설정하라고 메시지가 나온다.)

### 적용방법
참고 : 
- https://supawer0728.github.io/2018/03/22/spring-multi-transaction/#comment-4596136323 (매우 잘 설명되어있다.)

다중 Transaction 처리 하는 방법에는 두가지 정도의 방법이 있다.
- spring-data-commons의 `ChainedTransactionManager` 이용
- `JtaTransactionManager` 이용 (체택)

이중 `JtaTransactionManager` 로 구현해보았고 매우 잘 처리되고 표준으로 제공되는 라이브러리이니 이것을 구현하는 방법을 설명한다.

### JtaTransactionManager
JTA(Java Transaction Api)는 자바 표준으로써, 분산 transaction을 가능하게 해준다. 매우 간단하게 설명하자면, JTA를 지원하는 자원(XA Resource 인터페이스의 구현체들)을 등록하면, 해당 구현체들에 대해서 전역 transaction을 지원해준다. 때문에 어떤 자원이든 transaction을 지원할 수 있도록 정의한 셈인데, DataSource, JMS 외에는 쓰고 있는 곳이 없는 것 같다.

Java EE Application Server에서는 전역 tranction을 지원하기 위해서, JTA를 사용하기도 한다. Spring에서는 JNDI에서 Java EE Container가 사용 중인 DataSource를 가져와, JtaTransactionManager에 설정할 수도 있다.

#### 1. 의존성 추가
`atomikos` 모듈을 사용한다.  JTA 인터페이스를 구현한 오픈소스에는 다음과 같은 프로젝트가 있다.
- Atomikos
- Bitronix
- Narayana

pom.xml:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jta-atomikos</artifactId>
</dependency>
``` 
또는 grandle
```groovy
dependencies {
    compile('org.springframework.boot:spring-boot-starter-jta-atomikos')
}
```

#### 2. DataSource Config 설정

DatabaseConfigCommon:
```java
package com.api.config;

import java.util.Properties;

import javax.sql.DataSource;

import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.SqlSessionTemplate;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.jta.atomikos.AtomikosDataSourceBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;

import oracle.jdbc.xa.client.OracleXADataSource;

@Configuration
@MapperScan(basePackages = { "com.api.mapper.common" }, sqlSessionFactoryRef = "commonSqlSessionFactory")
public class DatabaseConfigCommon {
    @Autowired
    private Environment environment;

    @Bean
    public DataSource commonDataSource() {
        /**
         * 분상처리를 위한 Datasource 셋팅
         */
        AtomikosDataSourceBean dataSource = new AtomikosDataSourceBean();
        //XA 처리를 위한 MySQL 드라이버 변경: AtomikosDataSourceBean은 XADataSource 인터페이스를 참조하고 있다.
        //System.out.println("OracleXADataSource.class.getCanonicalName() = "+OracleXADataSource.class.getCanonicalName());
        dataSource.setXaDataSourceClassName(environment.getRequiredProperty("COMMON.driverClassName"));
        //XA 리소스를 식별할 고유 이름을 지정한다. 각 데이터소스별 고유한 값을 지정해도 되고 url이 각각 다르다면 식별 가능한 url로 지정해도 무방하다.
        dataSource.setUniqueResourceName("commonDataSource");
        dataSource.setMaxPoolSize(environment.getRequiredProperty("COMMON.maxActive", Integer.class));
        dataSource.setMinPoolSize(environment.getRequiredProperty("COMMON.minIdle", Integer.class));
        
        Properties xaProperties = new Properties();
        xaProperties.setProperty("user", environment.getRequiredProperty("COMMON.username"));
        xaProperties.setProperty("password", environment.getRequiredProperty("COMMON.password"));
        xaProperties.setProperty("URL", environment.getRequiredProperty("COMMON.url"));
        dataSource.setXaProperties(xaProperties);
        return dataSource;
    }

    @Bean
    public SqlSessionFactory commonSqlSessionFactory(@Qualifier("commonDataSource") DataSource dataSource) throws Exception {
        final SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);
        
        PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        sessionFactory.setMapperLocations(resolver.getResources("classpath:mapper/common/**/*-query.xml"));
        sessionFactory.setTypeAliasesPackage("com.api");
        return sessionFactory.getObject();
    }

    @Bean
    public SqlSessionTemplate commonSqlSessionTemplate(@Qualifier("commonSqlSessionFactory") SqlSessionFactory sqlSessionFactory) throws Exception {
        final SqlSessionTemplate sqlSessionTemplate = new SqlSessionTemplate(sqlSessionFactory);
        return sqlSessionTemplate;
    }
}
```

DatabaseConfigTravel:
```java
package com.api.config;

import java.util.Properties;

import javax.sql.DataSource;

import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.SqlSessionTemplate;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.jta.atomikos.AtomikosDataSourceBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;

import oracle.jdbc.xa.client.OracleXADataSource;

@Configuration
@MapperScan(basePackages = { "com.api.mapper.travel" }, sqlSessionFactoryRef = "travelSqlSessionFactory")
public class DatabaseConfigTravel {
    @Autowired
    private Environment environment;

    @Bean
    public DataSource travelDataSource() {
        /**
         * 분산처리를 위한 Datasource 셋팅
         */
        AtomikosDataSourceBean dataSource = new AtomikosDataSourceBean();
        //XA 처리를 위한 MySQL 드라이버 변경: AtomikosDataSourceBean은 XADataSource 인터페이스를 참조하고 있다.
        dataSource.setXaDataSourceClassName(environment.getRequiredProperty("TRAVEL.driverClassName"));
        //XA 리소스를 식별할 고유 이름을 지정한다. 각 데이터소스별 고유한 값을 지정해도 되고 url이 각각 다르다면 식별 가능한 url로 지정해도 무방하다.
        dataSource.setUniqueResourceName("travelDataSource");
        dataSource.setMaxPoolSize(environment.getRequiredProperty("TRAVEL.maxActive", Integer.class));
        dataSource.setMinPoolSize(environment.getRequiredProperty("TRAVEL.minIdle", Integer.class));
        
        Properties xaProperties = new Properties();
        xaProperties.setProperty("user", environment.getRequiredProperty("TRAVEL.username"));
        xaProperties.setProperty("password", environment.getRequiredProperty("TRAVEL.password"));
        xaProperties.setProperty("URL", environment.getRequiredProperty("TRAVEL.url"));
        dataSource.setXaProperties(xaProperties);
        return dataSource;
    }

    @Bean
    public SqlSessionFactory travelSqlSessionFactory(@Qualifier("travelDataSource") DataSource dataSource) throws Exception {
        final SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);

        PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        sessionFactory.setMapperLocations(resolver.getResources("classpath:mapper/travel/**/*-query.xml"));
        sessionFactory.setTypeAliasesPackage("com.api");
        return sessionFactory.getObject();
    }

    @Bean
    public SqlSessionTemplate travelSqlSessionTemplate(@Qualifier("travelSqlSessionFactory") SqlSessionFactory sqlSessionFactory) throws Exception {
        final SqlSessionTemplate sqlSessionTemplate = new SqlSessionTemplate(sqlSessionFactory);
        return sqlSessionTemplate;
    }

}
```
`transactionManager` 만들지 않았다는것이 중요하다. 만약 `TransactionManager`를 구현해놨었다면,
정상적으로 올라가지 않을 뿐더러 올라가더라도 다중 Transaction을 기대할 수 없다. 



## :bomb: troubleshooting
### 1. Srping-boot Transactional is not working
**3가지만 명심하자**
- Transaction 할 method 에 @transactional 달아주자 (service 또는 serviceImpl 둘중에 아무대나 걸어도 되는데 보기 쉽게 impl에 걸자)
- **다수의 Datasource 을 셋팅(다수 TrasactionManager 를 셋팅)한 경우 @transactional(transactionManager = "travelTransactionManager") `transactionManager`은 꼭 명시하자**
    - 직 경험담을 얘기 하자면 명시안할 경우 @primary 로 선언된 connection을 setAutoCommit하고 rollback 처리한다. 
    만약 다른 connection에서 update를 진행하는 거라면 rollback이 정상적으로 되지 않는다.   
- @transactional은 외부에서 호출할 경우에만 걸린다. 내부에서 호출할 경우엔 안먹는다. 
    - 무슨얘기냐 Acontroller 에서 Bservice.doInsert() 호출 할 경우, spring은 내부적으로 AOP 를 이용해
      Acontroller -> AOP transaction -> Bservice.doInsert()를 호출한다.
    
    - 내부에서 Acontroller -> Bservice.doTwiceInsert() ( Bservice.doInsert();  Bservice.doInsertOther(); ) 호출할 경우
      Bservice.doTwiceInsert()에 @transactional 이 안걸려 있다면 Transaction이 발생하지 않는다는 말이다

참고자료
- http://blog.naver.com/tkstone/50192718268 (Spring Transaction 사용법)
- http://blog.naver.com/tkstone/50193135886 (Spring Transaction 내부 동작 메커니즘)
- http://blog.naver.com/tkstone/50192724315 (TransactionTemplate 을 이용한 Spring Transaction 사용)

### 2. 분산 데이터베이스 환경 Datasource 간에 Transaction 해결하기
참고:
- https://supawer0728.github.io/2018/03/22/spring-multi-transaction/ (ChainedTransactionManager, JTA 예제)
