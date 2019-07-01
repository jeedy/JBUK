# Redis Replication

cluster는 sharding을 위한 것으로 replication 과는 다른 셋팅임. 

참고자료
- http://redisgate.kr/redis/server/redis_conf_han.php (config를 한글로 잘설명되어있다, 5.0버전 문서 UPDATE)
- 빅데이터 저장 및 분석을 위한 NoSQL & Redis (도서)
- https://ossian.tistory.com/37 (셋팅방법)
- https://crystalcube.co.kr/176
- 

## Replication 종류

1. Master-Slave 복제 시스템

    마스터에서 입력, 수정, 삭제를 하고 슬레이브는 마스터서버의 데이터를 실시간으로 복제한다. 그리고 슬레이브에서 조회만 한다.
    슬레이브는 오직 조회 작업만 수 행하고 마스터로 자동 전환(FailOver)가 되지 않는다. 마스터 서버가 장애가 발생하는 경우에도 
    슬레이브 서버에서는 지속적으로 조회가 가능하다.
 
1. Master-Slave-Sentinel 복제 시스템

    기본적인 구조는 위와 같다. 이 구성에서는 Sentinel 서버가 장애 모니터링 기능을 하고 마스터가 장애가 발생하면 슬레이브를 
    마스터로 승격시켜주는 역활을 한다. 
    sentinel 서버는 데이터를 저장하지 않고 단지 장애 모니터링과 failover 를 담당 하는 서버라 좋은 사양이 필요하지 않다.
    
    sentinel 서버에 장애가 발생하는 경우에 대비하여 sentinel 서버도 clustering를 구성할 수 있고 3대를 구성하는 것을 권장하고 있다.


## Master-Slave-Sentinel  구성방법
master slave가 sentinel에서 failover 를 해주더라도 client에서는 어떤서버가 master인지를 알수가 없다. 
lettuce 라이브러리를 사용할때 master, slave 주소를 모두 등록해 사용한다.

> lettuce 라이브러리 Redis Replication 접근 방법<br> 
> https://lettuce.io/core/release/reference/index.html#masterreplica.topology-updates

http://redisgate.kr/redis/configuration/replication.php

### 마스터 설정 (192.168.1.100)
redis-master.conf:
```bash 
port 5000
daemonize yes
replica-serve-stale-data yes

protected-mode yes -- yes: bind 나 password가 설정되지 않으면 local 에서만 접속이 가능, no: password 없어도 접속가능
bind 0.0.0.0 -- Redis Listen 대역 설정,  특정 IP들에 대한 접근만 허용할 경우 space(' ')를 구분자로 하여 여러개 입력가능

masterauth redis1234  -- [HA] Failover 발생시 다른 마스터 노드에 접근하기 위한 패스워드
requirepass redis1234 -- 슬레이브에서 접근시, 필수 패스워드

repl-ping-replica-period 10   -- 마스터와 동기화 주기 (초기 마스터라도 failover로 인해 slave가 될수 있으니 셋팅하는것으로 보인다.)
repl-timeout 60             -- 동기화 시도시 timeout 설정 (초기 마스터라도 failover로 인해 slave가 될수 있으니 셋팅하는것으로 보인다.)

repl-backlog-size 10mb  -- 최소 10mb, recommend 64mb, 이 설정이 없으면 master가 kill되고 다시 start 되었을때 데이터가 초기화 되면서 slave 데이터도 초기화 된다.
repl-backlog-ttl 3600   -- 마스터는 복제 서버와 연결 해재된 후 일정시간이 지나면 백로그 메모리를 해제(free)합니다.
# repl-diskless-sync yes -- (성능이 좋지 않아)disk를 사용하지 않을땐 repl-diskless-sync를 이용한다.
# repl-diskless-sync-delay 0  -- 바로 동기화하도록 0으로 셋팅한다.

pidfile /var/run/redis_5000.pid

pidfile /var/run/redis_5000.pid
dir ./repl/master/
logfile redis-server_5000.log
```

실행: 
```bash
$ ./src/redis-server ./redis-master.conf
```

