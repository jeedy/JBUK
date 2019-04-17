# Spring-Boot 에서 Mybatis Multi Datasource 를 사용하기 위한 annotation 셋팅

Spring 과 MyBatis (iBatis) 를 개발 환경으로 사용할 경우 여러 개의 datasource 를 써야 되는 경우가 있다.

여러 개의 data source 에 연결해야 할 경우 Mybatis config와 mapper 를 별도의 패키지로 분리하는게 개인적으로는 관리가 용이하다.

## 참고 자료
- https://lazymankook.tistory.com/31 여기서 힌트를 많이 얻음

## Mybatis Maven Dependency 설정

Spring boot에서 Mybatis를 이용해 MySQL을 연동하기 위해선 먼저 아래와 같이 Maven에 Dependency를 설정해줘야한다.

pom.xml
```xml
<!-- Mybatis-->
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>1.3.0</version>
</dependency>
 
<!-- Driver-->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.6</version>
</dependency>
```

Mybatis와 MySQL을 연동하기 위한 connector를 dependency로 추가했다. 이제 Database를 어떤 것을 사용할 지 property에 명시를 해야한다. 아래는 spring 프로젝트 생성 시 default로 있는 application.properties에 추가한 내용이다.

## Datasource Properties 설정
```
spring.db1.datasource.url=jdbc:mysql://localhost:3306/test_db
spring.db1.datasource.username=test_user
spring.db1.datasource.password=test_pw
spring.db1.datasource.driverClassName=com.mysql.jdbc.Driver
```

어떤 Database를 사용할 지 주소를 url에 명시하고, Database에 접근할 때 필요한 id, password를 명시해놨다. 그리고 mysql에 접근할 driver를 명시해놨다. 

이제 configuration class에서 Datasource, SqlSession, Template Bean을 설정해줘야 한다. 우선 아래의 코드를 보자.

## Datasource 설정 코드

```
@Configuration
@MapperScan(
    basePackages="com.example.demo",
    sqlSessionFactoryRef = "mysqlSessionFactory",
    sqlSessionTemplateRef = "mysqlSessionTemplate")
public class DemoConfig {
    @Bean(name="mysqlDataSource")
    @Primary
    @ConfigurationProperties(prefix = "spring.db1.datasource)
    public DataSource dbDataSource()
    {
        return DataSourceBuilder.create().build();
    }
 
    @Bean(name="mysqlSessionFactory")
    @Primary
    public SqlSessionFactory sqlSessionFactory(@Qualifier("mysqlDataSource")DataSource dataSource) throws Exception
    {
        SqlSessionFactoryBean sessionFactoryBean = new SqlSessionFactoryBean();
 
        sessionFactoryBean.setDataSource(dataSource);
        // annotation이 아닌 xml을 통한 mapping을 할거면 아래와 같이 사용, 
        // Annotaion을 이용할 경우 mapper interface에 @mapper 어노테이션 선언
        //PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        //sessionFactoryBean.setMapperLocations(resolver.getResources("classpath:mapper/abc.xml"));
 
        return sessionFactoryBean.getObject();
    }
 
    @Bean(name="mysqlSessionTemplate")
    @Primary
    public SqlSessionTemplate sqlSessionTemplate(SqlSessionFactory sqlSessionFactory) throws Exception
    {
        return new SqlSessionTemplate(sqlSessionFactory);
    }
}
```
> 핵심 @Qualifier 어노테이션을 통해 datasource, sqlSesionFactory 의 연결을 해줘야 한다. 그렇지 않으면 Defulat
> Datasource(@primary 선언된 메소드) 가 자동으로 들어간다.

@MapperScan annotation을 명시해 준 class는 basePackages로 지정한 곳에 존재하는 @Mapper로 명시된 interface를 스캔한다.
sqlSessionFactoryRef, sqlSessionTemplateRef 속성은 Database를 여러개 연결할 때 구분해주기 위한 속성이다. 두 개 이상의
MapperScan class 사용 시 명시를 안하면 오류가 난다. (역: sqlSessionTemplateRef 은 설정하지 않아도 오류 나지 않음)

`@Primary`는 Database가 두 개 이상 있을 때 어떤 Database를 첫 번째로 사용할 것인지 지정하는 annotation이다. (이부분이
가장 중요하다. 다중 Database 셋팅을 할때 저 어노테이션을 단 Datasource가 없으면 Spriong-boot에서 Default Datasource를
찾지를 못해 서버 가동을 하지 못한다.

이제 basePackages 속성에 지정한 package에 Mapper interface를 만들어보자.

## Mapper Interface
```java
@Mapper
public interface userMapper {
    @Select("SELECT * FROM user WHERE uid > #{uidNumber}")
    List<userDTO> getUsersOverUID(@Param("uidNumber")int uidNumber);
}
```
Mapper는 반드시 interface로 구현해야 한다. @Select annotation을 이용해 user라는 이름의 table에서 uid 값이 매개변수 uidNumber보다 큰 데이터를 userDTO의 List로 반환하고 있다. 저번 포스팅에서 DTO에 관해서 간단히 적었는데, Database를 이용할 때 값을 받아올 class이다. userDTO는 아래 코드처럼 구현된다.

## DTO Class
```java
public class userDTO {
    private BigInteger uid;
    private String id;
    private String pw;
    private Timestamp date;
    private Timestamp modDate;
    private String nickname;
 
    // 아래에 public으로 getter setter 구현 (길어서 생략)
}
```

위와 같이 data와 getter, setter로만 돼있는 순수 자바 객체(POJO)에 query문 결과가 담겨 List로 반환되는 것이다. 이것을 이용하려면 아래 DAO 클래스처럼 사용하면 된다.

```java
@Repository("userDAO")
public class userDAO {
    @Autowired
    @Qualifier("userMapper")
    private userMapper userMapper;
 
    public List<String> getUserIDs()
    {
        return userMapper.getUsersOverUID(0)
                .stream()
                .map(user->user.getId())
                .collect(Collectors.toList());
    }
}
```
