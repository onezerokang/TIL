# NestJS로 배우는 백엔드 프로그래밍

# 목차

# 1장 Hello NestJS

## NestJS 소개

NestJS는 Node.js에 기반을 둔 웹 프레임워크로 Express나 Fastify 프레임워크를 래핑하여 동작한다.

Node.js는 뛰어난 확장성을 가지고 있지만 자유도가 높은 탓에 SW 품질이 일정하지 않고 규모가 커지면 유지보수하기 어려워지며 라이브러리를 찾는데 많은 시간을 할애해야 한다. 반면 NestJS는 정해진 구조와 규칙을 제공하기 때문에 일관된 프로그래밍을 할 수 있다.

## NestJS 설치

NestJS 서버를 구축하기 위해서는 `@nestjs/cli`를 설치해야 한다.

```
npm i -g @nestjs/cli
```

이후 `nest new 프로젝트 이름`으로 프로젝트를 생성할 수 있다.

```
nest new project-name
```

프로젝트를 생성한 후 `npm install`명령어로 의존하고 있는 패키지를 설치한다.

# 2장 NestJS를 배우기 전에

## 웹 프레임워크

웹 프레임워크는 웹을 개발하는 과정에서 겪는 어려움을 줄이는 것이 목적으로 데이터를 관리하거나 세션을 맺고 유지하는 등의 동작을 정해진 방법과 추상화된 인터페이스로 제공한다.

## Node.js

Node.js는 오픈 소스 자바스크립트 엔진인 크롬 V8에 비동기 이벤트 처리 라이브러리인 libuv를 결합한 자바스크립트 런타임이다.
Node.js의 등장으로 JavaScript로 서버를 구동할 수 있게 되었는데, 이 경우 프론트와 백엔드가 같은 언어를 사용하기 때문에 생산성 증가에 이점이 있다.

### Node.js의 특징

#### 단일 쓰레드에서 구동되는 non-blocking I/O 이벤트 기반 비동기 방식

Node.js에서는 하나의 쓰레드에서 작업을 처리한다. 사실 어플리케이션 단에서만 단일 쓰레드이고 백그라운드에서는 쓰레드 풀을 생성해 작업을 처리한다.
개발자가 직접 쓰레드 풀을 관리하지 않도록 Node.js에 포함된 libuv가 그 역할을 하기 때문에 개발자는 단일 쓰레드에서 동작하는 것처럼 이해하기 쉬운 코드를 작성할 수 있다.

Node.js는 이렇게 들어온 작업을 앞의 작업이 끝날 때까지 기다리지 않고 비동기로 처리한다.
입력은 하나의 쓰레드에서 받지만 순서대로 처리하지 않고 먼저 처리된 결과를 이벤트로 반환해주는 방식이 바로 Node.js에서 사용하는 non-blocking 이벤트 기반 비동기 방식이다.

#### Node.js의 장단점

- 장점
  - 단일 쓰레드 이벤트 기반 비동기 방식은 서버의 자원에 크게 부하를 가하지 않는다.(대규모 애플리케이션 개발에 적합)
- 단점
  - 단일 쓰레드를 사용하기 때문에 쓰레드에 문제가 생기면 애플리케이션 전체에 오류를 일으킬 위험이 존재한다.

## 이벤트 루프

## 데코레이터

Nest는 데코레이터를 적극 활용한다. 데코레이터를 잘 사용하면 횡단관심사를 분리하여 관점 지향 프로그래밍을 적용한 코드를 작성할 수 있습니다. 타입스크립트의 데코레이터는 파이썬의 데코레이너, 자바의 어노테이션과 유사한 기능알 한다. 데코레이터는 클래스, 메서드, 접근자, 프로퍼티, 매개변수에 적용가능하다.

각 요소의 선언부 앞에 `@`로 시작하는 데코레이터를 선언하면 데코레이터로 구현한 코드를 함께 실행한다. 다음은 유저 생성 요청의 본문을 DTO로 표현한 클래스다.

```ts
class CreateUserDto {
  @IsEmail()
  @MaxLength(60)
  readonly email: string;

  @IsString()
  @Matches(/^[A-Za-z\d!@#$%^&*()]{8,30}$/)
  readonly password: string;
}
```

위 코드에서는 사용자가 요청을 잘못보낼 수 있기 때문에 데코레이터를 이용하여 유효성 검사를 하고 있다.

데코레이터는 `@expression`과 같은 형식으로 사용한다. 여기서 expression은 함수여야 한다.

