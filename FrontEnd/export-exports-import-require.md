# export, exports And import, require 차이

참고 
    - https://velog.io/@jch9537/Javascript-export-default (export, exports, import, require 차이 설명)

## 1. `export` 는 javascript 모듈에서 함수, 객체, 원시값을 내보낼 때 사용

test.js:
```javascript 
export var a = "hello";
export var b = "bye";
export var a = "cycle";  
```

### App.js: require 사용해서 가져오기
```javascript
var kk = require("./components/test.js");

function App() {
    console.log(kk.a);
    console.log(kk.b);
    console.log(kk.c);
}
export default App
```

### App.js: import 사용해서 가져오기
```javascript
import {a, b, c} from "./components/test.js";

function App() {
    console.log(a);
    console.log(b);
    console.log(c);
}
export default App
```

### javascript Debugger console: 결과 (require와 import로 가져온 값은 같음)
```console
hello
bye
cycle
```

## 2. `exports` 는 모듈에서 함수, 객체, 원시값을 객체에 담아서 내보낼 때 사용

test.js:
```javascript 
exports.a = "hello";
exports.b = "bye";
exports.c = "cycle";
```

### App.js: require 사용해서 가져오기
```javascript
var importTest = require("./components/test.js");

function App() {
    console.log(importTest);
    console.log(importTest.a);
    console.log(importTest.b);
    console.log(importTest.c);
}
export default App
```

### App.js: import 사용해서 가져오기
```javascript
import importTest from "./components/test.js";

function App() {
    console.log(importTest);
    console.log(importTest.a);
    console.log(importTest.b);
    console.log(importTest.c);
}
export default App
```

### javascript Debugger console: 결과 (require와 import로 가져온 값은 같음)
```console
{a: "hello", b: "bye", c: "cycle"}
hello
bye
cycle
```