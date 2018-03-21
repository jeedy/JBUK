# Dockerfile 작성법

## 명령어
```dockerfile
FROM ubuntu:14.04
MAINTAINER jeeyong
LABEL "purpose"="pratice"
RUN apt-get update
RUN apt-get install apache2 -y
ADD test.html /var/www/html
WORKDIR /var/www/html
RUN ["/bin/bash", "-c", "echo hello >> test2.html"]
EXPOSE 80
CMD apachectl -DFOREGROUND
```

### FROM
생성할 이미지의 베이스가 될 이미지를 뜻함.
FROM 명령어는 Dockerfile을 작성할 때 반드시 한 번 이상 입력해야 하며, 이미지 이름의 포멧은 docker run 명령어에서 이미지 이름과 같다.
```dockerfile
FROM java:8-alpine
...
```

### MAINTAINER
이미지를 생성한 개발자의 정보를 나타냅니다. 일반적으로 Dockerfile을 작성한 사람과 연락할 수 있는 이메일 등을 입력
```dockerfile
FROM java:8-alpine
MAINTAINER <user@email.com>
...
```

### LABEL
이미지에 메타데이터를 추가합니다. 메타뎅터는 '키:값'의 형태로 저장되며, 여러 개의 메타데이터가 저장될 수 있습니다. 추가된 메타데이터는 docker inspect 명령어로 이미지의 정보를 구해서 확인할 수 있습니다.
```dockerfile
...
LABEL "purpose"="practice"
...
```

### RUN
이미지를 만들기 위해 컨테이너 내부에서 명령어를 실행. 단, Dockerfile을 이미지로 빌드하는 과정에서 별도의 입력이 불가능하기 때문에 apt-get install apache2 명령어에서 실치할 것일지를 선택하는 Y/N을 Yes로 설정해야함. 이미지를 빌드할 때 별도의 입력을 받아야 하는 RUN이 있다면 build 명령어는 이를 오류로 간주하고 빌드를 종료한다.
> 일부 명령어는 배열 형태로 사용 가능
> `RUN ["실행 가능한 파일", "명령줄 인자 1", "명령줄 인자 2", ... ]`
```dockerfile
RUN ["echo", "$MY_ENV"] # (x)
RUN ["sh", "-c", "echo $MY_ENV"] # (o)
```

```dockerfile
...
RUN apt-get update
RUN apt-get install apache2 -y
...
```
### WORKDIR

### ENV
Dockerfile 내부 그리고 Docker에서 사용할 환경변수를 선언
```dockerfile
...
ENV test /home
WORKDIR $test
RUN touch $test/mytouchfile
```
```bash
$ docker run -it --name env_test myenv:0.0 /bin/bash
root@env_test:/home$ echo $test
/home 
```

### ADD
파일을 이미지에 추가. JSON 배열의 형태로 
`["추가할 파일 이름", ... "컨테이너에 추가될 위치"]`
와 같이 사용할 수 있습니다. 추가할 파일명은 여러 개를 지정할 수 있으며 배열의 마지막 원소가 컨테이너에 추가될 위치입니다.
> ADD와 COPY 차이있음
```dockerfile
...
ADD test.html /var/www/html
WORKDIR /var/www/html
RUN ["/bin/bash", "-c", "echo hello >> test2.html"]
...
```

### COPY

### EXPOSE
Dockerfile의 빌드로 생성된 이미지에서 노출할 포트를 설정합니다. 그러나 EXPOSE를 설정한 이미지로 컨테이너를 생성했다고 해서 반드시 이 포트가 호스트의 포트와 바인딩되는 것은 아니며, 단지 컨테이너의 80번 포트를 사용할 것임을 나타내는 것뿐입니다. EXPOSE는 컨테이너를 생성하는 run 명령어에서 모든 노출된 컨테이너의 포트를 호스트에 퍼블리시(Publish)하는 -P 플래그(flag)와 함께 사용됩니다.
```dockerfile
...
EXPOSE 80
CMD apachectl -DFOREGROUND
```
```bash
$ docker run -d -P --name myserver mybuild:0.0
```
> -P 옵션은 EXPOSE로 노출된 포트를 호스트에서 사용 가능한 포트에 차례로 연결하므로 이 컨테이너가  호스트의 어떤 포트와 연결됐는지 확인할 필요가 있다.

