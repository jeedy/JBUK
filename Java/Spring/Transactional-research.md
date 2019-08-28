# 스프링 transactional에 대한 고찰
tag: spring, spring-boot, transaction, transactional, annotation, autocommit, datasource, oracle, jdbc, 

## Spring Transaction 사용법

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











## :bomb: troubleshooting
### 1. Srping-boot Transactional is not working
**3가지만 명심하자**
- Datasource 생성시 setAutocommit(false) 로 설정
- Transaction 할 method 에 @transactional 달아주자 (service 또는 serviceImpl 둘중에 아무대나 걸어도 되는데 보기 쉽게 impl에 걸자)
- @transactional은 외부에서 호출할 경우에만 걸린다. 내부에서 호출할 경우엔 안먹는다. 
    - 무슨얘기냐 Acontroller 에서 Bservice.doInsert() 호출 할 경우, spring은 내부적으로 AOP 를 이용해
      Acontroller -> AOP transaction -> Bservice.doInsert()를 호출한다.
    
    - 내부에서 Acontroller -> Bservice.doTwiceInsert() ( Bservice.doInsert();  Bservice.doInsertOther(); ) 호출할 경우
      Bservice.doTwiceInsert()에 @transactional 이 안걸려 있다면 Transaction이 발생하지 않는다는 말이다

참고자료
- http://blog.naver.com/tkstone/50192718268 (Spring Transaction 사용법)
- http://blog.naver.com/tkstone/50193135886 (Spring Transaction 내부 동작 메커니즘)
- http://blog.naver.com/tkstone/50192724315 (TransactionTemplate 을 이용한 Spring Transaction 사용)
