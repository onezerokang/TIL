# Jest

jest는 페이스북에서 개발한 테스팅 프레임워크로 테스팅에 필요한 툴들을 대부분 갖고 있어 편리하게 사용할 수 있다.

```
npm i jest -D
```

jest를 설치한 후에는 package.json에 test 스크립트를 작성하여 jest로 테스트를 할 수 있도록 한다.

```json
{
  "name": "",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "nodemon index.js",
    "test": "jest"
  }
}
```

이제 테스트 코드를 작성할 파일을 만들어야 하는데, 테스트 파일은 파일명과 확장자 사이에 test나 spec을 넣으면 jest가 테스트 파일로 인식한다.

> 예시: users.test.js, users.spec.js

아래는 jest 사용법을 익히기 위한 간단한 테스트 코드다.

```js
describe("계산", () => {
  it("1 + 1은 2입니다.", () => {
    expect(1 + 1).toEqual(2);
  });
  test("2 + 2는 4입니다.", () => {
    expect(2 + 2).toEqual(5);
  });
});
```

- `describe`
  - 테스트 케이스를 그룹화하는 함수다.
- `it`, `test`
  - 첫번 째 인자에 테스트에 대한 설명을 적고, 두번쨰 인자로 테스트 내용을 적는다. it과 test 둘다 같읕 기능이며 코드 컨벤션에 따라 선택해 사용하면 된다.
- `expect`
  - 값을 테스트할 때 사용한다. expect는 혼자 사용되기보다는 toEqual 같은 Matcher와 함께 사용되어 다양한 항목의 유효성을 검사할 수 있다.
- `Matcher`
  - expect와 함께 사용된다. 위 예시에서는 toEqual()이 Matcher인데 expect에 넘겨진 코드가 테스트를 통과하기 위한 조건을 설정할 때 사용한다.

테스트 코드를 작성한 후 `npm run test`를 실행하면 테스트가 실행된다. 테스트의 결과는 console로 확인할 수 있다. 위 예시코드에서 첫번째 테스트는 통과하지만, 두번째 테스트는 실패하게 된다.

## Matchers

Jest는 matcher를 사용하여 다양한 방식으로 값을 테스트할 수 있다. 자주 사용되는 matcher는 다음과 같다.

### toEqual(value)

객체가 일치한지 검증한다.

```js
const { getProduct } = require("product");

test("return a product object", () => {
  expect(getProduct(1)).toEqual({ id: 1, name: "mac" });
});
```

### toBe(value)

단순히 값을 비교한다.

```js
expect(2 + 2).toBe(4);
```

### toBeDefined()

값이 undefined가 아닌지 테스트한다.

```js
test("", () => {
  expect(undefined).toBeDefined();
});
```

### toBeTruthy() toBeFalsy()

검증하려는 값이 참 같은 값인지, 거짓같은 값인지 테스트한다.

```js
expect("").toBeFalsy();
expect(123).toBeTruthy();
```

### toHaveBeenCalled()

alias: `toBeCalled()`  
특정 인자와 함께 모킹 함수가 호출되었는지 테스트한다.

```js
function drinkAll(callback, flavour) {
  if (flavour !== "octopus") {
    callback(flavour);
  }
}

describe("drinkAll", () => {
  test("drinks something lemon-flavoured", () => {
    const drink = jest.fn();
    drinkAll(drink, "lemon");
    expect(drink).toHaveBeenCalled();
  });

  test("does not drink something octopus-flavoured", () => {
    const drink = jest.fn();
    drinkAll(drink, "octopus");
    expect(drink).not.toHaveBeenCalled();
  });
});
```

### toHaveLength(number)

배열이나 문자열의 `.length`를 체크한다.

```js
expect([1, 2, 3]).toHaveLength(3);
expect("abc").toHaveLength(3);
expect("").not.toHaveLength(5);
```

### toContain(item)

배열의 인자로 넘긴 값이 존재하는지 체크할 때 사용한다.
물론 문자열에도 사용할 수 있다.

```js
test("the flavor list contains lime", () => {
  expect(getAllFlavors()).toContain("lime");
});
```

### toMatch(regexp | string)

정규식 기반의 테스트가 필요할 때 사용한다.

### toThrow()

예외 발생 여부를 테스트할 때 사용한다. `toThrow()` 함수는 인자도 받는데, 문자열을 넘기면 예외 메시지를 비교하고 정규식을 넘기면 정규식 체크를 해준다.

```js
function compileAndroidCode() {
  throw new Error("you are using the wrong JDK");
}

test("compiling android goes as expected", () => {
  expect(() => compileAndroidCode()).toThrow();
  expect(() => compileAndroidCode()).toThrow(Error);

  // You can also use the exact error message or a regexp
  expect(() => compileAndroidCode()).toThrow("you are using the wrong JDK");
  expect(() => compileAndroidCode()).toThrow(/JDK/);
});
```

