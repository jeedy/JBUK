# 자바 Garbage Collection 모니터링

참고
http://d2.naver.com/helloworld/6043

## 메모리 오류날 경우 살펴볼 블로그

http://javaslave.tistory.com/23

## 그밖에 jdk8에서 perm메모리 관련 자료

https://tonyne.jeju.onl/2016/07/15/java8-memory-setting-geoserver/
http://netframework.tistory.com/entry/Java8-PermGen에서-Metaspace로
http://starplatina.tistory.com/entry/JDK8에선-PermGen이-완전히-사라지고-Metaspace가-이를-대신-함
https://yckwon2nd.blogspot.kr/2015/03/java8-permanent.html

## Heap메모리 기본셋팅방법(자바성능튜닝 이야기 p.375)

보통 500MB 단위로 늘려서 설정
GC 튜닝 이전에 현재 상황을 모니터링한 결과를 바탕으로 Full GC가 발생한 이후에 남아 있는 메모리의 크기를 봐야한다.
Full GC 후에 남아 있는 Old 영역의 메모리가 300MB 정도라면 300MB(기본사용) + 500MB(Old 영역용 최소) + 200MB(여유 메모리)를 감안하여 1GB 정도 지정한다.
그래서 3대 정도 운영서버가 있다면, 1GB, 1.5GB, 2GB 정도로 지정한 후 결과를 지켜본 다음 결정한다.
이렇게 지정하면, 이론적으로 생각했을때 GC가 old 영역 1GB > 1.5GB > 2GB 순서로 빠르므로, 결국 1G일때 GC가 제일 빠르다고 볼 수 있으나 1GB떄 1초 걸린다고 2GB에 2초 걸린다고 보장할 수 없다.
만약, 1GB일때 1초 소요될때 1.5GB때 1.2초가 소요된다면 1.5GB일때 GC가 수행되는 빈도가 적어지게 되므로 1.5GB 로 선택이 좋을 수 있다. 

## jar 실행 후 GC메모리 확인
```bash
$ java -verbosegc -XX:+PrintGCTimeStamps -Xmx1g -Xms1g -jar project1.jar  &
```

## 자바사용 메모리 사용량 & gc 퍼포먼스 확인(퍼센트)
```bash
$ jstat -gcutil -t -h10 [JID] 1s > jstat_1.log
```

## 자바사용 메모리 사용량(용량)
```bash
$ jstat -gccapacity -t -h10 [JID] 1s > jstat_1.log
```
