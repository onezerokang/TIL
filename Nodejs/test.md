# Test

기능 개발을 완료한 후 개발자나 QA는 기능에 문제가 없는지 테스트를 한다. 개발자는 모든 기능을 일일이 테스트하기보단 테스트 프로그램을 만들어 테스트를 자동화 할 수 있다.

테스트를 한다고 모든 에러를 막을 수는 없지만 간단한 에러로 프로그램에 문제가 생기는 것을 막을 수 있기 때문에 테스트를 하는 것이 좋다.

## Jest

Node.js 테스트에 사용할 패키지는 페이스북에서 개발한 jest이다.
jest는 테스팅에 필요한 툴들을 대부분 갖고 있어 편리하게 사용할 수 있다.

jest에 대한 내용은 [jest]()문서를 참조하시오

## 단위 테스트(Unit Test)

단위 테스트는 가장 작은 단위의 테스트로 일반적으로 메서드 레벨을 테스트한다. 단위 테스트의 목적은 다음과 같다.

_단위 테스트 목적 자세하기 작성하기_

- 문제점 발견
- 쉬운 변경
- 품질 향상
- 코드의 문서화

_단위 테스트 하는 방법과 예시 작성하기_

좋은 단위 테스트는 다음과 같다.

_좋은 단위테스트에 대해 작성하기_

## 테스트 커버리지(Test coverage)

jest에는 coverage라는 기능이 있는데, 이를 사용하면 전체 코드 중 테스트되는 코드와 테스트되지 않은 코드의 비율을 확인할 수 있다. 커버리지 기능을 사용하기 위해서는 package.json에 아래와 같이 coverage 스크립트를 추가해준다.

```json
{
  "name": "",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "nodemon index.js",
    "test": "jest",
    "coverage": "jest --coverage"
  }
}
```

이제 테스트 커버리지를 확인할 수 있다.

```
npm run coverage
```

_커버리지 사진 추가하기_

_커버리지 보는 법, 각 항목에 대한 설명 추가하기_

## 통합 테스트(Integration Test)

_통합 테스트에 대한 설명_

통합 테스트를 하기 위해서는 supertest 패키지를 설치해야 한다.

```
npm i supertest -D
```

supertest 패키지로 통합 테스트를 하기 위해서는 express의 app 객체를 모듈로 만들어 불어와야 합니다.

```js
const express = require("express");
const app = express();

// ... 생략

module.exports = app;
```

통합 테스트를 할 때는 데이터베이스 코드를 모킹하지 않으므로 실제 데이터베이스를 사용하게 된다.
허나 실제 서비스 중인 데이터 베이스에 테스트 데이터가 들어가면 안되기 때문에 테스트용 데이터베이스를 따로 만들어 사용해야 한다.

## TDD

TDD란 Test Driven Development의 약자로 테스트 주도 개발을 의미한다.
테스트 주도 개발은 프로그램을 작성한 후 테스트를 하는 것이 아닌 테스트 코드를 먼저 만들고 프로덕션 코드를 나중에 짜는 것이다.

_테스트 주도 개발의 프로세스 이미지_

TDD의 장점은 다음과 같다.

- 테스트 커버리지가 자연스럽게 높아진다.
- 오버 엔지니어링을 방지한다.
- 설계에 대한 피드백이 빠르다.

## 참조

[Jest | JavaScript Testing Framework](https://codeamor.dev/js/2021-03-27/)  
[[10분 테코톡] 😼 피카의 TDD와 단위테스트](https://www.youtube.com/watch?v=3LMmPXoGI9Q&ab_channel=%EC%9A%B0%EC%95%84%ED%95%9CTech)
