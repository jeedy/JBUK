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


## Connector 

### connector 목록 조회
```sh
curl -X GET "http://localhost:8083/connectors/"
```

### connector 상세 정보 조회
```sh
curl -X GET "http://localhost:8083/connectors?expand=status&expand=info"
```

### connector config 조회
> GET 으로도 동일하게 동작함
```sh
curl -X PUT "http://localhost:8083/connectors/{connector_name}/config
```

### 특정 connector 상태 조회
```sh
curl -X GET "http://localhost:8083/connectors/{connector_name}/status"
```

### connector 재시작
> ※ task는 재시작되지 않음
```sh
curl -X POST "http://localhost:8083/connectors/{connector_name}/restart"
```

### connector 일시중지(pause)
> 비동기 방식이므로 상태 조회시 바로 PAUSE 를 리턴하지 않을 수 있음
```sh
curl -X PUT "http://localhost:8083/connectors/{connector_name}/pause"
```

### connector 복귀 (resume)
> - pause 상태인 connector 를 복귀시킨다.     
> - 비동기 방식이므로 상태 조회시 바로 RUNNING을 리턴하지 않을 수 있음
```sh
curl -X PUT "http://localhost:8083/connectors/{connector_name}/resume"
```

### connector 삭제
```sh
curl -X DELETE "http://localhost:8083/connectors/{connector_name}
```

-----

## Task

### connector의 task 목록 조회
```sh
curl -X GET "http://localhost:8083/connectors/{connector_name}/tasks"
```

### connector 의 task 상태 조회
```sh
curl -X GET "http://localhost:8083/connectors/{connector_name}/tasks/{task_id}/status"
```

### connector 의 task 재시작
> ※ connector 가 RUNNING, task 가 FAIL 일 경우 사용
```sh
curl -X POST "http://localhost:8083/connectors/{connector_name}/tasks/{task_id}/restart"
```

-----

## Topic

### connector topic 조회
```sh
curl -X GET "http://localhost:8083/connectors/{connector_name}/topics"
```

### connector topic reset
```sh
curl -X PUT "http://localhost:8083/connectors/{connector_name}/topics/reset"
```

-----


## Connector Plugin

### Kafka Connector Cluster 에 설치된 모든 plugin 목록 조회
```sh
curl -X GET "http://localhost:8083/connector-plugins"
```

### Kafka Connector plgin validate
> - ※ plugin 종류에 따라 필수 field가 다를 수 있음 
> - ex) FileStreamSinkConnector 로 test-topic 에 대해 validate 할 경우
```sh
echo '{"connector.class": "org.apache.kafka.connect.file.FileStreamSinkConnector", "tasks.max": "1", "topics": "test-topic"}' | curl -X PUT -d -@ "http://localhost:8083/connector-plugins/FileStreamSinkConnector/config/validate
```

