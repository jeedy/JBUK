# Redis

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

### 2. 직접 Local에 설치(비추)
```bash
$ wget http://download.redis.io/releases/redis-5.0.5.tar.gz
$ tar xzf redis-5.0.5.tar.gz
$ sudo chown -R ec2-user:ec2-user redis-5.0.5
$ cd redis-5.0.5
$ make

```

## 실행
```bash
$ ./redis-server
$ ps aux | grep redis-server
```

## Redis Client (redisdesktop for mac)
```bash
$ brew cask install rdm
```