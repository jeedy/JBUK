# Kafka connector

### 목차
1. [카프카 connect source 구성 for mysql](/Kafka/connector/Kafka-source-connector-for-mysql.md)
1. [카프카 connect source 구성 for oracle](/Kafka/connector/Kafka-source-connector-for-oracle.md)
1. [카프카 connect sink 구성 for mysql](/Kafka/connector/Kafka-sink-connector-for-mysql.md)
1. [카프카 connect cluster 구성](/Kafka/connector/Kafka-connector-cluster.md)

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