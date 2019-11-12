# 스프링 3 버전에서 redis 모듈 테스트 과정
tags: spring, spring-data-redis, lettuce, redis, jedis

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
현재 (*Spring 3.1, Java 1.7) 버전에서 구현 가능한 현실적인 버전을 살펴보자

> lettuce는 Java 7(jdk 1.7)를 지원하지 않기 때문에 Jedis를 이용하기로 한다.

1. Jedis client만 이용한 버전
2. Sprig-data-redis 를 이용한 버전


### 사전 프로퍼티 셋팅

Redis 서버가 같이 구성이 되었다는 전제로 시작한다.

classpath:property/db.properties:
```properties
...
# REDIS
MASTER.NAME=mymaster
REDIS.NODES="172.16.0.207:5000,172.16.0.207:5001,172.16.0.207:5002"
SENTINEL.NODES=172.16.0.207:5003
SENTINEL.PASSWORD=redis1234
...
```


### 1. Jedis client만 이용한 버전
최종 가장 현실적인 버전이다. Spring 3.1 with java 7 버전에서 최신버전(Jedis 3.1)까지도 올라가는 것으로 확인했고, 그래서 sentinal까지 지원하기 때문에 이렇게 이용하는 것이 적합하다.

#### Maven 셋팅
pom.xml:
```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>3.1.0</version>
</dependency>
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.0</version>
</dependency>
<!-- Log4j2 SLF4J Bridge -->
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-slf4j-impl</artifactId>
    <version>2.0</version>
</dependency>
```


#### config 셋팅
RedisConfig.java:
```java
import java.util.HashSet;
import java.util.Set;

import javax.inject.Inject;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
import redis.clients.jedis.JedisSentinelPool;
import redis.clients.jedis.util.Pool;

@Configuration
@PropertySource("classpath:property/db.properties")
public class RedisConfig {

    @Inject
    private Environment environment;
    
    @Bean(destroyMethod = "close")
    public Pool<Jedis> jedisPool() {
        Set<String> sentinels = new HashSet<>();
        sentinels.add("172.16.0.207:5003");
        JedisSentinelPool jedisSentinelPool = new JedisSentinelPool(environment.getProperty("MASTER.NAME"), sentinels, environment.getProperty("SENTINEL.PASSWORD"));
        
        return jedisSentinelPool;
    }
}
```

#### 비지니스 로직 구현
RedisExampleServiceImpl.java
```java
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.util.Pool;

@Service("redisExampleService")
public class RedisExampleServiceImpl {

    @Autowired
    private Pool<Jedis> jedisPool;
    
    @Override
    public String getTest() {
        //
        String key ="";
        System.out.println(jedisPool);
        try(Jedis jedis = jedisPool.getResource()){
            jedis.set("search:test", "1111");
            System.out.println(jedis.get("search:test"));
            String value = jedis.get("search:test")
            List<String> list = jedis.lrange("search:lise:L2AnsVwO3YN7v234PFiO6NDfY", 0, -1);
            for(String s : list) {
                System.out.println(s);
            }
        }
        
        return value;
    }
}
```


### 2. Sprig-data-redis 를 이용한 버전
Spring-data-redis 를 이용하겠다면 아래와 버전에 맞춰야 오류가 나지 않는다. 
단점은 아래와 같이 너무 낮은 버전이라 sentinal을 지원하지 않는다. 그래서 jedis를 

pom.xml:
#### Maven 셋팅
```xml
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-redis</artifactId>
    <version>1.1.1.RELEASE</version>
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

#### config 셋팅

RedisConfig.java:
```java
import java.util.HashSet;
import java.util.Set;

import javax.inject.Inject;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
import redis.clients.jedis.JedisSentinelPool;
import redis.clients.jedis.util.Pool;

@Configuration
@PropertySource("classpath:property/db.properties")
public class RedisConfig {

    @Inject
    private Environment environment;
    
    @Bean
    public RedisConnectionFactory redisConnectionFactory() {
        // 위 버전에선 sentinal 지원하지 않는다.
        // String masterName = environment.getProperty("MASTER.NAME");
        // String password = environment.getProperty("SENTINEL.PASSWORD");
        // Set<String> sentinels;
        // String[] sentinels = environment.getProperty("SENTINEL.NODES").split("\\|");
        // for (String sentinel : sentinels) {
        //     String[] nodes = sentinel.split(":");
        //     sentinelConfig.addSentinel(new RedisNode(nodes[0], Integer.parseInt(nodes[1])));
        // }
        //JedisSentinelPool sentinelPool = new JedisSentinelPool(masterName, sentinels, password);
        //JedisConnectionFactory connectionFactory = new JedisConnectionFactory(sentinelPool);
       JedisPoolConfig jedisPoolConfig = new JedisPoolConfig();
       JedisConnectionFactory connectionFactory = new JedisConnectionFactory(jedisPoolConfig);
       connectionFactory.setHostName("172.16.0.207");
       connectionFactory.setPort(5000);
       connectionFactory.setPassword("redis1234");
       
       return connectionFactory;
    }
   
    @Bean
    public RedisTemplate<String, Object> redisTemplate() {
       RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();
       redisTemplate.setConnectionFactory(redisConnectionFactory());
       redisTemplate.setKeySerializer(new StringRedisSerializer());
       redisTemplate.setValueSerializer(new StringRedisSerializer());
       
       return redisTemplate;
    }
}
```

#### 비지니스 구현

RedisExampleServiceImpl.java:
```java
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.util.Pool;

@Service("redisExampleService")
public class RedisExampleServiceImpl {

    @Autowired
    private RedisTemplate redisTemplate;
    
    @Override
    public String getTest() {
        //
        String key ="";
        System.out.println(redisTemplate);
        redisTemplate.opsForValue().set("search:test", "1111");
        System.out.println(redisTemplate.opsForValue().get("search:test"));
        String value = redisTemplate.opsForValue().get("search:test");
        List<String> list = redisTemplate.opsForList().range("search:list:L2AnsVwO3YN7v234PFiO6NDfY", 0, -1);
        for(String s : list) {
            System.out.println(s);
        }
        return value;
    }
}
```
