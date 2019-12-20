# 메이븐 스코프 설명
tags: maven, scope

## 스코프 종류
- compile - 기본값(프로젝트의 모든 classpath에 등록됨)

- provided - 컴파일 및 테스트 시에는 필요하지만 런타임 환경에서는 필요하지 않을 때 사용 (ex:servlet API, jsp)

- runtime - 컴파일 시에는 필요하지 않지만 런타임 환경에서는 필요할 때 사용 (classpath에는 추가되지만 컴파일 시에는 추가 안됨, ex: JDBC 드라이버 )

- test - 말 그대로 테스트 시에만 사용 (ex: easymock, JUnit )

- system - 메이븐 중앙 레파토리가 아닌 로컬 라이브러리를 별도로 로드할 때 사용함 (JAR 파일의 위치를 지정하는 systemPath 엘리먼트 명시적 입력)
 

링크 : http://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html
