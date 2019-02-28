# 비동기로 API 호출을 하기

> tags:
Httpclient, HttpAsyncClient, 비동기, HttpAsyncClient, CloseableHttpAsyncClient, HttpPost, HttpGet, API, Future, FutureCallback, CountDownLatch

HttpClient를 이용해 request를 던지고 response를 받는다는 기본구조에서 쉽게 생각하면 Request들을 모두 던저 놓고 response들을 가져다가 뿌려주면 된다고 생각할 수 있다.

그러나 실제로 구현할때는 저렇게 간단하지 않다.

각 request url들은 array로 선언해 순서대로 던질 것이고, 이때 던진 순서에 맞게 response도 Array 형태로 받아서 다른 비즈니스 로직에 던져지는 방식으로 개발될 것이다.

하지만 비동기기 때문에 누가 먼저  Response 될지는 알 수 없다.
그리고 전부 Response 된 시점도 알 수 없다.


## HttpAsyncClient

HttpClient는 동기 방식이고 HttpAsyncClient가 비동기 방식으로 호출한다.


## Future

HttpAsyncClient를 통해 request를 날릴때 마다 반환되는 객체가 Future<HttpResponse> 이다.


## FutureCallback

callback response 상황에서 각 상황별 처리 로직을 구현하기 위한 클래스이다.

## CountDownLatch

request들이 모두 회수 되는 시점을 알기 위해 사용하는 클래스이다.

