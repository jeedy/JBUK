# Kafka Source Connector for Oracle 11g

reference:
- https://rmoff.net/2018/12/12/streaming-data-from-oracle-into-kafka/
- https://github.com/debezium/debezium-examples/blob/main/tutorial/README.md#using-oracle
- https://muirandy.wordpress.com/2019/11/06/debezium-with-oracle-11g/ 
- https://app.gitter.im/#/room/#debezium_dev:gitter.im (debezium 개발자 커뮤니티)

## 1. About
Kafka Source Connector 설치하고 Oracle 에 특정 Table CDC 정보를 가져오는 것까지 실습한다. (silk connector 는 [Kafka Sink Connector for Mysql](./Kafka-sink-connector-for-mysql.md) 문서를 보고 구현하자)

`Debezium` 에서 오라클 11g 버전을 지원하는 버전은 공식적으로 1.3.x 버전이다. 그러나 실제로 테스트해본 결과 oracle 11g에서 정상 동작 못한다.    
그래서 찾은 버전은 1.5.x 버전이다. 본 예제는 `debezium 1.5.4.Final` 버전을 기준으로 작업 되었다.

> kafka source connector plugin 을 제공하는 그룹은 크게 두 가지로 나뉜다.    
> - Debezium
> - Confluent (유료, JDBC를 이용한 cdc는 무료이나 bulk 방식 또는 message queue 구성이 필요하다.)
>
> 둘 중에 `Debezium` 을 사용해 구현한 예제이다.

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
      - /home/tide/project/kafka/docker-volume/docker.sock:/var/run/docker.sock
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


