# 타입 별칭

타입 별칭은 특정 타입이나 인터페이스를 참조할 수 있는 '타입 변수'이다.

```ts
type User = {
  name: string;
  age: number;
};

const user: User = { name: "minzi", age: 21 };
```

타입 별칭은 제네릭을 사용할 수 있다.

```ts
type User<T> = {
  name: T;
};
```

타입별칭은 새로운 타입을 생성하는 것이 아닌 정의한 타입을 쉽게 참고할 수 있게 이름을 부여하는 것과 같다.

## type vs interface

타입 별칭과 인터페이스의 차이는 확장여부다. 인터페이스는 확장이 가능하지만 타입 별칭은 확장이 불가능하다.
좋은 소프트웨어는 확장이 용이해야 한다는 원칙에 따라 타입별칭보다는 인터페이스를 사용하는 것이 좋다.

## 참조

> https://joshua1988.github.io/ts/guide/type-alias.html
