# 도커 볼륨(Volume) 설정 관련내용
> 참고 자료
    - 시작하세요! 도커(위키북스) 36page

도커 이미지로 컨테이너를 생성하면 이미지는 읽기 전용이 되며 컨테이너의 변경 사항만 별도로 저장해서 각 컨테이너의 정보를 보존합니다. 예를 들어, 위에서 생성했던 mysql컨테이너는 mysql:5.7이라는 이미지로 생성되었지만 워드프레스 블로그를 위한 데이터베이스 등의 정보는 컨테이너가 갖고 있습니다.
이러한 구조로 인해 mysql 컨테이너를 삭제하면 컨테이너 계층에 저장되어있던 데이터베이스의 정보도 삭제된다는 점입니다. 이를 방지하기 위해 컨테이너의 데이터를 영속성(Persistent) 데이터로 활용할 수 있는 방법이 볼륨을 이용한 방법을 설명합니다.

## 볼륨 공유 방법

### 호스트 볼륨 공유 (호스트 디렉터리에 직접 파일을 올릴경우)
- -v [호스트의 공유디렉토리]:[컨테이너의 공유 디렉터리]

> 호스트에 이미 디렉터리와 파일이 존재하고 컨테이너에도 존재할 때 두 디렉터리를 공유하면?
    - 호스트의 디렉터리가 켄테이너 디렉터리에 마운트 된다.(호스트 디렉터리가 살아있고 컨테이너 디렉토리는 없어짐 / 실제로 삭제가 되는건 아니고 안 보일 뿐 다시 마운트 해제되면 보인다)

#### 설정
```sh
$ docker run -d \
-name wordpressdb_hostvolume \
-e MYSQL_ROOT_PASSWORD=password \
-e MYSQL_DATABASE=wordpress \
-v /home/wordpress_db:/var/lib/mysql \ # 중요
mysql:5.7

$ docker run -d \
-e WORDPRESS_DB_PASSWORD=password \
--name wordpress_hostvolume \
--link wordpressdb_hostvolume:mysql \
-p 80 \
wordpress
```

#### 접근방법
호스트의 /home/wordpress_db 디렉토리를 확인해보면 디렉토리와 파일이 생성된 것을 확인가능하다.
```sh
$ ls /home/wordpress_db
auto.cnf  ib_buffer_pool  ib_logfile0  ib_logfile1  ibdata1  mysql  performance_schema ....
```

### 볼륨 컨테이너(다른 컨테이너와 공유)
-v 옵션으로 볼륨을 사용하는 컨테이너(위 `호스트 볼륨 공유` 참조)를 다른 컨테이너에서 공유하는 것
컨테이너를 생성할 때 --volumes-from 옵션을 설정하면 -v 또는 --volume 옵션을 적용한 컨테이너의 볼륨 디렉터리를 공유할 수 있다. 그러나 이는 직접 -v 옵션을 이용해 공유하것이 아닌 -v 옵션을 적용한 컨테이너를 통해 공유하는 것이다.

- --volumes-from

#### 설정
```bash
# 1. 호스트 볼륨 공유 방식으로 호스트와 볼륨을 공유하는 컨테이너 생성
$ docker run -it \
--name volume_dummy \ # 중요
-v /home/wordpress_db:/home/testdir_2 \
mysql:5.7

# 2. 위 생성된 컨테이너(volume_dummy) 를 통해서 호스트와 디렉터리를 공유한다.
$ docker run -it \
--name volumes_from_container \
--volumes-from valume_dummy \ #중요
ubuntu:14.04

root@volumes_from_container$ ls /home/testdir_2/
auto.cnf  ib_buffer_pool  ib_logfile0  ib_logfile1  ibdata1  mysql  performance_schema ....
```

#### 접근방법
호스트의 /home/wordpress_db 디렉터리를 확인해보면 디렉토리와 파일이 생성된 것을 확인가능하다.
컨테이너의 /home/testdir_2/ 디렉터리를 확인해보면 파일이 생성된 것을 확인할 수 있다.
```sh
$ ls /home/wordpress_db
auto.cnf  ib_buffer_pool  ib_logfile0  ib_logfile1  ibdata1  mysql  performance_schema ....

$ docker run -it \
--name volume_dummy \ # 중요
-v /home/wordpress_db:/home/testdir_2 \
mysql:5.7

$ docker run -it \
--name volumes_from_container \
--volumes-from valume_dummy \ #중요
ubuntu:14.04

root@volumes_from_container$ ls /home/testdir_2/
auto.cnf  ib_buffer_pool  ib_logfile0  ib_logfile1  ibdata1  mysql  performance_schema ....
```

### 도커 볼륨

#### 설정

#### 접근방법