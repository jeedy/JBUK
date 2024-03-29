# 리눅스에서 사용하는 필수 기본 명령어 모음
- nohup과 & 차이
    ```
    $ ./run &
    $ nohup ./run \&
    ```
    위 두 명령어의 차이점은 다음과 같습니다.
    nohup 으로 실행하면 hang-up signal 이 와도 동작하기 때문에 터미널 연결이 끊어져도 실행을 멈추지 않습니다.
    '& 으로만 실행해도 터미널이 끊어져도 실행이 멈추지는 않던데...' 라고 말하는 분들이 있을 것입니다. & 은 백그라운드로 돌린다는 의미이며, 기본적으로는 nohup 이 아닐 경우 터미널이 끊어지면 실행도 끊어집니다. 하지만 요즘 옵션에 nohup 과 같은 동작을 하게 설정이 되어 있어서 & 만으로도 nohup 과 같은 동작을 보입니다.

    > 팁
    만약 nohup명령어로 직접 만든 스크립트를 실행하고자 하는데 명령어를 입력한 후 엔터를 치면 exit이 나온다면 스크립트에 에러가 있어 종료가 되는 것입니다. 

- ls ``파일 리스트``
    - -F : 파일 유형을 나타내는 기호를 파일명 끝에 표시 (디렉토리는 '/', 실행파일은 '*', 심볼릭 링크는 '@'가 나타남).
    - -l  : 파일에 관한 상세 정보를 나타냅니다.
    - -a : dot 파일(.access 등)을 포함한 모든 파일 표시.
    - -t  : 파일이 생성된 시간별로 표시
    - -C : 도스의 dir/w명령과 같 이 한줄에 여러개의 정보를 표시
    - -R : 도스의 dir/s 명령과 같이 서브디렉토리 내용까지.
    ```bash
    (예)
    $ ls -al  
    $ ls -aC
    $ ls -R
    ```
- cd `디렉토리 변경`
    - cd ~ 접속자 Home 디렉토리로
    - cd - 바로 이전 디렉토리로
    
- whoami ```현재 로그인한 계정```
- login ``사용자 인증과정``
    리눅스 시스템은 기본적으로 multi-user 개념에서 시작하였기 때문에 시스템을 이용하기 위해서는 반드시 로그인을 하여야 합니 다. 로그인은 PC 통신에서도 많이 사용되어져 왔기 때문에 그 개 념  설정에 그다지 어려움이 없을 것입니다. 흔히 말하는 ID를 입력하는 과정입니다. 
- passwd ``패스워드 변경``
    리눅스, 특히 인터넷의 세계에서는 일반 컴퓨팅 상황에 비하여 훨씬 해킹에 대한 위험이 높습니다. 패스워드는 완성된 단어 보다는 단어 중간에 숫자나 키보드의 ^, #, ' 등과 같은 쉽게 연상 할 수 없는 기호를 삽입하여 만들어 주는 것이 좋습니다
- du ``하드사용량 체크(chkdsk)``
    자신의 하드공간을 알려면
    ```bash
    $ du
    ```
    특정 디렉토리의 사용량을 알려면
    ```bash
    $ du -s diretory_name
    ```
- cp ``파일 복사(copy)``
    ```bash
    $ cp index.html index.old 
     : index.html 화일을 index.old 란 이름으로 복사.

    $ cp /home/test/*.*  . 
     : test 디렉토리내의 모든 화일을 현 디렉토리로 복사.
     ```
- mv ```파일이름(rename) / 위치(move)변경```
    ```bash
    $ mv index.htm index.html
     : index.htm 화일을 index.html 로 이름 변경

    $ mv file  ../main/new_file 
     : 파일의 위치변경
     ```
- mkdir ```디렉토리 생성```
- rm ```파일 삭제```
    ```bash
    $ rm test.html : test.html 화일 삭제
    $ rm -r <디렉토리> : 디렉토리 전체를 삭제
    $ rm -i a.* 
     : a로 시작하는 모든 파일을 일일이 삭제할 것인지 확인하면서 삭제 
    ```
- rmdir ```디렉토리 삭제```
- pwd ```현재의 디렉토리 경로를 보여줌```
- alias ```긴 명령어들을 예약 할 수 있음```
    " doskey alias" 와 비슷하게 이용할 수 있는 쉘 명령어 alias는 말그대로 별명입니다. 사용자는 alias를 이용하여 긴 유 닉스 명령어를 간단하게 줄여서 사용할 수도 있습니다. 
    이들 앨리어스는 [alias ls 'ls -al'] 같이 사용하시면 되는데, 한 번 지정한 alias를 계속해서 이용하시려면, 자신의 홈디렉토리에 있는 
    .cshrc(Hidden 속성)을 pico등의 에디터를 이용하여 변경시 키면 됩니다.
