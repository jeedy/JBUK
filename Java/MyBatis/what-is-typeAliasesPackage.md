# MyBatis 환경설정에 typeAliasesPackage 속성

참고 자료
- https://bryan7.tistory.com/70 typeAliasesPackage 정의

```xml
<!-- define the SqlSessionFactory -->
<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
    <property name="dataSource" ref="dataSource" />
    <property name="typeAliasesPackage" value="com.sample.mgmt" />
</bean>
```
or 
```java
SqlSessionFactoryBean.setTypeAliasesPackage("com.sample.mgmt")
```

위에서처럼 typeAliasesPackage 속성을 주면 이 하위 디렉터리의 클래스들은 
모두 myBatis Mapper XML에서 parameter type 이나 result Type으로 사용할 수 있다.
