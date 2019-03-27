# 오라클

## 랜덤 함수를 이용한 정렬

```sql
ORDER BY DBMS_RANDOM.RANDOM()
```

## 페이징 방법

```sql
SELECT PAGING_A.* FROM (
    SELECT PAGING_B.*, ROWNUM RNUM FROM (

    ) PAGING_B
    WHERE ROWNUM <= #{endRow}
) PAGING_A
WHERE RNUM >= #{startRow}
```

## :bomb: troubleshooting

1. Where 조건 식에서 "!=" 가 정상동작 하지 않는다.
```sql
-- 오라클 version
SELECT * FROM v$version WHERE banner LIKE 'Oracle%';
-- Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
```

예를 들어

```sql
select * from emp where YN = 'Y' OR (YN != 'Y' AND VIEW ='PC')
```

위와 같은 쿼리를 작성할때 YN 이라는 컬럼 값이 'Y' 이거나 'Y' 가 아니라면 VIEW 라는 컬럼값이 'PC' 인 값이 노출 되길 원할 것이다.  그러나 이런 예상과 다르게 리스트는 출력되지 않는다.

그 이유는  `YN != 'Y'` 이 표현식이 원하는 방식대로 동작하지 않는다. 공백으로 있다고 해서 `YN = ''` 이렇게 표현을 해도 나오지 않는다.
`YN is null` 이렇게 작성해야 나오는데, 빈공간(''), 'N', NULL 값으로 입력되었을때 일일이 처리하기 힘들다

그래서 이럴경우 `NVL()` 함수를 이용하자, 아래는 수정된 예제이다.
```sql
select * from emp where YN = 'Y' OR ( NVL(YN, 'N') != 'Y' AND VIEW ='PC')
```
이렇게 처리하도록 하자

1. Function execute ERROR ORA-00904 : "부적합한 식별자"  
```sql
-- 오라클 version
SELECT * FROM v$version WHERE banner LIKE 'Oracle%';
-- Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
```
A 계정에서 A.sampleFunction() 을 만들어 호출 할 경우 ORA-00904 : "부적합한 식별자" 오류가 발행하는 경우가 있다.

특이한 점은 매번 발생하는 것이 아닌 간혈적(특정조건)으로 발생하는 데, 원인을 알 수 없어 재현하기 힘들다.
```sql
-- A 계정
A.sampleFunction()  
```

해결방법은 해당 계정이 가지고 있는 Function은 "A." 을 붙이지 않고 아래처럼 호출하면 발생하진 않는다. 
```sql
-- A계정
sampleFunction()
```
