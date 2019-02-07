# Eclipse 에서 JSP Format setting 방법

JSP 페이지에서 자동 포멧팅(Ctrl + Shift + F) 할 경우 code를 잘 정돈되도록 셋팅하는 방법이다.

## JAVASCRIPT

**window > Preferences > JavaScriptr > Code Style > Formatter**

## Indentation > General settings > Tab policy

탭버튼을 `tab`으로 할지 `space`로 할지 정한다.
- `space`로 선택할 경우 `Indentation size` 값으로 space 사이즈 결정
- `tab`일 경우 `Tab size` 값으로 tab 사이즈 결정


## HTML

**windows > Preferences > Web > HTML > Editor**

### Formatting > Line width 값을 200이상으로 셋팅한다.

라인 길이가 설정값보다 작으면 자동으로 개행한다.

### 탭 대신 Space로 통일 하려면 `indent using spaces`로 체크한다.

`Indentation size`는 한 탭에 몇개의 `Space`를 넣을 껀지 결정한다. (4가 적당하다)

### 자동 포멧팅시 span 이나 li 경우 한줄로 붙어서 나온다.

`Inline Elements`에 li, span 을 `remove` 하게 되면 개행되어 정돈된다.

