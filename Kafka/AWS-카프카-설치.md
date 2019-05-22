# AWS 서버에 카프카 설치하기
tag:
 
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
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
This is a message
This is another message

```