```ts
function deco(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  console.log("데코레이터가 평가됨");
}

class TestClass {
  @deco()
  test() {
    console.log("함수 호출됨");
  }
}

const t = new TestClass();
t.test();
// 데코레이터가 평가됨
// 함수 호출됨
```

만약 데코레이터에 인자를 넘겨서 데코레이터의 동작을 변경하고 싶다면 데코레이터 팩토리, 즉 데코레이터를 리턴하는 함수를 만들면 된다. 위의 예시를 다음과 같이 value라는 인자를 받도록 만들어보겠다.

```ts
function deco(value: string) {
  console.log("데코레이터가 평가됨");
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    console.log(value);
  };
}

class TestClass {
  @deco("Hello")
  test() {
    console.log("함수 호출됨");
  }
}

// 데코레이터가 평가됨
// Hello
// 함수 호출됨
```

## 데코레이터 합성

여러개의 데코레이터를 사용한다면 수학에서의 함수 합성과 같이 적용된다. 다음 데코레이터의 합성 결과는 `f(g(x))`와 같다.

```ts
@f
@g
test
```

여러 데코레이터를 사용할 때 다음과 같은 단계가 수행된다.

1. 각 데코레이터의 표현은 위에서 아래로 평가된다.
2. 그런 다음 결과는 아래에서 위로 호출된다.

```ts
function first() {
  console.log("first(): factory evaluated");
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    console.log("first(): called");
  };
}

function first() {
  console.log("second(): factory evaluated");
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    console.log("second(): called");
  };
}

class ExampleClass {
  @first()
  @second()
  method() {
    console.log("method is called");
  }
}

// first(): factory evaluated
// second(): factory evaluated
// second(): called
// first(): called
// method is called
```

## 클래스 데코레이터(Class Decorator)

클래스 바로 앞에 선언되는 데코레이터로 클래스의 생성자에 적용되어 클래스 정의를 읽거나 수정할 수 있다. *선언 파일*과 선언 클래스(declare class)내에서는 사용할 수 없다.

```ts
function reportableClassDecorator<T extends { new (...args: any[]): [] }>(
  constructor: T
) {
  return class extends constructor {
    reportingURL = "http://www.example.com";
  };
}

@reportableClassDecorator()
class BugReport {
  type = "report";
  title: string;

  constructor(t: string) {
    this.title = t;
  }
}

const bug = new BugReport("Needs dark mode");
console.log(bug);
// {type: 'report', title: "Needs dark mode", reportingURL: "http://example.com"}
```

## 메서드 데코레이터(Method Decorator)

## 접근자 데코레이터(Accessor Decorator)

## 속성 데코레이터(Property Decorator)

## 매개변수 데코레이터(Parameter Decorator)

| 데코레이터          | 역할                        | 호출시 전달되는 인자                      | 선언 불가능한 위치                         |
| ------------------- | --------------------------- | ----------------------------------------- | ------------------------------------------ |
| 클래스 데코레이터   | 클래스의 정의를 읽거나 수정 | (constructor)                             | d.ts 파일, declare 클래스                  |
| 메서드 데코레이터   | 메서드의 정의를 읽거나 수정 | (target, propertyKey, propertyDescriptor) | d.ts 파일, declare 클래스, 오버로드 메서드 |
| 접근자 데코레이터   | 접근자의 정의를 읽거나 수정 | (target, propertyKey, propertyDescriptor) | d.ts 파일, declare 클래스                  |
| 속성 데코레이터     | 속성의 정의를 읽거나 수정   | (target, propertyKey)                     | d.ts 파일, declare 클래스                  |
| 매개변수 데코레이터 | 매개변수의 정의를 읽음      | (target, propertyKey, parameterIndex)     | d.ts 파일, declare 클래스                  |

# 3장 애플리케이션의 관문 - 인터페이스

## 컨트롤러(Controller)

컨트롤러는 들어오는 요청을 받고 처리된 결과를 응답해주는 인터페이스 역할을 한다.
컨트롤러는 엔드포인트 라우팅(routing) 매커니즘을 통해 각 컨트롤러가 받을 수 있는 요청을 분류한다. 컨트롤러를 사용 목적에 따라 구분하면 구조적이고 모듈화된 소프트웨어를 작성할 수 있다.

아래 커맨드로 컨트롤러를 생성할 수 있다.

```
nest g controller [name]
```

### 라우팅(routing)

