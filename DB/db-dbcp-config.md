# Database Connection Pool 설정 방법 및 고찰

처음 찾게된 원인은 Mysql DB에서 `com.mysql.jdbc.exception.jdbc4.CommunicationException` 이 발생하면서 알아보게 되었다.

> com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: The last packet successfully received from the server was 57,220,320 milliseconds ago.
The last packet sent successfully to the server was 57,220,324 milliseconds ago. 
is longer than the server configured value of 'wait_timeout'. 
You should consider either expiring and/or testing connection validity before use in your application, increasing the server configured values for client timeouts, or using the Connector/J connection property 'autoReconnect=true' to avoid this problem.
SQL : SELECT #

Oracle 경우 아래와 같은 오류가 발생한다.
> [ajp-nio-8109-exec-37] WARN mc.a.d.x.XAResourceTransaction - XA resource 'WWW.DATABASE.XXXX.DataSource': resume for XID '3137322E31362E3230312E3133312E746D313539303436383634313338363030303233:3137322E31362E3230312E3133312E746D3233' raised -7: the XA resource has become unavailable
oracle.jdbc.xa.OracleXAException: null


친절하게 `autoReconnect=true` 값을 넣어주라는 메시지가 있었지만 좀더 자세히 알아보고자 DBCP 설정방법에 대해서 찾게 되었다.

## 참고자료
- https://m.blog.naver.com/tyboss/70176230775 (DBCP 관련 오류가 발생한 경우들을 모두 스크립해놓은 블로그) -> [닫혔을 경우 여기](./db-dbcp-troubleshooting.md)
- https://ojava.tistory.com/120 (minEvictabledleTimeMillis 값 사용하지 않기, minEvictabledleTimeMillis = -1)
- https://www.codepedia.org/ama/tomcat-jdbc-connection-pool-configuration-for-production-and-development/ (그냥 셋팅 참고만하자)
- https://sjh836.tistory.com/148 (각 설정들에 대해 한글로 잘 설명해 놓았다.)
- https://d2.naver.com/helloworld/5102792 (Common DBCP에 대해 이해하기)
- https://d2.naver.com/helloworld/1321 (JDBC Internal - 타임아웃의 이해, timeout이 어디서 문제인지 판단해볼때 한번은 읽어볼만하다.)


## JDBC connection pool 설정 정리
- initialSize : maxActive 보다 생성된 connection 갯수가 적을 경우 connection pool에 한번에 채워 넣을 connection 개수
- maxActive(OR maxTotal) : 동시에 사용할 수 있는 최대 커넥션 개수
- maxWait(OR maxWaitMillis) : 60000(DB Connection이 부족할 경우 대기하는 시간:ms, 원문: The maximum number of milliseconds that the pool will wait (when there are no available connections) for a connection to be returned before throwing an exception, or -1 to wait indefinitely.)
- maxIdle : 모든 connection이 sleep 상태일때 최소로 남겨 놓을 connection 수
- minIdle : 이건 그냥 유휴한 connection을 생성해 놓는다.

```properties
...
jdbc.driverClassName=com.mysql.cj.jdbc.Driver
jdbc.url=jdbc:mysql://(..생략..)?useUnicode=true&serverTimezone=Asia/Seoul&useSSL=false
jdbc.username=(..생략..)
jdbc.password=(..생략..)
jdbc.encpassword=(..생략..)
jdbc.initialSize=2
jdbc.maxActive=18
jdbc.maxWait=10000
jdbc.maxIdle=6
jdbc.minIdle=2
...
```
위 설정으로 connection 생성 timeline을 기록해보면

1. 최초 **4 conn** 생성됨, (initialSize + **minIdle**)
2. (start stress test, 20 connection 초과) 부하시 **20 conn** 생성됨 (maxActive + **minIdle**)
3. (after maxWait with stress test ) **8 conn** 남음 (maxIdle + **minIdle**)

모든 connection이 생성될 때 **minIdle** 값이 영향을 준다. 이는 직접 테스트 하면서 processlist 를 통해 connection을 맺은 갯수를 보고 알아낸 것이기 때문에 확실하다.

어떤 블로그에서 "initialSize와 maxActive, maxIdle, minIdle 항목을 동일한 값으로 통일해도 무방하다." 라고 써있는데 사실 **initialSize와 maxActive, maxIdle** 값을 같은 값으로 한다면 minIdle 값은 0으로 설정하는게 바람직하다.


## 커넥션의 검사와 정리
유효성 검사 쿼리(validation query)와 Evictor 스레드 관련 설정으로도 애플리케이션의 안정성을 높일 수 있다.

