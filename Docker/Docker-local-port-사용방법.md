# localhost 에 올라간 port에 접속방법
참고: https://shanepark.tistory.com/209

상황설명
mysql:3306 container를 띄우고 jupyter notebook container 를 띄우고 jupyter notebook 에서 mysql 접근을 하려고 127.0.0.1 host로 접근 하려고 하면 찾을 수 없는 port 라고 나온다. 실제로 jupyter container bash에서 telnet 으로 포트 확인을 해봐도 찾을 수 없다고 나온는데, 단순히 localhost(127.0.0.1) 로는 로컬에 접속이 불가능 하다.


## 가장 간단한방법 host.docker.internal host 를 이용
container 안에서는 docker 엔진을 실행한 localhost의 host 명은 `host.docker.internal` 로 접근해야 한다.
    ```sh
    $ curl host.docker.internal:8080

    ```

> 그 밖에 다른 방법도 있으나 필요한 부분만 적는다. 다른 방법은 참고 URL 에서 확인