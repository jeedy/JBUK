# Commons DBCP 이해하기

## commons-dbcp 1.4 버그로 커넥션 메모리 누수 발생

- https://d2.naver.com/helloworld/5102792
- https://issues.apache.org/jira/browse/DBCP-330

## DBCP validationQuery 설정

DB 커넥션을 맺은후 오랫동안 사용이 없으면 데이터베이스에서 커넥션을 끈는다. 그래서 특정 시간 마다 커넥션을 확인하는 쿼리를 날리는 설정이 필요하다.

- MySQL
```
validationQuery="select 1"
```
- 오라클
```
validationQuery="select 1 from dual"
```
mysql wait_timeout 설정(기본값 28800 , 8시간) 에 의해 커넥션이 연결된 이후 해당커넥션의 close 없이 8시간이 지나면 해당 커넥션을 종료 시키게 된다.
문제는 이렇게 종료된 커넥션을 dbcp의 connection pool 에선 여전히 가지고 있는 상태라는 것이다.이런 상황에서 DB 관련 프로그램이 호출되면 커넥션 관련 에러가 발생된다.
해결방법은 java에서 DB를 사용하기 전에 해당 connection 이 정상적인지 검사를 하도록 하는 것이다. 이 옵션이 validationQuery 파라미터이다.

- 추가 작업
```
 validationQuery="select 1"
 testWhileIdle="true"
 timeBetweenEvictionRunsMillis="30000"
 testOnBorrow( default : true )="false"
 ```

    - testWhileIdle - true 일 경우 비활성화 커넥션을 추출할때 커넥션이 유효한지 여부를 검사해서 유효하지 않으면 제거
    - timeBetweenEvctionRunsMillis - 사용되지 않는 커넥션을 추출하는 쓰레드의 실행 주기를 지정 이값을 알맞게 지정해서 사용되지 않는 커넥션을 제거하는것이 좋다 보통 10~20분 단위 검사
    - testOnBorrow - 퍼포먼스가 문제 될거라고 생각된다면 testOnBorrow( default : true ) 값을 false 로 추가해주면 된다. true일 경우 커넥션을 가져올 때 커넥션이 유효한지의 여부를 검사

## 오라클 RAC JDBC 설정