### 유효성 검사 쿼리 설정
JDBC 커넥션의 유효성은 validationQuery 옵션에 설정된 쿼리를 실행해 확인할 수 있다. Commons DBCP 1.x에서는 다음과 같은 세 가지 테스트 옵션으로 유효성을 검사한다. 유효성을 검사할 때는 validationQuery 옵션에 하나 이상의 결과를 반환하는 쿼리를 설정해야 한다. Commons DBCP 2.x에서는 validationQuery 옵션이 없을 때 Connection.isValid() 메서드를 호출해 유효성을 검사한다.

- testOnBorrow: 커넥션 풀에서 커넥션을 얻어올 때 테스트 실행(기본값: true)
- testOnReturn: 커넥션 풀로 커넥션을 반환할 때 테스트 실행(기본값: false)
- testWhileIdle: Evictor 스레드가 실행될 때 (timeBetweenEvictionRunMillis > 0) 커넥션 풀 안에 있는 유휴 상태의 커넥션을 대상으로 테스트 실행(기본값: false)
- validationQuery 옵션에는 DBMS에 따라 다음과 같이 쿼리를 설정하기를 권장한다. 실제 테이블에 있는 데이터를 조회하는 쿼리를 validationQuery 옵션에 설정했다가 운영 서버에서 많은 데이터를 조회해 장애로 이어진 사례도 있다.

- Oracle: select 1 from dual
- Microsoft SQL Server: select 1
- MySQL: select 1
- CUBRID: select 1 from db_root

검증에 지나치게 자원을 소모하지 않게 testOnBorrow 옵션과 testOnReturn 옵션은 false로 설정하고, 오랫동안 대기 상태였던 커넥션이 끊어지는 현상을 막게 testWhileIdle 옵션은 true로 설정하는 것을 추천한다. 참고로 CUBRID는 자체적으로 커넥션을 관리하고 자동으로 다시 연결하도록 구현됐다. DBCP 수준에서 한 번 더 유효성 검사 쿼리를 보내는 것은 추가 비용을 소모할 뿐이므로 CUBRID를 사용할 때는 testWhileIdle 옵션도 false로 설정하기를 권장한다.

Oracle JDBC 드라이버 9.x에서는 강제로 세션을 종료했을 때 발생하는 ORA-00028 오류가 난 후 부적절한 상태의 커넥션이 커넥션 풀로 반납돼 데이터베이스에 로그인되지 않은 때 발생하는 오류인 ORA-01012 오류가 계속 발생한 사례가 있다. 근본적인 원인은 Oracle JDBC 드라이버가 해당 오류 상황에서 JDBC 명세에 정의된 ConnectionEventListener.connectionErrorOccurred() 메서드를 제대로 호출하지 않았기 때문이었다. Oracle JDBC 드라이버를 10.x로 업그레이드해서 테스트했을 때는 같은 오류가 재현되지 않았다. 오류가 발생하는 버전을 사용하는 애플리케이션에서 Commons DBCP의 testWhileIdle 옵션을 true로 설정한 서버에서도 오류가 발생하지 않았다. Commons DBCP에서 vadliationQuery 옵션을 실행하면서 오류가 발생하면 해당 커넥션을 커넥션 풀에서 제외했기 때문이다. 이렇듯 testWhileIdle 옵션과 유효성 검사 쿼리 설정으로 예상치 못한 오류 상황도 대비할 수 있다.

### Evictor 스레드와 관련된 속성
Evictor 스레드는 Commons DBCP 내부에서 커넥션 자원을 정리하는 구성 요소이며 별도의 스레드로 실행된다. 이와 관련된 속성은 다음과 같다.

- timeBetweenEvictionRunsMillis: Evictor 스레드가 동작하는 간격. 기본값은 -1이며 Evictor 스레드의 실행이 비활성화돼 있다.
- numTestsPerEvictionRun: Evictor 스레드 동작 시 한 번에 검사할 커넥션의 개수
- minEvictableIdleTimeMillis: Evictor 스레드 동작 시 커넥션의 유휴 시간을 확인해 설정 값 이상일 경우 커넥션을 제거한다(기본값: 30분)
- Evictor 스레드의 역할은 3가지인데 각각의 역할을 수행할 때 위의 속성이 어떻게 참조되는지 살펴보자.

첫째, 커넥션 풀 내의 유휴 상태의 커넥션 중에서 오랫동안 사용되지 않은 커넥션을 추출해 제거한다. 
Evictor 스레드 실행 시 설정된 numTestsPerEvictionRun 속성값만큼 CursorableLinkedList의 ObjectTimestampPair를 확인한다. 
ObjectTimestampPair의 타임스탬프 값과 현재 시간의 타임스탬프 값의 차이가 minEvictableIdleTimeMillis 속성값을 초과하면 해당 커넥션을 제거한다. 
커넥션 숫자를 적극적으로 줄여야 하는 상황이 아니라면 minEvictableIdleTimeMillis 속성값을 -1로 설정해서 해당 기능을 사용하지 않기를 권장한다.

