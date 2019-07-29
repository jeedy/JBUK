# SpringBoot

## :bomb: troubleshooting
1. spring boot에서 기본 sessionid `session`을 `JSESSIONID`로 수정하는 방법

    `application.properties` 파일에 `server.servlet.session.cookie.name`에 `JSESSIONID`을 입력한다.
    
application.properties:
```properties
server.port = 80
server.contextPath=/
server.servlet.session.cookie.name=JSESSIONID

... 
``` 