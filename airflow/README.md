# Airflow (에어플로우)

## Docker 로 설치
```
$ docker-compose docker-compose.yaml -d up
```

## airflow 예제
https://velog.io/@clueless_coder/Airflow-%EC%97%84%EC%B2%AD-%EC%9E%90%EC%84%B8%ED%95%9C-%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC-%EC%99%95%EC%B4%88%EC%8B%AC%EC%9E%90%EC%9A%A9


## 디버깅 방법
1. 중단점에 `import pdb; pdb.set_trace()` 소스 추가
 
2. docker container 접속해 테스트 command 실행
```sh
~/project/airflow/dags$ docker exec -it airflow_airflow-webserver_1 bash

# dag 전체 테스트
default@efc626414362:/opt/airflow$ python3 ./dags/naver_search_pipeline.py
# operator 테스트
default@efc626414362:/opt/airflow/dags$ airflow tasks test naver-search-pipeline preprocess_result 2022-01-07
```
3. https://docs.python.org/ko/3.7/library/pdb.html 디버거 명령어 참고해서 디버깅



## 번외. 원격 디버깅 방법 (remote debugging)
- [C언어 remote debugging gdb 이나 이와 비슷한 python용 remote pdb가 있을것으로 보인다.](https://lunatk.github.io/2020/08/10/20200810-vscode-remote-gdb/)
	- c level 단에 debugging 툴이기 때문에 python은 물론 java, go 까지도 디버깅가능하다.
		- java debugging symbols는 따로 추가 설치 하야한다. https://access.redhat.com/documentation/ko-kr/openjdk/11/html/installing_and_using_openjdk_11_on_rhel/installing-and-configuring-debug-symbols
	- gdb 에 확장패키지로 python 을 디버깅 가능하다.
	- gdb 는 실시간으로 올라가 있는 프로세스에 traceback도 가능하다.
