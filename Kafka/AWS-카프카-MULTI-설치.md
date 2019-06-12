# 카프카 Mulit Server 설치
tags: kafka, aws, 설치, 가이드, 카프카

### 참고자료
- https://kafka.apache.org/quickstart (카프카 퀵스타트 가이드 문서)
- https://arisu1000.tistory.com/27786 (클러스터 구축)
- https://epicdevs.com/20 (클러스터 구성 셋팅)
- https://engkimbs.tistory.com/560 (주키퍼 앙상블 셋팅)
- https://zookeeper.apache.org/doc/r3.1.2/zookeeperStarted.html (주키퍼 started guide)

## 주키퍼 앙상블 셋팅

zookeeper-공통 config/zookeeper.properties : 
```bash
# tick 단위 시간을 설정, milliseconds 단위. 위에서는 2초로 설정됨  (기본값 2000ms)
# tickTime=2000

# zookeeper가 사용할 데이터 디렉토리
# 주키퍼의 상태, 스냅션, 트랜잭션 로그들을 저장하고 업데이트하는 디렉토리의 위치를 지정
dataDir=/tmp/zookeeper 

# the port at which the clients will connect
# zookeeper가 사용할 포트, 클라이언트 연결을 감지하는 포트의 번호
clientPort=2181 

# disable the per-ip limit on the number of connections since this is a non-production config
# 하나의 클라이언트에서 동시접속하는 개수 제한. 기본은 60. (0으로 두면 무제한)
maxClientCnxns=0 

# multi setting require (앙상블 셋팅시 반드시 필요셋팅)
initLimit=10  #처음 주키퍼의 follower가 leader와의 연결 시도시 가지는 tick 제한 횟수. tick 제한 횟수가 넘으면 timeout. 위에서는 20초로 설정됨  
syncLimit=5   #follower가 leader와 연결된 후, 계속 ensemble 안에서 leader와 동기화되기 위한 tick 제한 횟수. tick 제한 횟수가 넘으면 timeout 위에서는 10초로 설정됨.

# setting servers
server.1=ip-172-31-41-231.ap-northeast-2.compute.internal:2888:3888  #server.id=host:port:port
server.2=ip-172-31-45-231.ap-northeast-2.compute.internal:2888:3888  #server.id=host:port:port
server.3=ip-172-31-39-41.ap-northeast-2.compute.internal:2888:3888   #server.id=host:port:port

```

zookeeper-1 /tmp/zookeeper/myid 파일생성 :
```bash
$ echo 1 > /tmp/zookeeper/myid
$ cat /tmp/zookeeper/myid
1
``` 
zookeeper-2 /tmp/zookeeper/myid 파일생성 :
```bash
$ echo 2 > /tmp/zookeeper/myid
$ cat /tmp/zookeeper/myid
2
``` 
zookeeper-3 /tmp/zookeeper/myid 파일생성 :
```bash
$ echo 3 > /tmp/zookeeper/myid
$ cat /tmp/zookeeper/myid
3
``` 

## 주키퍼 스타트

```bash
$ bin/zookeeper-server-start.sh config/zookeeper.properties
[2013-04-22 15:01:37,495] INFO Reading configuration from: config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
...

```

## 카프카 클러스터 셋팅

kafka-0 config/server.properties
```bash

# The id of the broker. This must be set to a unique integer for each broker.
broker.id=0
...
# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
# 외부에서 접근하려면 public DNS 주소를 입력해야한다.
advertised.listeners=PLAINTEXT://public-ip-52.79.116.39.compute.internal:9092
...
# A comma separated list of directories under which to store log files (broker.id 값이 이 로그에 기록되기 때문에 이미 구축했었다면 다른 폴더로 생성해야한다.)
log.dirs=/tmp/kafka-logs-cluster
...
# Zookeeper connection string (see zookeeper docs for details).
# This is a comma separated host:port pairs, each corresponding to a zk
# server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
# You can also append an optional chroot string to the urls to specify the
# root directory for all kafka znodes.
zookeeper.connect=ip-172-31-41-231.ap-northeast-2.compute.internal:2181,ip-172-31-45-231.ap-northeast-2.compute.internal:2181,ip-172-31-39-41.ap-northeast-2.compute.internal:2181
...
```

kafka-1 config/server.properties
```bash

# The id of the broker. This must be set to a unique integer for each broker.
broker.id=1
...
# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
# 외부에서 접근하려면 public DNS 주소를 입력해야한다.
advertised.listeners=PLAINTEXT://public-ip-54.180.117.24.compute.internal:9092
...
# A comma separated list of directories under which to store log files (broker.id 값이 이 로그에 기록되기 때문에 이미 구축했었다면 다른 폴더로 생성해야한다.)
log.dirs=/tmp/kafka-logs-cluster
...
# Zookeeper connection string (see zookeeper docs for details).
# This is a comma separated host:port pairs, each corresponding to a zk
# server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
# You can also append an optional chroot string to the urls to specify the
# root directory for all kafka znodes.
zookeeper.connect=ip-172-31-41-231.ap-northeast-2.compute.internal:2181,ip-172-31-45-231.ap-northeast-2.compute.internal:2181,ip-172-31-39-41.ap-northeast-2.compute.internal:2181
...
```

kafka-2 config/server.properties
```bash

# The id of the broker. This must be set to a unique integer for each broker.
broker.id=2
...
# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
# 외부에서 접근하려면 public DNS 주소를 입력해야한다.
advertised.listeners=PLAINTEXT://public-ip-52.79.226.201.compute.internal:9092
...
# A comma separated list of directories under which to store log files (broker.id 값이 이 로그에 기록되기 때문에 이미 구축했었다면 다른 폴더로 생성해야한다.)
log.dirs=/tmp/kafka-logs-cluster
...
# Zookeeper connection string (see zookeeper docs for details).
# This is a comma separated host:port pairs, each corresponding to a zk
# server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
# You can also append an optional chroot string to the urls to specify the
# root directory for all kafka znodes.
zookeeper.connect=ip-172-31-41-231.ap-northeast-2.compute.internal:2181,ip-172-31-45-231.ap-northeast-2.compute.internal:2181,ip-172-31-39-41.ap-northeast-2.compute.internal:2181
...
```

## 카프카 스타트
```bash
$ bin/kafka-server-start.sh config/server.properties
```