서버가 수행해야 하는 많은 귀찮은 작업을 데코레이터로 기술하여, 어플리케이션이 가지는 핵심 로직에 집중할 수 있도록 도와준다. `@Controller` 데코레이터를 클래스에 선언하는 것으로 해당 클래스는 컨트롤러의 역할을 하게 된다.

- app.controller.ts

```ts
import { Controller, Get } from "@nestjs/common";
import { AppService } from "./app.service";

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}
```

- `@Controller([prefix])`
- `@Get([pathname])`

### 요청 객체(Request Object)

Nest는 요청과 함께 전달된 데이터를 핸들러가 다룰 수 있는 객체로 변환한다. 이렇게 변환된 객체는 `@Req()` 데코레이터를 이용하여 다룰 수 있다.

```ts
import { Request } from "express";
import { Controller, Get, Req } from "@nestjs/common";
import { AppService } from "./app.service";

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(@Req() req: Request): string {
    console.log(req);
    return this.appService.getHello();
  }
}
```

Nest는 요청 객체 외에도 `@Body()`, `@Param(key?: string)`,`@Query()` 데코레이터를 이용해서 요청에 포함된 쿼리 본문, 패스 파리마터, 쿼리 파라미터를 쉽게 받을 수 있도록 한다.

## 응답

Nest는 응답을 어떤 방식으로 처리할지 미리 정의해뒀다. string, number, boolean 같이 원시타입을 반환한다면 직렬화 없이 바로 보내지만, 객체를 리턴한다면 직렬화를 통해 JSON으로 자동 변환한다.

## 헤더

Nest는 응답 헤더 역시 자동으로 구성해준다.

만약 커스텀 헤더를 추가하고 싶다면 `@Header` 데코레이터를 사용하면 된다. 인자로 헤더 이름과 값을 받는다. 혹은 라이브러리에서 제공하는 응답 객체를 사용해서 res.header() 메서드로 설정할 수도 있다.

## 리디렉션(Redirection)

`@Redirect` 데코레이터를 사용하면 리디렉션을 쉽게 구현할 수 있다. 해당 데코레이터의 첫번째 인자에는 리다이렉트할 주소가, 두번째 인자에는 상태코드가 들어간다.

```ts
import { Redirect } from '@nestjs/common';

@Redirect('https://nestjs.com', 301)
@Get(':id')
findOne(@Param('id') id: string) {
  return this.usersService.findOne(+id);
}
```

만약 요청 처리 결과에 따라 동적으로 리디렉트 하고자 한다면 응답을 다음 객체와 같이 리턴한다.

```ts
{
  "url": string,
  "statusCode": number
}
```

## 라우트 파라미터

라우트 파라미터 또는 패스 파라미터는 함수 인자에 `@Param` 데코레이터로 주입받을 수 있다.
만약 여러개의 라우트 파리미터가 전달될 경우 아래 코드처럼 받을 수 있다.

```ts
@Delete(':userId/memo/:memoId')
deleteUserMemo(
  @Param('userId') userId: string,
  @Param('memoId') memoId: string,
) {
  return `userId: ${userId}, memoId: ${memoId}`;
}
```

## 하위 도메인(Sub-Domain)

하위 도메인을 라우팅하기 위해서는 `@Controller` 데코레이터의 옵션으로 host 속성을 넘겨준다.

```ts
@Controller({ host: "api.example.com" })
export class ApiController {
  @Get()
  index(): string {
    return "Hello, API";
  }
}
```

`@HostParam` 데코레이터를 이용하면 서브 도메인을 변수로 받을 수 있다. 주로 API를 버저닝 할 때 사용한다.

```ts
@Controller({ host: ":version.api.localhost" })
export class ApiController {
  @Get()
  index(@HostParam("version") version: string): string {
    return `Hello, API ${version}`;
  }
}
```

## 페이로드 다루기

POST, PUT, PATCH 요청은 보통 처리에 필요한 데이터를 함께 실어보낸다. 이 데이터 덩어리(payload)를 본문(body)라고 한다. Nest는 본문을 DTO(Data Transfer Object)를 정의하여 쉽게 다룰 수 있다.

```ts
export class CreateUserDTo {
  name: string;
  email: string;
}
```

```ts
@Post()
createUser(@Body() createUserDto: CreateUserDto) {
  const {name, email} = createUserDto
  return `유저를 생성했습니다. 이름: ${name}, 이메일: ${email}`;
}
```

GET 요청에서 데이터를 전송할 때 사용하는 쿼리스트링에도 DTO를 정의하여 다룰 수 있다.

```ts
export class GetUsersDto {
  offset: number;
  limit: number;
}
```
