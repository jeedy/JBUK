# Kafka connector

### 목차
1. [카프카 connect source 구성 for mysql](/Kafka/connector/Kafka-source-connector-for-mysql.md)
1. [카프카 connect source 구성 for oracle](/Kafka/connector/Kafka-source-connector-for-oracle.md)
1. [카프카 connect sink 구성 for mysql](/Kafka/connector/Kafka-sink-connector-for-mysql.md)
1. [카프카 connect cluster 구성](/Kafka/connector/Kafka-connector-cluster.md)


## Kafka Connector REST Interface 
알아두면 유용한 Rest API 

reference:
- https://velog.io/@anjinwoong/Kafka-Connect-%EC%9E%90%EC%A3%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EB%8A%94-%EB%AA%85%EB%A0%B9%EC%96%B4API-%EC%A0%95%EB%A6%AC
- https://docs.confluent.io/platform/current/connect/references/restapi.html#kconnect-rest-interface


### Connector 

#### connector 목록 조회
```sh
curl -X GET "http://localhost:8083/connectors/"
```

#### connector 상세 정보 조회
```sh
curl -X GET "http://localhost:8083/connectors?expand=status&expand=info"
```

..TODO 작성필요