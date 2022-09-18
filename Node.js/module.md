# require vs import(CommonJS vs ES6)

<!-- 세줄 요약이 들어갈 공간: 개요 -->

ES6 이전 자바스크릅트에서는 모듈을 사용할 수 없었다. 이 때문에 Node.js에서 모듈을 사용하기 위해 `require`/`exports` 문법(CommonJS)을 도입하여 모듈을 사용할 수 있게 했다. 이후 ES6에서 `import`/`export` 키워드를 도입하여 자바스크립트에서 모듈을 사용할 수 있게 됐다.

## require와 import의 차이점

## CommonJS

- **모듈 전체 내보내기 / 가져오기**

```js
const math = {
  sum(a, b) {
    return a + b;
  },
  minus(a, b) {
    return a - b;
  },
};

module.exports = math;
```

```js
const math = require("./math.js");

math.sum(1, 2); // 3
math.minus(1, 2); // -1
```

- **모듈 개별 내보내기 / 가져오기**

```js
exports.sum = (a, b) => a + b;
exports.minus = (a, b) => a - b;
```

```js
const { sum, minus } = require("./math.js");

sum(1, 2); // 3
minus(1, 2); // -1
```

## ES6

- **모듈 전체 내보내기 / 가져오기**

```js
const math = {
  sum(a, b) {
    return a + b;
  },
  minus(a, b) {
    return a - b;
  },
};

export default math;
```

```js
const math = require("./math.js");

math.sum(1, 2); // 3
math.minus(1, 2); // -1
```

- **모듈 개별 내보내기 / 가져오기**

```js
export const sum = (a, b) => a + b;
export const minus = (a, b) => a - b;
```

```js
import {sum, minus} from require('./math.js')

sum(1, 2); // 3
minus(1, 2); // -1
```

## Node.js에서 import 키워드 사용 방법

package.json에 `"type":"module"`을 추가해준다.

```json
{
  "type": "module"
}
```

## 참조

https://velog.io/@gay0ung/require-import  
https://inpa.tistory.com/entry/NODE-%F0%9F%93%9A-require-%E2%9A%94%EF%B8%8F-import-CommonJs%EC%99%80-ES6-%EC%B0%A8%EC%9D%B4-1#Node.js_%EC%97%90%EC%84%9C_import_%ED%82%A4%EC%9B%8C%EB%93%9C_%EC%82%AC%EC%9A%A9_%EB%B0%A9%EB%B2%95
