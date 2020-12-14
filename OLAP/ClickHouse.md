# ClickHouse
tags: OLAP, spark, Apache Zeppelin, 빅데이터, bigdata, BigQuery, Firebase, analytic, ETL, database, Druid,

참고자료:
- [About ClickhHouse 1](https://medium.com/delightroom/clickhouse-%EA%B8%B0%EB%B0%98-%EB%B6%84%EC%84%9D-%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8-%EA%B5%AC%EC%B6%95-ea25b8ba43e9)
- [About ClickhHouse 2](http://whatdb.blogspot.com/2019/10/clickhouse.html)
- [ClickHouse 기본 문법](https://clickhouse.tech/docs/en/sql-reference/statements/select/sample/)
- [ClickHouse 설치방법](https://scorpio-mercury.tistory.com/27)

## 개요
- 대용량 데이터를 빠르게 쿼리해주는 솔루션
- 러시아에서 만들었고 RDB 형태로 저장되는 듯하나 row단위가 아닌 column 단위로 저장하고 관리한다. 사용되는 쿼리는 mysql 쪽에 가깝다.
- 특이한점은 column type 에 array, nested 형태를 지원한다.(MongoDB와 비슷하다고 볼 수도 있겠다.)
- spark와 비교되기도 하지만 조금은 다른 RDB 과에 가깝다.
- 한국어로 된 문서는 찾아보기 힘들고 영어로된 [reference 페이지](https://clickhouse.tech/docs/en/) 는 꽤 잘되어있는 편
- 설치(clustering)는 어려워보이지 않음.
- 해당 솔루션이 가진 특성 때문인지 데이터 마이그레이션도 어렵지 않게 다양하게 제공한다.

결국 도입이 문제가 아닌 원하는 데이터를 추출하기 위한 insight가 필요하다.