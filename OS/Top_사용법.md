# [Linux] Top 사용법

## top
아무런 옵션이 없다면 CPU 사용률에 따라서 정렬

## top -s
실행 후 추가 명령어가 가능

## top -d 2
2초 간격으로 정보를 갱신함

우선 <br/>
`top -s` <br/>
를 입력하면 5초 간격으로(기본값)을 갱신된 정보를 보여준다.<br/>
현재 아무런 명령어가 없기 때문에 기본값으로 CPU 정렬순이다.

이 상태에서 <br/>
대문자 M을 입력하면 메모리 사용률에 따라서 정렬<br/>

- q : 종료
- N: pid 순 정렬 나중순
- A: 최근 pid순 정렬
- P : CPU사용률에 따라서 정렬
- M : 메모리 사용률에 따라서 정렬
- T : 누적시간 (CTIME)순 정렬
- l : load average, uptime 사용정보 on/off
- m : 메모리 사용량 정보 on/off
- t: CPU사용률 정보 on/off
- c: 사용명령어/사용명령어full on/off ---명령어 추적시 용이

더 자세한건 man 페이지를 이용

출력된 결과중 head 부분
```
PID USER PRI NI SIZE RSS SHARE STAT %CPU %MEM CTIME COMMAND

PID : 프로세스 id
USER : 사용자(id)
PRI : 우선순위
NI : nice명령어값
SIZE : 가상이미지 크기(?)
RSS : 메모리 사용량
STAT: S(sleeping), R(running), W(swapped out process), Z(zombies)
%CPU : CPU 사용률
%MEM : 메모리 사용률
CTIME : 시작(running)후 누적시간
COMMAND : 명령어 or full path 명령어

```

Top은 CPU 1개당 100%로 계산합니다
