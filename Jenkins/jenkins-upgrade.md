# 젠킨스 업그레이드

## 1. 백업
1. 젠킨스 war 백업
1. 젠킨스 환경설정 백업 (JENKINS_HOME, .jenkins)
config.xml 이 있는 폴더 전체를 tar 압푹하면 좋다. (단, jobs는 용량이 클수 있으니 제외하자)
```bash
$ tar -cvf .jenkins.tar .jenkins/ --exclude .jenkins/jobs
```