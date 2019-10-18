# Sring에서 Mybatis 사용하기


## Spring에 Mybatis 셋팅하기 
출처
- http://blog.naver.com/tkstone/50192293603(Spring 에서 Mybatis 사용하기)

Spring 3.2.x framework 내에는 Mybatis 연동 라이브러리가 포함 되어 있지 않다. (ibatis에 대한 연동 라이브러리는 포함 되어 있다.) 따라서 Spring 3.2.x 에서 Mybatis 를 사용 하려면 Github 에 있는 별도 라이브러리를 포함해야 한다. (http://mybatis.github.io/spring/)

Maven 을 사용하는 경우에는 기본적으로 다음 Dependency 를 넣으면 Spring-Mybatis 연동 기능을 사용 가능하다.

```xml
  1 <dependency>
  2     <groupId>org.mybatis</groupId>
  3     <artifactId>mybatis-spring</artifactId>
  4     <version>1.2.2</version>
  5 </dependency>
  6 <dependency>
  7     <groupId>org.mybatis</groupId>
  8     <artifactId>mybatis</artifactId>
  9     <version>3.2.5</version>
 10 </dependency>
```

위의 1~5 라인은 spring - mybatis 연동 모둘이고, 6 ~ 10 라인은 mybatis  그 자체이다.
물론 JDBC Driver 도 별도로 추가해야 한다.

만일 Maven을 사용하지 않는 경우에는 mybatis-x.x.x.jar 와 mybatis-spring-x.x.x.jar를 classpath에 추가해 주면 된다.

일반적으로 Mybatis 를 사용하는 순서는 다음과 같다.

1) mybatis configuration 생성 (일반적으로 configuration.xml) - mybatis context 정보 (ex. DB 접속 정보)
2) mapper xml 생성 (일반적으로 mapper.xml) - 실행할 SQL 정보
3) mapper interface 생성 (mapper xml 과 1:1 연동을 하는 Java Inteface)
4) mapper interface 를 호출하는 Java Application (주로 DAO 역할 수행)

Spring 에서 Mybatis를 사용할 때에는 약간 순서가 바뀐다.

1) mybatis configuration 생성 (Mybatis 독립적으로 사용할 때 보다는 내용이 간소함. 나머지는 Spring context에서 관리)
2) mapper xml 생성 (위와 동일)
3) mapper interface 생성 (위와 동일)
4) Spring context 에 SqlSessionFactory 등록
5) Spring context 에 MapperFactoryBean 등록
6) mapper interface 를 사용하는 Spring Bean 에 앞의 5에서 생성한 Mapper bean 을 종속성 주입 (Dependency Injection)

이 순서에 따른 예제는 다음과 같다.

### 1) mybatis configuration (configuration.xml)
```xml
  1 <?xml version="1.0" encoding="UTF-8" ?> 
  2 <!DOCTYPE configuration 
  3     PUBLIC "-//mybatis.org//DTD Config 3.0//EN" 
  4     "http://mybatis.org/dtd/mybatis-3-config.dtd">  
  5 <configuration> 
  6   <settings>  
  7       <setting name="defaultExecutorType" value="REUSE"/>
  8       <setting name="cacheEnabled" value="false"/>
  9       <setting name="logImpl" value="LOG4J"/>
 10   </settings>     
 11   <mappers> 
 12     <mapper resource="mybatis/mapper.xml"/>  
 13   </mappers> 
 14 </configuration>
```
* 위의 12라인에 사용하는 mapper.xml 에 대한 정보를 입력한다.
* 위의 예제에서는 DB 접속 정보가 없다. 이것은 Spring context에 등록된 Datasource 를 사용하기 위함이다. 아래의 3)에서 DB 접속 정보를 설정한다.

### 2) mapper.xml
```xml
  1 <?xml version="1.0" encoding="UTF-8" ?>  
  2 <!DOCTYPE mapper 
  3     PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
  4     "http://mybatis.org/dtd/mybatis-3-mapper.dtd">  
  5 <mapper namespace="tkstone.test.mapping.Mapper1">
  6   <insert id="insertA1" 
  7         parameterType="tkstone.test.param.A1"
  8            flushCache="true" statementType="PREPARED"   
  9         >
 10     insert into a1(col1, col2)
 11     values(#{col1}, #{col2})
 12   </insert>
 13 </mapper>   
```
* Mybatis 만 사용할 때와 차이가 없음

### 3) mapper interface
```java
  1 package tkstone.test.mapping;
  2 
  3 import tkstone.test.param.A1;
  4 
  5 public interface Mapper1 {
  6     public int insertA1(A1 param);
  7 }
  8 
```
* Mybatis 만 사용할 때와 차이가 없음

