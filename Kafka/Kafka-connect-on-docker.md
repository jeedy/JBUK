# Kafka Connect on Docker

## 1. About
kafka Source Connector 설치하고 Mysql(DW database) 에 특정 Table(htl_v_city_mast_temp_20220825) 를 가져오는 것까지 실습한다. (silk connector 구현은 source connector를 참고.)

> kafka source connector plugin 을 제공하는 그룹은 크게 두 가지로 나뉜다.    
> - Debezium
> - Confluent (Atlassian 사 confluence 과 연관 없음)
>
> 둘 중에 `Debezium` 을 사용해 구현한 예제이다.


