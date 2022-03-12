# 유니온 타입과 앨리어스(Union Type & Alias)

## Union Type

유니온 타입은 여러개의 타입을 지정할 경우 사용한다.

```ts
const combine = (input1: string | number, input2: string | number) => {
  let result;
  if (typeof input1 !== typeof input2) {
    result = input1 + input2;
  }
  console.log(result);
};

combine("Hello", " world!"); // "Hello world!"
combine(1, 2); //3
```

## Type Alias

타입 앨리어스는 사용자 지정 타입을 정의한다.

```ts
type Combinable = string | number;

const combine = (input1: Combinable, input2: Combinable) => {
  let result;
  if (typeof input1 !== typeof input2) {
    result = input1 + input2;
  }
  console.log(result);
};

combine("Hello", " world!"); // "Hello world!"
combine(1, 2); //3
```

타입 앨리어스로 타입을 정의할 때는 `|`(or)을 사용하며 정의된 타입의 첫글자는 대문자이다.
