# Redis Replication

## Replication 종류

### 1. Master-Slave 복제 시스템

마스터에서 입력, 수정, 삭제를 하고 슬레이브는 마스터서버의 데이터를 실시간으로 복제한다. 그리고 슬레이브에서 조회만 한다.
슬레이브는 오직 조회 작업만 수 행하고 마스터로 자동 전환(FailOver)가 되지 않는다. 마스터 서버가 장애가 발생하는 경우에도 
슬레이브 서버에서는 지속적으로 조회가 가능하다.
 
### 2. Master-Slave-Sentinel 복제 시스템

기본적인 구조는 위와 같다. 이 구성에서는 Sentinel 서버가 장애 모니터링 기능을 하고 마스터가 장애가 발생하면 슬레이브를 
마스터로 승격시켜주는 역활을 한다. 
sentinel 서버는 데이터를 저장하지 않고 단지 장애 모니터링과 failover 를 담당 하는 서버라 좋은 사양이 필요하지 않다.

sentinel 서버에 장애가 발생하는 경우에 대비하여 sentinel 서버도 clustering를 구성할 수 있고 3대를 구성하는 것을 권장하고 있다.


## master - slave - sentinel  구성방법
master slave가 sentinel에서 failover 를 해주더라도 client에서는 어떤서버가 master인지를 알수가 없다. 
lettuce 라이브러리를 사용할때 master, slave 주소를 모두 등록해 사용한다.

https://lettuce.io/core/release/reference/index.html#masterreplica.topology-updates

master/redis-master.conf:
```bash 

```
