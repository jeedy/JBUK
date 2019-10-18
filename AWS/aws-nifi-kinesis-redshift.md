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
1. 테스트용 csv file(GenerateFlowFile) Process 생성 
2. PutKineisisFirehose Process 생성
3. GenerateFlowFile -> success -> PutKineisisFirehose 연결
4. LogAttribute Process 생성
5. PutKineisisFirehose -> success -> LogAttribute, PutKineisisFirehose -> fail -> LogAttribute 연결

큰 그림으로 보자면 위 순서로 진행된다. 이중에 핵심은 `2. PutKineisisFirehose Process 생성` 이다.
