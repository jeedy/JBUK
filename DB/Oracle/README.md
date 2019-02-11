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
