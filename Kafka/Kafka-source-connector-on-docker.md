# Kafka Source Connector on Docker

## 1. About
kafka Source Connector 설치하고 Mysql(DW database) 에 특정 Table(htl_v_city_mast_temp_20220825) 를 가져오는 것까지 실습한다. (silk connector 구현은 source connector를 참고.)

> kafka source connector plugin 을 제공하는 그룹은 크게 두 가지로 나뉜다.    
> - Debezium
> - Confluent (Atlassian 사 confluence 과 연관 없음)
>
> 둘 중에 `Debezium` 을 사용해 구현한 예제이다.

### reference:
- [Debezium Connector for MySQL :: Debezium Documentation](https://debezium.io/documentation/reference/1.3/connectors/mysql.html)
- [JDBC Source Connector Configuration Properties | Confluent Documentation](https://docs.confluent.io/kafka-connectors/jdbc/current/source-connector/source_config_options.html)
- [[Kafka] Kafka Connect - Debezium Connector 예제](https://wecandev.tistory.com/109)
- [[Kafka] Kafka Connect 개념/예제](https://cjw-awdsd.tistory.com/53)
- [[Kafka] Source Connector 생성](https://presentlee.tistory.com/5?category=915333)
- https://aws.amazon.com/ko/blogs/korea/introducing-amazon-msk-connect-stream-data-to-and-from-your-apache-kafka-clusters-using-managed-connectors/


## 2. Kafka 설치 on Docker
도커 위에 카프라 (with zookeeper) 를 띄우는 것부터 시작한다. connector는 kafka container 안에 접속해 설치한다.

> Docker engine 및 Docker-compose 설치는 생략한다. 


### 2.1. docker-compose 작성
로컬 PC에서 테스트를 위한 용도이므로 카프카, 주키퍼 한대씩 띄우도록 한다.

> kafka 와 zookeeper를 동시에 띄우고 내리고 서로 네트워크 통신을 위해서 `docker-compose` 로 생성해 관리하는 것이 편하다

docker-compose.yml:
```yaml
version: '3'
services:
  zookeeper:
    container_name: etl-zookeeper-kimjy
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"

  kafka:
    container_name: etl-kafka-kimjy
    image: wurstmeister/kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: 127.0.0.1
      KAFKA_ADVERTISED_PORT: 9092
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

```


### 2.2. docker-compose 실행
local bash:
```sh
# docker container 생성 및 run
tide@tide-OptiPlex-7071:~/project/kafka$ docker-compose -f docker-compose.yml up -d
Creating network "redash_default" with the default driver
Creating etl-zookeeper-kimjy ... done
Creating etl-kafka-kimjy     ... done

# container 생성 확인
tide@tide-OptiPlex-7071:~/project/kafka$ docker ps -a
CONTAINER ID   IMAGE                                                  COMMAND                  CREATED              STATUS                      PORTS                                                                                  NAMES
22bdd6b9d320   wurstmeister/kafka                                     "start-kafka.sh"         About a minute ago   Up About a minute           0.0.0.0:9092->9092/tcp, :::9092->9092/tcp                                              etl-kafka-kimjy
e6e357dcd0f9   wurstmeister/zookeeper                                 "/bin/sh -c '/usr/sb…"   About a minute ago   Up About a minute           22/tcp, 2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, :::2181->2181/tcp                  etl-zookeeper-kimjy

# 삭제 (down)
# docker-compose -f docker-compose.yml down
# 시작 (start)
# docker-compose -f docker-compose.yml start
# 중단 (stop)
# docker-compose -f docker-compose.yml stop
```

> docker-compose 명령에  -d 옵션을 붙여 background 에서 실행되도록 하자 


## 3. Kafka connect 설치

