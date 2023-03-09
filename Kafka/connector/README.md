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
curl -X GET "http://localhost:8083/connectors/{connector_name}/config
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

------


# :bomb: troubleshooting
## 1. Setting Sentry-log4j for Kafka connector 
- Sentry는 1.7.x 이후 부터 log4j2만 지원 (*log4j는 더이상 지원x)
- kafka connector 는 아직 log4j 사용

#### ref
- https://docs.sentry.io/platforms/java/legacy/log4j/
- https://docs.sentry.io/platforms/java/legacy/configuration/

### Legacy SDK (1.7)버전으로 설치 진행

1. kafka lib 폴더에 [sentry-1.7.30.jar](../asset/sentry-1.7.30.jar), [sentry-log4j-1.7.30.jar](../asset/sentry-log4j-1.7.30.jar) 복사
```sh
# kafka lib 폴더에 sentry-1.7.30.jar, sentry-log4j-1.7.30.jar 복사
root@66880a74b37f:/opt/kafka/libs# ls -al
total 70100
drwxr-xr-x 1 root root     4096 Mar  9 11:50 .
drwxr-xr-x 1 root root     4096 Feb 16 14:41 ..
-rw-r--r-- 1 root root    69409 Oct 15  2019 activation-1.1.1.jar
-rw-r--r-- 1 root root    27006 Jun 29  2020 aopalliance-repackaged-2.6.1.jar
..(생략)
-rw-r--r-- 1 root root   180927 Mar  9 11:50 sentry-1.7.30.jar
-rw-r--r-- 1 root root     7344 Mar  9 10:45 sentry-log4j-1.7.30.jar
..(생략)
-rw-r--r-- 1 root root    41472 Jan 12  2020 slf4j-api-1.7.30.jar
-rw-r--r-- 1 root root    12211 Jan 12  2020 slf4j-log4j12-1.7.30.jar
-rw-r--r-- 1 root root  1952778 Dec  2  2020 snappy-java-1.1.8.1.jar
-rw-r--r-- 1 root root   994800 Jan 29  2021 zookeeper-3.5.9.jar
-rw-r--r-- 1 root root   250557 Jan 29  2021 zookeeper-jute-3.5.9.jar

```


2. log4j sentry appender 추가
```sh
root@66880a74b37f:/opt/kafka/bin# vim ../config/connect-log4j.properties

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# (추가된) sentryAppender
log4j.rootLogger=INFO, stdout, connectAppender, sentryAppender

# Send the logs to the console.
#
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout

# Send the logs to a file, rolling the file at midnight local time. For example, the `File` option specifies the
# location of the log files (e.g. ${kafka.logs.dir}/connect.log), and at midnight local time the file is closed
# and copied in the same directory but with a filename that ends in the `DatePattern` option.
#
log4j.appender.connectAppender=org.apache.log4j.DailyRollingFileAppender
log4j.appender.connectAppender.DatePattern='.'yyyy-MM-dd-HH
log4j.appender.connectAppender.File=${kafka.logs.dir}/connect.log
log4j.appender.connectAppender.layout=org.apache.log4j.PatternLayout

# (추가된) Sentry log4j appender 
log4j.appender.sentryAppender=io.sentry.log4j.SentryAppender
log4j.appender.sentryAppender.Threshold=ERROR


# The `%X{connector.context}` parameter in the layout includes connector-specific and task-specific information
# in the log message, where appropriate. This makes it easier to identify those log messages that apply to a
# specific connector. Simply add this parameter to the log layout configuration below to include the contextual information.
#
connect.log.pattern=[%d] %p %m (%c:%L)%n
#connect.log.pattern=[%d] %p %X{connector.context}%m (%c:%L)%n

log4j.appender.stdout.layout.ConversionPattern=${connect.log.pattern}
log4j.appender.connectAppender.layout.ConversionPattern=${connect.log.pattern}
log4j.appender.sentryAppender.layout.ConversionPattern=${connect.log.pattern}

log4j.logger.org.apache.zookeeper=ERROR
log4j.logger.org.reflections=ERROR
```


3. java system 환경변수에 sentry dns 추가

```sh
root@66880a74b37f:/opt/kafka/bin# vim connect-distributed.sh

#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ $# -lt 1 ];
then
        echo "USAGE: $0 [-daemon] connect-distributed.properties"
        exit 1
fi

base_dir=$(dirname $0)

if [ "x$KAFKA_LOG4J_OPTS" = "x" ]; then
    export KAFKA_LOG4J_OPTS="-Dlog4j.configuration=file:$base_dir/../config/connect-log4j.properties"
fi

## logging 타임존 한국날짜로 -Duser.timezone=Asia/Seoul, sentry dsn 추가 by kimjy
if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
  export KAFKA_HEAP_OPTS="-Xms256M -Xmx2G -Duser.timezone=Asia/Seoul -Dsentry.dsn=https://4de2123063d4492fb85c9101ec0bdb64@o4504512854818816.ingest.sentry.io/4504806154502144"
fi

EXTRA_ARGS=${EXTRA_ARGS-'-name connectDistributed'}

COMMAND=$1
case $COMMAND in
  -daemon)
    EXTRA_ARGS="-daemon "$EXTRA_ARGS
    shift
    ;;
  *)
    ;;
esac

exec $(dirname $0)/kafka-run-class.sh $EXTRA_ARGS org.apache.kafka.connect.cli.ConnectDistributed "$@"

```

4. 재기동
```sh
root@66880a74b37f:/opt/kafka/bin# jobs
[1]+  Running                 nohup connect-distributed.sh /opt/kafka/config/connect-distributed.properties &
root@66880a74b37f:/opt/kafka/bin# kill %1
[1]+  Exit 143                nohup connect-distributed.sh /opt/kafka/config/connect-distributed.properties

root@66880a74b37f:/opt/kafka/bin# nohup connect-distributed.sh /opt/kafka/config/connect-distributed.properties &
```