주의할 점은 `toThrow()` 함수를 사용할 때 반드시 `expect()` 함수에 넘기는 검증 대산을 함수로 한번 감싸줘야 한다. 그렇지 않으면 예외 발생 여부를 체크하는 것이 아니라, 테스트 실행 도중 정말 그 예외가 발생하기 때문에 그 테스트는 항상 실패하게 되기 때문이다.

### toHaveProperty(keyPath, value?)

객체에 해당 key: value 값이 있는지 검사한다.

```js
test("find product property", () => {
  const product = {
    id: 1,
    name: "iphone",
  };
  expect(product).toHaveProperty(id, 1);
});
```

### toBeCalledTimes() / toBeCalledWith()

`toBeCalledTimes()`: 함수가 몇번 호출되었는지 검증

`toBeCalledWith()`: 함수가 설정한 인자로 호출되었는지 검증

```js
const printHi = (name) => console.log("Hi" + name);

printHi("Suzi");

expect(printHi).toBeCalledTimes(1);
expect(printHi).toBeCalledWith("Suzi");
```

### toReturn(), toHaveReturnedTimes()

함수가 오류없이 반환되는지 테스트

```js
test("drinks returns", () => {
  const drink = jest.fn(() => true);

  drink();

  expect(drink).toHaveReturned();
});
```

### toReturnTimes(), toHaveReturnedTimes()

함수가 지정한 횟수만큼 오류없이 반환되는지 테스트하는데 호출 횟수는 포함하지 않는다.

```js
test("drink returns twice", () => {
  const drink = jest.fn(() => true);

  drink();
  drink();

  expect(drink).toHaveReturnedTimes(2);
});
```

### toReturnWith(), toHaveReturnedWith(value)

함수가 지정한 값을 반환하는지 테스트

```js
test("drink returns La Croix", () => {
  const beverage = { name: "La Croix" };
  const drink = jest.fn((beverage) => beverage.name);

  drink(beverage);

  expect(drink).toHaveReturnedWith("La Croix");
});
```

## Mocking

단위 테스트를 짤 때는 테스트 할 함수가 다른 기능에 의존하지 않도록 해야한다. 테스트 하려고 한 함수의 문제가 아닌 의존하고 있는 기능의 문제로 인해 테스트가 실패할 수 있기 때문이다.

떄문에 의존하고 있는 객체나 함수를 가짜로 만들고 사용하여 정확한 테스트가 되도록 해야 한다. 이렇게 가짜 객체, 가짜 함수를 넣는 행위를 mocking이라고 한다.

### jest.fn()

함수를 모킹할 때는 `jest.fn()`을 사용한다. 반환 값을 지정해주고 싶다면 `jest(() => 반환값)`을 사용한다.

#### .mockReturnValue(value)

함수가 반환할 값을 지정해줄 수 있다.

```js
const mockFunc = jest.fn();

mockFunc(); // undefined

mockFunc.mockReturnValue("헤헤");
mockFunc(); // "헤헤"
```

#### .mockImplemetation(value)

모크 함수는 기본적으로 아무런 동작도 리턴도 하지 않는다. `.mockImplemetation()`을 사용하면 동작하는 모크함수를 구현할 수 있다.

```js
const printName = jest.fn();

printName.mockImplemetation((name) => console.log(name));

printName("Suzi");
```

#### . mockResolvedValue(value) / .mockRejectedValue(value)

비동기 함수에서 resolve / reject 값을 받는다.

```js
test("async resolve test", async () => {
  const asyncMock = jest.fn().mockResolvedValue(43);

  await asyncMock(); // 43
});

test("async reject test", async () => {
  const asyncMock = jest.fn().mockRejectedValue(new Error("Async error"));

  await asyncMock(); // throws "Async error"
});
```

모크함수는 자신이 어떻게 호출되었는지를 모두 기억한다.

```js
test("mock Test", () => {
  const mockFn = jest.fn();
  mockFn.mockImplementation((name) => `I am ${name}`);

  mockFn("a");
  mockFn(["b", "c"]);

  expect(mockFn).toBeCalledTimes(2); // 몇번 호출? -> 2번
  expect(mockFn).toBeCalledWith("a"); // a로 호출? -> true
  expect(mockFn).toBeCalledWith(["b", "c"]); // 배열로 호출? -> true
});
```

_jest.fn()_ 만 공부하자

### 예제

## 참조

> [Jest 공식문서](https://jestjs.io/)  
> [Node.js 교과서 11장 - 노드 서비스 테스트하기](http://www.yes24.com/Product/Goods/91213376)  
> [[JEST] 📚 Matcher 함수 종류 정리](https://inpa.tistory.com/entry/JEST-%F0%9F%93%9A-jest-%EA%B8%B0%EB%B3%B8-%EB%AC%B8%EB%B2%95-%EC%A0%95%EB%A6%AC?category=914656)  
> [[JEST] 📚 모킹 Mocking 정리 (jest.fn / jest.mock /jest.spyOn)
> ](https://inpa.tistory.com/entry/JEST-%F0%9F%93%9A-%EB%AA%A8%ED%82%B9-mocking-jestfn-jestspyOn?category=914656)
