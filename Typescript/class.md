# Class

클래스란 객체의 청사진이다. 클래스를 이용하여 같은 구조를 갖는 객체(instance)를 생성할 수 있다
다만 JS, TS에서 클래스는 사실 함수이고 기존 프로토타입의 문법적 설탕일 뿐이다.

## 기본 Class 만들기

먼저 자바스크립트로 클래스를 정의해보겠다.
클래스를 만드는 법은 `class`키워드를 사용하고 클래스 이름을 붙여주면 된다. 여기서 클래스 이름은 다른 변수와 구별하기 위해 첫 글자를 대문자로 작성한다.
`constructor(생성자)`는 인스턴스가 만들어질 때 실행되는데 주로 클래스의 프로퍼티를 선언하는데 사용한다. 이때 `this`는 클래스에 의해 생성된 인스턴스를 참조한다.

```js
class Person {
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}
```

자바스크립트의 클래스는 클래스 몸체에 클래스 프로퍼티를 선언할 수 없고 생성자 내부에서 클래스 프로퍼티를 선언하고 초기화 해야 한다.
하지만 타입스크립트 클래스는 클래스 몸체에 프로퍼티를 사전 선언해야 한다.

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
sumin.sleep();
```

클래스로 객체를 만들 때는 `new`키워드를 사용하며 인자로 constructor 매개변수에에 들어갈 값을 넣어준다.

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

## Access Modifier(점근 제어자 혹은 접근 제한자)

Access Modifier(접근 제어자)는 클래스의 프로퍼티나 메서드에 접근 범위를 지정하는 키워드다.
접근 제어자에는 `public`, `protected`, `private`이 있으며 접근제한자를 명시하지 않았을 때는 암묵적으로 public이 선언된다.

| 접근가능성       | Public | Protected | Private |
| ---------------- | ------ | --------- | ------- |
| 클래스 내부      | O      | O         | O       |
| 자식 클래스 내부 | O      | O         | X       |
| 클래스 인스턴스  | O      | X         | X       |
| 클래스 외부      | O      | X         | X       |

```ts
class Person {
  public name: string;
  protected age: number;
  private married: boolean;

  constructor(name: string, age: number, married: boolean) {
    this.name = name;
    this.age = age;
    this.married = married;
  }
}

const eunjae = new Person("enujae", 26, true);

console.log(eunjae.name); // public 접근 제어자는 인스턴스를 통해 외부에서 참조 가능하다.
console.log(eunjae.age); // protected 접근 제어자는 인스턴스를 통해 외부에서 참조할 수 없다.
console.lg(eunjae.married); // private 접근 제어자는 인스턴스를 통해 외부에서 참조할 수 없다.

class Male extends Person {
  constructor(name: string, age: number, married: boolean) {
    super(name, age, married);

    console.log(this.name); // 접근 가능
    console.log(this.name); //접근 가능
    console.log(this.name); // 접근 불가
  }
}
```

_참고: Access Modifier는 메서드에도 사용할 수 있다._

## Shorthand

접근 제어자는 생성자(constructor) 파라미터에도 선언할 수 있다. 이때 접근 제한자가 사용된 생성자 파라미터는 암묵적으로 클래스 프로퍼티로 선언되고
생성자 내부에서 별도의 초기화가 없어도 암묵적으로 초기화가 수행된다. 이를 통해 코드의 길이를 줄일 수 있다.

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

만약 생성자 파라미터에 접근 제어자를 선언하지 않으면 생성자 파라미터는 생성자 내부에서만 유효한 지역 변수가 되어 생성자 외부에서 참조가 불가능하게 된다.

```ts
class Person {
  constructor(name: string, public age: number) {
    // 이렇게 하지 않으면 name을 지역변수로 인식하기 때문에 unused error가 발생한다.
    console.log(name);
  }
}

