# CORS (Cross Origin Resource Sharing)
tags: cors, preflight, credential, Access-Control-, Origin, Access-Control-Request-Method, Access-Control-Request-Headers, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Max-Age, Access-Control-Allow-Credentials, xhr.withCredentials

참고자료:
- https://homoefficio.github.io/2015/07/21/Cross-Origin-Resource-Sharing/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS


## (핵심) Apache 설정 방법
내가 실제로 테스트해보고 경험을 토대로 적는다.

브라우저내에서 `www.other.com` 사이트에서 `www.test.com` 로 Ajax(API) 호출할 경우 기본적으로 cors 정책으로 호출이 불가능하다. 가능하게 하려면 `www.test.com` 서버측 설정이 필요한데
apache 기준으로 Preflight 를 위한 header set 을 해줘야한다. 

```sh
Header set Access-Control-Allow-Origin "*"
<IfModule mod_headers.c>
   SetEnvIfNoCase Origin "^(https?://.+\.other\.com|https?://.+\.another\.com)$" AccessControlAllowOrigin=$0
   Header set Access-Control-Allow-Origin %{AccessControlAllowOrigin}e env=AccessControlAllowOrigin
   Header set Access-Control-Allow-Credentials true
   Header set Access-Control-Allow-Headers "x-requested-with, Content-Type, origin, authorization, accept, X-Authorization"
</IfModule>
```

위 처럼 설정하면 `.other.com, another.com` 에서 `www.test.com` 에 Ajax(API) 호출이 가능해진다.

- SetEnvIfNoCase Origin : `other.com, another.com` 도메인에 대해서만 cors header 설정을 적용한다. (필수 설정)
- Access-Control-Allow-Origin: 허용하는 도메인을 설정한다. `SetEnvIfNoCase Origin` 를 통해 `other.com, another.com` 에 대해서만 CORS 요청이 가능하도록 한다. 값이 없을경우 Access-Control-Allow-Origin 값이 "*" 로 설정된다. 일부 Ajax는 Access-Control-Allow-Origin 값이 명시 되어야 한다.
- Access-Control-Allow-Headers: API 호출시 header 값에 `X-Authorization` 값에 accessToken 을 넣어 호출을 해야한다. 
만약 추가로 header 값을 받고 싶다면 `Access-Control-Allow-Headers` 에 추가한다.
- Access-Control-Allow-Credentials: true 라면 request시에 쿠키값까지 받을 수 있다. 물론 `.other.com` 에서 ajax 호출시 쿠키까지 보내는 설정 `xhr.withCredentials = true` 을 해줘야한다.


## CORS 에 대한 설명

HTTP 요청은 기본적으로 Cross-Site HTTP Requests 가 가능하다

하지만 **`<script></script>`로 둘러싸여 있는 스크립트**에서 생성된 Cross-Site HTTP Requests는 **Same Origin Policy를 적용** 받기 때문에 Cross-Site HTTP Requests가 불가능하다.

AJAX가 널리 사용되면서 <script></script>로 둘러싸여 있는 스크립트에서 생성되는 XMLHttpRequest에 대해서도 Cross-Site HTTP Requests가 가능해야 한다는 요구가 늘어나자 W3C에서 CORS라는 이름의 권고안이 나오게 되었다.

## 1. CORS 요청 종류

CORS 요청은 **Simple/Preflight, Credential/Non-Credential**의 조합으로 4가지가 존재한다.

### 1.1. Simple Request
아래의 3가지 조건을 모두 만족하면 Simple Request

- **GET, HEAD, POST** 중의 한 가지 방식을 사용해야 한다.

