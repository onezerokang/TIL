# 타입스크립트란?

2012년 마이크로소프트가 발표한 타입스크립트는 자바스크립트에 정적 타입 문법을 추가한 언어다.
타입스크립트를 브라우저에서 실행하기 위해 자바스크립트 파일로 변환하는 과정이 필요한데 이를 컴파일(compile)이라 한다.

## 타입스크립트의 장점

### 높은 수준의 코드 탐색과 디버깅

타입스크립트는 코드에 목적을 명시하고 목적에 맞지 않는 타입의 변수나 함수들에서 에러를 발생시켜 버그를 사전에 제거한다.
또한 코드 자동완성이나 실행전 피드백을 제공하여 작업과 동시에 디버깅이 가능해 생산성을 높일 수 있다.
이는 기존 자바스크립트의 경우 런타임에서만 버그를 확인할 수 있었던 것에 비해 가장 큰 장점이라 할 수 있다.

### 강력한 생태계

대부분의 라이브러리들이 타입스크립트를 지원하며 마이크로소프트의 VSCode를 비롯해 각종 에디터가 타입스크립트 관련 기능과 플러그인을 지원한다.

## 기본 타입

타입스크립트에는 변수나 함수에 타입을 정의할 수 있다. 타입스크립트의 기본 타입은 다음과 같다.

- String
- Number
- Boolean
- Object
- Array
- Tuple
- Enum
- Any
- Void
- Null
- Undefined
- Never

### 변수에 타입설정

```ts
const str: string = "타입스크립트는 정말 최고야!";
const num: number = 1004;
const bool: boolean = false;

const obj1: object = {};
const obj2: { name: string; age: number } = {
  name: "홍길동",
  age: 31,
};

const arr1: Array = [1, 2, 3];
const arr2: number[] = [1, 2, 3];
const arr3: Array<number> = [1, 2, 3];
const arr4: { name: string; age: number }[] = [
  { name: "홍길동", age: 31 },
  { name: "수지", age: 20 },
];
```

### 함수에 타입설정

```ts
const sum = (a: number, b: number): number => a + b;

// 옵셔널 파라미터
const log = (a: string, b?: string, c?: string): void => console.log(a);
```

### Tuple

튜플을 사용하면 배열의 길이를 고정하고 각 인덱스에 대응하는 타입을 정의할 수 있다.

```ts
const tuple: [number, string] = [2022, "년"];
```

### Enum

<!-- 이넘을 어떨 때 사용하는지까지 설명 보충하고 commit 하면 될 듯 -->

이넘은 특정 값(상수)들의 집합을 의미한다.

```ts
enum UserType {
  Normal,
  Admin,
}

const user: { name: string; type: UserType } = {
  name: "상혁",
  type: UserType.Admin,
};
```

이넘은 인덱스 번호로 접근할 수도 있다.

```ts
enum UserType {
  Normal,
  Admin,
}

const user: { name: string; type: UserType } = {
  name: "상혁",
  type: UserType[1],
};
```

원한다면 이넘의 인덱스를 변경하여 사용할 수도 있다.

```ts
enum UserType {
  Normal = 2,
  Admin,
}

const user: { name: string; type: UserType } = {
  name: "상혁",
  type: UserType[3],
};
```

### Any

Any는 어떤 타입이라도 허용하는 타입이다.
Any를 자주 사용할 경우 타입스크립트를 사용하는 의미가 없어 가급적 사용하지 않는 것이 좋다.
일반적으로 자바스크립트로 짜여진 코드를 점진적으로 타입스크립트로 변환해갈 때 활용하면 좋은 타입이다.

```ts
const sum = (a: any, b: any): any => a + b;
```

### Void

변수에는 `null`과 `undefined`만 할당하고, 함수에는 반환 값을 설정할 수 없는 타입이다.

```ts
const macGuffin: void = null;

const logName = (name: string): void => console.log(name);
```

### Never

함수의 끝에 절대 도달하지 않는다는 의미를 지닌 타입이다.

```ts
function neverEnd(): never {
  while (true) {}
}
```

_의문점: never 타입은 왜 필요하고 언제 사용할까?_

## 참조

> https://joshua1988.github.io/ts/guide/basic-types.html  
> https://www.udemy.com/course/understanding-typescript  
> https://www.samsungsds.com/kr/insights/typescript.html  
> https://yozm.wishket.com/magazine/detail/1376