### 슬레이브 설정 (192.168.1.101)
redis-slave.conf:
```bash
port 5001
daemonize yes
replica-serve-stale-data yes

# replicaof <masterip> <masterport>
replicaof 192.168.1.100 5000 -- Master IP Port

protected-mode yes
bind 0.0.0.0

masterauth redis1234           -- 마스터 노드 접근시, 패스워드 필요
requirepass redis1234          -- [HA] 만약, 현재의 슬레이브가 마스터로 승격후, 다른 슬레이브에서 접근시, 패스워드

repl-ping-replica-period 10   -- 마스터와 동기화 주기
repl-timeout 60             -- 동기화 시도시 timeout 설정

pidfile /var/run/redis_5001.pid
dir ./repl/slave/
logfile "redis-server_5001.log"
```

실행: 
```bash
$ ./src/redis-server ./redis-slave.conf
```


### Sentinel 설정(192.168.1.102)
http://redisgate.kr/redis/sentinel/sentinel_conf_han.php

sentinel.conf:
```bash
bind 0.0.0.0
protected-mode yes

port 5003
daemonize yes

pidfile /var/run/redis-sentinel_5003.pid
logfile "redis-sentinel_5003.log"
dir ./repl/sentinel/

# sentinel monitor <master-name> <redis-ip> <redis-port> <quorum> 
# quorum(쿼럼)은 레디스 마스터 서버가 다운되었을 때 몇 개의 센티널이 다운되었는지 인지해야 객관적으로 다운되었다고 판정하는 기준입니다.
sentinel monitor mymaster 192.168.1.100 5000 1      -- sentinel 이 한대일 경우 quorum은 '1' 값으로 셋팅해야 한다.
sentinel parallel-syncs mymaster 1              -- 장애조치(failover) 후 새 마스터로 부터 데이터를 받는데 몇 개 복제 노드에 한번 알려서 처리할지 정합니다
sentinel auth-pass mymaster redis1234           -- 센티널이 모니터하는 레디스 서버(마스터, 복제)에 암호(requirepass)를 설정
sentinel down-after-milliseconds mymaster 3000  -- 기본값은 30000(30sec)

```

실행: 
```bash
$ ./src/redis-sentinel ./sentinel.conf
```


### 복제 정보 확인

마스터 (192.168.1.100):
```bash
redis@node01 redis-2.8.8]$ redis-cli info replication
# Replication
role:master
connected_slaves:1
slave0:ip=192.168.1.101,port=6379,state=online,offset=7619005,lag=1
master_repl_offset:7619146
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:6570571
repl_backlog_histlen:1048576
```

슬레이브(192.168.1.101)
```bash
[redis@node02 redis-2.8.8]$ redis-cli info replication
# Replication
role:slave
master_host:192.168.1.100
master_port:6379
master_link_status:up
master_last_io_seconds_ago:1
master_sync_in_progress:0
slave_repl_offset:7624522
slave_priority:100
slave_read_only:1
connected_slaves:0
master_repl_offset:0
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0
```

Sentinel(192.168.1.102)
```bash
192.168.1.102:5003> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.1.100:5000,slaves=1,sentinels=1
```

*참고 자료: page 163. NoSQL&Redis Chapter 6, http://develop.sunshiny.co.kr/1005, https://ossian.tistory.com/37*


## :bomb: troubleshooting
1. Master 서버가 자신이 master인지 모를때
- redis.conf 파일에 `replicaof` 가 있는지 확인해볼것
- sentinel에서 failover 작동시 master conf 파일에 `replicaof` 값을 넣는다. `replicaof` 값이 있는 서버들은 모두 `slave`로 간주한다.

2. failover가 정상적이지 않을때
- sentinel.conf 파일안에 아래 속성들 전부 삭제하자 그리고 Master conf파일(redis.conf) 안에 `replicaof` 값이 있는지 확인하자  
```bash
sentinel config-epoch mymaster 2                    -- failover 일어날때마다 증가한다.
sentinel leader-epoch mymaster 2                    -- failover 일어날때마다 증가한다.
sentinel known-replica mymaster 127.0.0.1 5000      -- slave 를 나타낸다.
sentinel current-epoch 2                            -- failover 일어날때마다 증가한다.
```
