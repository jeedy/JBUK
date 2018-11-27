# Apache Jenkins

1. 프로젝트 빌드가 되는 workspace는 기본적으로 `~/.jenkins/workspace/` 폴더이나 이 위치를 수정하고 싶을 경우 `~/.jenkins/config.xml` 파일 안에 `<workspaceDir>` 태그에서 가능하다.
1. 톰켓으로 구동할때 톰켓 설정(server.xml)에서 `<context> > docBase > path` 값을 `/jenkins`로 설치할 경우, 젠킨스 시스템 설정 ( http://jenkinsip.com:8080/jenkins/configure/ ) 안에 `Jenkins Location > Jenkins URL` 값을 서버 Path에 맞게 설정이 꼭 필요하다.
1.