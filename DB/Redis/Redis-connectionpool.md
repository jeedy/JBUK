# Redis Connection pool 설정 변경

## Situation
간혈적으로 connection confuse 가 발생한다는 보고를 받아 확인.
확인해본 결과 timeout Exception이였음.

추가
Error 로그를 확인해보니 특정 테이블에 데이터를 모두 가져오려고함(예: tablekey:*), 추후 테이블이 커질수로 위와 같은 오류를 발생할 수 있는 여지가 있음 (* 레디스에선 저렇게 한번에 가져오는 명령어는 비추천함
참고:
https://charsyam.wordpress.com/2013/05/19/입-개발-redis-데이터-모델링시에-주의할점/


## Action

- Jedis Connection Pool 설정 변경

다량의 사용량이 발생할때 Idle pool을 가져오는 부분에서 time out이 발생 할수 있다.

참고:

http://kwonnam.pe.kr/wiki/nosql/redis

https://stackoverflow.com/questions/29305418/jedis-connection-settings-for-high-performance-and-reliablity

- Jedis(redis라이브러리) timeout default 2000ms

timeout 설정을 바꿔서 테스트 해볼것.

(*redis conf 설정은 기본값으로 0ms 로 설정으로 되어있다. 0은 timeout 기능을 사용하지 않는다는 뜻이다.

그러나 이를 또 통제하는 parameter 값이 있는데 그것은 "tcp-keepalive". 기본값은 300 seconds

참고: http://redisgate.kr/redis/configuration/param_timeout.php

http://redisgate.kr/redis/configuration/param_tcp-keepalive.php

http://download.redis.io/redis-stable/redis.conf

redis config 상태 보는 법

client console (rdm 또는 redis-cli) 실행 후 아래 명령어 실행

```
> config get *
```

redis info

client console (rdm 또는 redis-cli) 실행 후 아래 명령어 실행

```
> info
```
)