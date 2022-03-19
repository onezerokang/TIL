# Class

클래스란 객체의 청사진이다. 클래스를 이용하여 같은 구조를 갖는 객체(instance)를 생성할 수 있다

## 기본 Class 만들기

클래스를 만드는 법은 `class`키워드를 사용하고 클래스 이름을 붙여주면 된다. 여기서 클래스 이름은 다른 변수와 구별하기 위해 첫 글자를 대문자로 작성한다.
`constructor(생성자)`는 객체 내부의 프로퍼티를 정의하는데 사용되는데 이때 `this`는 클래스에 의해 생성된 인스턴스를 참조한다.

```ts
class Person {
  name: string;
  age: number;
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}
```

타입스크립트의 Class와 자바스크립트의 Class의 차이점 중 하나는, TS 같은 경우 프로퍼티의 이름과 타입을 미리 지정해주어야 한다는 것이다.
이제 class로 객체를 만들어보겠다.

```ts
class Person {
  name: string;
  age: number;
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}

const sumin = new Person("sumin", 24);
/*
Person: {
  name: "sumin",
  age: 24
}
*/
```

클래스로 객체를 만들 때는 `new`키워드를 사용하며 인자로 constructor에 들어갈 값을 넣어준다.

## 생성자 함수와 Class

사실 자바스크립틑 원래 클래스가 없었다.
원래 인스턴스를 만들 때 생성자 함수를 사용했었는데, Class 기반 프로그래머들이 사용하시 쉽도록 Class를 흉내낸 것이다(Syntax suger)
위에서 만든 class와 생성자 함수를 비교해보겠다.

```ts
class Person {
  name: string;
  age: number;
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}

function Person02(name, age) {
  this.name = name;
  this.age = age;
}

const sumin = new Person("sumin", 24);
const minsu = new Person02("minsu", 27);
```

## Access Modifier

Access Modifier(접근 제어자)는 클래스의 프로퍼티나 메서드에 접근 범위를 지정하는 키워드다.
접근 제어자에는 `public`, `protected`, `private`이 있다.

|               | Public    | Protected   | Private     |
| ------------- | --------- | ----------- | ----------- |
| class 내부    | 접근 가능 | 접근 가능   | 접근 가능   |
| 상속된 클래스 | 접근 가능 | 접근 가능   | 접근 불가능 |
| 인스턴스      | 접근 가능 | 접근 불가능 | 접근 불가능 |
| class 외부    | 접근 가능 | 접근 불가능 | 접근 불가능 |

public:

protected:

private:

## Shorthand

기본 클래스 만들기에서 이야기 했던 것처럼 타입스크립트에서 클래스의 프로퍼티를 지정할때는 constructor 밖에 프로퍼티 이름, 타입, 접근 제어자를 지정해줘야 한다.
그런데 클래스에 들어가는 데이터가 많을 경우 클래스가 너무 길어지고 가독성이 감소할 수 있다.
그래서 TS에서는 줄이는 법이 있다. 바로 Access Modifier와 타입을 constructor에 지정해주는 것이다.

**단축 하기 전**

```ts
class Person {
  private name: string;
  public age: number;
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}
```

**단축 한 후**

```ts
class Person {
  constructor(private name: string, public age: number) {}
}
```

위 코드를 보면 알겠지만 단축 문법을 사용하면 constructor안에 this.name = name 같이 프로퍼티를 직접 지정해주지 않아도 된다.

## readOnly properties

TS의 Class에는 `readonly`라는 키워드가 있는데, 속성을 읽는 용도로만 사용가능하고, 수정할 수 없게 하는 키워드다.

## Inheritance(상속)

상속이란...

```ts
class Person {
  constructor(private name: string, public age: number) {}
}

// 여기도 약식으로 써야 하나.?
class Male extends Person {
  constructor(
    private name: string,
    public age: number,
    protected exSoldier: boolean
  ) {
    super(name, age);
  }
}

const minho = new Male("minho", 17, false);
```

상속을 할 때는 `extends`키워드를 사용한다.
그리고 속성을 상속하기 위해서 constructor 안에 `super()`함수를 호출해야 하는데, 이는 상위 클래스의 constructor를 의미한다.
만약 추가 프로퍼티를 선언하고 싶다면 반드시 super()를 호출한 후에 선언해야 한다.

_참고: super는 superset의 약자로 추정된다._

## Overriding

클래스를 상속하면 메서드도 같이 상속 받게 되는데 이 때 이 메서드의 기능을 새로 변경하고 싶을 수 있습니다.
이것을 `Override`라고 합니다. 방법은 해당 메서드를 재선언하면 상위 클래스의 메서드를 덮어쓰게 됩니다.

```ts
class Person {
  constructor(private name: string, public age: number) {}
  printMyInfo() {
    console.log(`name: ${this.name}, age: ${this.age}`);
  }
}

// 여기도 약식으로 써야 하나.?
class Male extends Person {
  constructor(
    private name: string,
    public age: number,
    protected exSoldier: boolean
  ) {
    super(name, age);
  }
  printMyInfo() {
    console.log(
      `name: ${this.name}, age: ${this.age}, exSoldier: ${this.exSoldier}`
    );
  }
}

const mino = new Male("mino", 29, false);
mino.printMyInfo();
```

## Getter & Setter

## Static Method & Properties(정적 메서드 & 정적 프로퍼티)

`static` 키워드를 사용하면 인스턴스에서는 사용할 수 없는 정적 메서드와, 정적 프로퍼티를 만들 수 있습니다.
이는 Class 자체에 접근하여 메서드와 프로퍼티를 사용하게 하고, 데이터와 함수를 그룹화 하는 용도로 사용합니다.

**예시**

```ts
Math.PI;
Math.random();
```

위 예시는 Math 클래스에서 PI라는 정적 프로퍼티와 random이라는 정적 메서드를 사용하는 모습입니다.
Math 클래스에 직접 접근해야 하기 때문에 Math 인스턴스를 만들 필요가 없습니다. 만드는 방법은 다음과 같습니다.

**작석중**

```ts
class Person {
  constructor(private name: string, public age: number) {}
  printMyInfo() {
    console.log(`name: ${this.name}, age: ${this.age}`);
  }
}
```

## Abstract Class

Abstract Class는 추상 클래스로, 인스턴스를 만드는 용도가 아닌 클래스를 확장하는 용도로 사용하는 클래스입니다.

## Singleton & Private Constructors

싱글톤은 단 한개의 인스턴스만을 생성하는 패턴입니다. 이를 Private Constructor를 사용해서 만들 수 있습니다.

## Summary

| 키워드                           | 설명 |
| -------------------------------- | ---- |
| Class                            |      |
| Access Modifier                  |      |
| readonly                         |      |
| Inheritance                      |      |
| Overriding                       |      |
| Getter & Setter                  |      |
| Static                           |      |
| Abstract                         |      |
| Singleton & Private Constructors |      |

> 출처
> https://www.udemy.com/course/understanding-typescript
