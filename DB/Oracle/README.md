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

예를 들어

```
select * from emp where YN = 'Y' OR (YN != 'Y' AND VIEW ='PC')
```

위와 같은 쿼리를 작성할때 YN 이라는 컬럼 값이 'Y' 이거나 'Y' 가 아니라면 VIEW 라는 컬럼값이 'PC' 인 값이 노출 되길 원할 것이다.  그러나 이런 예상과 다르게 리스트는 출력되지 않는다.

그 이유는  `YN != 'Y'` 이 표현식이 원하는 방식대로 동작하지 않는다. 공백으로 있다고 해서 `YN = ''` 이렇게 표현을 해도 나오지 않는다.
`YN is null` 이렇게 작성해야 나오는데, 빈공간(''), 'N', NULL 값으로 입력되었을때 일일이 처리하기 힘들다

그래서 이럴경우 `NVL()` 함수를 이용하자, 아래는 수정된 예제이다.
```
select * from emp where YN = 'Y' OR ( NVL(YN, 'N') != 'Y' AND VIEW ='PC')
```
