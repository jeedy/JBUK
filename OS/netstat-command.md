# netstat 명령어 설명

netstat(network statistics)는  전송 제어 프로토콜, 라우팅 테이블, 수많은 네트워크 인터페이스(네트워크 인터페이스 컨트롤러 또는 소프트웨어 정의 네트워크 인터페이스), 네트워크 프로토콜 통계를 위한 네트워크 연결을 보여주는 명령 줄 도구이다.
(LINUX 기준, Windows는 옵션 사용법에서 조금 다르다.)
## 기본명령어
```bash
$ netstat -anp
```

## 옵션 (가장 많이 사용할 옵션 순서)
옵션 | 기능
---|---
-a | 모든 연결 및 수신 대기 포트를 표시한다.
-n | 주소나 포트 형식을 숫자로 표현한다.
-p | 해당프로토콜을 사용하는 프로그램, 프로세스 ID 보여줌
-e | 랜카드에서 송수신한 패킷 용량 및 사용자 정보
-t | tcp protocol
-u | udp protocol
-r | 라우팅 테이블 확인
-s | IP, ICMP, UDP프로토콜별의 상태를 보여줌

## 상태값
> SYN, ACK 등 handshake 관련 용어의 자세한 설명은 [Network Handshake](/network/tcp-3way-4way-handshake.md) 을 참고한다.

상태 | 내용
---|---
LISTEN | 연결 요구를 기다리는 상태, 포트가 열려 있음
ESTABLISHED | 서로 연결되어 있는 상태 (*별첨 1.)
SYN_SEND | [클라이언트 기준] 클라이언트가 서버에 SYN 패킷을 보내고 연결을 요청한 상태
SYN_RECV | [서버 기준] 서버가 클라이언트의 SYN 패킷으로 요청을 받은 후 응답으로 SYN/ACK 패킷을 보내고 클라이언트에게 ACK 를 받기 위해 기다리는 상태
TIME_WAIT | [클라이언트 기준] 이미 해당 사이트와 연결이 종료되었거나 다음 연결을 위해 기다리는 상태
CLOSE_WAIT | [서버 기준] 원격의 연결 요청을 받고 연결이 종료되길 기다리는 상태
LAST_ACK | [서버 기준] 연결이 종료되었고 승인을 기다리는 상태
CLOSED | 완전히 연결이 종료된 상태

## 별첨
1. ESTABLISHED 상태에서 오랫동안(약 7~8시간이상) 패킷 통신을 하지 않을 경우 강제로 low레벨의 네트워크 설정에서 이를 끈어버린다. 
일반적인 상황에서 특별히 문제가 되지 않지만 DB connection 과는 문제가 될 수 있다.
DB에서 connection 연결 되었다는 것은 프로토콜 상태가 ESTABLISHED 이라는 소리다. 이런 생태에서 오랫동안 쿼리가 없어 `The last packet successfully received from the server was 60,060,496 milliseconds ago. ... ` 와 같은 오류 메시지를 볼 수 있다. 
그렇기 때문에 DataSource 에 특정 주기로 testQuery를 날리는 설정이 필요하다.
참고: [datasource 설정](/DB/db-dbcp-config.md)

참고자료
- [MySQL 에서 대기시간(wait_timeout) 설정 방법](https://kjk3071.tistory.com/entry/DB-MySQL-timeout-%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0)
- [setting TCP timeout ESTABLISHED ](http://www.inetservicescloud.com/knowledgebase/how-to-change-tcp-established-timeout-value-in-linux/)
- [리눅스 서버의 TCP 네트워크 성능을 결정짓는 커널 파라미터 이야기 - 1편](https://meetup.toast.com/posts/53)
- [tcp_tw_reuse 와 tcp_tw_recycle](https://brunch.co.kr/@alden/3)