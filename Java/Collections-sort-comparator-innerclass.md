# Comparator Inner class로 sort 방법

tags:
Collections, sort,  Comparator, inner class,

## Collections.sort

```java
Collections.sort(reserveList, new Comparator<ReserveVO>() {
                @Override
                public int compare(ReserveVO o1, ReserveVO o2) {
                    //
                    return o1.getId() - o2.getId();
                }
            });
```