const me = new Person("me", 22);
// name 프로퍼티가 선언되지 않은 것을 확인 할 수 있다.
/*
  Person {
    age: 22
  }
*/
```

## readonly

TS의 Class에는 `readonly`라는 키워드가 있는데, 생성자 내부에서만 값을 할당할 수 있게 한다.
그 외의 경우는 값을 할당할 수 없고 오직 읽기만 가능한 상태가 된다. 이를 이용하여 **상수**의 선언에 사용한다.

```ts
class Person {
  private readonly id: string = "123";
  private readonly socialSecurityNumber: string;

  constructor() {
    this.socialSecurityNumber = "9103171234567";
  }

  printInfo() {
    this.id = "212"; //error
    this.socialSecurityNumber = "1234561234567"; //error

    console.log(this.id);
    console.log(this.socialSecurityNumber);
  }
}
```

## Inheritance(상속)

상속이란 기존의 클래스에 기능을 추가하거나 재정의 하여 새로운 클래스를 정의하는 것을 의미한다.
타입스크립트에서 서브 클래스를 만들기 위해서는 `extends`(확장하다) 키워드를 사용한다.

```ts
class Person {
  constructor(public name: string, public age: number) {}
}

class Male extends Person {
  // name과 age는 상속받아 사용하기 때문에 생성자 파라미터에 접근 제어자를 입력하지 않아도 된다.
  constructor(name: string, age: number, protected exSoldier: boolean) {
    super(name, age);
    this.exSoldier = exSoldier;
  }
}

const minho = new Male("minho", 17, false);
```

그리고 속성을 상속하기 위해서 constructor 안에 `super()`함수를 호출해야 하는데, 이는 상위 클래스의 constructor를 의미한다.
만약 추가 프로퍼티를 선언하고 싶다면 반드시 super()를 호출한 후에 선언해야 한다.

_참고: super는 상위 클래스를 super class의 약자로 추정된다._

## Overriding

클래스를 상속하면 메서드도 같이 상속 받게 되는데 이 때 이 메서드의 기능을 재정의하고 싶을 수 있다.
이것을 `Override`라고 한다. 방법은 재 정의 하고 싶은 메서드를 서브 클래스에서 재 정의하면 상위 클래스의 메서드를 덮어쓰게 된다.

```ts
class Person {
  constructor(public name: string, public age: number) {}
  printMyInfo() {
    console.log(`name: ${this.name}, age: ${this.age}`);
  }
}

class Male extends Person {
  constructor(name: string, age: number, protected exSoldier: boolean) {
    super(name, age);
    this.exSoldier = exSoldier;
  }
  // Override한 모습
  printMyInfo() {
    console.log(
      `name: ${this.name}, age: ${this.age}, exSoldier: ${this.exSoldier}`
    );
  }
}

const mino = new Male("mino", 29, false);
mino.printMyInfo();
```

_상기: private한 속성과 메서드는 서브 클래스에서 사용할 수 없습니다._

## Getter & Setter

비공개로 설정할 필요가 있는 속성을 private로 설정했을 때 Getter, Setter 함수를 사용하여 해당 속성에 접근할 수 있는 속성을 정의할 수 있다.

```ts
class Person {
  constructor(private _id: string) {}

  get id(): string {
    return this._id;
  }

  set id(newId: string) {
    if (newId) {
      this._id = newId;
    }
  }
}

const kim = new Person("아이뒤");
console.log(kim._id); //error
kim.id = "123";
console.log(kim.id); //123
```

## Static Method & Properties(정적 메서드 & 정적 프로퍼티)

`static` 키워드를 사용하면 인스턴스에서는 사용할 수 없는 정적 메서드와, 정적 프로퍼티를 만들 수 있다.
이는 Class 자체에 접근하여 메서드와 프로퍼티를 사용하게 하고, 데이터와 함수를 그룹화 하는 용도로 사용한다.
**정적 메서드 안에서 this는 인스턴스가 아닌 클래스 자신을 참조한다.**

**예시**

```ts
Math.PI;
Math.random();
```

위 예시는 Math 클래스에서 PI라는 정적 프로퍼티와 random이라는 정적 메서드를 사용하는 모습이다.
Math 클래스에 직접 접근해야 하기 때문에 Math 인스턴스를 만들 필요가 없습니다. 만드는 방법은 다음과 같다.

```ts
class Person {
  static instanceCounter = 0;
  constructor(private name: string, public age: number) {
    Person.instanceCounter++;
  }
  static countInstances() {
    console.log(this.instanceCounter);
    // 혹은
    console.log(Person.instanceCounter);
  }
}

