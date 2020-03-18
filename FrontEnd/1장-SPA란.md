# 1. SPA란, 단일 페이지 애플리케이션(Single Page Application, SPA)


## 1. SPA (Single Page Application)

### 참고자료
1. [https://poiemaweb.com/js-spa](https://poiemaweb.com/js-spa)
1. [https://jaroinside.tistory.com/24](https://jaroinside.tistory.com/24) 
SAP, SinglePageApplication 페이지에 대한 설명 부터
1. [https://ko.reactjs.org/docs/glossary.html#single-page-application](https://ko.reactjs.org/docs/glossary.html#single-page-application) babel, webpack, npm 등 리액트에서 나오는 용어 정리
1. [http://hacks.mozilla.or.kr/2014/12/an-easier-way-of-using-polyfills/](http://hacks.mozilla.or.kr/2014/12/an-easier-way-of-using-polyfills/) 폴리필(Polyfill)이란?
link tag를 사용하는 전통적인 웹 방식은 새로운 페이지 요청 시마다 정적 리소스가 다운로드되고 전체 페이지를 다시 렌더링하는 방식을 사용하므로 새로고침이 발생되어 사용성이 좋지 않다. 그리고 변경이 필요없는 부분를 포함하여 전체 페이지를 갱신하므로 비효율적이다.

SPA는 기본적으로 웹 애플리케이션에 필요한 모든 정적 리소스를 최초에 한번 다운로드한다. 이후 새로운 페이지 요청 시, 페이지 갱신에 필요한 데이터만을 전달받아 페이지를 갱신하므로 전체적인 트래픽을 감소할 수 있고, 전체 페이지를 다시 렌더링하지 않고 변경되는 부분만을 갱신하므로 새로고침이 발생하지 않아 네이티브 앱과 유사한 사용자 경험을 제공할 수 있다.


구분 | History 관리 | SEO 대응 | 사용자 경험 | 서버 렌더링 | 구현 난이도 | IE 대응
--- | :---: | :---: | :---: | :---: | :---: | :---:
전통적 링크 방식 | ◯ | ◯ | ✗ | ◯ | 간단	 
AJAX 방식 | ✗ | ✗ | ◯| ✗ | 보통 | 7 이상
Hash 방식 | ◯ | ✗ | ◯ | ✗ | 보통 | 8 이상
PJAX 방식 | ◯ | ◯ | ◯ | △ | 복잡 | 10 이상

모든 소프트웨어 아키텍처에는 trade-off가 존재한다. SPA 또한 모든 애플리케이션에 적합한 은탄환(Silver bullet)은 아니다. 애플리케이션의 상황을 고려하여 적절한 방법을 선택할 필요가 있다.

## 2. Babel 과 Webpack 이 뭐냐

### 참고자료
1. [Babel과 Webpack을 이용한 ES6 환경 구축](https://poiemaweb.com/es6-babel-webpack-1)

크롬, 사파리, 파이어폭스과 같은 에버그린 브라우저(Evergreen browser, 사용자의 업데이트 없이도 최신 버전으로 자동 업데이트를 수행하는 모던 브라우저)의 ES6 지원 비율은 약 98%

하지만 IE11 의 ES6 지원 비율은 약 11%, 그리고 매년 새롭게 도입되는 ES6+ 와 제안 단계에 있는 ES 제안 사양(ES NEXT)은 브라우저에 따라 지원 비율이 제각각이다.

따라서 ES6+ 또는 ES NEXT의 사양을 이용하여 프로젝트를 진행하려면 최신 사양으로 작성된 코드를 IE를 포함한 구형 브라우저에서 문제 없이 동작하기 위해서 바닐라JS 코드로 변환할 필요가 있다. 

- IE를 포함한 구형 브라우저는 ES6 모듈을 지원하지 않는다.
- 브라우저의 ES6 모듈 기능을 사용하더라도 트랜스파일링이나 번들링이 필요하다.
- 아직 지원하지 않는 기능(Bare import 등)이 있다. ([ECMAScript modules in browsers](https://jakearchibald.com/2017/es-modules-in-browsers/) 참고)
- 점차 해결되고는 있지만 아직 몇가지 이슈가 있다. ([ECMAScript modules in browsers](https://jakearchibald.com/2017/es-modules-in-browsers/) 참고)

트랜스파일러(Transpiler) **Babel**과 모듈 번들러(Module bundler) **Webpack**을 이용하면 ES6+ 코드로 작성된 javascript를 구형 브라우저에서도 돌아갈 수 있도록 변환할 수 있다.

### Babel

아래 예제는 ES6의 화살표 함수와 ES7의 지수 연산자를 사용하고 있다.
```javascript 
// ES6 화살표 함수와 ES7 지수 연산자
[1, 2, 3].map(n => n ** n);
```

IE와 다른 구형 브라우저에서는 이 두가지 기능을 지원하지 않을 수 있다. **Babel**을 사용하면 위 코드를 아래와 같이 ES5 이하의 버전으로 변환할 수 있다.

```javascript
// ES5
"use strict";

[1, 2, 3].map(function (n) {
  return Math.pow(n, n);
});
```

이처럼 Babel는 최신 사양의 자바스크립트 코드를 IE나 구형 브라우저에서도 동작하는 ES5 이하의 코드로 변환(트랜스파일링)할 수 있다. 


### Webpack
의존 관계에 있는 모듈들을 하나의 자바스크립트 파일로 번들링하는 **모듈 번들러**이다.
Webpack을 사용하면 의존 모듈이 하나의 파일로 번들링되므로 별도의 모듈 로더가 필요없다. 그리고 다수의 자바스크립트 파일을 하나의 파일로 번들링하므로 html 파일에서 script 태그로 다수의 자바스크립트 파일을 로드해야 하는 번거로움도 사라진다.

Webpack과 Babel 를 이용하여 ES6+ 개발을 진행한다면, Babel 이 ES6+ 코드를 ES5 코드로 **트랜스파일링** 을 진행하고 그다음 Webpack이 파일들을 번들링 할 것이다.

> 모듈로더(Module Loader) : 실행 시간에 스크립트를 로드해서 html에 부착한다.

> 모듈번들러(Module Bundler) : 컴파일 시간을 만들어서 일단 빌드하여 한개의 js파일로 내보낸다.

> vs Browserify(브라우저파이) : Browserify는 UNIX 철학을 근간으로 합니다(substack은 스스로를 유닉스 철학자라고 칭하고 있습니다) 즉, 핵심적 요소만 충실히 구현하고 다른 기능이 필요할 땐 모두 외부에서 구현한 모듈을 조합해 사용하도록 합니다. 반면 Webpack은 모든 기능을 포함해 구현하고 최적화를 충실히 이행하는 개발 방식을 취하고 있는 듯 합니다. (참고: https://coderifleman.tumblr.com/post/112564054684/browserify%EC%99%80-webpack)


### 추가: 폴리필(polyfill)
폴리필(polyfill)은 웹 개발에서 기능을 지원하지 않는 웹 브라우저 상의 기능을 구현하는 코드를 뜻한다.<br>
기능을 지원하지 않는 웹 브라우저에서 원하는 기능을 구현할 수 있으나, 폴리필 플러그인 로드 때문에 시간과 트래픽이 늘어나고, 브라우저별 기능을 추가하는 것 때문에 코드가 매우 길어지고, 성능이 많이 저하된다는 단점이 있다.[(위키)](https://ko.wikipedia.org/wiki/%ED%8F%B4%EB%A6%AC%ED%95%84_(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D))