- **POST** 방식일 경우 **Content-type**이 아래 셋 중의 하나여야 한다.
    - application/x-www-form-urlencoded (일반적인 HTML 폼으로 전송,  =와 함께 표현하고 &의 묶음으로 표현)
    - multipart/form-data (일반적인 HTML 폼으로 전송)
    - text/plain (요청 바디가 raw일 때
    - 즉 application/json 형태로는 사용할 수 없다.

- 커스텀 헤더를 전송하지 말아야 한다.


Simple Request는 서버에 1번 요청하고, 서버는 1번 회신하는 것으로 처리가 종료된다.

Simple Request:
```http
GET /resources/public-data/ HTTP/1.1
Host: bar.other
User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3pre) Gecko/20081130 Minefield/3.1b3pre
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,\*/\*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,\*;q=0.7
Connection: keep-alive
Referer: http://foo.example/examples/access-control/simpleXSInvocation.html
Origin: http://foo.example


HTTP/1.1 200 OK
Date: Mon, 01 Dec 2008 00:23:53 GMT
Server: Apache/2.0.61
Access-Control-Allow-Origin: *
Keep-Alive: timeout=2, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/xml

[XML Data]
```


### 1.2. Preflight Request
Simple Request 조건에 해당하지 않으면 브라우저는 Preflight Request 방식으로 요청한다.

따라서, Preflight Request는

- GET, HEAD, POST 외의 다른 방식으로도 요청을 보낼 수 있고,
- applicationj/xml 처럼 다른 Content-type으로 요청을 보낼 수도 있으며,
- 커스텀 헤더로 사용할 수 있다.

이름에서 짐작할 수 있듯, Preflight Request는 **예비 요청**과 **본 요청**으로 나뉘어 전송된다.

먼저 서버에 예비 요청(Preflight Request)를 보내고 서버는 예비 요청에 대해 응답하고, 그 다음에 본 요청(Actual Request)을 서버에 보내고, 서버도 본 요청에 응답한다.

**하지만, 예비 요청과 본 요청에 대한 서버단의 응답을 프로그래머가 프로그램 내에서 구분하여 처리 하는 것은 아니다.**
프로그래머가 `Access-Control-` 계열의 Response Header 만 적절히 정해주면, `OPTIONS` Method 요청으로 오는 예비 요청과 GET, POST, HEAD, PUT, DELETE 등으로 오는 본 요청의 처리는 서버가 알아서 처리한다.

아래는 Preflight Request로 오가는 HEADER를 보여준다.

**다시 강조하지만, 아래 내용에서 프로그래머가 OPTIONS 요청의 처리 로직과 POST 요청의 처리 로직을 구분하여 구현하는 것이 아니다.**


Preflight Request and Actual Request:
```http
OPTIONS /resources/post-here/ HTTP/1.1
Host: bar.other
User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3pre) Gecko/20081130 Minefield/3.1b3pre
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,\*/\*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,\*;q=0.7
Connection: keep-alive
Origin: http://foo.example
Access-Control-Request-Method: POST
Access-Control-Request-Headers: X-PINGOTHER


HTTP/1.1 200 OK
Date: Mon, 01 Dec 2008 01:15:39 GMT
Server: Apache/2.0.61 (Unix)
Access-Control-Allow-Origin: http://foo.example
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: X-PINGOTHER
Access-Control-Max-Age: 1728000
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Length: 0
Keep-Alive: timeout=2, max=100
Connection: Keep-Alive
Content-Type: text/plain

POST /resources/post-here/ HTTP/1.1
Host: bar.other
User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3pre) Gecko/20081130 Minefield/3.1b3pre
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,\*/\*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,\*;q=0.7
Connection: keep-alive
X-PINGOTHER: pingpong
Content-Type: text/xml; charset=UTF-8
Referer: http://foo.example/examples/preflightInvocation.html
Content-Length: 55
Origin: http://foo.example
Pragma: no-cache
Cache-Control: no-cache

<?xml version="1.0"?><person><name>Arun</name></person>


HTTP/1.1 200 OK
Date: Mon, 01 Dec 2008 01:15:40 GMT
Server: Apache/2.0.61 (Unix)
Access-Control-Allow-Origin: http://foo.example
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Length: 235
Keep-Alive: timeout=2, max=99
Connection: Keep-Alive
Content-Type: text/plain

[Some GZIP'd payload]
```


### 1.3. Request with Credential (Cookie, http authenication 접근 )

**HTTP Cookie와 HTTP Authentication 정보를 인식할 수 있게 해주는 요청**

Simple Credential Request:
```javascript
var invocation = new XMLHttpRequest();
var url = 'http://bar.other/resources/credentialed-content/';

function callOtherDomain(){

  if(invocation) {
    invocation.open('GET', url, true);
    invocation.withCredentials = true;
    invocation.onreadystatechange = handler;
    invocation.send();
  }
  ...

```

요청 시 `xhr.withCredentials = true`를 지정해서 Credential 요청을 보낼 수 있고,
서버는 Response Header에 반드시 `Access-Control-Allow-Credentials: true`를 포함해야 하고,

**`Access-Control-Allow-Origin` 헤더의 값에는 `*`가 오면 안되고 `http://foo.origin`과 같은 구체적인 도메인이 와야 한다.**


### 1.4. Request without Credential
CORS 요청은 기본적으로 Non-Credential 요청이므로, xhr.withCredentials = true를 지정하지 않으면 Non-Credential 요청이다.



## 2. CORS 관련 HTTP Response Header 
서버에서 CORS 요청을 처리할 때 지정하는 헤더


### 2.1. Access-Control-Allow-Origin
Access-Control-Allow-Origin 헤더의 값으로 지정된 도메인으로부터의 요청만 서버의 리소스에 접근할 수 있게 한다.

Response Header:
```
Access-Control-Allow-Origin: <origin> | *
```

`<origin>`에는 요청 도메인의 URI를 지정한다.

모든 도메인으로부터의 서버 리소스 접근을 허용하려면 `*`를 지정한다. Request with Credential의 경우에는 `*`를 사용할 수 없다.


### 2.2. Access-Control-Expose-Headers
기본적으로 브라우저에게 노출이 되지 않지만, 브라우저 측에서 접근할 수 있게 허용해주는 헤더를 지정한다.

기본적으로 브라우저에게 노출이 되는 HTTP Response Header는 아래의 6가지 밖에 없다.

- Cache-Control
- Content-Language
- Content-Type
- Expires
- Last-Modified
- Pragma

다음과 같이 `Access-Control-Expose-Headers`를 Response Header에 지정하여 회신하면 브라우저 측에서 커스텀 헤더를 포함하여, 기본적으로는 접근할 수 없었던 Content-Length 헤더 정보도 알 수 있게 된다.

Resopnse Header:
```http
Access-Control-Expose-Headers: Content-Length, X-My-Custom-Header, X-Another-Custom-Header
```


### 2.3. Access-Control-Max-Age
Preflight Request의 결과가 캐쉬에 얼마나 오래동안 남아있는지를 나타낸다.

Response Header:
```http
Access-Control-Max-Age: <delta-seconds>
```


### 2.4. Access-Control-Allow-Credentials
Request with Credential 방식이 사용될 수 있는지를 지정한다.

Response Header:
```http
Access-Control-Allow-Credentials: true | false
```

예비 요청에 대한 응답에 `Access-Control-Allow-Credentials: false`를 포함하면, 본 요청은 Request with Credential을 보낼 수 없다.

Simple Request에 `withCredentials = true`가 지정되어 있는데, Response Header에 `Access-Control-Allow-Credentials: true`가 명시되어 있지 않다면, 그 Response는 브라우저에 의해 무시된다.


### 2.5. Access-Control-Allow-Methods
예비 요청에 대한 Response Header에 사용되며, 서버의 리소스에 접근할 수 있는 HTTP Method 방식을 지정한다.

Response Header:
```http
Access-Control-Allow-Methods: <method>[, <method>]*
```


### 2.6. Access-Control-Allow-Headers
예비 요청에 대한 Response Header에 사용되며, 본 요청에서 사용할 수 있는 HTTP Header를 지정한다.

Response Header:
```http
Access-Control-Allow-Headers: <field-name>[, <field-name>]*
```



## 3. CORS 관련 HTTP Request Headers
클라이언트가 서버에 CORS 요청을 보낼 때 사용하는 헤더로e, 브라우저가 자동으로 지정하며, XMLHttpRequest를 사용하는 프로그래머가 직접 지정해 줄 필요 없다.


### 3.1. Origin
Cross-site 요청을 날리는 요청 도메인 URI을 나타내며, access control이 적용되는 모든 요청에 `Origin` 헤더는 반드시 포함된다.

Request Header:
```http
Origin: <origin>
```

`<origin>`은 서버 이름(포트 포함)만 포함되며 경로 정보는 포함되지 않는다.

`<origin>`은 공백일 수도 있는데, 소스가 data URL일 경우에 유용하다.


### 3.2. Access-Control-Request-Method
예비 요청을 보낼 때 포함되어, 본 요청에서 어떤 HTTP Method를 사용할지 서버에게 알려준다.

Request Header:
```http
Access-Control-Request-Method: <method>
```

### 3.3. Access-Control-Request-Headers
예비 요청을 보낼 때 포함되어, 본 요청에서 어떤 HTTP Header를 사용할 지 서버에게 알려준다.

Request Header:
```http
Access-Control-Request-Headers: <field-name>[, <field-name>]*
```



## 4. XDomainRequest
**XDomainRequest(XDR)** 는 W3C 표준이 아니며, IE 8, 9에서 비동기 CORS 통신을 위해 Microsoft에서 만든 객체다.

- XDR은 `setRequestHeader`가 없다.
- XDR과 XHR(XMLHttpRequest)을 구분하려면 `obj.contentType`을 사용한다.(XHR에는 이게 없음)
- XDR은 http와 https 프로토콜만 가능



## 5. 결론
- CORS를 쓰면 AJAX로도 Same Origin Policy의 제약을 넘어 다른 도메인의 자원을 사용할 수 있다.
- CORS에서 `Preflight` 는 브라우저가 임의로 날리는 request이다. 그렇기 때문에 `server to server` 에서 이런 이슈가 없는 것이고 `Postman` 또는 `curl` 을 통한 호출시에도 CORS error가 발생하지 않는 것이다. 
- cors 테스트를 위해 `postman` 또는 `curl` 에서 `OPTIONS` Method로 호출하면 정상 Status 200 이 떨어지나 실제 브라우저에서는 status 401 error 가 발생하는 경우가 있어 `postman`, `curl`만으로 cors 를 테스트 하긴 역부족이다. 
- CORS를 사용하려면
  - ~~클라이언트에서 `Access-Control-**` 류의 HTTP Header를 서버에 보내야 하고,~~
  - 서버도 `Access-Control-**` 류의 HTTP response Header를 클라이언트에 회신하게 되어 있어야 한다.
  - 클라이언트에서 Ajax 호출시 쿠키값을 보내고 싶을땐 `withCredentials: true` 을 추가해야하고 서버에서도 `Access-Control-Allow-Credentials: ture` 값을 http response Header를 통해 회신해줘야한다.
  - 클라이언트가 `Origin`, `Authorization`, `X-PINGPONG` 과 같은 임의의 Header값들을 제공하려면 서버측 `Access-Control-Allow-Headers`(또는 `Access-Control-Expose-Headers`) 값에 해당 해더들을 등록해놔야한다.
  - `Authorization`, `X-Authorization` 또는 `숨기고 싶은 사용가능한 Header` 들은 `Access-Control-Expose-Headers`에 등록하면 Preflight response에 노출되지 않는다.



## 6. 참고 자료
- http://www.w3.org/TR/cors/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS


