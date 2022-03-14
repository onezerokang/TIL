# 이넘(Enum)

이넘은 특정 값들의 집합을 의미하는 자료형이다.

## 숫자형 이넘

```ts
enum Category {
  FOOD = 2,
  SHOES,
  PHONE,
}
```

숫자형 이넘 선언시 초기값을 주면 초기 값부터 차례대로 1씩 증가한다.(초기값을 주지 않았을 시에는 0부터 시작한다)

## 숫자형 이넘 사용하기

```ts
enum Response {
    No = 0;
    Yes = 1;
}

const respond = (recipient: string, message: Response): void => {
    // ...
}

response("hong Kill dong", Response.Yes)
```

## 문자형 이넘

문자형 이넘은 이넘 값 전부다 특정 문자 또는 다른 이넘 값으로 초기화 해줘야 한다.

```ts
enum Category {
  FOOD = "Food",
  SHOES = "Shoes",
  PHONE = "Phone",
}
```

## 복합 이넘(Heterogeneous Enums)

```ts
enum BooleanLikeHeterogeneousEnum {
  No = 0,
  Yes = "YES",
}
```

## 런타임 시점에서의 이넘 특징

이넘은 런타임시에 실제 객체 형태로 존재한다.

```ts
enum E {
  X,
  Y,
  Z,
}

function getX(obj: { X: number }) {
  return obj.X;
}
getX(E); // 이넘 E의 X는 숫자이기 때문에 정상 동작
```

## 컴파일 시점에서의 이넘 특징

이넘이 런타임 시점에서는 실제 객체지만 `keyof`를 사용할 때 주의해야 합니다. 일반적으로 `keyof`를 사용해야 되는 상황에서는 대신 `keyof typeof`를 사용하세요.

```ts
enum LogLevel {
  ERROR,
  WARN,
  INFO,
  DEBUG,
}

// 'ERROR' | 'WARN' | 'INFO' | 'DEBUG';
type LogLevelStrings = keyof typeof LogLevel;

function printImportant(key: LogLevelStrings, message: string) {
  const num = LogLevel[key];
  if (num <= LogLevel.WARN) {
    console.log("Log level key is: ", key);
    console.log("Log level value is: ", num);
    console.log("Log level message is: ", message);
  }
}
printImportant("ERROR", "This is a message");
```

## 리버스 매핑

리버스 매핑은 숫자형 이넘에만 존재한다. 이넘의 key로 value를 얻을 수 있고 value로 key를 얻을 수도 있다. 단 리버스 매핑은 문자형 이넘에는 존재하지 않는다.

```ts
enum Enum {
  A,
}
let a = Enum.a;
let keyName = Enum[a];
```

출처

> https://www.udemy.com/course/understanding-typescript/ > https://joshua1988.github.io/ts/guide/enums.html#%EC%BB%B4%ED%8C%8C%EC%9D%BC-%EC%8B%9C%EC%A0%90%EC%97%90%EC%84%9C%EC%9D%98-%EC%9D%B4%EB%84%98-%ED%8A%B9%EC%A7%95
