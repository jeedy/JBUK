# Apache 설정 관련

## httpd -V
아파치가 올라가 있다면 현재 아파치 환경설정들을 볼수있다.

##  –with-mpm=worker 혹은 –with-mpm=prefrork

*MPM(Multi-Processing Module) 다중처리모듈

## chrome Access-Control-Allow-Origin 설정

참고 자료
- http://huns.me/development/1291  cross domain 해결 방법에 대해 자세히 다루고 있다

https://www.travel.com/ 에서 https://static.travel.com/css/font/no-english.toff 파일을 읽어 오려고 한다면
https://static.travel.com Apache 서버에서 `Access-Control-Allow-Origin` 을 해줘야한다.


## Access-Control-Allow-Credentials ( Cross Origin Resource Sharing - CORS )

참고 자료
- http://huns.me/development/1291  cross domain 해결 방법에 대해 자세히 다루고 있다
- https://homoefficio.github.io/2015/07/21/Cross-Origin-Resource-Sharing/

표준 CORS는 기본적으로 요청을 보낼 때 쿠키를 전송하지 않는다. 쿠키를 요청에 포함하고 싶다면 XMLHttpRequest 객체의 withCredentials 프로퍼티 값을 true로 설정해준다.

```javascript
xhr.withCredentials = true;
```

그리고 서버 측도 반드시 Access-Control-Allow-Credentials 응답 헤더를 true로 설정해야 하고 Access-Control-Allow-Origin 헤더의 값에는 *가 오면 안되고 http://foo.origin 과 같은 구체적인 도메인이 와야 한다. (참고: https://homoefficio.github.io/2015/07/21/Cross-Origin-Resource-Sharing/)

```
Access-Control-Allow-Origin: http://foo.example
Access-Control-Allow-Credentials : true
```

CORS 요청이 성공하기 위해서는 이 두 개의 값(xhr.withCredentials, Access-Control-Allow-Credentials)이 모두 true 여야 하며, 그렇지 않을 경우 요청은 실패한다.