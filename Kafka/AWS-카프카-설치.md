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
listeners=PLAINTEXT://:9093
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

