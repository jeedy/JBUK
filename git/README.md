# Git

## 기본 명령어

### 저장소 받아오기
```bash
# 로컬
$ git clone /로컬/저장소/경로
$ git clone /usr/workspace/target-project

# 원격
$ git clone 사용장명@호스트:/원격/저장소/경로
$ git clone https://github.com/jeedy/JBUK.git
$ cd JBUK
$ git remote set-url origin https://jeedy@github.com/jeedy/JBUK.git
(이후 .git/config 설정 생략..)
```

### 추가, 커밋 그리고 푸쉬
```bash
$ git add .
$ git commit -m '커밋 코멘트'
$ git push origin master
```

### 관리대상이 아닌 파일 삭제
- -n : 옵션을 붙이면 삭제되는 파일 확인.
- -f : 실제로 파일을 삭제
- -x : .gitignore에 지정된 파일도 삭제
```bash
$ git clean
```

### commit 되돌리기
```bash
# [방법 1] commit을 취소하고 해당 파일들은 staged 상태로 워킹 디렉터리에 보존
$ git reset --soft HEAD^
# [방법 2] commit을 취소하고 해당 파일들은 unstaged 상태로 워킹 디렉터리에 보존
$ git reset --mixed HEAD^ // 기본 옵션
$ git reset HEAD^ // 위와 동일
$ git reset HEAD~2 // 마지막 2개의 commit을 취소
# [방법 3] commit을 취소하고 해당 파일들은 unstaged 상태로 워킹 디렉터리에서 삭제
$ git reset --hard HEAD^
```

#### 잘못 올라간 파일 삭제 방법
```bash
# 원격 저장소와 로컬 저장소에 있는 파일을 삭제한다.
$ git rm [File Name]
# 원격 저장소에 있는 파일을 삭제한다. 로컬 저장소에 있는 파일은 삭제하지 않는다.
$ git rm --cached [File Name]
# maven target/ 폴더 하위의 모든 파일 삭제 
$ git rm --cached -r target/
# .gitignore 파일에 제외파일(폴더) 설정
```