## 3. Kafka connector 설치
Kafka container(`etl-kafka-kimjy`) 안에 Kafka connector plugin 파일을 설치하고 config 설정도 수정해주자
> [Debezium Documentation 1.5](https://debezium.io/documentation/reference/1.5/)

local bash:
```sh
# kafka container bash 접속
tide@tide-OptiPlex-7071:~/project/kafka$ docker exec -it etl-kafka-kimjy bash
# kafka bash 접속
root@22bdd6b9d320:/#

# connectors 관리를 편하게 하기 위해 카프카가 설치된 폴더에 connectors 용 폴더 생성
root@22bdd6b9d320:/# cd /opt/kafka
root@22bdd6b9d320:/opt/kafka# mkdir connectors
root@22bdd6b9d320:/opt/kafka# exit

# 미리 다운받아둔 connetors plugin 파일을 container안에 복사한다.
tide@tide-OptiPlex-7071:~/project/kafka$ wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-oracle/1.5.4.Final/debezium-connector-oracle-1.5.4.Final-plugin.tar.gz
tide@tide-OptiPlex-7071:~/project/kafka$ docker cp debezium-connector-oracle-1.5.4.Final-plugin.tar.gz etl-kafka-kimjy:/opt/kafka/connectors/

# connector plugin 압축 해제
tide@tide-OptiPlex-7071:~/project/kafka$ docker exec -it etl-kafka-kimjy bash
root@22bdd6b9d320:/# cd /opt/kafka/connectors/
root@66880a74b37f:/opt/kafka/connectors# tar -zxvf debezium-connector-oracle-1.5.4.Final-plugin.tar.gz
debezium-connector-oracle/CHANGELOG.md
debezium-connector-oracle/CONTRIBUTE.md
debezium-connector-oracle/COPYRIGHT.txt
debezium-connector-oracle/LICENSE-3rd-PARTIES.txt
debezium-connector-oracle/LICENSE.txt
debezium-connector-oracle/README.md
debezium-connector-oracle/README_ZH.md
debezium-connector-oracle/debezium-core-1.5.4.Final.jar
debezium-connector-oracle/debezium-api-1.5.4.Final.jar
debezium-connector-oracle/guava-30.0-jre.jar
debezium-connector-oracle/failureaccess-1.0.1.jar
debezium-connector-oracle/debezium-ddl-parser-1.5.4.Final.jar
debezium-connector-oracle/antlr4-runtime-4.7.2.jar
debezium-connector-oracle/jsqlparser-2.1.jar
debezium-connector-oracle/debezium-connector-oracle-1.5.4.Final.jar

# kafka config 수정
root@22bdd6b9d320:/opt/kafka/config# vim connect-distributed.properties
# vim 설치가 안되어 있다면 설치하자
# apt-get update && apt-get install -y vim

```
> 예제에서 사용하는 Kafka docker image(`wurstmeister/kafka`) 는 kafka 운영시 필요한 최소한의 명령어들로만 구성된 상태로 구동된다. 추가로 필요한 툴이 있다면 설치해가며 진행하자.

connect-distributed.properties 파일에 connector 디렉토리 위치를 알려주자

/opt/kafka/config/connect-distributed.propertie:
```sh
# 원래 경로
#plugin.path=

# 수정 경로
plugin.path=/opt/kafka/connectors
```


### 3.1. kafka connect 실행
분산모드(distributed) 카프카 커넥트를 실행한다. 분산모드는 2개 이상의 커넥트를 한 개의 클러스터를 묶어서 운영한다.

kafka container bash:
```sh
root@22bdd6b9d320:/# cd /opt/kafka/bin
root@22bdd6b9d320:/opt/kafka/bin# nohup connect-distributed.sh /opt/kafka/config/connect-distributed.properties &
[1] 1747
root@22bdd6b9d320:/opt/kafka/bin# nohup: ignoring input and appending output to 'nohup.out'

# 로그 확인
root@22bdd6b9d320:/opt/kafka/bin# tail -f nohup.out
... 
[2022-08-25 06:13:45,045] INFO [Worker clientId=connect-1, groupId=connect-cluster] Starting connectors and tasks using config offset -1 (org.apache.kafka.connect.runtime.distributed.DistributedHerder:1244)
[2022-08-25 06:13:45,045] INFO [Worker clientId=connect-1, groupId=connect-cluster] Finished starting connectors and tasks (org.apache.kafka.connect.runtime.distributed.DistributedHerder:1272)
[2022-08-25 06:13:45,084] INFO [Worker clientId=connect-1, groupId=connect-cluster] Session key updated (org.apache.kafka.connect.runtime.distributed.DistributedHerder:1587)

# Kafka Connect 8083 port 열려 있는지 확인
root@22bdd6b9d320:/opt/kafka/bin# netstat -lnp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.11:37749        0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:44911           0.0.0.0:*               LISTEN      1747/java
tcp        0      0 0.0.0.0:44549           0.0.0.0:*               LISTEN      1/java
tcp        0      0 0.0.0.0:9092            0.0.0.0:*               LISTEN      1/java
tcp        0      0 0.0.0.0:8083            0.0.0.0:*               LISTEN      1747/java
udp        0      0 127.0.0.11:44552        0.0.0.0:*                           -
Active UNIX domain sockets (only servers)
Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path

# Kafka Connector 클러스터 정보 확인
root@22bdd6b9d320:/opt/kafka/bin# curl http://localhost:8083/
{"version":"2.8.1","commit":"839b886f9b732b15","kafka_cluster_id":"XoOMaweJQaSV2mxGoG-TeA"}

```

> `nohup` 명령어로 background 에서 connect가 구동 되도록 한다. nohup.out 로그에 `Finished starting connectors and tasks (org.apache.kafka.connect.runtime.distributed.DistributedHerder:1272)` 라고 나오면 정상 구동이다.


### 3.2. Oracle connector plugin 확인
Kafka Connector가 올라갈 때 앞에서 설치한 플러그인(`io.debezium.connector.oracle.OracleConnector`)을 물고 올라 갔는지 확인해보자

kafka container bash:
```sh
root@22bdd6b9d320:/opt/kafka/bin# curl --location --request GET 'localhost:8083/connector-plugins'
[
  {
    "class": "io.debezium.connector.oracle.OracleConnector",
    "type": "source",
    "version": "1.5.4.Final"
  },
  {
    "class": "org.apache.kafka.connect.file.FileStreamSinkConnector",
    "type": "sink",
    "version": "2.8.1"
  },
  {
    "class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
    "type": "source",
    "version": "2.8.1"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorCheckpointConnector",
    "type": "source",
    "version": "1"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorHeartbeatConnector",
    "type": "source",
    "version": "1"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
    "type": "source",
    "version": "1"
  }
]

```


## 4. Rest API 로 Source Connector 생성
source database 에서 데이터를 끌어올 Source Connector 를 생성해 줘야 한다. 

> Connector plugin은 크게 두 가지로 나뉜다. Open source 공개된 플러그인 debezium connector plugin (이 예제에서 사용 중이다.) 그리고 Confluent 에서 개발한 Confluent connector plugin, 플러그인 마다 생성하는 `Configuration Properties` 가 서로 다르다. 이 예제에선 debezium 방식으로 생성한다. confluent 방식이 궁금한 분들은 [JDBC Source Connector Configuration Properties | Confluent Documentation](https://docs.confluent.io/kafka-connectors/jdbc/current/source-connector/source_config_options.html#) 참조.

kafka container bash:
```sh
# source debezium connector 생성
$ curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "dz-oracle-source-connector_01",
    "config": {
        "connector.class" : "io.debezium.connector.oracle.OracleConnector",
        "tasks.max" : "1",
        "database.oracle.version":"11",
        "database.connection.adapter": "logminer",
        "database.tablename.case.insensitive": "false",
        "database.hostname": "localhost",
        "database.port": "1521",
        "database.dbname" : "oradb",
        "database.schema" : "COMMON",
        "database.user" : "DMS",
        "database.password" : "dms1234",
        "database.server.name" : "oraserver1",
        "database.history.kafka.topic": "dbhistory.oradb1",
        "database.history.kafka.bootstrap.servers" : "kafka:9092",
        "table.include.list": "COMMON.TEST_DMS",
        "key.converter": "org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable": "true",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter.schemas.enable": "true",
        "transforms": "unwrap,addTopicPrefix",
        "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
        "transforms.unwrap.drop.tombstones": "false",
        "transforms.addTopicPrefix.type":"org.apache.kafka.connect.transforms.RegexRouter",
        "transforms.addTopicPrefix.regex":"(.*)",
        "transforms.addTopicPrefix.replacement":"$1"
    }
}'


# Connector 삭제
curl --location --request DELETE 'http://localhost:8083/connectors/dz-oracle-source-connector_01'

# 생성된 connectors 목록 
curl --location --request GET 'http://localhost:8083/connectors'

# connector 상세 정보
curl --location --request GET 'http://localhost:8083/connectors/dz-oracle-source-connector_01/config ' \
--header 'Content-Type: application/json'
```

#### properties hierarchy 참조: 
- https://github.com/debezium/debezium/blob/1.5/debezium-testing/debezium-testing-testcontainers/src/main/java/io/debezium/testing/testcontainers/ConnectorConfiguration.java
  - https://github.com/debezium/debezium/blob/1.5/debezium-core/src/main/java/io/debezium/relational/RelationalDatabaseConnectorConfig.java
    - https://github.com/debezium/debezium/blob/1.5/debezium-core/src/main/java/io/debezium/relational/HistorizedRelationalDatabaseConnectorConfig.java
      - https://github.com/debezium/debezium/blob/1.5/debezium-connector-oracle/src/main/java/io/debezium/connector/oracle/OracleConnectorConfig.java


#### 주요 properties
- **connector.class** 는 위에서 설치한 connector plugin 중에 사용할 커넥터의 java class 를 입력해준다.
- **tasks.max** 는 이 커넥터에 대해 생성되어야 할 태스크의 최대 수 
- **database.oracle.version** Oracle 11g 에서는 `11` 값 픽스
- **database.connection.adapter** 는 `logminer` or `xstream` 여기선 `logminer` 를 사용한다.
- **database.tablename.case.insensitive** 대소문자 구분을 하겠냐는 옵션, DB 설정에 따라`true` or `false` 로 설정한다.
- **database.hostname** 은 DB IP주소
- **database.server.name** 은 Mysql 인스턴스를 고유하게 식별하는데 사용하는 문자열인데, 값이 없으면 알아서 들어가지만 중복되지 않도록 그리고 확인 가능하도록 정의해주자
- **table.include.list** 는 source 대상이 될 Table을 입력한다. 콤마(,) 로 여러개의 table 을 입력 할 수도 있고 `database.include.list` 를 이용하면 database 등록 가능하다. 
- **database.history.kafka.bootstrap.servers** 는 kafka 부트스트랩 주소 포트 입력
- **database.serverTimezone** 은 DW database Datasource 연결시 timezone 관련 에러로 접속이 안되는 상황에서는 이 프로퍼티 설정이 ***필수*** 다.
- **transforms.unwrap.type** 는 RDB(MySQL)에 connect를 하기 때문에 `io.debezium.transforms.ExtractNewRecordState` 가 픽스다.
- **transforms.unwrap.add.fields** 은 topic 메시지에 추가할 metatag field 값으로 "op,table" 값을 넣으면 CUD 코드 값과 테이블 이름을 알 수 있다.
- **transforms.unwrap.add.fields** 은 topic 메시지에 추가할 metatag field 값으로 "op,table" 값을 넣으면 CUD 코드 값과 테이블 이름을 알 수 있다.
- **transforms.unwrap.drop.tombstones** 은 delete 된 데이터를 전달 여부이다. `ture` 면 delete 는 전달하지 않는다. `false`일 경우 delete event를 전달하지만 topic 메시지는 null 값으로 오기 때문에 `transforms.unwrap.delete.handling.mode` 와 함께 사용되어야 한다.
- **transforms.unwrap.delete.handling.mode** 은 `transforms.unwrap.drop.tombstones` 값을 false 로 할 경우 null 대신 delete 된 데이터의 삭제 직전 데이터를 넘겨준다.


> Mysql(RDB) 는 `io.debezium.transforms.ExtractNewRecordState`(https://debezium.io/documentation/reference/0.9/configuration/event-flattening.html) 를 이용해서 데이터를 가져온다. 가져올 때 다양한 처리가 가능하지만 지금 프로젝트에서 가장 중요한 요소는 delete 시에도 메시지를 받아 처리를 해야할 경우 이다 이때 중요한  propertie 옵션이 `transforms.unwrap.add.fields`, `transforms.unwrap.drop.tombstones`, `transforms.unwrap.delete.handling.mode` 이다.

### 4.1. 생성된 Topic 목록
Connector로 연결되면 connector내부에서 사용하기 위한 topic과 source table을 트래킹 할 수 있는 topic이 자동으로 생기고 초기 데이터도 들어간다.

Kafka container bash:
```sh
root@22bdd6b9d320:/opt/kafka/bin# kafka-topics.sh --list --bootstrap-server localhost:9092
__consumer_offsets
connect-configs
connect-offsets
connect-status
dbhistory.oradb1
oraserver1
oraserver1.COMMON.TEST_DMS

```

## 5. 콘솔 컨슈머 확인
실제로 Database에 데이터를 수정해보고 콘솔 컨슈머를 통해 message가 어떻게 오는지 확인해보자

Kafka container bash:
```sh
root@22bdd6b9d320:/opt/kafka/bin# kafka-console-consumer.sh --topic oraserver1.COMMON.TEST_DMS --bootstrap-server localhost:9092 --formatter kafka.tools.DefaultMessageFormatter --property print.timestamp=true --property print.key=true --property print.value=true --from-beginning
```

> 처음부터 다 가져오려면 `--from-beginning` 옵션을 넣자


## 6. Sink Connector 생성

Confluent사(https://www.confluent.io/) 에서 제공하는 sink connector를 사용한다.

### 6.1. Mysql Sink Connector
```sh
$ curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data '{
  "name": "oracle-oraserver-mysql-sink-connector_01",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:mysql://xxx.xxx.xxx.xx:3306/common_dev?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Seoul&useSSL=false",
    "connection.user": "DMS",
    "connection.password": "dms4321",
    "auto.create": "true",
    "auto.evolve": "true",
    "delete.enabled": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_key",
    "table.name.format":"${topic}",
    "topics.regex": "oraserver1.COMMON.(.*)",
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

# connector 삭제
$ curl --location --request DELETE 'http://localhost:8083/connectors/oracle-oraserver-mysql-sink-connector_01'
```

### 6.2. Postgresql Sink Connector
```sh
$ curl --location --request POST 'http://localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data '{
  "name": "oracle-oraserver-postgresql-sink-connector_01",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:postgresql://xxx.xxxx.xxx.xxx:5432/postgres?currentSchema=myschema",
    "connection.user": "postgres",
    "connection.password": "postgres1234",
    "auto.create": "true",
    "auto.evolve": "true",
    "delete.enabled": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_key",
    "table.name.format":"${topic}",
    "topics.regex": "oraserver1.COMMON.(.*)",
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

# connector 삭제
$ curl --location --request DELETE 'http://localhost:8083/connectors/oracle-oraserver-postgresql-sink-connector_01'
```



## :bomb: troubleshooting
1. ora-01882: TimeZone Region not found. with Kafka Connect JdbcSource connector.

`oracle.jdbc.timezoneAsRegion=false` 옵션 추가

1. source connector 생성시 아래와 같은 에러가 발생한다면
```sh
[2023-02-21 06:30:48,360] ERROR WorkerSourceTask{id=dz-oracle-source-connector_04-0} Task threw an uncaught and unrecoverable exception. Task is being killed and will not recover until manually restarted (org.apache.kafka.connect.runtime.WorkerTask:190)
org.apache.kafka.connect.errors.ConnectException: An exception occurred in the change event producer. This connector will be stopped.
        at io.debezium.pipeline.ErrorHandler.setProducerThrowable(ErrorHandler.java:42)
        at io.debezium.connector.oracle.logminer.LogMinerStreamingChangeEventSource.execute(LogMinerStreamingChangeEventSource.java:208)
        at io.debezium.pipeline.ChangeEventSourceCoordinator.streamEvents(ChangeEventSourceCoordinator.java:152)
        at io.debezium.pipeline.ChangeEventSourceCoordinator.lambda$start$0(ChangeEventSourceCoordinator.java:119)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Unknown Source)
        at java.base/java.util.concurrent.FutureTask.run(Unknown Source)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)
        at java.base/java.lang.Thread.run(Unknown Source)
Caused by: io.debezium.DebeziumException: Supplemental logging not configured for table DMS.test_dms.  Use command: ALTER TABLE DMS.test_dms ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS
        at io.debezium.connector.oracle.logminer.LogMinerHelper.checkSupplementalLogging(LogMinerHelper.java:407)
        at io.debezium.connector.oracle.logminer.LogMinerStreamingChangeEventSource.execute(LogMinerStreamingChangeEventSource.java:132)
        ... 7 more

```

아래 쿼리를 실행해주자 

```sql
ALTER TABLE DMS.TEST_DMS ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;
```

> Kafka connector 를 이용하는 테이블은 Supplemental Logging Data를 생성해야 한다.  
> Supplemental Logging Data 란? https://bestugi.tistory.com/21
