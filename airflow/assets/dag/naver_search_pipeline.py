## 
# https://velog.io/@clueless_coder/Airflow-%EC%97%84%EC%B2%AD-%EC%9E%90%EC%84%B8%ED%95%9C-%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC-%EC%99%95%EC%B4%88%EC%8B%AC%EC%9E%90%EC%9A%A9
#
## 사전 준비
# 1. sqlite connection 생성 
# 1.1. tourch /opt/airflow/dags/airflow.db
# 1.2. Airflow webserver > Admin > Connections > add 'db_sqlite' conn id 생성
# 2. Http Connection 생성
# 2.1. Airflow webserver > Admin > Connections > add 'naver_search_api' conn id 생성
#
## 디버깅 방법
# 1. 중단점에 `import pdb; pdb.set_trace()` 소스 추가
# 
# 2. docker container 접속해 테스트 command 실행
# ```
# ~/project/airflow/dags$ docker exec -it airflow_airflow-webserver_1 bash
# 
# # dag 전체 테스트
# default@efc626414362:/opt/airflow$ python3 ./dags/naver_search_pipeline.py
# # operator 테스트
# default@efc626414362:/opt/airflow/dags$ airflow tasks test naver-search-pipeline preprocess_result 2022-01-07
# ```
# 3. https://docs.python.org/ko/3.7/library/pdb.html 디버거 명령어 참고해서 디버깅

import json
from datetime import datetime, timedelta
from airflow import DAG
from pandas import json_normalize
from preprocess.naver_preprocess import preprocessing

from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.bash import BashOperator

default_args = {
	"start_date": datetime(2022,1,1)
}

# import pdb; pdb.set_trace() # 디버깅 start 지점

# 대그 완료 출력
def _complate():
	print("네이버 검색DAG 완료")

with DAG(
	dag_id="naver-search-pipeline"
	, schedule_interval=None
	, default_args=default_args
	, tags=["naver", "search"]
	, catchup=False) as dag:


	# ? 개별로 task 실행할 경우엔 잘되는데 전체 flow에서는 안될까?
	# 저장될 테이블 생성
	creating_table = SqliteOperator(
		task_id="creating_table"
		, sqlite_conn_id="db_sqlite"
		, sql='''
		CREATE TABLE IF NOT EXISTS naver_search_result( 
                title TEXT,
                address TEXT,
                category TEXT,
                description TEXT,
                link TEXT
            )
		'''
	)

	# 네이버 API 키 입력
	NAVER_CLI_ID = "lCgc5qM_zlI8eNQIcsEQ"
	NAVER_CLI_SECRET = "MAmelJys0R"

	# 네이버 API 접속 테스트
	is_api_available = HttpSensor(
		task_id="is_api_available"
		, http_conn_id="naver_search_api"
		, endpoint="v1/search/local.json"
		, headers={
			"X-Naver-Client-Id" : f"{NAVER_CLI_ID}",
			"X-Naver-Client-Secret" : f"{NAVER_CLI_SECRET}"
		}
		, request_params={
			"query": "김치찌개"
			, "display": 5
		}
		, response_check=lambda response: response.json()
	)

	# 네이버 API 이용 크롤링
	crawl_naver = SimpleHttpOperator(
		task_id="crawl_naver"
		, http_conn_id="naver_search_api"
		, endpoint="v1/search/local.json"
		, headers={
			"X-Naver-Client-Id" : f"{NAVER_CLI_ID}",
			"X-Naver-Client-Secret" : f"{NAVER_CLI_SECRET}"
		}
		, data={
			"query": "김치찌개"
			, "display": 5
		}
		, method="GET"
		, response_filter=lambda res: json.loads(res.text)
		, log_response=True
	)

	# 검색 결과 전처리 후 csv 저장
	preprocess_result=PythonOperator(
		task_id="preprocess_result"
		, python_callable=preprocessing
	)

	# ? 개별로 task 실행할 경우엔 잘되는데 전체 flow에서는 안될까?
	# csv 파일 sqlite에 저장
	store_result=BashOperator(
		task_id="store_result"
		, bash_command='echo -e ".separator ","\n.import /opt/airflow/dags/data/naver_processed_result.csv naver_search_result" | sqlite3 /opt/airflow/airflow.db'
	)

	print_complate = PythonOperator(
		task_id="print_complate"
		, python_callable=_complate
	)

	creating_table >> is_api_available >> crawl_naver >> preprocess_result >> store_result >> print_complate

	if __name__ == "__main__":
		dag.test()