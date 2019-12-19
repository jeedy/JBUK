# CORS (Cross Origin Resource Sharing)
tags: cors, preflight, credential, Access-Control-, Origin, Access-Control-Request-Method, Access-Control-Request-Headers, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Max-Age, Access-Control-Allow-Credentials, xhr.withCredentials

HTTP 요청은 기본적으로 Cross-Site HTTP Requests 가 가능하다

하지만 **`<script></script>`로 둘러싸여 있는 스크립트**에서 생성된 Cross-Site HTTP Requests는 **Same Origin Policy를 적용** 받기 때문에 Cross-Site HTTP Requests가 불가능하다.

AJAX가 널리 사용되면서 <script></script>로 둘러싸여 있는 스크립트에서 생성되는 XMLHttpRequest에 대해서도 Cross-Site HTTP Requests가 가능해야 한다는 요구가 늘어나자 W3C에서 CORS라는 이름의 권고안이 나오게 되었다.

## 1. CORS 요청 종류

CORS 요청은 Simple/Preflight, Credential/Non-Credential의 조합으로 4가지가 존재한다.

### 1.1. Simple Request
아래의 3가지 조건을 모두 만족하면 Simple Request

- **GET, HEAD, POST** 중의 한 가지 방식을 사용해야 한다.

- **POST** 방식일 경우 **Content-type**이 아래 셋 중의 하나여야 한다.
    - application/x-www-form-urlencoded (일반적인 HTML 폼으로 전송,  =와 함께 표현하고 &의 묶음으로 표현)
    - multipart/form-data (일반적인 HTML 폼으로 전송)
    - text/plain (요청 바디가 raw일 때
    - 즉 application/json 형태로는 사용할 수 없다.

- 커스텀 헤더를 전송하지 말아야 한다.


Simple Request는 서버에 1번 요청하고, 서버는 1번 회시하는 것으로 처리가 종료된다.

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



### 2.3. Access-Control-Max-Age




### 2.4. Access-Control-Allow-Credentials



### 2.5. Access-Control-Allow-Methods



### 2.6. Access-Control-Allow-Headers





## 3. CORS 관련 HTTP Request Headers
클라이언트가 서버에 CORS 요청을 보낼 때 사용하는 헤더로, 브라우저가 자동으로 지정하며, XMLHttpRequest를 사용하는 프로그래머가 직접 지정해 줄 필요 없다.


### Origin

