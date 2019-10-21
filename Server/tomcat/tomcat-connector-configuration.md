# Apache tomcat connector configuration
tags:
톰켓, apache tomcat, connector, HTTP, HTTPS, AJP 

## Address, port
한 호스트 내에서 여러 IP address를 사용하고 있다면 address 속성을 통해 특정 IP address만 listen하도록 
설정할 수 있다. 기본 설정 값은 0.0.0.0으로 모든 IP address가 listen한다. 
o.a.tomcat.util.net.JIoEndpoint 클래스의 bind 메서드를 통해 BIO 방식 Connector의 소켓 생성에 대해 알아본다.

o.a.tomcat.util.net.JIoEndpoint.class :
```java
@Override
public void bind() throws Exception {
    //... 생략 ...
    if (serverSocket == null) {
        try {
            if (getAddress() == null) {
                serverSocket = serverSocketFactory.createSocket(getPort(), getBacklog());
            } else {
                serverSocket = serverSocketFactory.createSocket(getPort(), getBacklog(), getAddress());
            }
        } catch (BindException orig) {
            //... 생략 ...
        }
    }
}
```
위와 같이 address 속성이 설정되어 있지 않다면 port와 backlog를 parameter로 갖는 createSocket 메서드를 통해 소켓을 생성한다. 
이 때는 모든 IP address를 listen한다. 이번에는 o.a.tomcat.util.net.NioEndpoint 클래스의 bind 메서드를 통해 NIO 방식 Connector를 확인해본다.

o.a.tomcat.util.net.NioEndpoint.class:
```java
@Override public void bind() throws Exception { 
    serverSock = ServerSocketChannel.open();
    socketProperties.setProperties(serverSock.socket()); 
    InetSocketAddress addr = (getAddress()!=null) ? 
        new InetSocketAddress(getAddress(), getPort()) : new InetSocketAddress(getPort()); 
    serverSock.socket().bind(addr, getBacklog()); 
    serverSock.configureBlocking(true); //mimic APR behavior 
    serverSock.socket().setSoTimeout(getSocketProperties().getSoTimeout()); 
    // ... 생략 ...
}
```

만약 address 속성이 설정되어 있으면 address와 port를 parameter로 갖는 생성자를 사용한다. 
설정되어 있지 않다면 port만을 parameter로 갖는 생성자를 사용하며 모든 IP address를 listen하게 된다. 
APR 방식 Connector의 경우도 o.a.tomcat.util.net.AprEndpoint 클래스의 bind 메서드를 통해 확인 가능 하지만 
APR은 순수 자바가 아닌 C언어로 구현되어 있으므로 apr_sockaddr_t 구조체와 Tomcat Native의 address.c 등 관련 소스를 확인하면 된다.

Connector가 사용하는 포트는 port 속성을 통해 설정한다. 만약 0으로 설정하면 임의의 포트를 사용하게 된다.


## allowTrace
HTTP/1.1부터 TRACE 메서드를 제공하는데 이 메서드 사용은 보안상 취약점이 될 수 있다. allowTrace는 TRACE 메서드 허용 여부를 설정하는 속성으로 기본 false이다. 
o.a.catalina.connector.Connector 클래스를 확인하면 기본값을 확인할 수 있다.
`protected boolean allowTrace = false;`

o.a.catalina.connector.CoyoteAdapter 클래스를 확인하면 아래와 같다.

o.a.catalina.connector.CoyoteAdapter.class : 
```java
if (!connector.getAllowTrace()
        && req.method().equalsIgnoreCase("TRACE")) {
    Wrapper wrapper = request.getWrapper();
    String header = null;
    if (wrapper != null) {
        String[] methods = wrapper.getServletMethods();
        if (methods != null) {
            for (int i=0; i<methods.length; i++) {
                if ("TRACE".equals(methods[i])) {
                    continue;
                }
                if (header == null) {
                    header = methods[i];
                } else {
                    header += ", " + methods[i];
                }
            }
        }
    }
    res.setStatus(405);
    res.addHeader("Allow", header);
    res.setMessage("TRACE method is not allowed");
    request.getContext().logAccess(request, response, 0, true);
    return false;
}
```

## connectionTimeout
nnector와 클라언트 간에 Connection이 연결된 이후 실제 요청이 들어올때까지 대기 시간이다. 
단위는 ms이며 Connector 종류에 따라 기본값이 다르다. HTTP Connector의 기본은 20000, 즉 20초이고, AJP Connector의 경우는 기본 -1이다. 
-1로 설정하면 무한 대기한다.

