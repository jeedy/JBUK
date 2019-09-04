# 1. Transaction 이란?

## 1. 기존 트렌젝션 구현방법
pure:
```java
package com.priviatravel.api.config.security.service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
public class OjdbcTransactionTest {

    public static void main(String[] args) {

        Connection conn = null;
        PreparedStatement stmt = null;

        try {
            // travel/devtravel!0, common, devcommon!0
            conn = DriverManager.getConnection("jdbc:oracle:thin:@172.16.2.210:4000:odindev", "common", "devcommon!0");
            conn.setAutoCommit(false);

            String sql = "UPDATE TRAVEL.TRAVEL_COUPON_ISSUE_INFO" +
                    "        SET COUPON_STS = 1" +
                    "        , COUPON_USE_AMT = 123421" +
                    "        , COUPON_USE_DATE = SYSDATE" +
                    "        WHERE MEMBER_NO = 544187" +
                    "        AND COUPON_ISSUE_NO = '7be87bd3-0904-4d10-add9-bbae1151a1bc'";
            stmt = conn.prepareStatement(sql);
            int result = stmt.executeUpdate();
//            ResultSet rs = stmt.getResultSet();
//            rs.getRow();
            if(result==1) {
                throw new Exception("go rollback!!");
            }
            conn.commit();
            System.out.println("commit!! row = "+result);
        }catch (Exception e) {
            e.printStackTrace();
            try {
                conn.rollback();
            }catch (Exception e1) {
                e1.printStackTrace();
            }
        }finally {
            try {
                conn.setAutoCommit(true);
                stmt.close();
                conn.close();
            }catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
```

case1(하나의 Datasource):
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
 30 }
```

case2(다수의 Datasource):
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
 14
 15  @Transactional
 16  public void doInternalTransaction() throws Exception{
 17   a1dao.insertA1();
 18   a2dao.insertA2();
 19  }
 20 }
```

> 분산 Transaction 을 직접 구현을 하려면 어떻게 해야할지 생각해보자?



## 2. 분산 Transaction
 오라클 xaDriver "oracle.jdbc.xa.client.OracleXADataSource"

변경전-DatabaseConfigCommon:
```java
package com.priviatravel.api.config;
import javax.sql.DataSource;
...
import com.priviatravel.api.common.utils.DecryptDataSourceUtil;
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

@Configuration
@MapperScan(basePackages = { "com.priviatravel.api.mapper.common" }, sqlSessionFactoryRef = "commonSqlSessionFactory")
@EnableTransactionManagement
public class DatabaseConfigCommon {
    @Autowired
    private Environment environment;

    @Bean(destroyMethod = "close")
    @Primary
    public DataSource commonDataSource() {
        /*
         * Hikari Datasource 용
         */
        HikariConfig hikariConfig =new HikariConfig();
        hikariConfig.setDriverClassName(environment.getRequiredProperty("COMMON.driverClassName"));
        hikariConfig.setJdbcUrl(environment.getRequiredProperty("COMMON.url"));
        hikariConfig.setUsername(environment.getRequiredProperty("COMMON.username"));
        hikariConfig.setPassword(DecryptDataSourceUtil.decryptor(environment.getRequiredProperty("COMMON.password")));
        hikariConfig.setMaximumPoolSize(environment.getRequiredProperty("COMMON.maxActive", Integer.class));
        hikariConfig.setMinimumIdle(environment.getRequiredProperty("COMMON.minIdle", Integer.class));
        DataSource dataSource = new HikariDataSource(hikariConfig);

        return dataSource;
    }

    @Bean
    @Primary
    public SqlSessionFactory commonSqlSessionFactory(@Qualifier("commonDataSource") DataSource dataSource) throws Exception {
        final SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);

        PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        sessionFactory.setMapperLocations(resolver.getResources("classpath:mapper/common/**/*-query.xml"));
        sessionFactory.setTypeAliasesPackage("com.priviatravel.api");
        return sessionFactory.getObject();
    }

    @Bean
    @Primary
    public SqlSessionTemplate commonSqlSessionTemplate(@Qualifier("commonSqlSessionFactory") SqlSessionFactory sqlSessionFactory) throws Exception {
        final SqlSessionTemplate sqlSessionTemplate = new SqlSessionTemplate(sqlSessionFactory);
        return sqlSessionTemplate;
    }

    @Bean
    @Primary
    public DataSourceTransactionManager commonTransactionManager(@Qualifier("commonDataSource") DataSource dataSource) {
        DataSourceTransactionManager dataSourceTransactionManager = new DataSourceTransactionManager(dataSource);
        return dataSourceTransactionManager;
    }
}

```

변경후-DatabaseConfigCommon:
```java
  package com.api.config;
  import java.util.Properties;
  import javax.sql.DataSource;
  ...
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

couponService:
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


