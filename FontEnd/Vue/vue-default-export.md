# Default Export 란?

- 모듈에는 딱하나의 Default Export만 존재해야한다.
- 기본적으로 main 함수라고 생각하면된다.

아래와 같이 export 할 수 있습니다.

Named exports: 
```javascript
// module "my-module.js"
function cube(x) {
    return x * x * x;
}
const foo = Math.PI + Math.SQRT2;
export { cube, foo };
위의 export된 값들을 import하여 사용할 때 아래와 같이 사용할 수 있습니다.

import { cube, foo } from 'my-module';
console.log(cube(3)); // 27
console.log(foo);    // 4.555806215962888

```

아래와 같이 Default export 할 수 있습니다.

Default exportsL
```javascript
// module "my-module.js"
let cube = function cube(x) {
    return x * x * x;
}
export default cube;
default exports된 값을 import 하는 방법은 아래와 같습니다.

// module "my-module.js"
import myFunction from 'my-module';
console.log(myFunction(3)); // 27
```