## enableLookups
request.getRemoteHost()는 DNS(Domain Name System) Lookup을 통하여 클라이언트 이름을 리턴하며, request.getRemoteAddr()는 
바로 클라이언트의 IP address를 리턴한다. 그런데 enableLookups 속성을 false로 설정하면 getRemoteHost() 요청시에 DNS Lookup 과정을 생략한다. 
즉, getRemoteAddr()를 수행한 결과와 같아진다. DNS Lookup은 적지 않은 시간이 소요되는 작업으로 결국 성능에 영향을 끼친다. 
꼭 필요한 경우가 아니면 false로 설정하는 것이 좋다. 기본값도 false다.

```java
protected String remoteHost = null; 

public String getRemoteHost() { 
    if (remoteHost == null) {
        if (!connector.getEnableLookups()) { 
            remoteHost = getRemoteAddr(); 
        } else {
            coyoteRequest.action(ActionCode.REQ_HOST_ATTRIBUTE, coyoteRequest);
            remoteHost = coyoteRequest.remoteHost().toString(); 
        } 
    } return remoteHost; 
}
```

## maxParameterCount
GET, POST 메소드 사용시 최대 parameter 수를 설정하는 속성으로 기본 10000이다. 
그 이상의 parameter는 무시한다. 만약 0 미만으로 설정하면 최대 parameter 수 제한은 없다. 
단, 0으로 설정하면 안된다. 최대 parameter가 0이라는 의미이기 때문이다.

## maxPostSize
POST 사용 시 최대 byte로 기본은 2097152(2MB)이며, -1 이하로 설정하면 제한이 없다.

## maxThreads, minSpareThreads
**maxThreads는 Connector가 생성할 수 있는 최대 Thread 수로 기본 200이다.** 
Thread 수 설정은 CPU 사용량을 고려해야 한다. 만약 호스트 CPU 사용량이 적은 경우 Thread 수 증가를 고려해볼 수 있다. 
Connector를 Executor로 설정했다면 이 값은 무시된다.

**minSpareThreads는 Connector를 생성시 최초에 만드는 Thread 수로 기본 10이다.** Connector는 항상 이 수만큼의 여유 Thread를 유지한다.

## protocol
Connector가 사용하는 프로토콜이다. HTTP는 HTTP/1.1, AJP는 AJP/1.3를 기본 사용한다. 
방식은 BIO(Blocking I/O)가 기본이며 NIO(Non-blocking I/O 혹은 New I/O)와 APR(APR/Native)도 사용할 수 있다.

BIO, NIO는 자바로 구현한 방식이며 NIO의 사용이 점점 증가하고 있다. 한편 ARP는 C 언어로 구현되어 있다. 
HTTP Connector 방식은 아래와 같이 설정한다.

org.apache.coyote.http11.Http11Protocol → blocking Java connector

org.apache.coyote.http11.Http11NioProtocol → non blocking Java connector  

org.apache.coyote.http11.Http11AprProtocol → the APR/native connector

그러면 HTTP Connector 방식을 BIO에서 NIO(org.apache.coyote.http11.Htto11NioProtocol)로 변경한후 
Tomcat을 기동하면 아래아 같은 로그를 확인할 수 있다.

```bash
org.apache.coyote.AbstractProtocol start INFO: Starting ProtocolHandler ["http-nio-8080"]
org.apache.coyote.AbstractProtocol start INFO: Starting ProtocolHandler ["ajp-bio-8009"]
```

Http11NioProtocol은 Tomcat 6.0 이상부터, AjpNioProtocol은 7.0 이상부터 사용할 수 있다. 
기본 Connector 방식은 Tomcat 7.0까지만 BIO를 사용하며, 8.0은 NIO를 사용한다.


##acceptCount

Thread Pool 내에 할당 가능한 Thread가 없다면 사용자 요청은 queue 안에서 대기하게된다. 당연히 queue의 크기가 크면 대기 가능한 요청 수도 많아진다. acceptCount 속성은 queue에 저장 가능한 최대 요청 수를 설정한다. 만약 Thread Pool 내 할당 가능한 Thread가 없을때 대기 요청을 queue 안에 담아두기보다 빠른 응답(오류)를 주고 싶다면 acceptCount 수를 줄이면 된다. 내부적으로는 backlog 속성으로 관리된다.

