# Encrypting Amazon RDS Resources : AWS RDS 데이터 암호화방법
tags: aws, rds, 암호, kms, key management service, aroura, mysql, 

## 참고 자료
- https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/UserGuide/Overview.Encryption.html (암호화방법에 대한 AWS 문서)


## 작업 

### 확인된 내용
- AWS Aroura 를 이용해야 AWS에서 제공하는 암호화를 사용할  수 있다. 2019년 11월 기준으로 mysql, PostgreSQL 과 호환되는 DB를 구축할 수 있다.
- 

### 작업순서 

1. KMS(key management service) 생성

    Amazon RDS 리소스의 암호화 및 암호 해독에 사용되는 키

1. RDS 생성
    
    1. 생성시 위에서 생성한 KMS를 이용하자.