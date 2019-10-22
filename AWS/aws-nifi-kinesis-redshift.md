# AWS 에서 Nifi를 이용해 redshift에 데이터 적제방법 (feat. kinesis firehose)
nifi 설치 및 실행방법은 [nifi 설치](/infi/instrall-nifi.md) 페이지를 참고한다.

## 참고
- [How Stream Data Into AWS Redshift with Apache NiFi](https://www.youtube.com/watch?v=SZrcFlmViBY)

## 테스트 개요
결국, 위 테스트는 csv 파일을 읽어 AWS Redshift에 데이터를 적재 하는 것이 목표이다. 

그러나 Redshift에 데이터를 적재하기까지는 많은 기술들과 tool의 사용 경험치를 필요로 한다. 
단순히 나열하면 Apache Nifi를 시작으로 
AWS Kinesis firehose,AWS S3,AWS IAM 그리고 SQLWorkbench 까지 전부 경험해야 한다.  

## 순서 
1. [테스트용 csv file(GenerateFlowFile) Process 생성](#1-테스트용-csv-filegenerateflowfile-process-생성) 
2. PutKineisisFirehose Process 생성
    - SQLWorkbench 설치
3. GenerateFlowFile -> success -> PutKineisisFirehose 연결
4. LogAttribute Process 생성
5. PutKineisisFirehose -> success -> LogAttribute, PutKineisisFirehose -> fail -> LogAttribute 연결
6. 시작

큰 그림으로 보자면 위 순서로 진행된다. 이중에 핵심은 `2. PutKineisisFirehose Process 생성` 이다.

## 1. 테스트용 csv File(GenerateFlowFile) Process 생성
1. GenerateFlowFile Process 추가
2. `properties` 탭에서 `Custom Text` 속성 값에 csv형태의 텍스트(AO, 12, M) 로 입력.
3. `scheduling` 탭에서 `Run Schedule` 속성 값을 `1 sec`로 데이터가 많이 쌓이지 않도록 적절하게 셋팅하자 


## 2. PutKineisisFirehose Process 생성

### SQLWorkbench 설치 
Redshift에 data 들어가는거 편하게 확인하려면 설치, 설치 주소는 http://www.sql-workbench.net/manual/install.html

### PutKineisisFirehose Process 추가
- `Amazon Kinesis Firehose Delivery Stream Name` 입력:  firehose 생성시 알게됨.
- Region 설정: firehose 생성한 region
- `Access Key ID`, `Secret Access Key` : **매우 중요** AWS IAM 계정하나 만들어서 그 계정 정보를 넣어함. 이 설명이 어디에도 없어.

### redshift 생성
- redshift IAM Roles에는 특별히 등록한 것이 없음    
- 마스터 사용자 아이디/암호는 잘 기록해놔야 함

### AWS Kinesis firehose 생성
- 생성시 S3도 같이 생성

### AWS IAM 계정 생성 of Firehose
- nifi 에서 firehose 사용시 `IAM 계정` 반드시 필요
- nifi `PutKinesisFirehose` proessor 에서 properties 설정시 `Access Key ID`, `Secret Access Key` 값에 IAM 키입력


## 3. GenerateFlowFile -> success -> PutKineisisFirehose 연결


## 4. LogAttribute Process 생성


## 5. PutKineisisFirehose -> success -> LogAttribute, PutKineisisFirehose -> fail -> LogAttribute 연결


## 6. 시작