```java
protected static HashMap<String, String> replacements = new HashMap<String, String>();
static {
    replacements.put("acceptCount", "backlog");
    replacements.put("connectionLinger", "soLinger");
    replacements.put("connectionTimeout", "soTimeout");
    replacements.put("rootFile", "rootfile");
}
```

backlog 기본 값은 100이다. o.a.tomcat.util.net.AbstractEndpoint 클래스를 확인하면 아래와 같다.

```java
private int backlog = 100;
public void setBacklog(int backlog) { if (backlog > 0) this.backlog = backlog; }
public int getBacklog() { return backlog; }
```

각 Connector의 소켓 생성시 backlog 값을 적용한다.

```java
if (getAddress() == null) {
    serverSocket = serverSocketFactory.createSocket(getPort(), getBacklog());
} else {
    serverSocket = serverSocketFactory.createSocket(getPort(), getBacklog(), getAddress());
}
```

> Socket에서 backlog란? (https://twilight0119.tistory.com/90) <br>
int listen(int s, int backlog);<br>
연결을 받아들이기 위해, 소켓은 우선 들어오는 연결들을 받아들이기 위한 socket을 만들고, 들어오는 연결들에 대한 큐 제한 값을 listent으로 명시하고, 그리고 연결들을 accept로 받아들인다. listen함수는 SOCK_STREAM이나 SOCK_SEQPACKET 타입의 소켓들에만 적용된다.<br>
<br>
backlog 인자는 아직 미결인 연결들에 대한 큐의 늘어날 수 있는 최대 길이를 정의한다. 큐에 도착한 연결 요청들이 꽉 찬다면 클라이언트는 ECONNREFUSED를 가리키는 에러를 받거나, 만일 하위 프로토콜이 재전송을 지원한다면, 요청은 재시도가 성공되도록 하기 위해 무시된다.

## acceptorThreadPriority, threadPriority
각각 Acceptor Thread와 요청 처리 Thread의 priority를 설정하는 속성으로 두 속성 모두 기본 값은 5(Thread.NORM_PRIORITY)이다.

## maxConnections
동시 처리 가능한 최대 Connection 수로 Connector 방식에 따라 기본값이 다르다. BIO의 경우는 maxThreads 값을 따른다. 
o.a.tomcat.util.net.JIoEndpoint 클래스를 확인한다.

o.a.tomcat.util.net.JIoEndpoint.class :
```java
public JIoEndpoint() {
    setMaxConnections(0);
    setExecutorTerminationTimeoutMillis(0);
}
```

0인 경우, maxThreads 값이 된다. NIO는 기본 10000이다. o.a.tomcat.util.net.AbstractEndpoint 클래스를 확인해 보자.

```java
private int maxConnections = 10000;
public void setMaxConnections(int maxCon) {
    this.maxConnections = maxCon;
    LimitLatch latch = this.connectionLimitLatch;
    if (latch != null) {
        if (maxCon == -1) {
            releaseConnectionLatch();
        } else {
            latch.setLimit(maxCon);
        }
    } else if (maxCon > 0) {
        initializeConnectionLatch();
    }
}
```

APR은 기본 8192이다. o.a.tomcat.util.net.AprEndpoint 클래스를 확인해보자.

o.a.tomcat.util.net.AprEndpoint.class : 
```java
public AprEndpoint() {
    setMaxConnections(8 * 1024);
}

public void setMaxConnections(int maxConnections) {
    if (maxConnections == -1) {
        log.warn(sm.getString("endpoint.apr.maxConnections.unlimited", Integer.valueOf(getMaxConnections())));
        return;
    }
    if (running) {
        log.warn(sm.getString("endpoint.apr.maxConnections.running", Integer.valueOf(getMaxConnections())));
        return;
    }
    super.setMaxConnections(maxConnections);
}
```

## tcpNoDelay
Nagle 알고리즘은 전송 패킷수를 줄임으로서 네트워크 효율성을 높이는데 목적이 있다. 
즉, 패킷을 주고 받을때 ack를 수신할 때까지 버퍼에 담아놓은 후 전송하는 방식(RFC 896)이다. 하지만 최근의 인터넷 환경은 기반 인프라가 눈에 띄게 향상했고, 
빠른 응답 속도를 요하는 애플리케이션이 많아졌다.

TCP_NODELAY는 Nagle 알고리즘을 무력화한다. 속도 향상에 도움이 되지만 작은 패킷을 빈번하게 전송하기 때문에 네트워크 트래픽은 증가하게 된다. 
기본은 기본은 true로 Nagle 알고리즘을 사용하지 않는다. 내부적으로는 Socket 클래스의 setTcpNoDelay() 메서드를 사용한다.

```java
socket.setTcpNoDelay(getTcpNoDelay());
```

## URIEncoding
URI 인코딩 방식을 결정하는 속성으로 Tomcat7.0의 기본은 ISO-8859-1이다. 
o.a.catalina.connector.Connector 클래스를 확인하면 다음과 같다.

o.a.catalina.connector.Connector.class: 
```java
protected String URIEncoding = null;

public Connector(String protocol) {
    setProtocol(protocol);
    try {
        Class<?> clazz = Class.forName(protocolHandlerClassName);
        this.protocolHandler = (ProtocolHandler) clazz.newInstance();
    } catch (Exception e) {
        log.error(sm.getString("coyoteConnector.protocolHandlerInstantiationFailed"), e);
    }
}
``` 

반면 아래는 Tomcat8.0의 Connector 클래스이다.

```java
protected String URIEncoding = null;
protected String URIEncodingLower = null;

public Connector(String protocol) {
    setProtocol(protocol);
    ProtocolHandler p = null;
    try {
        Class<?> clazz = Class.forName(protocolHandlerClassName);
        p = (ProtocolHandler) clazz.newInstance();
    } catch (Exception e) {
        log.error(sm.getString("coyoteConnector.protocolHandlerInstantiationFailed"), e);
    } finally {
        this.protocolHandler = p;
    }
    if (!Globals.STRICT_SERVLET_COMPLIANCE) {
        URIEncoding = "UTF-8";
        URIEncodingLower = URIEncoding.toLowerCase(Locale.ENGLISH);
    }
}
``` 

8.0의 경우 STRICT_SERVLET_COMPLIANCE가 false일때 기본은 UTF-8이다. 
STRICT_SERVLET_COMPLIANCE의 기본은 false이므로 이 값을 true로 설정하지 않는 한 Tomcat 8.0 URIEncoding의 기본은 UTF-8이 된다. 
다만 서블릿 3.1 Spec 중 '3.11 Request data encoding'에 따라 표준 URL 인코딩 방식은 ISO-8859-1이기 때문에 
만약 Spec을 준수하도록 설정한다면 URIEncoding은 ISO-8859-1이 된다.

## Executor (org.apache.catalina.Executor)
Executor는 공유 Thread Pool이다. 운영 시스템에서 Executor 설정을 사용하는 경우는 많지 않다.

```xml
<Executor name="tomcatThreadPool" namePrefix="catalina-exec-" maxThreads="150" minSpareThreads="4" />
```

Excuetor는 Service Element(<Service>)내에 존재하며 위와 같이 기본적으로 주석처리 되어 있다. 
namePrefix는 각 Thread 이름에 사용되는 prefix이다. 기본 설정 상 catalina-exec-이므로 Thread ID가 5라면 해당 Thread 이름은 catalina-exec-5가 된다. 
BIO 방식 HTTP Connector일 때 Thread 덤프를 통해 Thread 이름을 확인해보면, "http-bio-8080-exec*"로 시작하는 것을 확인할 수 있다.

maxThreads는 최대 동시 사용 가능 Thread 수로 기본 200이며, minSpareThreads는 Thread Pool 내에 항상 유지되는 최소 Thread 수로 기본 25이다. 
maxIdleTime은 Idle 상태인 Thread를 종료하기 위한 시간으로 기본 60000(ms), 즉 1분이다. 
단, 실행 중인 Thread가 minSpareThreads보다 적은 경우 maxIdleTime이 동작하지 않는다.


---

## HTTP Connector 전용 속성

## compression
클라이언트 요청에 대한 응답시 deflate 알고리즘을 사용하는 GZIP 압축 후 전송하도록 설정하는 속성이다. 
deflate 알고리즘은 'DEFLATE Compressed Data Format Specification version 1.3', RFC 1951에, 
GZIP은 'GZIP file format specification version 4.3', RFC 1952에 각각 정의되어 있다.

compression 속성의 설정 값 중 off는 압축 기능 해제, on은 텍스트 데이터만 압축, force는 모두 압축이다. 
만약 값을 숫자 type으로 설정하면 설정 값 크기 이상의 응답만 압축하여 전송한다. 기본은 off이다. 
압축 기능은 네트워크 속도가 느릴때 효과적이며, 응답 데이터가 어느정도 커야 의미가 있다. 
데이터 크기가 너무 작으면 오히려 압축을 위한 부하 때문에 효율이 떨어질 수 있기 때문이다. 
또한 JPG나 MP3와 같이 이미 압축되어 있는 형식의 파일은 압축 대상에서 제외해야 한다.

compressableMimeType은 압축 대상 mime(Multipupose Internet Mail Extensions, RFC 1521) type을 ,(comma)로 구분하여 설정한다. 
Tomcat 7.0.64의 기본 mime type은 다음과 같다.

```java
private String compressableMimeTypes = "text/html,text/xml,text/plain,text/css,text/javascript,application/javascript";
```

compressableMimeType 기본 값은 버전별로 다소 차이가 있다. 

## maxKeepAliveRequest, keepAliveTimeout

**HTTP/1.1부터 제공하는 keepalive 기능은 Connection의 재사용을 가능하게 한다.** 
그러나 많은 요청을 처리하는 웹 시스템의 경우 자칫 독이 될 수 있는 기능이다. 
keepalive 시간동안 Connection을 'keep' 하고 있기 때문에 적절하지 않은 설정으로 인해 Connection 부족 현상이 발생할 수 있기 때문이다.

먼저 maxKeepAliveRequests는 keepalive 가능한 최대 요청 수로 기본설정은 100이고 -1은 무제한, 1은 비활성화이다. 
o.a.coyote.http11.AbstractHttp11Processor 클래스를 확인해보자.

o.a.coyote.http11.AbstractHttp11Processor.class :
```java 
if (maxKeepAliveRequests == 1) {
    keepAlive = false;
} else if (maxKeepAliveRequests > 0 && socketWrapper.decrementKeepAlive() <= 0) {
    keepAlive = false;
}
```

keepAliveTimeout는 속성 이름에서 의미를 파악할 수 있다. 
기본 값은 connectionTimeout을 따르며 -1로 설정하면 Connection을 계속 유지한다. 
o.a.tomcat.util.net.AbstractEndpoint 클래스를 확인해보자.

o.a.tomcat.util.net.AbstractEndpoint.class : 
```java
private Integer keepAliveTimeout = null;
public int getKeepAliveTimeout() {
    if (keepAliveTimeout == null) {
        return getSoTimeout();
    } else {
        return keepAliveTimeout.intValue();
    }
}
public void setKeepAliveTimeout(int keepAliveTimeout) {
    this.keepAliveTimeout = Integer.valueOf(keepAliveTimeout);
}
```

keepAliveTimeout을 설정하지 않으면 soTimeout 값이 적용된다. soTimeout은 SocketProperties에서 정의된다. 
soTimeout의 기본값은 20초이다. 그런데 앞서 keepAliveTimout의 기본 값은 connectionTimeout을 따른다고 했다. 
하지만 코드에는 connectionTimeout이 아닌 soTimeout으로 되어있다. 

```java
protected static HashMap<String, String> replacements = new HashMap<String, String>();
static {
    replacements.put("acceptCount", "backlog");
    replacements.put("connectionLinger", "soLinger");
    replacements.put("connectionTimeout", "soTimeout");
    replacements.put("rootFile", "rootfile");
}
```
**tcpdump나 curl을 이용하면 keepalive 여부를 확인할 수 있다.**

## disableKeepAlivePercentage

disableKeepAlivePercentage는 Thread 수가 점점 증가하여 maxThreads 대비 일정 비율 초과할때 더이상 keepalive를 하지 않는 속성이다.
o.a.coyote.http11.Http11Processor 클래스를 확인해보자.

o.a.coyote.http11.Http11Processor.class : 
```java
private int disableKeepAlivePercentage = 75;

protected boolean disableKeepAlive() {
    int threadRatio = -1;
    int maxThreads, threadsBusy;
    if ((maxThreads = endpoint.getMaxThreads()) > 0 
        && (threadsBusy = endpoint.getCurrentThreadsBusy()) > 0) {
        threadRatio = (threadsBusy * 100) / maxThreads;
    }
    // Disable keep-alive if we are running low on threads
    if (threadRatio > getDisableKeepAlivePercentage()) {
        return true;
    }
    
    return false;
}
```

기본설정은 75(%)이며, threadRatio가 disableKeepAlivePercentage를 넘으면 disableKeepAlive()는 true가 된다. 
o.coyote.http11.AbstractHttp11Processor 클래스도 확인해보자.

o.coyote.http11.AbstractHttp11Processor.class : 
```java
if (disableKeepAlive()) {
    socketWrapper.setKeepAliveLeft(0);
}
```

disableKeepAlive()가 true이면 keepAliveLeft는 0이 된다.


