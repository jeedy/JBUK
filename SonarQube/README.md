# 소나큐브(SonarQube)
tags: sonarqube, 소나큐브, 젠킨스, 
## 목차
1. [소나큐브 설치 및 젠킨스 연결](./install-sonarqube-with-jenkins-svn-maven.md)
2. [소나큐브 개발자 가이드](./sonarqube-user-guide.md)

## :bomb: troubleshooting

### 1. 소나큐브 대쉬보드에서 이슈 조회시 매우 느린 현상

#### condition
- mysql
- 매우 오래동안 접속하지 않았음

한동안 조회를 안하다가 조회하려고 보니 부하가 생긴 것이 아닌가 하는 생각.

#### 해결방법
Mysql 통계 정보를 갱신을 해주니 속도가 나아졌음.

editor.sql:
```sql
ANALYZE TABLE tb_test;
```
