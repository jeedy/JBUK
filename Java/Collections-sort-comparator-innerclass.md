# Comparator Inner class로 sort 방법

tags:
Collections, sort,  Comparator, inner class,

## Collections.sort

참고자료
- https://gmlwjd9405.github.io/2018/09/06/java-comparable-and-comparator.html

```java
Collections.sort(reserveList, new Comparator<ReserveVO>() {
    @Override
    public int compare(ReserveVO o1, ReserveVO o2) {
        //
        return o1.getId() - o2.getId();
    }
});
```
