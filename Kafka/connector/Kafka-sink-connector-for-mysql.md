# Kafka sink connector for Mysql

## 1. About
앞서 설명한 [Kafka Source Connector on Docker](./Kafka-source-connector-for-mysql.md) 를 참고해 다수의 Source table 를 CDC 하는 Source Connector를 생성하고 이를 Target table에 CDC sink connector 를 생성하는 방법과 사용법을 다룬다.

Docker내에 Kafka 설치 Connector plugin 설치는 이전 글을 참고하자. [Kafka Source Connector on Docker](./Kafka-source-connector-for-mysql.md)

### reference:
- [[Kafka] Kafka Connect - JDBC Connector 예제](https://wecandev.tistory.com/110)


## 2. Sink Database 설정
Source Connector 때와 마찬가지로 Sink Connector 를 생성 할 때도 Database에 사전 작업이 존재한다. 

매뉴얼에는 따로 구체적으로 설명이 나와있지 않지만 실제로 권한이 없어 테이블 접근을 못하는 경우가 생긴다.

### 2.1. Sink Database에 Sink Connector 용 계정 생성
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
> Source Connector plugin (debezium) 는 [Kafka Source Connector on Docker](./Kafka-source-connector-for-mysql.md) 를 참고하자 아래 코드는 sink connector plugin 설치만 다룬다.

```sh
tide@tide-OptiPlex-7071:~/project/kafka$ docker cp confluentinc-kafka-connect-jdbc-10.5.2.zip etl-kafka-kimjy:/opt/kafka/connectors/
tide@tide-OptiPlex-7071:~/project/kafka$ docker exec -it etl-kafka-kimjy bash

root@22bdd6b9d320:/# cd /opt/kafka/connectors/
root@22bdd6b9d320:/opt/kafka/connectors# unzip confluentinc-kafka-connect-jdbc-10.5.2.zip
```

plugin 설치 후 connect 를 재기동 하자.


## 4. Source Connector 생성
sick connector CDC 전용 Source Connector 를 생성해야 한다. 

Source table이 다수인 경우를 예제로 실습 한다. 실습에 대상이 되는 table은 PK가 있는 table, PK 없이 Unique Key로 구성된 table, PK 없고 Unique key 도 없는 table로 구성했다.

sick connector CDC 전용 Source Connector 를 생성해야 한다.

kafka container bash:
```sh
root@22bdd6b9d320:/# curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data '{
  "name": "dz-mysql-source-connector_testcase",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "localhost",
    "database.port": "3306",
    "database.user": "mysql",
    "database.password": "mysql1234",
    "database.server.id": "8405",
    "database.server.name": "dwserver_testcase",
    "table.include.list": "kimjydata.htl_v_city_mast_temp_pkey, kimjydata.htl_v_city_mast_temp_uniquekey, kimjydata.htl_v_city_mast_temp_nonkey",
    "database.history.kafka.topic": "dbhistory_testcase.kimjydata",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.allowPublicKeyRetrieval": "true",
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

- `table.include.list` : CDC 할 Source table들을 입력한다.

> 대상을 위 예제처럼 table별로 구성할 수도 있고 database 별( [Debezium Connector for MySQL :: Debezium Documentation](https://debezium.io/documentation/reference/1.3/connectors/mysql.html#mysql-property-database-include-list) ) 로도 구성 가능하다.    
> 좀 더 다양한 설정이 궁금하면  [Debezium Connector for MySQL :: Debezium Documentation](https://debezium.io/documentation/reference/1.3/connectors/mysql.html#mysql-connector-configuration-properties_debezium) 를 통해 확인하자


### 5. Sink Connector 생성
Sink connector 는 Source table 스키마 상태에 맞춰 다르게 조금씩 다르게 설정이 필요한 경우도 있다.
> 대체적으로 PK 가 있는 table과 Unique  Key로 구성된 table 이라면 같은 설정을 사용해도 무방하다.  그러나 PK, Unique key 가 없는 table이라면 설정이 조금 다르다.

kafka container bash:
```sh
# PK 로 구성된 Source table
root@22bdd6b9d320:/#  curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data '{
  "name": "cf-mysql-sink-connector-pkey-autocreate",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:mysql://localhost:3306/sink_db?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Seoul&useSSL=false",
    "connection.user": "sinkuser",
    "connection.password": "sinkuser1234",
    "auto.create": "true",
    "auto.evolve": "true",
    "delete.enabled": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_key",
    "table.name.format":"${topic}",
    "topics.regex": "dwserver_testcase.kimjydata.(.*)_pkey",
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

# Unique key로 구성된 Source table 
root@22bdd6b9d320:/#  curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data '{
  "name": "cf-mysql-sink-connector-uniquekey-autocreate",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:mysql://localhost:3306/sink_db?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Seoul&useSSL=false",
    "connection.user": "sinkuser",
    "connection.password": "sinkuser1234",
    "auto.create": "true",
    "auto.evolve": "true",
    "delete.enabled": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_key",
    "pk.fields": "CITY_MASTER_ID",
    "table.name.format":"${topic}",
    "topics.regex": "dwserver_testcase.kimjydata.(.*)_uniquekey",
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

# PK, Unique key 없는 Source table
root@22bdd6b9d320:/#  curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data '{
  "name": "cf-mysql-sink-connector-nonkey-autocreate",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:mysql://localhost:3306/sink_db?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Seoul&useSSL=false",
    "connection.user": "sinkuser",
    "connection.password": "sinkuser1234",
    "auto.create": "true",
    "auto.evolve": "true",
    "delete.enabled": "false",
    "insert.mode": "upsert",
    "pk.mode": "record_value",
    "pk.fields": "CITY_MASTER_ID",
    "table.name.format":"${topic}",
    "topics": "dwserver_testcase.kimjydata.htl_v_city_mast_temp_nonkey",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "true",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "true",
    "transforms": "unwrap, route",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "true",
    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
    "transforms.route.replacement": "$3"
  }
}'