- source ```스크립트 파일을 수정한 후에 수정된 값을 바로 적용하기 위해 사용하는 명령어```
    예륻들어 ``~/.bash_profile`` 파일을 수정 후 저장하여도 수정한 내용이 바로 적용되지 않는다.
    왜냐하면 ``~/.bash_profile`` 파일은 유저가 로그인할 때 읽어들이는 파일이여서, 로그아웃 후 로그인하거나 리눅스를 재시작해야 적용이 된다.
    이럴경우 간단하게 ``$ source ~/.bash_profile`` 명령어로 수정된 내용을 바로 적용할 수 있다.
- ps ``현재 시스템에서 돌고있는 프로세스``
    > ps 명령은 옵션 입력 방법이 bsd 스타일과 unix 스타일, gnu 스타일로 나뉩니다. bsd 스타일은 'ps aux'와 같이 대쉬가 없는 스타일인 반면 unix 스타일은 'ps -ef' 처럼 옵션앞에 대쉬를 넣어 옵션임을 표시하는 스타일입니다. gnu 스타일은 대쉬를 두개 넣는 스타일로 'ps --help' 처럼 사용합니다. 동일하게 문자 u를 사용하는 옵션이라도 대쉬의 유무에 따라 의미가 달라집니다.
    ```bash
    $ ps ax 
      PID   TTY     STAT TIME COMMAND 
        1   ?       Ss   0:04 /sbin/init
        2   ?       S    0:00 [kthreadd]
    25011   pts/14  Ss   0:00 -bash
    25107   pts/14  R+   0:00 ps ax 

    $ ps -e 
      PID   TTY     TIME      CMD 
        1   ?       00:00:04  init 
        2   ?       00:00:00  kthreadd
    25011   pts/14  00:00:00  bash 
    25149   pts/14  00:00:00  ps

    $ ps aux
        : 더 자세한 프로세스의 정보 (ps -ef)
    
    $ ps -fu user
        : 특정 사용자 이름으로 검색
    
    $ ps aux --sort=-pcpu,-pmem | head -5
        : cpu나 메모리 사용량으로 정렬, 상위 5개만 출력 (오름차순과 내림차순을 지정하는 심볼은 '+', '-')
    ```
- grep ``명령은 파일 내에서 지정한 패턴이나 문자열을 찾은 후에, 그 패턴을 포함하고 있는 모든 행을 표준 출력해 준다.``
    ```bash
    $ grep [옵션] [찾을 문자열 정규 표현식] [파일명]
    $ grep "run[-] time" ch04
        : 이 구문은 ch04라는 파일에서 run-time 또는 run time이 들어 있는 행을 찾을 때 사용한다. 생물 데이터를 다루다보면 특정 유전자의 이름이 들어 있는 행 등 특정 키워드를 가진 행을 찾을 때 사용하면 된다.
    $ ps aux | grep python
        : 이 구문은 현재 작업 중인 프로세스 중에서 python이 들어간 행을 찾아낸다. 복잡한 프로세스 과정 중에서 현재 실행 중인 프로세스를 조회하는 ps 명령을 파이프 | 와 함께 사용하면 특정 이름을 가진 프로세스를 찾아낼 수 있게 된다.
    ```
     *자주 쓰는 명령어 옵션에는 -i, -c, -w를 사용한다*
    - -c : 패턴이 일치하는 행의 수를 출력한다.
    - -i : 비교시 대소문자를 구별하지 않는다.
    - -v : 지정한 패턴과 일치하지 않는 행만 출력한다.
    - -n : 행의 번호를 함께 출력한다.
    - -l : 패턴이 포함된 파일의 이름을 출력한다.
    - -w : 패턴이 전체 단어와 일치하는 행만 출력한다.
    ```bash
    $ ps aux | grep python | grep -v grep
        : 이 경우에는 grep 을 포함한 명령어가 출력되기 때문에 grep 명령어는 제외할 수가 있다.
    ```
- export ```리눅스에서 환경변수 선언```
    export [변수명]=[데이터값]
    ```bash
    $ export Hello="hi"
    ``` 
- echo ```문자열 및 환경변수(export로 선언된) 출력```
    ```bash
    $ echo "Hello world"
    Hello world
        : 단순 문자 출력

    $ export Hello="hi"
    $ echo $Hello
    hi
        : export로 선언된 변수 값 출력
    ```
- chown ```파일의 소유자나 그룹을 변경```
    사용예
    ```bash
    $ chown root FILE
        : FILE의 소유 유저를 root로 변경 한다.

    $ chown root:staff FILE
        : FILE의 소유 유저를 root로, 그룹을 staff로 변경 한다.

    $ chown -hR root FILE
        : FILE의 서브 디렉토리의 모든 파일의 소유 유저를 root로 변경한다. 심볼릭 링크의 권한까지 변경한다.
    ```
