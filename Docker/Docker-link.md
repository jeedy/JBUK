# 도커 링크(Link) 관련

> 참고자료 
    - 시작하세요! 도커(위키북스) 35page

같은 도커 엔진에 속한 A컨테이너에서 B컨테이너로 접근하는 방법 중 가장 간단한 방법은 NAT로 할당받은 내부 IP를 쓰는 것이다. B컨테이너의 IP가 172.17.0.3이라면 A컨테이너는 이 IP를 써서 B컨테이너에 접근할 수 있다. 그러나 도커 엔진은 컨테이너에게 내부 IP를 시작할 때마다 재할당하기 때문에 IP로 접근하려고 하면 문제가 발생할 수 있다.

그래서 내부 컨테이너끼리 간단히 접근이 가능하도록 컨테이너의 별명(alias)로 접근가능 하도록 설정하는 것이다

```bash
(RUN을 할때 아래와 같은 옵션을 주었을 경우)
$ docker run -d --name wordpressdb -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=wordpress mysql:5.7

$ docker run -d -e WORDPRESS_DB_PASSWORD=password --name wordpress --link wordpressdb:mysql -p 80 wordpress

$ docker port wordpress
80/tcp -> 0.0.0.0:32769

$ curl localhost:32769
(사이트 열림)
```

워드프레스 웹 서버 컨테이너는 wordpressdb의 IP를 몰라도 mysql이라는 호스트명으로 접근할 수 있게 된다.
```bash
$ docker exec wordpress ping -c 2 mysql
PING mysql (172.17.0.2): 56 data byte
64 bytes from 172.17.0.2: icmp_seq=0 ttl=64 time=0.100 ms
64 bytes from 172.17,9,2: icmp_seq=1 ttl=64 time=0.079 ms
--------- mysql ping staticstics ---------
... (이하생략)
```

--link 옵션을 쓸 때 유의할 점은 --link에 입력된 컨테이너가 실행 중이지 않거나 존재하지 않는다면 --link를 적용한 컨테이너 또한 실행할 수 없다는 것입니다. 이를 확인하려면 호스트에서 다음 명령어를 입력합니다.

`주의할 점은 --link에 입력한 컨테이너(wordpressdb)가 실행 중이지 않거나 존재하지 않는다면 --link를 적용한 컨테이너(wordpress) 또한 실행할 수 없다는 것입니다.`