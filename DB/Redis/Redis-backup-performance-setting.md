# 레디스 백업 및 성능 셋팅관련

## backup
레디스는 `RDB` 방식과 `AOF(Append Only File)`을 지원한다.

### RDB
`dump.rdb` 파일에 어느 시점에 데이터 (스냅샷) 처럼 저장한다.<br>
`save`, `bgsave` 명령어를 통해 동작하고 redis.conf 파일에 기본적으로 사용함(`save 명령어`)으로 셋팅되어있다.

redis.conf:
```bash
dbfilename dump.rdb  -- 저장될 파일명

# save <Seconds> <changes>
save 900 1           -- 900초 안에 1번 변경이 있었을 때
save 300 10          -- 300초 안에 10번의 변경이 있었을 때
save 60 10000        -- 60초 안에 10,000번의 변경이 있었을 때
```

### AOF (Append Only File)
수행할 명령어(set,del) 히스토리를 저장해두고, 장애가 발생하면 AOF를 기반으로 복구한다.(기본적으로 `사용안함` 으로 되어있다.)

redis.conf:
```bash
appendonly yes                      -- aof를 사용할 경우 yes, default no
appendfilename appendonly.aof       -- aof 파일명

appendfsync everysec                -- 디스크와 동기화를 얼마나 자주할지, 속도: "no" > "everysec" > "alway"
```
AOF를 파일에 저장할 때, OS가 파일쓰기 시점을 결정하여 파일을 버퍼 캐시(메모리)에 저장하고 적절한 시점에 데이터를 디스크로 
정장한다. `appendfsync`는 디스크와 동기화를 얼마나 자주 할 것인지에 대해서 설정하는 값으로, 다음과 같이 세 가지가 있다.

**appendfsync**
- always   : AOF값을 추가할 때마다 fsync를 호출해서 디스크에 실제 쓰기를 한다.
- everysec : 매초마다 fsync를 호출해서 디스크에 실제 쓰기를 한다.
- no       : OS가 실제 sync를 할 때까지 따로 설정하지 않는다.



## 레디스는 몇 램을 사용해야할까?
Redis 자체는 64bit에서 메모리를 다루기 때문에 한계는 없다. (다만 Key, Value는 각각 512MB 한계)

다음과 같은 기준으로 할당할 것을 추천 (*참고 자료: page 30. Redis 운영관리 2장 Redis 운영과 관리*)

예를들어 Core 4, RAM 32GB 장비라면, 프로세스 별로(레디스는 싱글쓰레드) 6GB 정도를 할당 하는 것이 좋다. (4 * 6 = 24GB)
멀티 코어를 사용하는 PC라면 하나의 장비에 core 갯수만큼 redis를 셋팅하는것이 성능면에서 좋다.

여러 개의 reids 서버를 한 서버에 띄우면, RDB 저장으로 인해서 자식 프로세스가 생성된다. 즉 프로세스 4개와 RDB용 저장 프로세스를
합쳐 총 5개의 프로세스가 생성되더라도, 30GB(=프로세스 5 * 6GB)만 사용하므로 메모리에 여유가 있다.

### 데이터를 통한 접근
실제 RAM 사용량이 얼마나 될지 계산 필요

https://redis.io/commands/memory-usage

 

## Redis 복제를 이용한 실시간 마이그레이션
1. 데이터 이전을 위한 새로운 Redis 인스턴스 실행

2. 새로운 Redis 인스턴스를 기존 마스터의 슬레이브로 설정한다.
```bash
# 기존 마스터 IP Port
redis new-redis-ip:6379> slaveof 127.0.0.1 6379
``` 
3. 새로운 장비의 `slave-read-only` 설정을 끈다.
기본적으로 슬레이브는 `slave-read-only`로 설정되는데, 이 기능을 꺼서 슬레이브에서도 업데이트가 가능하도록 설정한다. 다만
슬레이브의 변경이 마스터로 전달되지는 않는다.
```bash
redis new-redis-ip:6379> config set slave-read-only no
```
4. 클라이언트들이 새로운 Redis 인스턴스를 마스터로 인식하도록 설정을 바꾼다.
```bash
# 새로운 마스터 IP Port
redis redis-slave:6379> slaveof 127.0.0.2 6379
```

5. `salveof no one` 명령을 이용하여 새로운 Redis 인스턴스와 기존 마스터와의 연결을 종료한다.
이 작업을 하기 전에, 기존 마스터 장비에 더는 요청이 없다는 것을 확인해야 한다. 
```bash
redis new-redis-ip:6379> slaveof no one
```

6. 기존 마스터 장비를 제거한다.


## Redis 모니터링 툴

- https://github.com/junegunn/redis-stat






## :bomb: troubleshooting

### 1. Read는 가능한데 Write만 실패하는 경우
정기적인 Heartbeat 체크(PING)에는 이상없으나 write는 실패하는 경험(99% 경험한다고한다) 원인은 RDB 저장이 실패할 때,
기본 설정상 **RDB 저장이 실패하면** 해당 자비에 뭔가 이상이 있다고 생각하여 Write 명령을 더는 처리하지 않으며, 데이터가 변경되지
않도록 관리한다. 

