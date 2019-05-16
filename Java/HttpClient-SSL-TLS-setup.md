# HttpClient 에서 TLSv1.2 셋팅 방법

> tags: Httpclient, SSLContext, HttpPost, HttpGet, API, TLS, HTTPS, SSL

Java 1.8 부터는 Defualt `TLSv1.2` 를 지원하지만 Java1.7은 `TLSv1.1` 으로 지원한다. 그래서 `TLSv1.2` 을 지원하는 API
서버와 통신을 할 경우 protocol version 관련 Exception이 발생, 이를 해결하기 위해선 HttpClient 생성시 `TLSv1.2` 버전으로
인스턴스를 생성해서 request를 날려야한다.

## 참고 예제 소스

주석 ※ TLSv1.2 셋팅 부분 확인.

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
    RequestConfig requestConfig = null;
    if(timeout > 0){
        requestConfig = RequestConfig.custom()
                .setConnectTimeout(timeout *1000)
//                .setConnectionRequestTimeout(timeout*1000)
                .setSocketTimeout(timeout*1000)
                .build();
    }else{
        requestConfig = RequestConfig.DEFAULT;
    }
    
    /*
     * ※ TLSv1.2 셋팅
    */
    SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
    sslContext.init(null, null, null);  // 반드시 init 메소드 호출 필요

    String[] results = new String[urls.length];
    try (CloseableHttpAsyncClient httpclient = HttpAsyncClients
        .custom()
        .setSslcontext(sslContext)
        .setDefaultRequestConfig(requestConfig)
        .build()) {

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