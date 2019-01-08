# Git section

## 기본 명령어

- 저장소 받아오기
    ```bash
    -- 로컬
    $ git clone /로컬/저장소/경로
    $ git clone /usr/workspace/target-project

    -- 원격
    $ git clone 사용장명@호스트:/원격/저장소/경로
    $ git clone https://github.com/jeedy/JBUK.git
    $ cd JBUK
    $ git remote set-url origin https://jeedy@github.com/jeedy/JBUK.git
    (이후 .git/config 설정 생략..)
    ```

- 추가, 커밋 그리고 푸쉬
    ```bash
    $ git add .
    $ git commit -m '커밋 코멘트'
    $ git push origin master
    ```

- 관리대상이 아닌 파일 삭제
    - -n : 옵션을 붙이면 삭제되는 파일 확인.
    - -f : 실제로 파일을 삭제
    - -x : .gitignore에 지정된 파일도 삭제
    ```bash
    $ git clean
    ```

