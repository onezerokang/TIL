# 함수

TS에서 함수는 매개변수의 타입과 반환 타입을 지정할 수 있다.

```ts
const sum = (num1: number, num2: number): number => num1 + num2;

sum(1, 2);
sum(1, "2"); // 에러 발생

// 값을 반환하지 않을 때는 void라도 사용한다.
const printResult = (text: string): void => console.log(text);
printResult("Up down func!");
```

## 인자

TS에서는 함수의 인자를 필수값으로 간주하고, 넘기지 않았을 경우 에러를 던진다.

```ts
const sum = (num1: number, num2: number): number => num1 + num2;

sum(1, 2); // 3
sum(1, 2, 3); //error, too many parameters
sum(10); //error, too few parameters
```

선택적으로 넘기고 싶은 매개변수(옵셔널 파라미터)가 있을 경우에는 `?`를 사용한다.

```ts
const sum = (num1: number, num2?: number): number => num1 + num2;

sum(1, 2); // 3
sum(1, 2, 3); //error, too many parameters
sum(10); //10
```

매개변수 초기화는 ES6문법과 동일하다.

```ts
const sum = (num1: number, num2 = 0): number => num1 + num2;
```

REST문법의 경우 다음과 같이 사용할 수 있다.(REST문법이란 여러 인자들을 하나의 배열로 반환하는 문법이다.)

```ts
const sum = (a: number, ...nums: number[]): number => {
  const totalOfNums = 0;

  for (let key in nums) {
    totalOfNums += nums[key];
  }
  return a + totalOfNums;
};

sum(1, 2, 3, 4, 5);
```

## 참조

> https://www.udemy.com/course/understanding-typescript  
> https://joshua1988.github.io/ts/guide/functions.html
