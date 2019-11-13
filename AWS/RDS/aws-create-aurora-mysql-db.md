# AWS Aurora MySQL Database

## 데이터베이스 생성

### 생성방법 참조
- https://ap-northeast-2.console.aws.amazon.com/rds/home?region=ap-northeast-2#databases:

### EC2 서버에서 MySQL Client 접속
```bash
$ mysql -h database-etl-instance-1.cdzyivfisi6u.ap-northeast-2.rds.amazonaws.com -P 3306 -u admin -p
password:
...
```


## JDBC 설정방법

### 참조
- https://docs.aws.amazon.com/ko_kr/dms/latest/sbs/CHAP_RDSOracle2Aurora.Steps.ConnectAurora.html

