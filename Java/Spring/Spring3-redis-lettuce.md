# 스프링 3 버전에서 lettuce(redis) 모듈 테스트 과정
tags: spring, spring-data-redis, lettuce, redis, 

## 참고 URL
- https://spring.io/projects/spring-data-redis
- https://jojoldu.tistory.com/297
- https://dydtjr1128.github.io/redis/2019/04/03/Redis.html
- https://github.com/spring-projects/spring-data-keyvalue-examples/blob/master/retwisj/src/main/webapp/WEB-INF/spring/applicationContext-redis.xml
- http://arahansa.github.io/docs_spring/redis.html#new-in-1-5-0
- https://handcoding.tistory.com/137
- https://lettuce.io/core/release/reference/#spring.redis-client.xml-configuration


## 버전정리
https://docs.spring.io/spring-data/data-redis/docs/current/reference/html/#requirements

### New in Spring Data Redis
- 2.2 
- 2.1
- 2.0
    - Upgrade to Java 8.
    - Upgrade to Lettuce 5.0.
- 1.8
    - Upgrade to Jedis 2.9.
    - Upgrade to Lettuce 4.2 (Note: Lettuce 4.2 requires Java 8).

- 1.7
    - Spring 3.1 with Java 6 에서 그나마 가장 최적의 버전
    - Lettuce는 3.5 Final 버전 (https://github.com/lettuce-io/lettuce-core/releases/tag/3.5.0.Final) Java 6 부터 지원함
    - 
- 1.6
- 1.5
    - Java 6
    - PropertySource-based configuration for connecting to Redis Sentinel (see: Redis Sentinel Support).

> *Requirements* <br>
Spring Data Redis 2.x binaries require JDK level 8.0 and above and Spring Framework 5.2.1.RELEASE and above.<br>
In terms of key-value stores, Redis 2.6.x or higher is required. Spring Data Redis is currently tested against the latest 4.0 release.


## 구현
현재 (*Spring 3.1, Java 1.7) 버전에서 구현 가능한 현실적인 버전

### maven 

```xml
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-redis</artifactId>
    <version>1.1.0.RELEASE</version>
</dependency>
<!-- https://mvnrepository.com/artifact/redis.clients/jedis -->
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>2.1.0</version>
</dependency>
<!-- https://mvnrepository.com/artifact/org.slf4j/slf4j-log4j12 -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-log4j12</artifactId>
    <version>1.7.29</version>
</dependency>
```

