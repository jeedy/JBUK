# 카프카 Mulit Server 설치
tags: kafka, aws, 설치, 가이드, 카프카

## 주키퍼 앙상블 셋팅

zookeeper-공통 config/zookeeper.properties : 
```bash
dataDir=/tmp/zookeeper
# the port at which the clients will connect
clientPort=2181
# disable the per-ip limit on the number of connections since this is a non-production config
maxClientCnxns=0
# multi setting require (앙상블 셋팅시 반드시 필요셋팅
initLimit=10
syncLimit=5
# setting servers
server.1=ip-172-31-41-231.ap-northeast-2.compute.internal:2888:3888
server.2=ip-172-31-45-231.ap-northeast-2.compute.internal:2888:3888
server.3=ip-172-31-39-41.ap-northeast-2.compute.internal:2888:3888

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