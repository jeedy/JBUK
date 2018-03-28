도커
========

참고
- ``블로그`` [초보를 위한 도커 안내서 - 도커란 무엇인가?](https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html)
- ``도서`` [시작하세요! 도커](http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=9791158390617&orderClick=LAG&Kc=)

## 설치
[도커 설치 방법](/Docker/Docker-설치.md)

## 기본 명령어

### $ docker images
> 이미지 이름이 \<none> 인 댕글링(dangling) 이미지 리스트 확인방법
> `$ docker images -f dangling=true`
> 사용 중이지 않은 댕글링 이미지 삭제
> `$ docker images prune`

```sh
$ docker images
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
wordpress                   latest              b1fe82b15de9        43 hours ago        400.2 MB
ubuntu                      16.04               104bec311bcd        4 weeks ago         129 MB
```

### $ docker search 검색어
도커 이미지 검색

```bash
$ docker search mysql
```

#### 태그명 알아 보기

> *jq 설치 필요*

```bash
$ wget -qO- https://registry.hub.docker.com/v1/repositories/mysql/tags | jq '.[].name'
```

### $ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
container를 pull 하고 create 하고 start 한다.
> run flow : docker pull(이미지가 없다면) -> docker create -> docker start -> docker attack(-i-t 옵션을 사용했을 때)

- --name : 이미지의 이름
- -e, --env=[] : 설정값
- -it : -i와 -t를 동시에 사용한 것으로 터미널 입력을 위한 옵션
- -rm : 프로세스 종료시 컨테이너 자동 제거
- -d, --detach=false : 컨테이너를 백그라운드 실행, 이 옵션을 안 넣어 주면 실행상태에서 바로 꺼진 상태로 들어 가게 됨
- -p, --publich=[] : 컨테이너의 포트를 호스트로 사용 합니다.
- -v, --volume=[] : 호스트의 파일을 컨테이너 위치로 연결 합니다.
    > 데이터베이스를 띄우지만, 그냥 사용하게 되면, 컨테이너 이미지 안에 파일을 저장합니다.
    > 호스트파일에 저장 할려면, --volume(or -v)이라는 옵션을 사용해야 합니다.
- ``deprecated`` -link : 컨테이너 연결 [컨테이너명:별칭]
```bash
$ docker \ 
    run \ 
    --detach \ 
    --volume /opt/mysql:/var/lib/mysql \ 
    --env MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}\ 
    --env MYSQL_USER=${MYSQL_USER} \ 
    --env MYSQL_PASSWORD=${MYSQL_PASSWORD} \ 
    --env MYSQL_DATABASE=${MYSQL_DATABASE} \ 
    --name ${MYSQL_CONTAINER_NAME} \ 
    --publish 3306:3306 \ 
    --name mysql-volume \ 
    mysql:latest;
```

### $ docker ps [OPTIONS]
생성된 container를 볼수 있다.

- -a, --all : 중단(Exited)된 Container 까지 리스트

```sh
$ docker ps -a
CONTAINER ID        IMAGE                           COMMAND                  CREATED             STATUS                      PORTS                                                    NAMES
6a1d027b604f        teamlab/pydata-tensorflow:0.1   "/opt/start"             2 minutes ago       Up 2 minutes                0.0.0.0:6006->6006/tcp, 22/tcp, 0.0.0.0:8888->8888/tcp   desperate_keller
52a516f87ceb        wordpress                       "docker-entrypoint.sh"   9 minutes ago       Up 9 minutes                0.0.0.0:8080->80/tcp                                     happy_curran
2e2c569115b9        mysql:5.7                       "docker-entrypoint.sh"   10 minutes ago      Up 10 minutes               0.0.0.0:3306->3306/tcp                                   mysql
56341072b515        redis                           "docker-entrypoint.sh"   18 minutes ago      Up 10 minutes               0.0.0.0:1234->6379/tcp                                   furious_tesla
e1a00c5934a7        ubuntu:16.04                    "/bin/bash"              32 minutes ago      Exited (0) 32 minutes ago                                                            berserk_visvesvaraya
```

### $ docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
container가 start된 상태에서 container에 셸명령어를 날리기 위한, 이 명령어를 이용해서 container 셸에 직접 접근할 수도 있다.

- -it : -i와 -t를 동시에 사용한 것으로 터미널 입력을 위한 옵션

```sh
$ docker exec -it mysql /bin/bash
```

### $ docker build
미리 작성된 Dockerfile(작성법은 [여기](./Dockerfile-작성법)) 를 이용해 Docker Image 를 만든(Build)다.

### $ docker volume
container들이 저장공간을 공유하기 위한 공간을 volume 이라고 한다.

### $ docker [network, volume] create
기본적으로 container를 생성할때 사용하는 명령어지만 앞에 옵션(networkd, volume, 등..) 을 붙이면 옵션에 대한 생성을 담당한다.
> create flow: docker pull(이미지가 없다면) -> docker create

### $ docker start
container를 시작 한다.

### docker attach
start와 비슷한 명령어지만 attach는 컨테이너의 내부로 들어가는 명령어다. (run에서 -it 옵션을 준것과 같은)

### $ docker stop CONTAINER [CONTAINER...]
container를 중지 한다. (삭제 되지는 않는다.)

```sh
$ docker ps # get container ID
$ docker stop ${TENSORFLOW_CONTAINER_ID}
$ docker ps -a # show all containers
```

### $ docker rm [OPTIONS] CONTAINER [CONTAINER...]
container 삭제(삭제 되상인 container는 중지 상태이여야 한다.)

- -f : 실행중인 container 도 삭제
```sh
$ docker ps -a # get container ID
$ docker rm ${UBUNTU_CONTAINER_ID} ${TENSORFLOW_CONTAINER_ID}
$ docker ps -a # check exist
(중지된 컨테이너들 한번에 삭제)
$ docker rm -v $(docker ps -a -q -f status=exited)
```

### $ docker pull [OPTIONS] NAME[:TAG|@DIGEST]
run 할때 pull이 실행되어서 자동으로 이미지를 다운 받지만, 이미지가 업데이트 된 경우 새로 다운 받을 수 있다.

```sh
$ docker pull ubuntu:14.04
```

### $ docker rmi [OPTIONS] IMAGE [IMAGE...]
docker image를 삭제한다.(삭제 하기 위해선 해당 image를 이용해 생성된 container가 삭제 되어 있어야한다.)
```sh
$ docker images # get image ID
$ docker rmi ${TENSORFLOW_IMAGE_ID}
```

### $ docker logs [OPTIONS] CONTAINER
> 기본적으로 컨테이너 로그는 JSON 형태로 도커 내부에 저장
> `$ cat /var/lib/docker/containers/${CONTAINER_ID}/${CONTAINER_ID}-json.log`
- --tail n : 마지막 n 줄 출력
- -f : 실시간 로그
- -t : 타임스템프 표시
- --since time : 유직스 시간 입력해 특정 시간 이후 로그

```sh
(마지막 10줄 출력)
$ docker logs --tail 10 ${CONTAINER_ID}
```

### docker [container ID, networdk, volume] inspect
상세내용을 확인하는 명령어

### docker network
Container 의 네트워크 환경 구성관련
[Dokcerfile-network 문서 참조](./Docker-network)