# JSONP 에서 TLSv1.2 셋팅 방법 for Jboss

> tags: JSONP, Jboss, TLS, HTTPS, SSL

## 참고
- https://stackoverflow.com/questions/34236421/jsoup-error-remote-host-closed-connection-during-handshake

## spec
- java 1.7
- jboss6

## 상황
JSONP 을 사용하는 코드에서 "Remote host closed connection during handshake" javax.net.ssl.SSLHandshakeException 발생
(이전엔 잘되었으나 어느 시점부터 호출이 불가능했는지 알 수 없음)

## 해결방법
서버 start.sh 시 자바 옵션에 `-Dhttps.protocols=TLSv1.2` 추가

```
-Dhttps.protocols=TLSv1.2
```

Tomcat 7 에서는 정상동작하는 것으로 봐선 Tomcat 7 에선 TLS v1.2 버전을 기본적으로 지원하는 듯함. 그러나 Jboss는
자바옵션을 붙여주지 않으면 handshake 과정에서 Exception 발생.
