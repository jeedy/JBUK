# tip memo

umount /sdb1/nfs/develop2/server
mount -t nfs 172.16.2.207:/svc/AWP/www_root/omega_tide /sdb1/AWP/www_root/omega_tide

-----

mysql 접속한 사용자 권한
show grants for CURRENT_USER;

-----

rsync -Cavpr --delete /sdb1/svc/AWP/www_root/omega_privia/WebContent.war/css 172.16.1.6::OMEGA_PRIVIA_TEST

------

폴더별용량
du -sch *

----

chown -R sam:abbey example

--------------------------

VIM ctrl +z 터미널 빠져나오기
jobs
fg (job번호)

-----------------

ps -ef | grep java | grep --color 'offset'

------------------------------------------

```bash
netstat -atp
netstat -anp
```
----

find ./ -name "*.conf"|xargs grep 'staging'

---

```bash
TMOUT=0
```
----

```bash
$ ln -Tfs [새로바꿀경로] [바꿀심볼릭링크]
ex) ln -Tfs /sample/change_path/20161219 /root/user/change
```
----

1) 원격 서버 → 로컬 서버로 파일 전송
    ```bash
    $ scp [옵션] [계정명]@[원격지IP주소]:[원본 경로 및 파일] [전송받을 위치]
    $ scp abc@111.222.333.444:/home/abc/index.html /home/me/
     ```
2) 로컬 서버 → 원격 서버로 파일 전송
    ```bash
    $ scp [옵션] [원본 경로 및 파일] [계정명]@[원격지IP주소]:[전송할 경로]
    ```
3) ssh포트를 기본 22번으로 사용하고 있지 않는 서버로의 전송
    ```bash
        # scp –P 2222 abc@111.222.333.444:/home/abc/index.html /home/me/
        # scp –P 2222 /home/me/wow.html abc@111.222.333.444:/home/abc/
        [주의사항]
        옵션중에 –P와 –p가 있으니 대/소문자 확인을 하여야 한다.
        -P : 포트번호를 지정함
        -p : 원본파일 수정/사용시간 및 권한을 유지함
        -r : 하위 디렉토리 및 파일 모두 복사함
    ```
----

### telnet으로 port 확인 방법

1. ping test를 한다.
    ```bash
    [svr:usr] ping 172.0.0.1
    ```
    응답없으면(ping이 되지 않으면) firewall에 등록이 되지 않은 것이다.
    정상적 결과 172.0.0.1  is alive

2. telnet ip port 로 확인한다.
    ```bash
    [svr:usr] telnet 172.0.0.1 9999
    Trying 172.0.0.1...
    ```
    계속 대기 중이면 방화벽 오픈이 안된 것이다.

2. curl 로 IP port 확인한다.
```bash
$ curl -v 172.0.0.1:999
* About to connect() to 1172.0.0.1 port 9224 (#0)
*   Trying 172.0.0.1... connected
* Connected to 172.0.0.1 (172.0.0.1) port 9224 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2
> Host: 1172.0.0.1:999
> Accept: */*
>
...

```

3.
    ```bash
    [svr:usr] telnet 172.0.0.1 9999
    Trying 172.0.0.1...
    telnet: Unable to connect to remote host: Connection refused
    ````
    바로 연결거부가 발생하면 방화벽 오픈은 되었으나 프로세스가 안 떠있는 것이다.
    (포트를 열고 대기하고 있지 않은 상태)

4.
    ```bash
    [svr:usr] telnet 172.0.0.1 9999
    Trying 172.0.0.1...
    Connected to 172.0.0.1
    Escape character is '^]'.
    ```
    방화벽 오픈이 정상적으로 되었고 프로세스가 올라가 있는 것이다.
    (포트를 열고 대기하고 있는 상태)
    => 이상태가 되야 통신테스트를 할 수 있다

5. 라우팅 테이블 확인하기
    ```bash
    [svr:usr] netstat -rn | grep 172.0.0.1
    172.0.0.1         172.0.0.1            UG       1 186064
    ```
    여기에 값이 있으면 올바로 설정된 것임.

----

### 마운트 정보 또는 용량 확인

```bash
$ df -h
```
----

### 파일 압축 복사

```bash
$ tar cvf test_module.tar ./test_module --exclude test_module/log --exclude test_module/tmp
$ tar xvf test_module.tar
$ cp ./test_module.tar /nas/share
```
----

### 텔넷으로 포트 체크
```bash
$ telnet www.google.com 80
Trying 172.217.24.196...
Connected to www.google.com.
Escape character is '^]'.

GET / HTTP/1.1
host: www.google.com

...something more...

```
---

### netstat -anp|grep java

---

mkdir -p /home2/test/test/test

---

chown -R sam:abbey example

---

폴더별용량
```bash
du -sch *
```

---

disk mount 접속정보
```bash
df
```

---

VIM ctrl +z 터미널 빠져나오기
jobs
fg (job번호)

---

특정 파일이나 디렉토리를 사용하는 프로세스의 user/pid/접근 권한 등을 자세히 볼 때
fuser -v /usr/bin/java

---

접속한 사용자 보기
w

---

nfs 마운트 설정
local(192.168.0.2) --> remote(192.168.0.3)
loca2(192.168.0.4) -->

```bash
# remote(192.168.0.3)
$ vim /etc/exports
/sdb1/share 192.168.0.2(rw) 192.168.0.4(rw)
# or /sdb1/share 192.168.0.*(rw)

$ service nfs restart
```

```bash
# local(192.168.0.2)
$ mount -t nfs 192.168.0.3:/sdb1/share /sdb1/nfs/share
$ df

$ umount /sdb1/nfs/share
```

---

rsync 전송 시
failed: Permission denied (13)
rsync error: some files/attrs were not transferred (see previous errors) (code 23) at main.c(1039) [sender=3.0.6]
에러 발생

rsync 서버 설정 4) rsync 설정
vi /etc/rsyncd.conf
[rsync_test]                   -> 사용할 rsync 서비스 이름
path=/data/rsync_test/           -> 데이터 원본 경로
comment = rsync_test             -> 코멘트
uid = root                       -> 권한 사용자
gid = root                       -> 권한 그룹
use chroot = yes
read only = yes
hosts allow = 192.168.123.11     -> rsync 클라이언트 IP. localhost일 경우 입력하지 않아도 됨
max connections = 3
timeout=600

sync 서버 설정 5) xinetd 서비스 재시작 및 방화벽 확인
/etc/init.d/xinetd restart

----

vim  ip 변경
%s/192\.16\.0\.1/192\.16\.2\.2/gc

----

여러파일 특정 문자열 한번에 치환하기
find ./ -name "*.properties" -exec sed -i 's/192\.16\.0\.1/192\.16\.2\.2/g' {} \;

----

현재 사용중인 포트들 갯수
netstat -an|grep EST|grep "172.16.0.22"|wc -l

---

A서버에서 B서버 호출하는지 확인할때

$ netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n
watch -n 1 "netstat -ntu | awk '{print \$5}' | cut -d: -f1 | sort | uniq -c | sort -n"

----
