# Spring Batch

- 대용량 데이터: 대량의 데이터를 가져오거나, 전달하거나, 계산하는 등의 처리를 할 수 있어야 합니다.
- 자동화: 심각한 문제 해결을 제외하고는 `사용자 개입 없이 실행` 되어야 합니다.
- 견고성: 잘못된 데이터를 충돌/중단 없이 처리할 수 있어야 합니다.
- 신뢰성: 지정한 시간 안에 처리를 완료하거나 동시에 실행되는 다른 어플리케이션을 방해하지 않도록 수행되어야 합니다.

## Spring Batch 4.0 (Spring Boot 2.0) Reader & Writer

DataSource | 기술 | 설명
---|---|---
Database | JDBC  | 페이징, 커서, 일괄 업데이트 등 사용가능
Database | Hibernate  | 페이징, 커서 사용 가능
Database | JPA  | 페이징 사용 가능 (현재 버전에선 커서 없음)
Database | Flat file  | 지정한 구분자로 파싱 지원

> iBatis 모듈은 현재 삭제되었습니다.
  iBatis를 reader로 사용하셨던 분들은 JDBC ItemReader로 교체하시길 추천드립니다.


## Batch vs Quartz ?

Quartz는 스퀘줄러의 역활, Batch와 같은 `대용량 데이터 배치 처리`에 대한 기능을 지원하지 않는다. 반대로 Batch역시 Quartz의 다양한 스케줄 기능을 지원하지
않아서 보통 Quartz + Batch 를 조합해서 사용합니다.

정해진 스케줄마다 Quartz가 Spring Batch를 실행하는 구조

