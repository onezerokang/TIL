# 타입종류

타입스크립트의 타입종류는 다음과 같다

## 기본타입

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

## 기본적인 타입선언 방법

```ts
// :를 이용해서 타입읠 정의하는 방식을 타입표기(Type Annotation)이라 한다.
const name: string = "Minsu";
const age: number = 27;
const married: boolean = true;
```

## Object

### Array

```ts
const firends: String[] = ["Eunjae", "Homin", "Byeong-geon"];
//제네릭을 사용한 경우
const firends: Array<string> = ["Eunjae", "Homin", "Byeong-geon"];
```

### Tuple

튜플은 길이가 고정되고, 각 요소마다 타입이 정해져있는 배열이다.

```ts
const arr: [string, boolean] = ["Homin", true];

arr.push("haha"); // length가 2가 되어 에러 발생
arr[1] = 40; // 1번 요소에 boolean이 아닌 number를 할당할 경우 에러 발생
```

### Enum

상수들의 집합이다.

```ts
enum Category {
  FOOD,
  PHONE,
  CAR,
  // 이렇게 이넘의 인덱스를 변경할 수 있다.
  SHOES = 7,
}
const car = Category.FOOD;
const phone = Category[1];
```

### Any

Any는 어떤 타입이든 상관없는 타입이다. Any를 남발할 경우 TS를 사용하는 의미가 없기에 사용하지 않는 것이 좋다. 단, 기존 JS 코드를 점진적으로 TS코드로 변환할 때 사용하면 좋다.

```ts
let randomBox: any;
randomBox = "Coke";
randomBox = 10000;

const arr: Any[] = ["Coke", false];
```

### Void

Void는 변수에는 null과 undefined만 할당하고 함수는 반환값을 설정할 수 없다.

```ts
const macGuffin: void = null;

const printHello = (): void => console.log("Hello");
printHello(); //"Hello"
```

### Never

함수가 끝나지 않는다는 의미를 지닌 타입

```js
const neverEndingStory = (): never => {
  while (true) {
    console.log("더 이상은 Naver...");
  }
};

//혹은...

function generateError(message: string, code: number): never {
  throw { message: message, errorCode: code };
}
```

### Undefined

Undefined는 변수에 선언할 경우 undefined가 돼 버리고, 함수에 선언할 경우 명시적으로 undefined를 return 해주어야 한다.

```ts
const ud: undefined;

const getUndefined = (): undefined => {
  return undefined;
};
```

> 출처
> https://www.udemy.com/course/understanding-typescript/ >https://joshua1988.github.io/ts/guide/basic-types.html#string
