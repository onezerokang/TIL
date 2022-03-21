# Interface

인터페이스는 **타입체크를 위해 사용된다**.
인터페이스에 선언된 프로퍼티와 메서드의 구현을 강제하여 일관성을 유지할 수 있도록 한다.
또 클래스나 함수에 사용할 경우 내부 로직을 읽지 않더라도 '어떤 프로퍼티와 메서드가 있을 것이다'를 알 수 있다.

## 변수와 인터페이스

변수에 인터페이스를 사용할 경우, 변수는 인터페이스를 준수해야 한다.

```ts
interface Todo {
  id: number;
  content: string;
  completed: boolean;
}

let todo: Todo;

todo = { id: 1, content: "Study", completed: false };
```

또 인터페이스를 사용하여 함수 파라미터 선언을 할 수 있다.
이때 함수 파라미터는 인터페이스를 준수하는 인자를 전달해야 한다.
함수는 객체를 전달할 때 복잡한 매개변수 체크를 하지 않아도 되기에 매우 유용하다.

```ts
interface Todo {
  id: number;
  content: string;
  completed: boolean;
}

let todos: Todo[] = [];

const addTodo = (todo: Todo) => {
  todo = [...todos, todo];
};

const newTodo: Todo = { id: 1, content: "Study", completed: false };
addTodo(newTodo);
```

## 함수와 인터페이스

함수에 인터페이스를 사용할 경우 타입이 선언된 파라미터와 리턴 값을 정의해야 한다.

```ts
interface SquareFunc {
  (num: number): number;
}

const squareFunc: SquareFunc = (num: number) => {
  return num * num;
};
```

## 클래스와 인터페이스

클래스 선언문 뒤에 `implements`를 붙이고 인터페이스를 사용하면 해당 클래스는 지정된 인터페이스를 반드시 구현해야 한다.
이는 클래스의 일관성을 유지할 수 있는 장점을 갖는다. 인터페이스는 프로퍼티나 메서드를 가질 수 있다는 점에서 클래스와 유사하나
인스턴스를 생성할 수 없다. 그리고 인터페이스의 메서드는 반드시 추상메서드어야 한다.

```ts
interface ICar {
  carNum: number;
  name: string;
  used: boolean;
  move(): void;
}

class Car implements Icar {
  constructor(
    public carNum: number,
    public name: string,
    public used: boolean
  ) {}

  move() {
    console.log(`${this.name} is moving...`);
  }
}

const sm3 = new Car(1371, "sm3", true);
sm3.move();
```

## 덕 타이핑

인터페이스를 구현했다는 것만이 타입체크를 통과하는 유일한 방법은 아니다.
타입체크에서 중요한 것은 실제로 그 값을 갖고 있는지이다.

```ts
interface IDuck {
  quack(): void;
}

class MallardDuck implements IDuck {
  // 3
  quack() {
    console.log("Quack!");
  }
}

class RedheadDuck {
  // 4
  quack() {
    console.log("q~uack!");
  }
}

function makeNoise(duck: IDuck): void {
  // 2
  duck.quack();
}

makeNoise(new MallardDuck()); // Quack!
makeNoise(new RedheadDuck()); // q~uack! // 5
```

makeNoise 함수는 IDuck을 구현한 클래스의 인스턴스를 인자로 받는다.
그런데 RedheadDuck은 quack 메서드를 갖고 있지만 IDuck 인터페이스를 구현한 것은 아니다.
타입스크립트는 해당 인터페이스에서 정의한 프로퍼티나 메서드를 갖고 있다면 그 인터페이스를 구현한 것으로 인정한다.
이를 `Duck typing` 또는 구조적 타이핑(`structral typing`)이라 한다.

덕 타이핑은 변수에도 적용된다.

```ts
interface ICar {
  name: string;
}

const move = (car: ICar): void => {
  console.log(`${car.name} is moving...`);
};

const sm3 = { name: "sm3" };
move(sm3);
```

변수 sm3는 ICar와 일치하지 않는다. 하지만 ICar의 name 프로퍼티를 가지고 있기 때문에 인터페이스에 부합한 것으로 인정된다.

## 선택적 프로퍼티

인터페이스의 프로퍼티는 반드시 구현해야 한다. 허나 프로퍼티 뒤에 `?`를 붙일 경우 해당 프로퍼티 구현이 강제되지 않는다.

```ts
interface IHouse {
  rooms: number;
  address: string;
  telephone?: string;
  _type: "APT" | "detached";
}

const myHouse: IHouse = {
  rooms: 1,
  address: "Seoul",
  _type: "detached",
};
```

## 인터페이스 상속

인터페이스는 `extends` 키워드를 사용하여 인터페이스 또는 클래스를 상속받을 수 있다.

```ts
interface Person {
  name: string;
  age?: number;
}

interface Female extends Person {
  height: number;
}

const suzi: Female = {
  name: "suzi",
  height: "172",
};

interface Developer {
  position: "Front" | "Back";
}

// 인터페이스는 복수로 상속할 수 있다.

interface CTO extends Person, Developer {
  career: string;
}

const Wozniak: CTO = {
  name: "Wozniak",
  position: "Back",
  career: "Apple",
};
```

인터페이스는 클래스도 상속받을 수 있다. 단, 클래스의 모든 멤버(public, protected, private)가 상속되지만 구현까지 상속하지는 않는다.

```ts
class Person {
  constructor(public name: string, public age: number) {}
}

interface Developer extends Person {
  skills: string[];
}

const developer: Developer = {
  name: "Lee",
  age: 20,
  skills: ["HTML", "CSS", "JavaScript"],
};
```

> 출처
> https://poiemaweb.com/typescript-interface
