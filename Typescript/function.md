# 함수

함수에는 매개변수의 타입과 반환 타입을 지정할 수 있다.

```ts
const add = (num1: number, num2: number): number => num1 + num2;

add(1, 2);
add(1, "2"); //error
```