- chmod ```파일 permission 변경```
    리눅스에서는 각 화일과 디렉토리에 사용권한을 부여.
    
    ```
    예) -rwxr-xr-x   guestbookt.html
    rwx  :처음 3개 문자 = 사용자 자신의 사용 권한
    r-x  :그다음 3개 문자 = 그룹 사용자의 사용 권한
    r-x  :마지막 3개 문자 = 전체 사용자의 사용 권한
    ```
    ```
    읽기(read)---------- 화일 읽기 권한
    쓰기(write)---------- 화일 쓰기 권한
    실행(execution)---------- 화일 실행 권한
    없음(-)---------- 사용권한 없음
    ```
    ```
    chmod **7(사용자) 7(그룹) 7(전체)**
    r은 파일 읽기(4), w는 파일 쓰기(2), x는 파일 실행(1)
    큰수(r: 4) 부터 차례대로 빼면 어떤 권한이 나오는지 알수 있음.
    ```

    **명령어 사용법**
    **chmod [변경모드] [파일]**
    ```bash
    $ chmod 666  guestbook.html
        : test.html 화일을 자신과 그룹사용자와 전체사용자에게 r,w 권한을 줌

    $ chmod 766  guestbook.html
        : 자신은 모든 권한을 그룹사용자와, 전체사용자에게는 r와 w 권한만 줌
    ```
    
    #### 파일권한

    <table cellspacing="0" bordercolordark="white" bordercolorlight="black" border="1" width="685">
    <tbody>
    <tr>
    <td colspan="3" width="38">
    <p align="center"><font color="#d00000">Owner</font></p></td>
    <td colspan="3" width="38">
    <p align="center"><font color="#d00000">Group</font></p></td>
    <td colspan="3" width="38">
    <p align="center"><font color="#d00000">Other</font></p></td>
    <td width="553">
    <p><font color="#003098">Owner와 Group은 파일소유자자신과 자신이 속한그룹. Other은 제3자, 웹사이트 
    방문객은 제3자로 nobody로 취급.</font></p></td></tr>
    <tr>
    <td width="10" halign="center">
    <p align="center"><font color="#d00000">r<br>(4)</font></p></td>
    <td width="10" halign="center">
    <p><font color="#d00000">w<br>(2)</font></p></td>
    <td width="10" halign="center">
    <p><font color="#d00000">x<br>(1)</font></p></td>
    <td width="10" halign="center">
    <p align="center"><font color="#d00000">r<br>(4)</font></p></td>
    <td width="10" halign="center">
    <p><font color="#d00000">w<br>(2)</font></p></td>
    <td width="10" halign="center">
    <p><font color="#d00000">x<br>(1)</font></p></td>
    <td width="10" halign="center">
    <p align="center"><font color="#d00000">r<br>(4)</font></p></td>
    <td width="10" halign="center">
    <p><font color="#d00000">w<br>(2)</font></p></td>
    <td width="10" halign="center">
    <p><font color="#d00000">x<br>(1)</font></p></td>
    <td width="553" halign="center">
    <p><font color="blue">r은 파일 읽기(4), w는 파일 쓰기(2), x는 파일 
    실행(1)</font></p></td></tr>
    <tr>
    <td colspan="3" width="38">
    <p align="center">7<br>r + w + x</p></td>
    <td colspan="3" width="38">
    <p align="center">5<br>r + x</p></td>
    <td colspan="3" width="38">
    <p align="center">5<br>r + x</p></td>
    <td width="553">
    <p><font color="#003098">파일소유자는 그것을 읽고 쓰고 실행시킬 수 
    있지만, 제3자는 읽고 실행만 시킬 수 있다.</font></p></td></tr>
    <tr>
    <td colspan="3" width="38">
    <p align="center">7<br>r + w + x</p></td>
    <td colspan="3" width="38">
    <p align="center">7<br>r + w + x</p></td>
    <td colspan="3" width="38">
    <p align="center">7<br>r + w + x</p></td>
    <td width="553">
    <p> <font color="#003098">제3자도 쓰기 권한이 주어진다.</font></p></td></tr></tbody></table>

- hostnamectl ```서버 호스트명 변경```
```sh
$ sudo hostnamectl set-hostname {변경할 호스트명}

#예시
$ sudo hostnamectl set-hostname apache-01
$ hostname
apache-01
```

- kill -HUP ```프로세스 종료가 아닌 refresh, 환경설정을 반영하고 싶을때```
    > 참고: https://ktdsoss.tistory.com/312
    ### 그 밖에 옵션들
    - kill -KILL(9) <pid> : 하드웨어적 종료 (가장강력)
    - kill -TERM(15) <pid> : 소프트웨어적 종료 (소프트웨어에 따라 실행유무결정)
    - kill -HUP(1) <pid> : 데몬의 경우 종료 후, 다시시작 (프로세스 종료가 아닌 코드 및 데이터 refresh 역할)
    - kill -2 <pid> : 포그라운드에서 `ctrl + c` (작업취소)를 누르는 것과 동일
    - kill -3 <pid> : 포그라운드에서 `ctrl + w` (더 강력한 작업취소)를 누르는 것과 동일

    ```sh
    $ sudo kill -HUP $(ps -ef | grep 'openresty\/nginx' | awk '{ print $2; }')

    ```
