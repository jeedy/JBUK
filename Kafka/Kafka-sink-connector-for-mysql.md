# Kafka sink connector for Mysql

## 1. About
앞서 설명한 Kafka Source Connector for mysql on docker 이 후 Data를 다른 Database 에 sink 하는 plugin 을 구성한다.

Docker내에 Kafka 설치 Connector plugin 설치는 이전 글을 참고하자. [Kafka Source Connector on Docker](./Kafka-source-connector-on-docker.md)

### reference:
- [[Kafka] Kafka Connect - JDBC Connector 예제](https://wecandev.tistory.com/110)


## 2. Sink Database 설정
Source Connector 때와 마찬가지로 Sink Connector 를 생성 할 때도 Database에 사전 작업이 존재한다. 

매뉴얼에는 따로 구체적으로 설명이 나와있지 않지만 실제로 권한이 없어 테이블 접근을 못하는 경우가 생긴다.


### 2.1. Sink 될 테이블 생성
sink 대상 Database에 target table을 생성해주자 반드시 source쪽 table 과 컬럼명, 컬럼갯수가 맞아야 한다.

```sql
use sink_db

-- 테이블 생성 생략
CREATE TABLE `htl_v_city_mast_temp_20220825` ( .... )
``` 

### 2.2. Sink Database에 Sink Connector 용 계정 생성
`sinkuser` 대신 원하는 계정으로 치환해서 작업하면 된다.

```sql
use sink_db;

// sinkuser 가 추가 되어 있는지 확인
select host, user from user;

// sinkuser 없으면 생성
CREATE USER 'sinkuser'@'%' IDENTIFIED BY 'sinkuser1234';
// sinkuser 에게 권한 부여
GRANT ALL PRIVILEGES ON *.* TO 'sinkuser'@'%';

FLUSH PRIVILEGES;

```
## 3. Sink Connector plugin  설치 

### 4. Source Connector 생성
sick connector CDC 전용 Source Connector 를 생성해야 한다.

kafka container bash:
```sh
root@22bdd6b9d320:/# curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "dz-mysql-source-connector_07",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "localhost",
    "database.port": "3306",
    "database.user": "mysql",
    "database.password": "mysql1234",
    "database.server.id": "8405",
    "database.server.name": "dwserver7",
    "table.include.list": "tidedata.htl_v_city_mast_temp_20220825",
    "database.allowPublicKeyRetrieval": "true",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "dbhistory7.dwdata",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "true",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "true",
    "transforms": "unwrap,addTopicPrefix",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false",
    "transforms.addTopicPrefix.type":"org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.addTopicPrefix.regex":"(.*)",
    "transforms.addTopicPrefix.replacement":"$1",
    "time.precision.mode":"connect",
    "database.serverTimezone": "Asia/Seoul"
  }
}'

```


### 5. Sink Connector 생성

kafka container bash:
```sh
root@22bdd6b9d320:/# curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "cf-mysql-sink-connector_07",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:mysql://localhost:3306/sink_db?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Seoul&useSSL=false",
    "connection.user": "sinkuser",
    "connection.password": "sinkuser1234",
    "auto.create": "false",
    "auto.evolve": "false",
    "delete.enabled": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_key",
    "table.name.format":"${topic}",
    "topics.regex": "dwserver7.tidedata.(.*)",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "true",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "true",
    "transforms": "unwrap, route",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false",
    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
    "transforms.route.replacement": "$3"
  }
}'
```