### 4) Spring context에 SqlSessionFactory 등록
```xml
  1 <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
  2     <property name="dataSource" ref="testDataSource" />
  3     <property name="configLocation" value="classpath:mybatis/configuration.xml"/>
  4 </bean>
```
* SqlSessionFactoryBean 등록 시 DB 접속 정보 (Datasource) 및 Mybatis main config 정보를 등록함
* configLocation 에는  1)에서 생성한 Mybatis configuration 파일 경로를 설정

### 5) Spring context에 MapperFactoryBean 등록 (앞의 3)에서 생성한 Mapper1 interface에 대한 Factory
```xml
  1 <bean id="mapper1" class="org.mybatis.spring.mapper.MapperFactoryBean">
  2     <property name="mapperInterface" value="tkstone.test.mapping.Mapper1" />
  3     <property name="sqlSessionFactory" ref="sqlSessionFactory" />
  4 </bean>
```
* mapperInterface 에는 3)에서 생성한 Mapper interface 를 설정
* sqlSessionFactory 에는 4)에서 등록한 sqlSessionFactory를 설정. 이 값을 설정하지 않으면 "sqlSessionFactory" ID 값을 가진 Bean을 자동으로 설정

### 6) Spring Bean 에 mapper interface 주입
```xml
  1 <bean id="myBean" class="tkstone.test.transaction.MyBean">
  2     <property name="mapper1" ref="mapper1"/>
  3 </bean>
```
이렇게 하면 기본적으로 Spring 에서 Mybatis 를 이용하여 SQL을 실행할 수 있다.


## Spring - Mybatis 에서 Mapper interface 를 주입받는 방법과 SqlSession 을 주입받는 방법
출처
- http://blog.naver.com/tkstone/50192410997(Spring - Mybatis 에서 Mapper interface 를 주입받는 방법과 SqlSession 을 주입받는 방법)

Spring - Mybatis 에서 SQL을 실행 하려면 크게 다음 2가지 방법을 사용 가능하다.
1) Mapper interface 를 주입받는 방법
2) SqlSession 을 주입받는 방법

### 1) Mapper interface 를 주입 받는 방법은 앞에서 설명 했듯이 MapperFactoryBean을 이용하는 것이다.
MapperFactoryBean 을 이용해서 Mapper interface bean 을 선언하는 방법은 다음과 같다.
```xml
  1 <bean id="mapper1" class="org.mybatis.spring.mapper.MapperFactoryBean">
  2     <property name="mapperInterface" value="tkstone.test.mapping.Mapper1" />
  3     <property name="sqlSessionFactory" ref="sqlSessionFactory" />
  4 </bean>
```
SQL을 실행 하려는 Bean 에서는 "mapper1" 을 주입 (Dependency injection) 받아서 실행하면 된다.


### 2) SqlSession 을 주입 받는 방법은 SqlSessionTemplate 을 이용하는 것이다.
다음은 SqlSession 을 Bean 으로 선언하는 부분이다.

```xml
  1 <bean id="sqlSession" class="org.mybatis.spring.SqlSessionTemplate">
  2     <constructor-arg index="0" ref="sqlSessionFactory" />
  3 </bean> 
```

이렇게 선언된 SqlSession 을 사용하는 Bean (주로 DAO 클래스) 에서는 다음과 같이 구현한다.

```java
  1 import org.apache.ibatis.session.SqlSession;
  2 
  3 public class MyDao {
  4     private SqlSession sqlSession;
  5  
  6     @Resource(name="sqlSession")
  7     public void setSqlSession(SqlSession sqlSession){
  8         this.sqlSession = sqlSession;
  9     }
 10  
 11     public void insertA1() throws Exception{
 12         sqlSession.insert("tkstone.test.mapping.Mapper1.insertA1", SomeParam);
 13     }
 14 }
```
위의 예제의 11라인에서는 Mybatis SqlSession.insert() 메소드를 바로 호출하고 있다.  

결과적으로 실행되는 SQL은 동일하다. 개인적으로 생각하는 장단점은 다음과 같다.

분류 | Mapper interface bean 선언 | SqlSession bean 선언 
----|----|----
장점 | Java 소스 내에 Mybatis 에 종속적인 API 를 사용하지 않음 | DAO 클래스가 늘어날수록 Bean 선언이 용이함 (DAO를 @Component 로 선언하는 경우)
단점 | Mapper interface 개수가 늘어날수록 선언해야 하는 Bean 도 늘어남 | Sql 종류, Parameter type에 따라 SqlSession API 를 구분해서 사용해야 함 
