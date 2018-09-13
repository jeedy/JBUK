# RxJava

## Observable
RxJava1.x 에서는 이 클래스 하나만 존재 했으나 2.x 부터는 상황에 맞게 세분화 되어 Maybe, Flowable 클래스가 추가되었다.
기본적으로 옵서버(Observer) 패턴을 구현, 라이프 사이클 x, 보통 단일 함수를 통해 변화만 알림
사용자가 버튼을 누르면 버튼에 미리 등록해둔 onClick() 메소드를 호출해 원하는 처리를 하는 것이 옵서버 패턴의 대표적인 예.

### 구독자에게 전달하는 알림 종류
- onNext : Observable이 데이터의 발행을 알립니다. 기존의 옵서버 패턴과 같습니다.
- onComplete : 모든 데이터의 발행을 완료했음을 알립니다. onComplete 이벤트는 단 한번만 발생하며, 발생한 후에는 더 이상 onNext 이벤트가 발생해선 안됨.
- onError : Observable에서 어떤 이유로 에러가 발생했음을 알림, onError 이벤트가 발생하면 onNext, onComplete 이벤트가 발생하지 않음. 즉, Observable 실행을 종료.

## Maybe
reduce() 함수나 firstElement() 함수와 같이 데이터가 발행될 수 있거나 혹은 발행되지 않고도 완료되는 경우를 의미.

## Flowable
Observable에서 데이터가 발행되는 속도가 구독자가 처리하는 속도보다 현저하게 빠른 경우 발생하는 배압(back pressure) 이슈에 대응하는 기능을 추가로 제공한다.