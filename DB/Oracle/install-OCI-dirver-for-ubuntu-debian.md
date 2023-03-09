# 데비안(Ubuntu) 에 OCI(Oracle instant client) 설치하기
tags: ubuntu, debian, linux, 유분투, 데비안, 리눅스, OCI, oracle instant client, oracle, jdbc, thin

> Kafka connector 에 오라클 구축시  OCI(Oracle instant client) driver를 사용해야하는 이슈로 OCI 설치 리서치했던 내용 중 성공했던 방법을 기록한다.

## Reference
- [ubuntu Oracle Instant Client 설치하기](https://www.mynotes.kr/ubuntu-oracle-instant-client-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0/)

## 1. Download Oracle instant clinet 
https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

- instantclient-basic-linux.x64-12.1.0.2.0.zip
- instantclient-sdk-linux.x64-12.1.0.2.0.zip

>  꼭 같은 버전으로 셋트 맞춰 다운받자! (나중에 보면 왜그런지 알게 된다.)

## 2. 압축 해제
위에서 다운받은 압축 파일을 설치한 디렉토리에 복사(본 예제는 `/opt/`안에 생성한다.) 한 이후 과정이다.

```sh
$ cd /opt
$ unzip instantclient-basic-linux.x64-12.1.0.2.0.zip 
$ unzip instantclient-sdk-linux.x64-12.1.0.2.0.zip

# 버전이 같아야 아래 디렉토리 안에 압축해제된 파일들이 모두 들어간다.
$ ls -al
..
drwxr-xr-x 4 root root     4096 Aug 31 03:07 instantclient_12_1
..

```

## 3. Oracle 환경 변수 설정

```sh
$ vi ~/.bashrc

...
export OCI_HOME=/opt/instantclient_12_1
export OCI_LIB_DIR=$OCI_HOME
export OCI_INCLUDE_DIR=$OCI_HOME/sdk/include
export OCI_VERSION=12
export NLS_LANG=AMERICAN_AMERICA.UTF8
export LD_LIBRARY_PATH=/opt/instantclient_12_1:${LD_LIBRARY_PATH}
export TNS_ADMIN="/opt/instantclient_12_1/network/admin"
export NLS_LANG=KOREAN_KOREA.KO16MSWIN949 
...

$ source ~/.bashrc
```

> source 명령어로 갱신했지만 그냥 로그아웃했다가 다시 접속하는게 나을 수도 있다.


## 4. Id에 Oracle Instant Client 라이브러리 설정 (옵션)
```sh
$ echo '/opt/instantclient_12_1' | sudo tee -a /etc/ld.so.conf.d/oracle_instant_client.conf
$ ldconfig
```

## 5. NS_ADMIN 디렉토리 및 tnsnames.ora 설정 (옵션)

```sh
mkdir -p /opt/instantclient_12_1/network/admin
 
cd $TNS_ADMIN
vi tnsnames.ora
 
DEV =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS_LIST =
        (ADDRESS_LIST =
          (ADDRESS =(PROTOCOL=TCP)(HOST=192.168.0.40)(PORT=1521)
          )
        )
      )
    )
    (CONNECT_DATA =(SERVICE_NAME=orcl)
    )
  )
```

## 부록

### ora-01882: TimeZone Region not found. with Kafka Connect JdbcSource connector.
오라클 접속시 `ora-01882: TimeZone Region not found.` 에러가 발생할 경우 다양한 방법으로 `oracle.jdbc.timezoneAsRegion=false` 옵션을 주고 접속하면 된다.

그러나 이를 지원하지 않는 plugin의 경우 강제로 `ojdbc8.jar` 파일을 수정해 해결 할 수 있다.

해결방법:
1. `ojdbc8.jar` 압축 해제 (linux에서는 `.jar` 확장자를 `.zip` 로 수정하고 `unzip` 으로 압축해제 하자.)
2. ojdbc8/oracle/jdbc/defaultConnectionProperties.properties 파일에 `oracle.jdbc.timezoneAsRegion=false` 라인 추가 후 저장
3. 수정된 파일이 있는 디렉토리(ojdbc8) 다시 `.zip` 으로 압축
4. 확장자를 `.zip` -> `.jar` 로 수정

> 간단한 properties 파일 같은 텍스트 기반에 파일을 수정하는 경우는 재컴파일 할 필요없이 압축해서 확장자만 바꿔줘도 정상 동작한다.