```

- `auto.create` : target table 이 없는 경우 자동으로 생성해 준다. ( !!주의: 자동 생성시 varchar, char 과 같은 string  타입들은 모두 TEXT 타입으로 생성된다. 공식문서에서는  auto.create 를  false 로 할 것을 권장하고 있다.)
- `auto.evolve` : target table 에 해당 컬럼이 없을 경우 자동 생성해준다. 컬럼은 추가는 되지만 삭제는 되지 않는다, 컬럼명을 수정했다면 target table에는 컬럼 하나 더 생성한다. ( !!주의: 자동 생성시 varchar, char 과 같은 string  타입들은 모두 TEXT 타입으로 생성된다. )
- `delete.enabled` : source table에서 delete 가 발생할 경우 taget 에도 delete를 할지 여부, `pk.mode` 값이 `"record_value"` 라면 반드시 false로 설정해야 한다.
- `insert.mode` : insert 만 할지 update 만 할지 insert, update 모두 할지 선택
- `pk.mode` : PK 가 있거나 Unique key 가 있는 경우 record_key , 그외엔 record_value를 선택해야 한다.
- `pk.fields` : `pk.mode` 필드와 한쌍으로 입력된다. (`auto.create` 가 **true** 인 경우 target table 자동 생성시, 입력된 컬럼명으로 PK(primary key) 가 구성된다.)


## 회고
1. `auto.create` 값이 true인 경우와 false인 경우 조금씩 차이가 있다.    
자동생성(true) 될 경우에는 PK, Unique key 가 없는 테이블이라도 `pk.fields` 값으로 PK를 알아서 구성한다.     
수동생성(false) 인 경우에는 PK 또는 Unique key가 없기 때문에 update 하지않고 insert만 수행한다. (Target table에 unique key를 설정한다면 정상적으로 update 동작한다.)

