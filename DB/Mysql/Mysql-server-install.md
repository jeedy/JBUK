# Mysql 서버 설치 방법

## Docker로 설치
> [도커 설치](/Docker/Docker-설치.md)

## MySQL 이미지 검색

> docker search <검색어>

```bash
$ docker search mysql
```

## 테크명 알아 보기

> *jq 설치 필요*

```bash
$ wget -qO- https://registry.hub.docker.com/v1/repositories/mysql/tags | jq '.[].name'
```

## 설치 및 실행

### 환경 변수

- --name : 이미지의 이름
- -e, --env=[] : 설정값
- -d, --detach=false : 컨테이너를 백그라운드 실행, 이 옵션을 안 넣어 주면 실행상태에서 바로 꺼진 상태로 들어 가게 됨
- -p, --publich=[] : 컨테이너의 포트를 호스트로 사용 합니다.
- -v, --volume=[] : 호스트의 파일을 컨테이너 위치로 연결 합니다.
    > 데이터베이스를 띄우지만, 그냥 사용하게 되면, 컨테이너 이미지 안에 파일을 저장합니다.
    > 호스트파일에 저장 할려면, --volume(or -v)이라는 옵션을 사용해야 합니다.

```bash
$ docker \ 
    run \ 
    --detach \ 
    --volume /opt/mysql:/var/lib/mysql \ 
    --env MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} \ 
    --env MYSQL_USER=${MYSQL_USER} \ 
    --env MYSQL_PASSWORD=${MYSQL_PASSWORD} \ 
    --env MYSQL_DATABASE=${MYSQL_DATABASE} \ 
    --name ${MYSQL_CONTAINER_NAME} \ 
    --publish 3306:3306 \ 
    --name mysql-volume \ 
    mysql:latest;
```
> /opt/mysql 경로에 mysql의 db가 생성 된 것을 확인 할 수 있습니다.

## 컨테이너에서 mysql실행 확인

```bash
$ docker exec -i -t mysql-volume bash
(mysql 실행하여 로그인 한다)
root@1d458d3c99b9:/$ mysql -u mysql_user -p sample_db
```


참조 http://hunp.tistory.com/7?category=567302

