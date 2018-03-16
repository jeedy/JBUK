# Docker가 어떤 명령어를 실행(Ex: docker info)해도 응답하지 않을 경우 (Hang 걸렬을 때)

1. Docker deamon 중지
    ```sh
    $ sudo service docker stop
    ```
1. docker 데이터 삭제
    ```sh
    $ sudo rm -rf /var/run/docker
    $ sudo rm /var/run/docker.*
    ```
1. 서비스 재시작
    ```sh
    $ sudo service docker start
    ```
1. 컨테이너 시작
    ```sh
    $ docker start mycontainer
    ```
