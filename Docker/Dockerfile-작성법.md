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

### CMD
가장 마지막에 Container가 생성될 때 가장 마지막에 실행해야할 최종 명령어.
