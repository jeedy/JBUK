# tip memo

```bash
netstat -atp
```
----

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
$ telnet localhost 80
Trying ::1...
Connected to localhost.
Escape character is '^]'.

GET / HTTP/1.0

....

```
