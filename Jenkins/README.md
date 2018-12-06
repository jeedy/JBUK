# Apache Jenkins

1. 프로젝트 빌드가 되는 workspace는 기본적으로 `~/.jenkins/workspace/` 폴더이나 이 위치를 수정하고 싶을 경우 `~/.jenkins/config.xml` 파일 안에 `<workspaceDir>` 태그에서 가능하다.
1. 톰켓으로 구동할때 톰켓 설정(server.xml)에서 `<context> > docBase > path` 값을 `/jenkins`로 설치할 경우, 젠킨스 시스템 설정 ( http://jenkinsip.com:8080/jenkins/configure/ ) 안에 `Jenkins Location > Jenkins URL` 값을 서버 Path에 맞게 설정이 꼭 필요하다.
1. 젠킨스 구조
    - 기본 셋팅 환경설정 ~/.jenkins/config.xml
    - 플러그인 파일 ~/.jenkins/plugins/
    - 자바,메이븐등 툴 자동설치 위치 ~/.jenkins/tools/
    - 프로젝트 빌드 Item 정보 ~/.jenkins/jobs/
    - 유저 정보 ~/.jenkins/users/
1.

## Exception
1. /usr/lib/tomcat/temp/jenkins480174068218113004.sh: line 2: unexpected EOF while looking for matching `"'
    - Execute shell command 값에 잘못된 표현식이 있는지 확인