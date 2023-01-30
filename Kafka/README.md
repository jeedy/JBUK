# Kafka 

## Apache kafka 카프카, 데이터 플랫폼의 최강자목차
1. [1장 카프카란 무엇인가?](/Kafka/1%EC%9E%A5-%EC%B9%B4%ED%94%84%EC%B9%B4%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80.md)
1. [3장 카프카 디자인](/Kafka/3%EC%9E%A5-%EC%B9%B4%ED%94%84%EC%B9%B4-%EB%94%94%EC%9E%90%EC%9D%B8.md)
1. [6장 카프카 운영 가이드](/Kafka/6%EC%9E%A5-%EC%B9%B4%ED%94%84%EC%B9%B4-%EC%9A%B4%EC%98%81-%EA%B0%80%EC%9D%B4%EB%93%9C.md)
1. [7장 카프카를 활용한 데이터 파이프라인 구축](/Kafka/7%EC%9E%A5-%EC%B9%B4%ED%94%84%EC%B9%B4%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8-%EA%B5%AC%EC%B6%95.md)


## Kafka connect 

### 목차
1. [카프카 connect source 구성](/Kafka/Kafka-source-connector-on-docker.md)
1. [카프카 connect sink 구성](/Kafka/Kafka-sink-connector-for-mysql.md)
1. [카프카 connect cluster 구성](/Kafka/Kafka-connector-cluster.md)

## kafka console commands
```sh
# 토픽 목록
##  kafka 스타트 
/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties
/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties

## 끄기 server -> zookeeper
bin/kafka-server-stop.sh config/server.properties
bin/zookeeper-server-stop.sh config/zookeeper.properties

## show topic list
/usr/local/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

## view description topic
/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --topic my_topic --describe

## create the topic
/usr/local/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic my_topic

## show the topic
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic my_topic

## show the topic partiton 1
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --partition 1 --topic my_topic

## delete the topic
/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic my_topic

## consumer list
/usr/local/kafka/bin/kafka-consumer-groups.sh  --bootstrap-server localhost:9092 --list

## consumer status and offset
/usr/local/kafka/bin/kafka-consumer-groups.sh  --bootstrap-server localhost:9092 --group console-consumer-23 --describe

## consumer reset offset 
### offset 을 reset 했을 때 어떻게 되는지 예상 결과값을 보여줌
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server  localhost:9092 --group console-consumer-23 --topic my_topic --reset-offsets --to-earliest --dry-run
### 실제 offset reset 명령어
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group console-consumer-23 --topic my_topic --reset-offsets --to-earliest --execute

## consumer group delete
/usr/local/kafka/bin/kafka-consumer-groups.sh --zookeeper localhost:2181 --delete --group console-consumer-23

## server log check
cat /usr/local/bin/kafka/logs/server.log 
```