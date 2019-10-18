# ETL (Extract, Transform, Load)
tag: nifi, streamsets, Talend open source,

## 참고자료
1. nifi vs streamsets 장단점 비교 https://cube.dev/blog/open-source-etl/
    - Apache NiFi
        - Pros:
            1. Clean and well-thought-out implementation of the dataflow programming concept
            1. Can handle binary data
            1. Data Provenance
        - Cons:
            1. Spartan User Interface
            1. No live monitoring/debugging features with per-record statistics
    - Streamsets
        - Pros:
            1. Live monitoring/debugging features with visual per-record statistics for every processor
            1. Sexy UI
            1. Well-suited for record-based data and streaming
        - Cons:
            1. You need to stop the whole dataflow to edit a single processor configuration
            1. No reusable JDBC configuration for processors
2. ETL Tools List: Overview & Pricing https://cube.dev/blog/etl-tools-list/
3. Extract, Transform, Load를 위한 도구 오픈소스 ETL 솔루션 활용하기 (그냥 오래된 자료 참고만 할것) https://www.kdata.or.kr/info/info_04_view.html?field=&keyword=&type=techreport&page=135&dbnum=128486&mode=detail&type=techreport

## 기대되는 솔류션 순위 (private)
1. nifi (그나마 조금 경험이 있어서)
1. streamsets (nifi 와 대비되는 솔류션이라는 점이라서)
1. Talend Open Studio (소문에 좋다고 들어서)