**RDB 저장이 실패하는 경우**
1. RDB를 저장할 수 있을 정도의 디스크 여유 공간이 없는 경우
1. 실제 디스크가 고장 난 경우
1. 메모리 부족으로 인해서 자식 프로세스를 생성하지 못한 경우
1. 누군가 강제적으로 자식 프로세스를 종료시킨 경우
1. 그외 기타

위의 이유 등으로 RDB 저장을 실패하면 Redis 내부의 'lastbgsave_status' 라는 변수가 `REDIS_ERR`로 설정된다. 그러면 'processCommand'
라는 함수에서 사용자 요청이 들어왔을 때 Write 관련 요청은 모두 무시하게 된다.(src/redis.c)<br>
그리고 lastbgsave_status 값은 src/rdb.c의 'backgroundSaveDoneHandler'에서 처리된다.

#### RDB 저장시 오류확인 방법

redis-cli:
```bash
$ redis-cli -p 5000 -a redis1234

redis 172.0.0.1:5000> set a 123
(error) MISCONF Redis is configured to save RDB snapshots, but is ...


redis 172.0.0.1:5000> info
...

# Persistence
rdb_last_bgsave_status:ok
...
```

#### 해결방법
1. 이미 운영 중인 Redis 서버에서 변경하는 방법
```bash
redis 172.0.0.1:5000> config set stop-writes-on-bgsave-error no
OK
```
2. redis.conf에 미리 등록하는 방법 (redis 2.6.13 버전 이후)
redis.conf:
```bash
# 기본적으로는 stop-writes-on-bgsave-error yes로 되어 있음
stop-writes-on-bgsave-error no
```
해당 장애를 많이 격는이유는 conf로 지정하는 방법이 없을뿐더러, 1번을 사용하는 방법을 잊어버리는 경우가 많아 장애가 많았다.


### 2. Redis가 메모리를 두 배로 사용하는 문제
Redis가 운영되는 중에 장애를 일으키는 가장 큰 원인은 RDB를 저장하는 Persistent기능으로, Fork를 사용하기 때문이다. 그럼, fork를
 사용하는 것이 왜 문제가 될까? 이전에는 운영체제가 자식 프로세스를 생성하면, 부모 프로세스의 메모리를 모두 자식 프로세스에 복사해야
 했다. 예를 들어, 부모 프로세스가 10GB 메모리를 사용중이라면 자식 프로세스를 생성할 때 10GB의 메모리가 추가로 필요했다.
 
 시간이 자나고 OS가 발전하여 'COW:copy on write' 라는 기술이 개발되었다. 이에 따라 fork 후, 자식 프로세스와 부모 프로세스의 메모리에서
 실제로 변경이 발생한부분마나 차후에 복사하게 되었다. 하지만 Redis와 같은 솔루션을 사용하는 곳은 대부분 Write가 많으므로 예전의 경우와
 마찬가지로 메모리를 두 배로 사용하는 경우가 생긴다.
 
 
### 3. Redis Connection pool 설정 변경

#### Situation
간혈적으로 connection confuse 가 발생한다는 보고를 받아 확인.
확인해본 결과 timeout Exception이였음.

추가
Error 로그를 확인해보니 특정 테이블에 데이터를 모두 가져오려고함(예: tablekey:\*), 추후 테이블이 커질수로 위와 같은 오류를 발생할 수 있는 여지가 있음 (* 레디스에선 저렇게 한번에 가져오는 명령어는 비추천함
참고:
https://charsyam.wordpress.com/2013/05/19/입-개발-redis-데이터-모델링시에-주의할점/


#### Action
- Jedis Connection Pool 설정 변경
- Jedis(redis라이브러리) timeout default 2000ms

다량의 사용량이 발생할때 Idle pool을 가져오는 부분에서 time out이 발생 할수 있다.

참고:
- http://kwonnam.pe.kr/wiki/nosql/redis
- https://stackoverflow.com/questions/29305418/jedis-connection-settings-for-high-performance-and-reliablity


timeout 설정을 바꿔서 테스트 해볼것.
(*redis conf 설정은 기본값으로 0ms 로 설정으로 되어있다. 0은 timeout 기능을 사용하지 않는다는 뜻이다.
그러나 이를 또 통제하는 parameter 값이 있는데 그것은 "tcp-keepalive". 기본값은 300 seconds)

참고: 
- http://redisgate.kr/redis/configuration/param_timeout.php
- ttp://redisgate.kr/redis/configuration/param_tcp-keepalive.php
- http://download.redis.io/redis-stable/redis.conf

##### redis config 상태 보는 법
client console (rdm 또는 redis-cli) 실행 후 아래 명령어 실행

```bash
> config get *
```

##### redis 서버 상태 확인(info)
client console (rdm 또는 redis-cli) 실행 후 아래 명령어 실행

```bash
> info
```
