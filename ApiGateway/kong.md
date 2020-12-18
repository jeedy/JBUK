# Kong - API Gateway 
tags: API, gateway

## https://konghq.com/

## 느낌점
spring cloud gateway와 다른점은 직접 소스로 구현을 할 필요가 없는 솔류션으로 보인다.
GUI 어드민 페이지도 제공해 페이지에서 직접 컨트롤하고 지표도 뽑아 볼수있다. 

개발자가 직접 설치하는 것이 아닌 인프라 영역에 가까운 솔류션, 엄블렐라(API umbrella)도 마찬가지이다. 


## 참고자료
1. https://medium.com/@keendev/kong%EC%9C%BC%EB%A1%9C-%EC%8B%9C%EC%9E%91%ED%95%98%EB%8A%94-%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C-%EC%84%9C%EB%B9%84%EC%8A%A4-%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98-1-824f5ae4606b (2016년글이지만 사용방법과 kong의 설치 및 구동방식을 대략적으로 이해 가능하다)

1. https://study-develop.tistory.com/39 (kong & konga 설치하기)

1. https://ibks-platform.tistory.com/378 (kong 설치)
1. https://ibks-platform.tistory.com/379 (konga 설치)

## 개요
엔진은 무료로 사용가능한것 같다. 그러나 gui는 유료모델인것 같다. 그러나 [konga](https://github.com/pantsel/konga) 라는 오픈소스로 gui 를 사용할 수 있다.

2018년도에 1.0버전 릴리스하게 된다. 주 기반언어는 Lua language.

client로는 T telekom(도이치 텔레콤, 독일), 익스피디아, 제너럴 일렉트릭, 시스코, AXA 프랑스의 보험 금융 그룹, 삼성, 파파존스, 나스닥 등등..

## kong enterprise vs community
https://konghq.com/subscriptions/

### 공통제공
- 모든 아키텍처 (모놀리스, 마이크로 서비스, 서비스 메시 등)에서 작동하는 경량 API 게이트웨이 (*Lightweight API gateway that works with any architecture (monolith, microservices, service mesh and more))
- Kubernetes 수신 컨트롤러 (*Kubernetes Ingress Controller)
- 기본 트래픽 제어 플러그인 (*Basic traffic control plugins)
- gRPC 지원 (*gRPC support)
- 기본 인증 (HMAC, JWT 키 인증, 제한된 OAuth 2.0 포함) (*Basic authentication (includes HMAC, JWT Key Auth, limited OAuth 2.0))
- 서드파티 분석 (*Third-party analytics)
- 게이트웨이 및 Kubernetes의 선언적 구성 (CI / CD 파이프 라인에 Kong 구성 파일을 추가 할 수 있음) (*Declarative configuration of gateway and Kubernetes (enables adding Kong config file to your CI/CD pipeline))
- GitOps 용 Git 동기화 (*Git sync for GitOps)

### Enterprise Only
- 고급 트래픽 제어 플러그인 (고 가용성 속도 제한, 고급 서비스 라우팅, 분산 캐싱)
- GraphQL 및 Kafka 지원
- Kong 클러스터, 플러그인, API 및 소비자를 관리하기위한 Admin GUI 및 작업 공간 
- 자율 모니터링 및 이상 감지 (Kong Immunity)
- 클러스터 상태 모니터링 (Kong Vitals)
- 감사 로그
- 비주얼 서비스 맵
- 고급 인증 (전체 OAuth 2.0, OpenID Connect, Vault, 상호 TLS 및 향상된 암호화 포함)
- Kong Studio 통합을 통한 엔드 투 엔드 API 사양 및 디자인
- 24x7x365 전문가 지원
- 기타 등등...

## 설치
참조: https://study-develop.tistory.com/39

### 1. kong installation.
- https://konghq.com/get-started/#install 접속.
- 운영체제 선택(CentOS)
    ```sh 
    #운영체제 확인
    $ cat /etc/os-release
    ```
- 패키지 다운로드 및 설치
    ```sh
    # 운영체제 버전에 맞는 패키지 다운로드
    $ wget -O centos7-kong-2.1.4.el7.amd64.rpm https://bintray.com/kong/kong-rpm/download_file?file_path=centos/7/kong-2.1.4.el7.amd64.rpm
    # 다운로드된 패키지 인스톨
    $ sudo yum install ./centos7-kong-2.1.4.el7.amd64.rpm --nogpgcheck
    $ whereis kong
    kong: /etc/kong /usr/local/bin/kong /usr/local/kong
    # root 계정으로 변환 (root 권한으로 설치되기 때문에 root로 계정으로 변환한다.)
    $ su -
    $ cd /etc/kong
    $ cp ./kong.conf.default ./kong.conf
    ```
### 2. postgreSQL 설치(konga와 같이 이용하기 위해 postgresql-11을 설치하자)
- https://www.postgresql.org/download/ 사이트 접근 (redhat, centOS 는 여기로 https://www.postgresql.org/download/linux/redhat/)
- yum repository를 이용한 database 설치
    ```sh
    # postgresql-13 버전 설치
    $ yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
    $ yum install -y postgresql13-server
    $ /usr/pgsql-13/bin/postgresql-13-setup initdb
    $ systemctl enable postgresql-13
    $ systemctl start postgresql-13

    # postgresql-11 버전 설치
    $ yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
    $ yum install -y postgresql11-server
    $ /usr/pgsql-11/bin/postgresql-11-setup initdb
    $ systemctl enable postgresql-11
    $ systemctl start postgresql-11
    ```

### 3.postgresSQL에 kong 계정 및 Database 설정 후 kong.conf 값 수정
- kong 계정 및 database 생성
    ```sh
    $ su - postgres
    $ psql
    postgres=# \password postgres
    새 암호를 입력하세요 : *****
    다시 입력해주세요 : *****
    postgres=# CREATE USER kong; CREATE DATABASE kong OWNER kong;
    postgres=# \password kong
    새 암호를 입력하세요 : *****
    다시 입력해주세요 : *****
    postgres=# quit
    $ exit
    ```
- kong.conf 에 database 정보 수정

    /etc/kong/kong.conf:
    ```sh
    # root 계정으로 진행
    database = postgres
    pg_host = 127.0.0.1
    pg_port = 5432
    pg_timeout = 5000
    pg_user = kong
    pg_password = (password) # postgresql에 입력한 kong 패스워드를 입력하자
    pg_database = kong
    ```

### 4. kong 최초 마이크레이션 실행
```sh
$ kong migrations bootstrap ./kong.conf
Bootstrapping database...
migrating core on database 'kong'...
core migrated up to: 000_base (executed)
core migrated up to: 003_100_to_110 (executed)
core migrated up to: 004_110_to_120 (executed)
core migrated up to: 005_120_to_130 (executed)
core migrated up to: 006_130_to_140 (executed)
...(생략)

```

### 5. kong 실행 및 테스트
```sh
$ cd /etc/kong
$ kong start ./kong.conf
Kong started

$ curl -i http://localhost:8001/
HTTP/1.1 200 OK
Date: Wed, 07 Oct 2020 07:38:24 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
Access-Control-Allow-Origin: *
Server: kong/2.1.4
Content-Length: 9998
X-Kong-Admin-Latency: 326
...(생략)
# kong stop (종료)

```

정상적으로 kong이 실행되었다면 아래 port들이 올라가 있어야한다.
```
 By default Kong listens on the following ports:

   :8000 on which Kong listens for incoming HTTP traffic from your clients, and forwards it to your upstream services.
   :8443 on which Kong listens for incoming HTTPS traffic. This port has a similar behavior as the :8000 port, except that it expects HTTPS traffic only. This port can be disabled via the configuration file.
   :8001 on which the Admin API used to configure Kong listens.
   :8444 on which the Admin API listens for HTTPS traffic.
```

> ssl 인증서를 설치하기 위해선 kong.conf 파일안에 엔진용(`ssl_cert`, `ssl_cert_key`), 어드민용(`admin_ssl_cert`, `admin_ssl_cert_key`) 속성에 인증서 absolute path 값이 들어가야한다. 

### 6. konga 설치하기 (https://github.com/pantsel/konga)
참고: 
- https://study-develop.tistory.com/40
- https://dev.to/vousmeevoyez/setup-kong-konga-part-2-dan
- [Konga service 등록 및 route 등록방법](./konga.md)

#### 중요사항 (2020-10-14일자 기준)
- node 12.16.0 버전에서 빌드하면 node 12.16.0 버전으로 실행해야한다.
- postgresql-11 버전은 추천
- postgresql-13 버전은 지원하지 않는다.(postgresql-12도 지원하지 않은 것으로 보인다.)
- konga 0.14.9 버전 기준 kong 2.1.3 까지 지원한다.

#### kong 설치
```sh
# root
$ su -

# git 설치 
# yum install git

# nvm 설치
# yum install wget
$ wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.2/install.sh | bash
$ source ~/.bashrc

# node, npm 설치
$ nvm install 12.16.0
$ nvm list
$ nvm alias default 12.16.0

# kong 설치된 곳에 같이 설치하자
$ cd /usr/local
$ git clone https://github.com/pantsel/konga.git
$ cd konga
$ npm i
$ cp .env_example .env

$ vim .env
# .env: database 정보 수정
PORT=1337
NODE_ENV=production
KONGA_HOOK_TIMEOUT=120000
DB_ADAPTER=postgres
DB_URI=postgresql://konga:password@localhost:5432/konga
KONGA_LOG_LEVEL=warn
TOKEN_SECRET=some_secret_token

# Database 마이그레이션
$ node ./bin/konga.js prepare --adapter postgres --uri postgresql://konga:password@localhost:5432/konga

# konga 실행
$ npm start

# konga 접속 테스트
$ curl -i http://localhost:1337/
HTTP/1.1 302 Found
X-Powered-By: Sails <sailsjs.org>
Location: /register
Vary: Accept, Accept-Encoding
Content-Type: text/plain; charset=UTF-8
Content-Length: 31
Date: Wed, 14 Oct 2020 05:35:26 GMT
Connection: keep-alive

```

#### PM2(production process manager for Node.js) 설치 및 konga 구동
참고자료: 
- https://github.com/Unitech/pm2
- https://medium.com/idomongodb/how-to-npm-run-start-at-the-background-%EF%B8%8F-64ddda7c1f1

```sh
# su -
$ npm install pm2 -g
# 설치 완료후

$ cd /usr/local/konga
# 시작
$ pm2 start ./app.js --name konga

# 재시작
$ pm2 restart konga

# 중지
$ pm2 stop konga

# 삭제
$ pm2 delete konga


# 등록된 리스트 확인
$ pm2 list

# 모니터링(Terminal Based Monitoring)
$ pm2 monit

# 로그 tail
$ pm2 logs

# 무중단 재기동(Zero Downtime Reload)
$ pm2 reload all
```
> 브라우저를 통해 Konga(http://localhost:1337/) 접속후 최초 어드민 생성하는 절차가 진행된다.


## Kong Admin API
```

$ curl -i -X POST http://localhost:8001/services/2f9d8cee-8098-4968-ad71-6729c6b8a5ef/routes \
  --data 'paths[]=/acc' \
  --data name=tacc


$ curl -i -X PUT http://localhost:8001/routes/394345fb-2e86-4172-b6eb-17bfcc065c26 \
  --data 'paths[]=/acc' \
  --data 'hosts[]=tacc..com'


$ curl -i -X DELETE http://localhost:8001/routes/574be0a3-d2ff-464a-80f0-e2ee8c9e1eac
$ curl -i -X DELETE http://localhost:8001/routes/394345fb-2e86-4172-b6eb-17bfcc065c26
```

## postgresql cli 
```sh
root$ su - postgres
postgres$ psql -d kong
psql (13.0)
도움말을 보려면 "help"를 입력하십시오.

kong=# select version();
                                                 version
---------------------------------------------------------------------------------------------------------
PostgreSQL 11.9 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-11), 64-bit
(1개 행)

kong=# \dt
                 릴레이션(relation) 목록
 스키마 |             이름              |  종류  | 소유주
--------+-------------------------------+--------+--------
 public | acls                          | 테이블 | kong
 public | acme_storage                  | 테이블 | kong
 public | basicauth_credentials         | 테이블 | kong
 public | ca_certificates               | 테이블 | kong
 public | certificates                  | 테이블 | kong
 public | cluster_events                | 테이블 | kong
 public | consumers                     | 테이블 | kong
 public | hmacauth_credentials          | 테이블 | kong
 public | jwt_secrets                   | 테이블 | kong
 public | keyauth_credentials           | 테이블 | kong
 public | locks                         | 테이블 | kong
 public | oauth2_authorization_codes    | 테이블 | kong
 public | oauth2_credentials            | 테이블 | kong
 public | oauth2_tokens                 | 테이블 | kong
 public | plugins                       | 테이블 | kong
 public | ratelimiting_metrics          | 테이블 | kong
 public | response_ratelimiting_metrics | 테이블 | kong
 public | routes                        | 테이블 | kong
 public | schema_meta                   | 테이블 | kong
 public | services                      | 테이블 | kong
 public | sessions                      | 테이블 | kong
 public | snis                          | 테이블 | kong
 public | tags                          | 테이블 | kong
 public | targets                       | 테이블 | kong
 public | ttls                          | 테이블 | kong
 public | upstreams                     | 테이블 | kong
 public | workspaces                    | 테이블 | kong
(27개 행)

kong=# select * from plugins;
 id | created_at | name | consumer_id | service_id | route_id | config | enabled | cache_key | protocols | tags | ws_id
----+------------+------+-------------+------------+----------+--------+---------+-----------+-----------+------+-------
(0개 행)
```


### :bomb: troubleshooting
1. **#중요#** Clustering 구성시 kong engine health check 방법

    > 부제: localhost:8443(또는 localhost:8000) 으로 health chech를 할 수 있는 방법.

    1. service 에 self-localhost 등록
        1. name: localhost-status
        1. protocol: http
        1. **host: localhost** (이게중요)
        1. port: 8001
        1. Path: /status
    1. Routes 에 /health Path 등록
        1. name: health
        1. Paths: /health
        1. Methods: GET
        1. Protocals: https
    
    이렇게 등록 후 `$ curl -X GET 'http://kong-engine-x:8000/health/status'` 호출하면 정상적으로 동작중인지 확인 가능하다.

1. **#중요#** centos7에 postgresql 설치후 kong 실행시 아래와 같은 오류 발생

    ```sh
    # postgresql-11 경우
    $ kong start
    Error: [PostgreSQL error] failed to retrieve PostgreSQL server_version_num: 치명적오류: 사용자 "kong"의 Ident 인증을 실패했습니다.

    # postgresql-13 경우
    $ kong start --v
    2020/10/07 14:20:29 [verbose] Kong: 2.1.4
    2020/10/07 14:20:29 [verbose] reading config file at /etc/kong/kong.conf
    2020/10/07 14:20:29 [verbose] prefix in use: /usr/local/kong
    Error:
    /usr/local/share/lua/5.1/pgmoon/init.lua:211: don't know how to auth: 10
    stack traceback:
            [C]: in function 'auth'
            /usr/local/share/lua/5.1/pgmoon/init.lua:211: in function 'connect'
            .../share/lua/5.1/kong/db/strategies/postgres/connector.lua:211: in function 'connect'
            .../share/lua/5.1/kong/db/strategies/postgres/connector.lua:527: in function 'query'
            .../share/lua/5.1/kong/db/strategies/postgres/connector.lua:279: in function 'init'
            /usr/local/share/lua/5.1/kong/db/init.lua:139: in function 'init_connector'
            /usr/local/share/lua/5.1/kong/cmd/start.lua:31: in function 'cmd_exec'
            /usr/local/share/lua/5.1/kong/cmd/init.lua:88: in function </usr/local/share/lua/5.1/kong/cmd/init.lua:88>
            [C]: in function 'xpcall'
            /usr/local/share/lua/5.1/kong/cmd/init.lua:88: in function </usr/local/share/lua/5.1/kong/cmd/init.lua:45>
            /usr/local/bin/kong:9: in function 'file_gen'
            init_worker_by_lua:47: in function <init_worker_by_lua:45>
            [C]: in function 'xpcall'
            init_worker_by_lua:54: in function <init_worker_by_lua:52>

    ```
    원인 postgresql 의 기본 설정된 인증방식 때문이다. 이를 수정해주면 해결된다. (참고: https://sysops.tistory.com/8, 인증방식 document: https://www.postgresql.org/docs/10/auth-pg-hba-conf.html)

    /var/lib/pgsql/11/data/pg_hba.conf:
    ```sh
    # $ cd /var/lib/pgsql/11/data/
    # $ cp ./pg_hba.conf ./pg_hba.conf.default
    # $ vim /var/lib/pgsql/11/data/pg_hba.conf
    
    # postgresql-11 버전의 경우
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    # "local" is for Unix domain socket connections only
    local   all             all                                     peer
    # IPv4 local connections:
    # 여기 METHOD 부분을 md5로 수정
    host    all             all             127.0.0.1/32            md5
    # IPv6 local connections:
    # 여기 METHOD 부분을 md5로 수정
    host    all             all             ::1/128                 md5
    # Allow replication connections from localhost, by a user with the
    # replication privilege.
    local   replication     all                                     peer
    host    replication     all             127.0.0.1/32            scram-sha-256
    host    replication     all             ::1/128                 scram-sha-256

    ```

    /var/lib/pgsql/13/data/pg_hba.conf:
    ```sh
    # $ cd /var/lib/pgsql/13/data/
    # $ cp ./pg_hba.conf ./pg_hba.conf.default
    # $ vim /var/lib/pgsql/13/data/pg_hba.conf
    
    # postgresql-13 버전의 경우
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    # "local" is for Unix domain socket connections only
    local   all             all                                     peer
    # IPv4 local connections:
    # 여기 METHOD 부분을 password로 수정
    host    all             all             127.0.0.1/32            password
    # IPv6 local connections:
    # 여기 METHOD 부분을 password로 수정
    host    all             all             ::1/128                 password
    # Allow replication connections from localhost, by a user with the
    # replication privilege.
    local   replication     all                                     peer
    host    replication     all             127.0.0.1/32            scram-sha-256
    host    replication     all             ::1/128                 scram-sha-256

    ```

    postgresql 재기동한다. 
    ```sh 
    $ systemctl restart postgresql-11

    # postgresql-13 경우
    # $ systemctl restart postgresql-13
    ```

## 라이센스

### 리셀러
https://konghq.com/partners/?itm_source=website&itm_medium=nav

#### 한국
http://bmtsys.com/kr/bbs/content.php?co_id=micro02




#### postgresql URIs
```
postgresql://
postgresql://localhost
postgresql://localhost:5433
postgresql://localhost/mydb
postgresql://user@localhost
postgresql://user:secret@localhost
postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp
```
