# Node.js 디자인 패턴 바이블

## Node.js 플랫폼

### Node.js의 철학

Node.js는 코어, 모듈, 인터페이스 등을 최대한 작고, 가볍고, 간단하게 만드는 것을 지향한다.

- 경량코어
  - Node.js는 최소한의 코어 기능만을 갖고 코어 바깥부분에 사용자 전용 모듈 생태계를 두었다.
- 경량모듈
  - 작은 모듈은 재사용성이 뛰어나고 테스트 및 유지보수가 쉽다는 장점을 갖는다.
- 작은 외부 인터페이스
  - Node.js에서 모듈을 정의할 때 명백한 단일 진입점을 제공하기 위해서 단 하나의 함수나 클래스를 노출하는 패턴을 사용한다. 이는 유스케이스를 줄이고 구현을 단순화하며 유지관리를 용이하게 하고 가용성을 높인다는 장점을 갖는다.

### Node.js는 어떻게 작동하는가

#### I/O는 느리다

I/O는 컴퓨터의 기본 기능인 제어, 연산, 입력, 출력, 기억중 입력과 출력을 의미한다.
I/O는 비용이 많이 들진 않지만 요청과 작업이 완료되는 사이에 지연이 발생하기에 컴퓨터의 기본적인 동작중 가장 느린 작업이라고 할 수 있다.

다음은 I/O 작업의 예시이다.

- 파일 시스템
- 네트워크 요청/응답

#### 블로킹 I/O

전통적인 블로킹 I/O 프로그래밍에서는 I/O를 요청하는 함수가 호출되면 작업이 끝날 때까지 스레드 실행을 차단했다.
이런 단점을 보완하기 위해 블로킹 I/O로 구현된 웹서버는 동시연결을 처리하기 위해서 멀티 스레드 혹은 멀티 프로세스를 사용했다.
다만 멀티 스레드/프로세스는 비용이 많이 늘고 동시성 프로그래밍이 꽤 어렵다는 단점을 갖는다.

#### 논블로킹 I/O

대부분의 최신 OS는 논블로킹 I/O를 매커니즘을 지원한다.
I/O를 요청하는 함수가 호출되면 데이터 처리를 기다지 않고 미리 정의된 상수를 반환하여
데이터가 처리 되지 않음을 알린다. 그리고 loop을 돌려 데이터 처리가 완료되었는지를 지속적으로 확인하는 방식을 사용했다.
이런 방식을 busy-waiting이라 하는데 계속 상태를 확인하는 방식인만큼 CPU 낭비가 심하다는 단점이 있다.

#### 이벤트 디멀티플렉싱

`busy-waiting` 방식보다 효율적인 논 블로킹 I/O처리 매커니즘을 OS는 제공한다.
이를 동기 이벤트 디멀티플렉서 혹은 이벤트 통지 인터페이스라한다.

- 멀티플렉싱
  - 전기 통신 용어로 여러 신호를 하나로 합성하여 제한된 수용범위 내에서 매개체를 통해 쉽게 전달
- 디멀티플렉싱
  - 멀티플렉싱으로 온 신호를 원래 구성요소로 분할하는 작업
- 동기 이벤트 디멀티플렉서
  - I/O작업을 관찰하다 처리가 완료됐을 시 새 이벤트를 반환한다.

#### 리액터(Reactor) 패턴

Reactor 패턴은 관찰 대상 리소스에서 새 이벤트를 사용할 수 있을 때까지 블로킹하여 I/O를 처리하고, 각 이벤트를 관련된 핸들러에 전달함으로써 반응한다.

### Node.js에서 JavaScript

#### 최신 JavaScript를 실행시켜라

브라우저에서 JS를 사용할 경우 브라우저의 종류의 버전에 따라 JS의 최신 기능을 지원하지 않는 경우가 있다.
하지만 Node.js는 가장 최신 버전의 V8을 가지고 있기 때문에 최신 ECMAScript 사양의 특성을 대부분 사용할 수 있다.

다만 서드파티에서 사용되기 위한 라이브러리를 개발한다면 우리의 코드가 다양한 Node.js 버전에서 실행될 수 있음을 고려해야 한다.

#### 운영체제 기능에 대한 모든 접근

Node.js는 JavaScript가 운영체제에서 제공하는 기본적인 기능을 사용할 수 있게 바인딩해준다. 다음은 Node.js에서 사용할 수 있는 운영체제 기능의 예시이다.

- 파일시스템
- TCP or UDP 소켓
- HTTP 서버 생성
- 해시 알고리즘 사용
- 애플리케이션이 돌고 있는 프로세스 정보 접근

## 모듈 시스템

모듈은 어플리케이션을 구조화하고 정보에 대한 은닉성을 강화시켜주는 주된 장치이다.
이를 통해 코드의 가독성과 재사용성을 높일 수 있다.

과거 웹이 지금과 같이 복잡하지 않았을 때는 모듈 시스템이 존재하지 않았다.
하지만 JS 브라우저 애플리케이션이 점점 복잡해지고 여러 프레임워크가 생태계를 점유해가면서

Node.js는 CommonJS라는 모듈 시스템을 고안했다.

2015년 ECMAScript의 발표와 힘꼐 표준 모듈 시스템이 고안된다.

### CommonJS 모듈

CommonJS는 Node.js의 첫 번째 내장 모듈 시스템으로 CommonJS 명세를 고려하여 추가적인 자체 확장 기능과 께 구현되었다.

- `require`는 로컬 파일 시스템으로부터 모듈을 임포트한다.
- `exports`와 `module.exports`는 특별한 변수로서 현재 모듈에서 공개될 기능을 내보내기 위해서 사용된다.

#### 직접 만드는 모듈 로더

```js
function moduleLoader(filename, module, require) {
  const wrappedSrc = `(function (module, exports, require) {
    ${fs.readFileSync(filename, "utf8")}
  })(module, module.exports, require)`;
  eval(wrappedSrc);
}
```

```js
function require(moduleName) {
  console.log(`Required invoked for module: ${moduleName}`);
  const id = require.resolve(moduleName);
  if (require.cached[id]) {
    return require.cached[id].exports;
  }

  // 모듈 메타데이터
  const module = {
    exports: {},
    id,
  };

  // 캐시 업데이트
  required.cache[id] = module;

  // 모듈 로드
  loadModule(id, module, require);

  // 익스포트되는 변수반환
  return module.exports;
}
```

#### 모듈 정의

```js
// 또 다른 종속성 로드
const dependency = require("./anotherModule");

// private 함수
function log() {
  console.log(`Well done ${dependency.username}`);
}

// 공개적으로 사용되기 위해 익스포트되는 API

module.exports.run = () => {
  log();
};
```

### 모듈 정의 패턴

- 함수 내보내기

```js
module.exports = (message) => {
  console.log(`info: ${message}`);
};
module.exports.verbose = (message) => {
  console.log(`verbose: ${message}`);
};
```

- 클래스 내보내기

```js
class Logger {
  constructor(name) {
    this.name = name;
  }

  info(message) {
    console.log(`info: ${message}`);
  }

  verbose(message) {
    console.log(`verbose: ${message}`);
  }
}

module.exports = Logger;
```

- 인스턴스 내보내기

```js
class Logger {
  constructor(name) {
    this.count = 0;
    this.name = name;
  }
  log(message) {
    this.count++;
    console.log(`[${this.name}] ${message}`);
  }
}

module.exports = new Logger("DEFAULT");
```