```bash
$ docker port myserver
80/tcp -> 0.0.0.0:32769
```

### ENTRYPOINT
ENTRYPOINT 에 값이 있을 경우 명령어가 되어 CMD로 선언된 명령어는 인자로 들아가게 된다.
```dockerfile
ENTRYPOINT ["echo"]
CMD ["hello", "world"]
# 결국 명령어가 `$ echo hello world` 이렇게 실행된다

# 일반형식과 배열 형태의 차이
# 1) 일반 형식
CMD echo test
# -> /bin/sh -c echo test
ENTRYPOINT /entrypoint.sh
# -> /bin/sh -c /entrypoint.sh
# 실제 컨테이너에서 실행되는 명령어 /bin/sh -c entirypoint.sh /bin/sh -c echo test

# 2) 배열 형태
CMD ["echo", "test"]
# -> echo test
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
# -> /bin/bash /entrypoint.sh
# 실제 컨테이너에서 실행되는 명령어는 /bin/bash entrypoint.sh echo test
```

### CMD
가장 마지막에 Container가 생성될 때 가장 마지막에 실행해야할 최종 명령어.
```dockerfile
...
EXPOSE 80
CMD apachectl -DFOREGROUND
```

### VOLUME
컨테이너의 내부 디렉터리를 호스트와 공유가 필요할 경우 사용

### ARG
build 명령어를 실행할 때 추가로 입려을 받아 Dockerfile 내에서 변수의 값으로 사용가능

### USER
컨테이너 내에서 사용될 사용자 계정 이름이나 UID를 설정하면 그 아래 명령어는 해당 사용자 권한으로 실행된다. 일반적으로 RUN은 사용자의 그룹과 계정을 생성한 뒤 사용한다. 루트 권한이 필요하지 않다면 USER를 사용하는 것을 권장.

### ONBUILD
빌드된 이미지를 기반으로 하는 다른 이미지가 Dockerfile로 생성될 때, 실행할 명령어를 추가한다.
즉 내가 만든 이미지를 가지고 다른 사람이 추가 된 빌드를 하려할 경우

### STOPSIGNAL

### HEALTHCHECK
이미지로부터 생성된 컨테이너에서 동작하는 애플리케이션의 상태를 체크 하도록 설정.
*컨테이너 내부에서 동작 중인 애플리케이션의 프로세스가 종료되지는 않았으나 애플리케이션이 동작하고 있지 않은 상태를 방지하기 위해 사용*
- --interval : 컨테이너의 상태를 체크하는 주기
- --timeout : 설정된 시간을 초과하면 상태 체크에 실패한 것으로 간주하고 `--retries` 의 횟수만큼 명령어 반복. `--retries`에 설정된 횟수만큼 상태 체크에 실패하면 해당 컨테이너는 unhealthy 상태로 설정

```dockerfile
FROM nginx
RUN apt-get update -y && apt-get install curl -y
HEALTHCHECK --interval=1m --timeout=3s --retries=3 CMD curl -f http://localhost || exit 1
```

### SHELL
Dockerfile에서 기본적으로 사용하는 셸은 리눅스에서 "/bin/sh -c", 윈도우에서 "cmd /S /C"입니다. 예를 들어, Dockerfile에 다음과 같은 명령어가 있다면 윈도우와 리눅스는 다르게 수행합니다.
```dockerfile
RUN echo "hello, world!"
# 리눅스에서는 `/bin/sh -c echo hello, world`, 윈도우에서는 `cmd /S /C echo hello, world`로 실행됨
```
그렇지만 사용하려는 셸을 따로 지정하고 싶을 수도 있습니다.
```dockerfile
FROM node
RUN echo hello, node!
SHELL ["/usr/local/bin/node"] # node 셸로 변경
RUN -v
```