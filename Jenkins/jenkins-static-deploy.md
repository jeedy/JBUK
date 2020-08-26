# 젠킨스 정적파일(static) 배포 방법

tags: jenkins, 젠킨스, 정적파일, static, deploy

Git에서 정적파일을 모두 pull 해온 이후 상황에서 apache web 서버에 배포(copy) 해야할 경우 어떻게 배포(copy) 해야 할까?


## try

### 1. ~~scp~~
ssh 프로토콜를 통해 scp를 이용할 경우 간단히 복사는 가능하나 **전체파일** 을 대상으로 복사하는건 네트워크 리소스 낭비

### 2. rsync
scp 대안으로 rsync 사용, 몇가지 주의사항만 이해하면 충분히 scp를 대체하고 static 파일들을 효율적으로 배포가능하다.

#### 주의사항
1. 젠킨스 item 생성시 `빌드 환경 > Delete workspace before build starts` 체크박스를 반드시 해제하자, 체크되어 있으면 빌드전에 workspace를 전체 삭제하기 때문에 매번 파일이 갱신되어 rsync 하는 의미가 없다.

2. git에서 pull 할때 젠킨스 `workspace`에 생성된 파일은 젠킨스 user로 되어 있고 파일 권한도 `640`(디렉토리 `750`) 로 되어있다. apache에서 사용하려면 apache user 와 디렉토리/파일 권한도(--chmod=D755,F644) 변경 해줘야 한다. 이는 rsync 옵션에서 제공하고 있어 한번에 처리 가능하다.

rsync with options:
```sh
# 젠킨스 서버내
$ rsync -alvr --delete --chown=apache:apache --chmod=D755,F644 --exclude='.git' /app/jenkins/workspace/static /target/cdn/static
```
