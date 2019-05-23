# AWS 서버에 카프카 설치하기
tag: kafka, aws, 설치, 가이드, 카프카
 
### 참고자료
- https://kafka.apache.org/quickstart (카프카 퀵스타트 가이드 문서)

## 1. Open JDK(java 1.8) 설치하기

## 2. Kafka 다운로드

## 3. Zookeeper 실행

```bash
$ bin/zookeeper-server-start.sh config/zookeeper.properties
[2013-04-22 15:01:37,495] INFO Reading configuration from: config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
...
```

## 4. Kafka 실행

```bash
$ bin/kafka-server-start.sh config/server.properties
```

## 5. topic 생성

```bash
$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test

bin/kafka-topics.sh --list --bootstrap-server localhost:9092
test
```

## 5. Producer topic 메시지 전송

```bash
$ bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
> This is a message
> This is another message

```

## 6. Consumer topic 메시지 가져오기

```bash
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
This is a message
This is another message

```

## 7. Setting up a Multi-broker cluster (멀티 클러스터 구성하기)

1. config 파일 복사 : 
```bash
$ cp config/server.properties config/server-1.properties
$ cp config/server.properties config/server-2.properties 
```

2. config/server-1.properties :
```bash
broker.id=1
listeners=PLAINTEXT://:9093
log.dirs=/tmp/kafka-logs-1
```

3. config/server-2.properties :
```bash
broker.id=2
listeners=PLAINTEXT://:9094
log.dirs=/tmp/kafka-logs-2
```

4. 카프카 서버1, 서버2 실행 : 
```bash
$ bin/kafka-server-start.sh config/server-1.properties &
...

$ bin/kafka-server-start.sh config/server-2.properties &
...
```


## 8. Create New Topic with Multi-broker cluster (새 토픽 멀티 클러스터로 생성하기)

```bash
$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 3 --partitions 1 --topic my-replicated-topic
...

$ bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic my-replicated-topic
Topic:my-replicated-topic   PartitionCount:1    ReplicationFactor:3 Configs:
    Topic: my-replicated-topic  Partition: 0    Leader: 1   Replicas: 1,2,0 Isr: 1,2,0
```


## 그 밖에 알아낸 사실
- 프로듀서(or consumer) 는 broker 한대만 바라보고 액션을 해도 된다. (kafka_2.12-2.2.0 기준)
- ReplicationFactor 1 이라고 해도 다른 broker에 send를 보내더라도 전송된다. 
- AWS 의 경우 public DNS 주소는 매번 바뀐다. `private DNS` 주소는 인서턴스 삭제하지 않는 한 고정인듯 하다 
  (주키퍼 앙상블 셋팅이나 카프카 셋팅시 `private DNS`를 이용하자, 서로 서브마스크 주소와 port는 열어놔야 한다.
   확인결과 private DNS 주소도 바뀐다고 한다. 바뀌는 타이밍이 좀 늦을뿐 바뀌는 듯
   test-server pivateDNS kafka-0: ip-172-31-41-231.ap-northeast-2.compute.internal
   내일 바뀌는지 확인해보자.
   ) 
- bin/kafka-topic.sh, bin/kafka-console-*.sh는 클라이언트 명령어들이다. (kafka 압축 풀고 다른설정 필요없이 카프카 서버로 명령어 날릴 수 있다.)
- config/server.properties 안에 주키퍼 서버 주소를 넣는 것으로 봐서 주키퍼를 통해 서로 연결된 broker들을 서로 알 수 있는 것같다.
그래서 메시지를 보낼때(또는 받을때) `--bootstrap-server` 값에 모든 broker들의 주소를 넣을 필요가 없어진듯하다.
(이것은 멀티 서버로 구성한 뒤에 다시 확인해볼 필요가 있음)
- bin/kafka-server-stop.sh 명령어 날리면 모든 카프카서버들 한번에 내린다. (port 번호도 입력안했는데, 어떻게 다 내리지?) 
```bash
$ bin/kafka-server-stop.sh
```

