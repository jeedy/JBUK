# nifi processor 정리
참고 : 
- https://www.popit.kr/%EC%BD%94%EB%93%9C-%ED%95%9C%EC%A4%84-%EC%97%86%EC%9D%B4-%EC%84%9C%EB%B9%84%EC%8A%A4-dashboard-%EB%A7%8C%EB%93%A4%EA%B8%B02/
- https://eyeballs.tistory.com/290 (유용한 정보들)
- https://eyeballs.tistory.com/397?category=875897 (security 적용하는 방법(TLS), 아무나 nifi 접근 하지 못하도록 하는 방법, 그냥 IP접근 제한을 하는게 더 나을지도 ;) )
### 용어
- properties
- attributes


<a id="idx-QueryDatabaseTable"></a>
## 1. QueryDatabaseTable
DB에서 쿼리를 통해 데이터를 추출.

### properties
- Database Connection Pooling Service : 접속할  datasource connection pool 선택 (선택할 connection pool 이 없다면 `NiFi Flow Configuration`에서 생성한다.)
- Database Type : Database 선택
- **Table Name (중요)** : 임의의 쿼리를 실행해 컬럼들을 가져오려면 `Table name` 을 `dummy`로 입력한다.
- Custom Query : `Table name`을 `dummy`로 입력했다면 원하는 쿼리를 이 필드안에 작성할 수 있다.
- Maximum-value Columns : 시쿼스 컬럼을 지정. 설정된 값은 QueryDatabaseTable > 우측클릭 > `View state` 에 보면 key:value 값으로 현재 상태를 기록하고 있다.<br>
**해당 컬럼은 Custom Query 에서 order by 로 꼭 지정해줘야 한다.** (이유는 모르겠다.)
- output(content type): `application/avro-binary` 

## 2. SplitAvro
[QueryDatabaseTable](#idx-QueryDatabaseTable) output 은 `application/avro-binary` 로 리턴되는데 이게 하나의 파일에 리스트로 리턴된다. 이것을 각각의 파일로 split 시키기 위해 `SplitAvro` 를 사용한다. 나중에 각각의 파일로 접근해 데이터 변형이라던지 sql문으로 convert 시키기 위함이다.
- 특별히 속성을 수정할 필요는 없다.