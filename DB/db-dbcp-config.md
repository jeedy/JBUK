# Database Connection Pool 설정 방법 및 고찰

처음 찾게된 원인은 Mysql DB에서 `com.mysql.jdbc.exception.jdbc4.CommunicationException` 이 발생하면서 알아보게 되었다.

> com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: The last packet successfully received from the server was 57,220,320 milliseconds ago.
The last packet sent successfully to the server was 57,220,324 milliseconds ago. 
is longer than the server configured value of 'wait_timeout'. 
You should consider either expiring and/or testing connection validity before use in your application, increasing the server configured values for client timeouts, or using the Connector/J connection property 'autoReconnect=true' to avoid this problem.
SQL : SELECT #

친절하게 `autoReconnect=true` 값을 넣어주라는 메시지가 있었지만 좀더 자세히 알아보고자 DBCP 설정방법에 대해서 찾게 되었다.

## 참고자료
- https://m.blog.naver.com/tyboss/70176230775 (DBCP 관련 오류가 발생한 경우들을 모두 스크립해놓은 블로그)
- 