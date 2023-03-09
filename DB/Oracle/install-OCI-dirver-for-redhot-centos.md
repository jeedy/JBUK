# 레드핫(centos) 에 OCI(Oracle instant client) 설치하기
tags: ubuntu, 레드핫, redhot, centos, linux, 리눅스, OCI, oracle instant client, oracle, jdbc, thin

> Kafka connector 에 오라클 구축시  OCI(Oracle instant client) driver를 사용해야하는 이슈로 OCI 설치 리서치했던 내용 중 성공했던 방법을 기록한다.

## Reference
- [redhot에 Oracle Instant Client 설치하기](https://gomu92.tistory.com/72)

## 1. Oracle instant clinet & SQL*PLUS package (RPM) 파일 다운로드
https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html
```sh
$ wget https://download.oracle.com/otn_software/linux/instantclient/1918000/oracle-instantclient19.18-basic-19.18.0.0.0-2.x86_64.rpm
$ wget https://download.oracle.com/otn_software/linux/instantclient/1918000/oracle-instantclient19.18-sqlplus-19.18.0.0.0-2.x86_64.rpm

```

## 2. RPM 인스톨
```sh
$ yum install -y oracle-instantclient19.18-basic-19.18.0.0.0-2.x86_64.rpm
...(생략)
설치되었습니다:
  oracle-instantclient19.18-basic-19.18.0.0.0-2.x86_64                                                                     

완료되었습니다!


$ yum install -y oracle-instantclient19.18-sqlplus-19.18.0.0.0-2.x86_64.rpm
...(생략)
설치되었습니다:
  oracle-instantclient19.18-sqlplus-19.18.0.0.0-2.x86_64

완료되었습니다!
```

> rpm 설치시 `Failed dependencies:libaio is needed by ...` 오류가 발생하면 `libaio` 라이브러리 설치를 진행해야 한다.
```sh
$ yum install -y libaio
```

## 3. `/etc/profile.d/oracle.sh` 생성 후  $ORACLE_HOME, $TNS_ADMIN 설정 추가

/etc/profile.d/oracle.sh:
```sh
$ vi /etc/profile.d/oracle.sh


export ORACLE_HOME=/usr/lib/oracle/19.15/client64
export TNS_ADMIN=/usr/lib/oracle/19.15/client64/bin
```

## 4. oracle instant client 사용 계정 .bash_profile에 $ORACLE_HOME, $TNS_ADMIN, $PATH 설정

bash_profile: 
```sh
$ vi ~/.bash_profile에


...(생략)

export NLS_LANG=KOREAN_KOREA.AL32UTF8
export ORACLE_HOME=/usr/lib/oracle/19.15/client64
export TNS_ADMIN=/usr/lib/oracle/19.15/client64/bin
export PATH=${PATH}:$HOME/bin:$ORACLE_HOME/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$ORACLE_HOME/lib


$ source ~/.bash_profile
```

## 5. Oracle server 접속 tnsnames.ora 설정
tnsnames.ora:
```sh
serviceName =
  (DESCRIPTION =
        (ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.xxx.xxx)(PORT = xxxx))
        (CONNECT_DATA =
                (SERVER = DEDICATED)
                (SID = sid)
        )
 )
```

## 6. oracle server 접속 확인
```sh
$ sqlplus id/passwd@serviceName

SQL*Plus: Release 19.0.0.0.0 - Production on 금 4월 29 16:15:19 2022
Version 19.15.0.0.0
Copyright (c) 1982, 2022, Oracle.  All rights reserved.
마지막 성공한 로그인 시간: 금 4월  29 2022 16:14:30 +09:00
다음에 접속됨:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0

```
