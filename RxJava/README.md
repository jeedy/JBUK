# RxJava (리액티브 자바))

참고

- ``도서`` [RxJava 프로그래밍](http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=9788968488658&orderClick=LAG&Kc=)

## 용어해석

- 도수(frequency) : 하나의 범주 안에 얼마나 많은 항목이 들어 있는지 나타내는 통계적 방법
- 범주적(categorical) : 일정한 범주로 나누어진 다음 각 범주의 성질이나 특성을 묘사, 숫자로 해석될 수 없는 데이터, 게임장르나 개의 종류, 디저트의 타입 등 정량적(qualitative) 데이터 라고도 한다.
- 수치적(numerical) : 값의 측정이나 개수 처럼 어떤 숫자로서의 의미를 갖는 데이터, 정량적(quantiative) 데이터라고도 한다.

## 평균(average)

- 평균값(mean, Ʃ) : n개의 데이터를 모두 더해서 n개로 나눈 수
- 중앙값(median) : 가운데 수
- 최빈값(mode) : 빈도가 가장 높은 수(최고 빈도의 수가 n개 발생할 수 있다.)

## 변위와 분포

### 기본 데이터
기본 데이터 | | | | | | | |
-----|--|--|--|--|--|--|--
시합 당 올린 점수 | 3 | 6 | 7 | 10 | 11 | 13 | 30
도수           | 2 | 1 | 2 | 3 |  1  |  1  | 1

### 집합의 범위 = ``상한`` - ``하한`` 
> 제일 높은 값에서 제일 낮은 값을 뺏을때

집합의 범위 | ``하한`` | | | | | | ``상한`` |
-----|--|--|--|--|--|--|--
시합 당 올린 점수 | 3 | 6 | 7 | 10 | 11 | 13 | 30
도수           | 2 | 1 | 2 | 3 |  1  |  1  | 1

- 집합 범위 = 30 - 3 = 27

### 사분위수
> 데이터를 4개의 조각으로 분할 하는 값들, 가장 큰 사분위수를 ``상한사분위수`` 가장 작은 사분위수를 ``하한사분위수`` 라고 합니다. 가운데있는 사분위수는 ``중앙값``입니다.

사분위수 | | |``하한사분위수``| | | | ️️️| |``상한사분위수``| | |
-----|--|--|--|--|--|--|--|--|--|--|--|
시합 당 올린 점수 | 3 | 3 | 6 | 7 | 7 | 10| 10 | 10 | 11 | 13 | 30

- 하한사분위수 = ceil(n / 4) = ceil(11 / 4) = ceil(2.75) = 3
- 상항사분위수 = ceil(3n / 4) = ceil(3 * 11 / 4) = ceil(8.25) = 9

### 사분범위 = ``상한 사분위수`` - ``하한 사분위수``
> 데이터를 4등분 했을때 1q(25%)와 4q(25%)를 제외시키고 가운데 위치한 50% 데이터의 범위입니다.

사분위수 | | |``하한사분위수``| | | | ️️️| |``상한사분위수``| | |
-----|--|--|--|--|--|--|--|--|--|--|--|
시합 당 올린 점수 | 3 | 3 | **6** | 7 | 7 | 10| 10 | 10 | **11** | 13 | 30

- 사분범위 = 11 - 6 = 5

### 백분위수 또는 십분위수
> 사분위수가 데이터를 4개 조각으로 나누는 것처럼 데이터를 10% 퍼센트로 나누는 값

### 표준편차
값들이 평균값으로부터 떨어져 있는 정도를 나타낸다. 표준편차가 작을수록 평균값에 더 가깝다.
표준편차의 가장 작은 값은 0이다.