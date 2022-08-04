# 스프링배치(Spring-batch) 4.x 버전 사용방법
tags: spring, spring-batch, 

### 참고
- https://khj93.tistory.com/entry/Spring-Batch%EB%9E%80-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B3%A0-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

## Spring Batch 용어

### Job
배치처리 과정에서 전체 계층 최상단, job은 배치러기 과정을 하나의 단위로 만들어 놓은 객체입니다. 

### Job Instance
Job의 실행 단위, Job을 실행시키게 되면 하나의 Job Instance가 생성됩니다.   
예를들어 1월 1일 실행, 1월 2일 실행을 하게 되면 Job Instance가 생성되어 1월 1일 실행한 Job Instance가 실패하여 다시 실행 시키더라도 이 Job Instance는 1월 1일에 대한 데이터만 처리하게 됩니다.

