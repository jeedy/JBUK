# 레디스 서버 설치방법
tag: redis, 레디스, 설치, install 

## 필요 스팩
- 운영이라면 최소한 8G 이상의 램을 요구한다.(8램이하일 경우 서버 올릴때 경고 메시지 나온다)

## 설치방법

### 1. docker를 통한 설치 (추천)

    - [Docker 설치](https://docs.docker.com/install/)
    - Redis 3.2 서버 이미지 다운로드 후 Run

```bash
$ docker run -d -name dispatch-redis -p 6379:6379 redis:3.2
b85e3cb2ddc....(docker_container_id)
$ docker exec dispatch-redis redis-cli ping
pong
```

### 2. 직접 Local에 설치
설치 폴더 `/usr/local/`에 설치하는 기준으로 설명

```bash
$ cd /usr/local/
$ wget http://download.redis.io/releases/redis-5.0.5.tar.gz
$ tar xzf redis-5.0.5.tar.gz
$ sudo chown -R ec2-user:ec2-user redis-5.0.5
$ cd redis-5.0.5
$ make

```

#### 서버 직접 실행
```bash
$ cd /usr/local/redis-5.0.5/
# ./src/redis-server ./redis.conf --daemonize yes 데몬으로 background 로 띄울경우
$ ./src/redis-server ./redis.conf

# 프로세스확인
$ ps aux | grep redis-server
```

## 3. 포트 확인
```bash
# 포트확인
$ netstat -nlpt | grep 6379
```


## 셋팅
기본적으로 제공하는 `redis.conf` 파일을 수정한다.

### 1. 외부 접근을 위한 셋팅
외부 IP에서 접근을 위해선 서버를 실행할 때 `bind` 값 수정이 필요하다. (인증암호 `requirepass` 도 설정해야한다는 문서도 있지만 실제로 해보니 필요 없이 외부에서 접근가능하다.)

./redis.conf:
```sh
# bind 172.0.0.1
bind 0.0.0.0 
```

#### 외부 접속 테스트
```
# redis-cli -h <redis 서버 ip> -p <redis port> -a <password>
$ redis-cli -h 192.168.2.1 -p 6379
```
