# 인터페이스

인터페이스는 타입을 정의한 규칙을 의미한다. 인터페이스는 보통 다음과 같은 범주에 대해 타입을 정의할 수 있다.

- 객체의 스펙
- 함수의 파라미터
- 함수의 스펙(파라미터, 반환 타입)
- 배열과 객체에 접근하는 방식
- 클래스

특히 클래스가 특정 메서드나, 프로퍼티를 갖게 하여 객체의 구조를 정의할 수 있는데 이를 통해 일관된 프로그래밍이 가능하다.
인터페이스가 클래스와 비슷하다고 느낄 수 있는데 인터페이스는 인스턴스를 생성할 수 없고 클래스와 객체의 타입을 정의하는 용도로만 사용된다.

## 변수와 함수에 활용한 인터페이스

```ts
interface User {
  name: string;
  age: number;
}

const person: User = {
  name: "수지",
  age: 21,
  // 인터페이스에 정의된 속성, 타입의 조건만 만족한다면 객체의 속성 수가 더 많아도 문제 없다.
  isAdmin: false,
};

const getUser = (user: User): User => {
  return user;
};
```

## 옵션 속성

옵션 속성을 사용하면 인터페이스에 정의된 속성과 타입을 모두 구현하지 않아도 된다.

```ts
interface Car {
  name: string;
  releaseDate?: Date;
}

const cyberTruck: Car = {
  name: "테슬라 사이버트럭",
};
```

## 읽기 전용 속성

읽기 전용 속성은 인터페이스로 처음 객체를 생성할 때만 값을 할당하고, 그 이후에는 변경할 수 없는 속성이다.

```ts
interface Car {
  readonly name: string;
  releaseDate?: Date;
}

const cyberTruck: Car = {
  name: "테슬라 사이버트럭",
};

cyberTruck.name = "싸이버트럭"; // Error
```

## 읽기 전용 배열

`ReadonlyArray<T>` 타입을 사용하면 읽기 전용 배열을 생성할 수 있다.

```ts
const arr: ReadOnlyArray<string> = ["ㄱ", "ㄴ", "ㄷ"];

arr.push("ㄹ"); // Error
arr.splice(0, 1); // Error
```

## 객체 선언과 관련된 타입 체킹

## 함수 타입

인터페이스는 함수의 타입을 정의할 때도 사용할 수 있다.

```ts
interface Login {
  (email: string, password: string): boolean;
}

let loginUser: Login;
loginUser = (email: string, password: string) => true;
```

## 클래스 타입

자바나 C#처럼 타입스크립트도 클래스가 일정 조건을 만족하도록 타입 규칙을 정할 수 있다.

```ts
interface CraftBeer {
  beerName: string;
  nameBeer(beer: string): void;
}

class myBeer implements CraftBeer {
  beerName: string = "Baby Guinness";
  nameBeer(b: string) {
    this.beerName = b;
  }
  constructor() {}
}
```

## 인덱싱

```ts
interface StringArray {
  [index: number]: string;
}

const arr: StringArray = ["1번 마", "2번 마", "3번 마"];
arr[0] = 10; // Error
```

## 딕셔너리 패턴

```ts
interface StringRegexDictionary {
  [key: string]: RegExp;
}

const obj: StringRegexDictionary = {
  cssFile: /\.css$/,
  jsFile: "a", // Error
};

obj["cssFile"] = /\.css$/;
obj["jsFile"] = "a"; //Error
```

## 인터페이스 확장

```ts
interface User {
  name: string;
  age: number;
}

interface Developer extends User {
  langauge: string[];
}

const linus: Developer = {
  name: "리누스",
  age: 52,
  language: ["C", "Linux"],
};
```

## 참조

> https://www.udemy.com/course/understanding-typescript  
> https://poiemaweb.com/typescript-interface  
> https://www.samsungsds.com/kr/insights/typescript.html
