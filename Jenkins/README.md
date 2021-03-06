# Apache Jenkins

1. 프로젝트 빌드가 되는 workspace는 기본적으로 `~/.jenkins/workspace/` 폴더이나 이 위치를 수정하고 싶을 경우 `~/.jenkins/config.xml` 파일 안에 `<workspaceDir>` 태그에서 가능하다.
1. 톰켓으로 구동할때 톰켓 설정(server.xml)에서 `<context> > docBase > path` 값을 `/jenkins`로 설치할 경우, 젠킨스 시스템 설정 ( http://jenkinsip.com:8080/jenkins/configure/ ) 안에 `Jenkins Location > Jenkins URL` 값을 서버 Path에 맞게 설정이 꼭 필요하다.
1. 젠킨스 구조
    - 기본 셋팅 환경설정 ~/.jenkins/config.xml
    - 플러그인 파일 ~/.jenkins/plugins/
    - 자바,메이븐등 툴 자동설치 위치 ~/.jenkins/tools/
    - 프로젝트 빌드 Item 정보 ~/.jenkins/jobs/
    - 유저 정보 ~/.jenkins/users/

## Job configure 에서 패스워드 환경변수 설정

job configure > 빌드 환경 > "Use secret text(s) or file(s)" 체크 > Bindings > Add

등록후 Build.xml 설정에서 아래
#### 참고
https://support.cloudbees.com/hc/en-us/articles/203802500-Injecting-Secrets-into-Jenkins-Build-Jobs

![패스워드 환경변수 설정](./images/binding-secret-text.PNG)


## 프로젝트별 권한 설정

플러그인 설치

https://wiki.jenkins.io/display/JENKINS/Role+Strategy+Plugin

1. Jenkins 관리 > Configure Global Securitry > Enable security checked. > Role-Based Strategy radio checked.

    ![Enable security](./images/role-strategy-01.png)

1. Jenkins 관리 > Manage and Assign Roles > Manage Roles

    1. Global roles 에 기본 권한("job-creator") 추가 > Overall > Read 체크 (이래야 메인화면이 제대로 노출)

    1. Project roles 에서 각 프로젝트별 role 설정을 한다. role은 "name" Pattern은 "job 이름 패턴" 이다.

        예) Sample.* 패턴을 가지면 Sample-common, Sample-mobile, Sample-front ... 등 "Sample" 로 시작하는 모든 job을 묶어준다.

     ![global role](./images/role-strategy-04.png)

1. Jenkins 관리 > Manage and Assign Roles > Assign Roles

    1. Global roles 에서 유저 설정

    1. Item roles 에서 앞서 생성한 "Project roles" 과 유저간의 룰 매칭



## :bomb: troubleshooting
1. /usr/lib/tomcat/temp/jenkins480174068218113004.sh: line 2: unexpected EOF while looking for matching `"'
    - 프로젝트 job > 구성(configure) > `Execute shell command` 필드에 잘못된 표현식이 있는지 확인

1. jenkins에서 빌드된 war를 ant로 전송하려고 할때 permission 에러 발생
    - 원인: TOMCAT을 통해 jenkins를 올렸을 경우 파일을 권한이 750으로 권한주고 빌드하기 때문이라고함.
    - 해결방법: {TOMCAT_HOME}/bin/catalina.sh  파일안에 `umask = "0027"` 이부분을 `umask = "0022"` 로 수정해야함.

1. jenkins 서버 용량 부족 에러 (No space left on device)
    - 원인: JENKINS_HOME(기본위치 /home/user/.jenkins) 가 속한 root 디렉토리의 용량이 (`df -h`로 확인가능) full로 차있어서 `.jenkins/jobs` 에 있는 build history 파일들을 생성을 못해 발생하는 오류
    - 해결방법:
        1. root 디렉토리 용량을 늘린다.
        2. /home/user 디렉토리를 용량 많은 디렉토리(`/sdb1/`)로 `symbolick link` 한다.
        3. .bash_profile에서 `JENKINS_HOME` 경로를 변경해 준다. (Default : ~/.jenkins)