둘째, 커넥션에 대해서 추가로 유효성 검사를 수행해 문제가 있을 경우 해당 커넥션을 제거한다. 
testWhileIdle 옵션이 true로 설정됐을 때만 이 동작을 수행한다. 첫 번째 작업 시 minEvictableIdleTimeMillis 속성값을 초과하지 않은 커넥션에 대해서 추가로 유효성 검사를 수행하는 것이다.

셋째, 앞의 두 작업 이후 남아 있는 커넥션의 개수가 minIdle 속성값보다 작으면 minIdle 속성값만큼 커넥션을 생성해 유지한다.

예를 들어, `testWhileIdle=true && timeBetweenEvictionRunMillis > 0`이면 위의 3가지 역할을 다 수행하고, 
`testWhileIdle=false && timeBetweenEvictionRunMillis > 0`이면 두 번째 동작은 수행하지 않는다.

Evictor 스레드는 동작 시에 커넥션 풀에 잠금(lock)을 걸고 동작하기 때문에 너무 자주 실행하면 서비스 실행에 부담을 줄 수 있다. 
또한 numTestsPerEvictionRun 값을 크게 설정하면 Evictor 스레드가 검사해야 하는 커넥션 개수가 많아져 잠금 상태에 있는 시간이 길어지므로 역시 서비스 실행에 부담을 줄 수 있다. 
게다가 커넥션 유효성 검사를 위한 테스트 옵션(testOnBorrow, testOnReturn, testWhileIdle)을 어떻게 설정하느냐에 따라 애플리케이션의 안정성과 DBMS의 부하가 달라질 수 있다. 
그러므로 Evictor 스레드와 테스트 옵션을 사용할 때는 데이터베이스 관리자와 상의해서 사용하는 DBMS에 최적화될 수 있는 옵션으로 설정해야 한다.

IDC(internet data center) 정책에 따라서는 서버 간의 소켓 연결 후 정해진 시간 이상 아무런 패킷도 주고받지 않으면 연결을 종료한다. 
이런 경우 timeBetweenEvictionRunsMillis 속성 등으로 의도하지 않게 연결이 끊어지는 것을 방어할 수 있다. 
예를 들어 30분 동안 통신이 없을 때 연결이 끊어지는 정책으로 네트워크를 운영한다면, 
BasicDataSource가 풀링(pooling)하는 커넥션의 수가 30개라고 가정할 때 30분 안에 모든 커넥션에 유효성 검사 쿼리를 한 번씩은 실행하는 것이 바람직하다. 
Evictor 스레드가 5분에 한 번씩 실행되도록 설정했을 때 30분 동안 Evictor 스레드 실행 횟수는 6번이므로 매번 5개의 커넥션을 검사해야 전체 커넥션을 테스트할 수 있다. 
30분 안에 5분마다 Evctor 스레드가 실행되면 6번 실행되지만 오차를 감안해 5번으로 가정하면 이때 설정해야 할 numTestsPerEvictionRun 값은 다음과 같이 구할 수 있다.

> 6 * numTestsPerEvictionRun > 30개  

따라서 numTestsPerEvictionRun 속성값은 최소 6 이상이어야 한다. 일반적인 공식으로 정리하면 다음과 같다.

```
 ('IDC 정책에서 허용하는 최대 유휴 커넥션 유지 시간' / timeBetweenEvictionRunsMillis 속성값) * numTestsPerEvictionRun 속성값) > 전체 커넥션 개수
```


## AtomikosDataSourceBean 사용시 설정방법
BasicDataSource 와 다르게 AtomikosDataSource 는 위 속성을 지원하지 않는다.
~~`?다른 속성값으로 지원하는 것으로 보이는데, 어떤 값을 확인해봐야 할지는 찾아보자?`~~

우선 TestQuery를 하나 달아 놓았더니 오류는 안났으나 좀더 확인이 필요하다.

MySQL:
```java
dataSource.setTestQuery("SELECT 1");
```
Oracle:
```java
dataSource.setTestQuery("SELECT 1 FROM DUAL");
```

testQuery를 입력해 놓으면, 쿼리를 날리기전에 TestQuery를 통해 connection 확인을 한다. 
만약, 서버에서 강제로 connection을 닫은 상태(일정 시간동안 통신을 안하면 connection을 강제로 닫는 셋팅을 하는 서버들도 있다)라면 testQuery를 통해 connection reset을 진행해 다시 재생성한다.
하지만 testQuery가 없다면 확인없이 계속 쿼리를 날릴려고 하기 때문에 계속 Exception을 발생시킬 것이다.

**결론: testQuery를 반드시 입력해놓자.**
