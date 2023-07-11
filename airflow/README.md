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