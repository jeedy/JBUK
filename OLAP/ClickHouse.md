# ClickHouse
tags: OLAP, spark, Apache Zeppelin, 빅데이터, bigdata, BigQuery, Firebase, analytic, ETL, database, Druid,

참고자료:
- [About ClickhHouse 1](https://medium.com/delightroom/clickhouse-%EA%B8%B0%EB%B0%98-%EB%B6%84%EC%84%9D-%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8-%EA%B5%AC%EC%B6%95-ea25b8ba43e9)
- [About ClickhHouse 2](http://whatdb.blogspot.com/2019/10/clickhouse.html)
- [ClickHouse 기본 문법](https://clickhouse.tech/docs/en/sql-reference/statements/select/sample/)
- [ClickHouse 설치방법](https://scorpio-mercury.tistory.com/27)
- [if(kakao)2020 clickhouse 사용기발표](https://tv.kakao.com/channel/3693125/cliplink/414129353)

## 개요
- 대용량 데이터를 빠르게 쿼리해주는 솔루션
- 러시아에서 만들었고 RDB 형태로 저장되는 듯하나 row단위가 아닌 column 단위로 저장하고 관리한다. 사용되는 쿼리는 mysql 쪽에 가깝다.
- 특이한점은 column type 에 array, nested 형태를 지원한다.(MongoDB와 비슷하다고 볼 수도 있겠다.)
- spark와 비교되기도 하지만 조금은 다른 RDB 과에 가깝다.
- 한국어로 된 문서는 찾아보기 힘들고 영어로된 [reference 페이지](https://clickhouse.tech/docs/en/) 는 꽤 잘되어있는 편
- 설치(clustering)는 어려워보이지 않음.
- 해당 솔루션이 가진 특성 때문인지 데이터 마이그레이션도 어렵지 않게 다양하게 제공한다.

결국 도입이 문제가 아닌 원하는 데이터를 추출하기 위한 insight가 필요하다.


## 설치 및 실행하기
하드웨어 환경: AWS, Amazon Linux 2

### 1. ClickHouse 설치

```sh
$ sudo yum install yum-utils
$ sudo rpm --import https://repo.clickhouse.tech/CLICKHOUSE-KEY.GPG
$ sudo yum-config-manager --add-repo https://repo.clickhouse.tech/rpm/stable/x86_64
$ sudo yum install clickhouse-server clickhouse-client

```

### 2. ClickHouse server 실행
```sh
#$ sudo /etc/init.d/clickhouse-server start
# Init script is already running
$ sudo systemctl start clickhouse-server

## server가 정상적으로 올라갔는지 확인해보자
$ sudo systemctl status clickhouse-server

# systemctl 로그 보기 https://twpower.github.io/171-journalctl-usage-and-examples
$ sudo journalctl -f -u clickhouse-server

## server stop 
$ sudo systemctl stop clickhouse-server
```
> 매뉴얼상에는 `/etc/init.d/clickhouse-server` 를 이용하도록 되어 있으나 Amazon Linux 2(레드핫, centos) 서버에서 start 할 경우 `Init script is already running` 라고 뜨면서 안 올라간다. 


### 3. ClickHouse client 실행
```sh
$ clickhouse-client
```

### 4. Clustering 셋팅

/etc/clickhouse-server/config.xml:
```xml
...
<!-- 모든 IP에서 접근 가능하도록(필수) -->
<listen_host>::</listen_host>
...

...
<!--  shard & replication 설정 -->
<jykim_2shard_1replicas>
    <shard>
        <replica>
            <host>ip-172-31-46-53.ap-northeast-2.compute.internal</host>
            <port>9000</port>
        </replica>
    </shard>
    <shard>
        <replica>
            <host>ip-172-31-43-111.ap-northeast-2.compute.internal</host>
            <port>9000</port>
        </replica>
    </shard>
</jykim_2shard_1replicas>
...
```

#### 4-1. shard clustering
- 데이터 분산 저장하고 읽어올땐 분산된 데이터에서 취합해서 준다.
- 취합을 하는 기준은 최초 요청을 받은 shard-1 node(Initiator Node)가 다른 shard-x node 들에게 쿼리를 전달해 주고 각각 역활을 맡은 shard-x node들은 Aggregates locally 해서 다시 Initiator Node 에게 전달해준다. Initiator Node는 이를 머지해서 최종 사용자에게 전달한다.

#### 4-2. Reqlication(복제) clustering
- 비동기 멀티마스터 복제방식
- Replica-1 node(Initiator Node) 가 사용자에게 입력을 받으면 바로 사용자에게 응받을 보내고 Background로 Replica-x node 로 copy가 진행된다. (그렇기 때문에 데이터를 저장한 직후 Replica-x node로 데이터를 요청하면 데이터가 없는 case가 생긴다.)
- 모든 Replica node들은 master가 될 수 있다. 즉 모든 서버가 insert가 가능하다.

#### 셋팅방법



### record
```sh
# sudo su -
$ sudo systemctl start clickhouse-server
$ sudo systemctl status clickhouse-server
$ sudo systemctl stop clickhouse-server

# systemctl 로그 보기 https://twpower.github.io/171-journalctl-usage-and-examples
$ sudo journalctl -f -u clickhouse-server

$ curl "https://play-api.clickhouse.tech:8443/?query=SELECT+*+from+hits_100m_obfuscated+limit+10;&user=playground&password=clickhouse&database=datasets"

$ clickhouse-client
$ clickhouse-client --query "CREATE DATABASE IF NOT EXISTS tutorial"
$ clickhouse-client --query "INSERT INTO tutorial.hits_v1 FORMAT TSV" --max_insert_block_size=100000 < hits_v1.tsv

$ sudo chmod 600 /etc/clickhouse-server/config.xml
$ sudo vim /etc/clickhouse-server/config.xml
```

```sql
-- 
select count(*) from hits_100m_obfuscated;


CREATE TABLE tutorial.hits_local
(
    `WatchID` UInt64,
    `JavaEnable` UInt8,
    `Title` String,
    `GoodEvent` Int16,
    `EventTime` DateTime,
    `EventDate` Date,
    -- ...
    `RequestNum` UInt32,
    `RequestTry` UInt8
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(EventDate)
ORDER BY (CounterID, EventDate, intHash32(UserID))
SAMPLE BY intHash32(UserID)
SETTINGS index_granularity = 8192;



CREATE TABLE tutorial.hits_all AS tutorial.hits_local
ENGINE = Distributed(jykim_2shard_1replicas, tutorial, hits_local, rand());

```