const mino = new Person("mino", 23);
const eunjae = new Person("eunjae", 21);

Person.countInstances();

mino.countInstances(); //에러
```

## Abstract Class

Abstract Class는 추상 클래스로, 직접 인스턴스를 생성할 수 없고 상속만을 위해 사용된다.
추상 클래스는 하나 이상의 추상 메서드를 포함하여 일반 메서드도 포함할 수 있다.
추상 메서드는 내용이 없이 메서드 이름과 타입만이 선언된 메서드를 말하며 선언할 때 abstract 키워드를 사용한다.

```ts
abstract class Person {
  abstract sleep(): void;
  move(): void {
    console.log("Moving...");
  }
}

const me = new Person(); //에러

class Female extends Person {
  // 추상 클래스를 상속한 클래스 추상 클래스의 추상 메서드를 반드시 구현하여야 한다.
  sleep() {
    console.log("Sleeping...");
  }
}

const eunha = new Person();
eunha.sleep();
eunha.move();
```

인터페이스는 모든 메서드가 추상 메서드이지만 추상 클래스는 하나 이상의 추상 메서드와 일반 메서드를 포함할 수 있다.

## Singleton & Private Constructors

private 접근 제어자을 constructor()앞에 붙이면 new 키워드를 통해 인스턴스를 생성하지 못하게 제한이 가능하다.
대신 공개된 getInstance()를 통해 **오직 단 한번만 인스턴스를 생성**할 수 있다. 이를 싱글턴 패턴이라 한다.

```ts
class OnlyOne {
  private static instance: OnlyOne;

  private constructor(public name: string) {}

  public static getInstance() {
    if (!OnlyOne.instance) {
      OnlyOne.instance = new OnlyOne("싱글턴 객체");
    }
    return OnlyOne.instance;
  }
}
```

## Summary

| 키워드                           | 설명                                                                                                                                                                                  |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Class                            | 객체를 만드는 청사진                                                                                                                                                                  |
| Access Modifier                  | 프로퍼티나 메서드의 접근 범위를 지정하는 키워드                                                                                                                                       |
| readonly                         | constructor 안에서만 값이 할당된다. 그 외는 읽는 것밖에 안되도록 하는 키워드                                                                                                          |
| Inheritance                      | 기존 클래스에서 속성이나 메서드를 추가하여 새로운 서브 클래스를 만드는 행동                                                                                                           |
| Overriding                       | 슈퍼 클래스의 메서드를서 서브 클래스에서 재 정의 하는 것                                                                                                                              |
| Getter & Setter                  | private 속성을 접근하고 수정할 수 있도록 하는 함수                                                                                                                                    |
| Static                           | 클래스에서만 사용할 수 있는 프로퍼티나 메서드를 만드는 키워드.                                                                                                                        |
| Abstract                         | 인스턴스를 만들 수 없고 오로지 상속만 할 수 있는 추상 클래스를 만드는 키워드. 하나 이상의 추상 메서드를 포함하고 있어야 하며, 서브 클래스에서는 추상 메서드를 반드시 구현하여야 한다. |
| Singleton & Private Constructors | new 키워드로 인스턴스를 생성할 수 없고 단 한개의 인스턴스만을 갖게 하는 패턴을 싱글턴 패턴이라하고, 이를 private constructor로 만들 수 있다.                                          |

> 출처
> https://www.udemy.com/course/understanding-typescript > https://poiemaweb.com/typescript-class > http://www.tcpschool.com/java/java_inheritance_concept > https://yamoo9.gitbook.io/typescript/classes/getter-setter > https://yamoo9.gitbook.io/typescript/classes/singleton
