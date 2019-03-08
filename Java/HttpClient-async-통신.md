# 비동기로 API 호출을 하기

> tags:
Httpclient, HttpAsyncClient, 비동기, HttpAsyncClient, CloseableHttpAsyncClient, HttpPost, HttpGet, API, Future, FutureCallback, CountDownLatch

HttpClient를 이용해 request를 던지고 response를 받는다는 기본구조에서 쉽게 생각하면 Request들을 모두 던저 놓고 response들을 가져다가 뿌려주면 된다고 생각할 수 있다.

그러나 실제로 구현할때는 저렇게 간단하지 않다.

각 request url들은 array로 선언해 순서대로 던질 것이고, 이때 던진 순서에 맞게 response도 Array 형태로 받아서 다른 비즈니스 로직에 던져지는 방식으로 개발될 것이다.

하지만 비동기기 때문에 누가 먼저 Response 될지는 알 수 없다. 그리고 전부 Response 된 시점도 알 수 없다.

누가 먼저 Response 될지는 `FutureCallback`을 통해서 그리고 전부 response 된 시점을 알기 위해 `CountDownLatch` 객체를 사용한다.


## HttpAsyncClient

HttpClient는 동기 방식이고 HttpAsyncClient가 비동기 방식으로 호출한다.


## Future

HttpAsyncClient를 통해 request를 날릴때 마다 반환되는 객체가 Future<HttpResponse> 이다.


## FutureCallback

callback response 상황에서 각 상황별 처리 로직을 구현하기 위한 클래스이다.

## CountDownLatch

request들이 모두 회수 되는 시점을 알기 위해 사용하는 클래스이다.

## 참고 예제 소스
```java
/**
   * 비동기 HttpPost 호출
   *
   * @param headers 해더 입력
   * @param urls (필수) 순서 중요함. request 날릴 url 배열
   * @param bodys (필수) urls 같은 순서로 배열
   * @return urls 배열 순서대로 리턴
   */
  public static String[] getAsyncHttpPOST2Strings(Map<String, String> headers, String[] urls,
      String[] bodys) {

    int timeout = 480;    // sec
    RequestConfig requestConfig = RequestConfig.custom()
        .setSocketTimeout(timeout * 1000)
        .setConnectionRequestTimeout(timeout * 1000)
        .setConnectTimeout(timeout * 1000)
        .build();

    String[] results = new String[urls.length];
    try (CloseableHttpAsyncClient httpclient = HttpAsyncClients.custom()
        .setDefaultRequestConfig(requestConfig).build()) {

      httpclient.start();

      Future<HttpResponse>[] responses = new Future[urls.length];
      final CountDownLatch latch = new CountDownLatch(urls.length);

      for (int idx = 0; idx < urls.length; idx++) {
        HttpPost post = new HttpPost(urls[idx]);

        if (headers != null && !headers.isEmpty()) {
          for (String key : headers.keySet()) {
            post.addHeader(key, headers.get(key));
          }
        }

        if (bodys[idx] != null) {
          StringEntity params = new StringEntity(bodys[idx], "UTF-8");
          post.setEntity(params);
        }

        responses[idx] = httpclient.execute(post, new FutureCallback<HttpResponse>() {
          @Override
          public void completed(HttpResponse httpResponse) {
            latch.countDown();
            try {
              if (httpResponse.getStatusLine().getStatusCode() != 200) {

                String body = EntityUtils.toString(post.getEntity(), "UTF-8");
                String res = EntityUtils.toString(httpResponse.getEntity(), "UTF-8");
                logger.error("{} -> {} -> {} => {}", post.getRequestLine(), body,
                    httpResponse.getStatusLine(), res);

              } else {
                if (logger.isDebugEnabled()) {
                  String body = EntityUtils.toString(post.getEntity(), "UTF-8");
                  String res = EntityUtils.toString(httpResponse.getEntity(), "UTF-8");
                  logger.debug("{} -> {} -> {} => {}", post.getRequestLine(), body,
                      httpResponse.getStatusLine(), res);
                }
              }
            } catch (IOException ie) {
            }
          }

          @Override
          public void failed(Exception e) {
            latch.countDown();

            try {
              String body = EntityUtils.toString(post.getEntity(), "UTF-8");
              logger.error("{} -> {} -> {}", post.getRequestLine(), body, e);
            } catch (IOException ie) {
            }
          }

          @Override
          public void cancelled() {
            latch.countDown();
            try {
              String body = EntityUtils.toString(post.getEntity(), "UTF-8");
              logger.info("{} -> {} -> cancelled", post.getRequestLine(), body);
            } catch (IOException ie) {
            }
          }
        });
      }
      latch.await();

      for (int idx = 0; idx < responses.length; idx++) {
        try {
          results[idx] = EntityUtils.toString(responses[idx].get().getEntity(), "UTF-8");
        } catch (Exception e) {
          results[idx] = null;
        }
      }
    } catch (Exception e) {
      return null;
    }

    return results;

  }
```