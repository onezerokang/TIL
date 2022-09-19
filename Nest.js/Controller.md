# Nest.js/Controller

컨트롤러는 클라이언트의 요청을 분류하여 받고 요청에 대한 처리 결과를 응답하는 프로그램의 구성요소다.
Nest.js에서는 `@Controller()` 데코레이터를 사용하여 클래스가 컨트롤러의 역할을 하도록 한다.

```ts
import { Controller, Get } from "@nestjs/common";

@Controller("users")
export class UserController {
  @Get()
  getUser(): string {
    return "User";
  }
}
```

## 라우팅(Routing)

라우팅을 하기 위해서는 컨트롤러 내부에서 `@Get()`, `@Post()`, `@Put()`, `@Delete()` 등 HTTP Method 데코레이터를 사용한다.

```ts
import { Controller, Get, Post, Put, Delete } from "@nestjs/common";

@Controller("users")
export class UserController {
  @Post()
  createUser(): string {
    return "Created";
  }

  @Get()
  getUser(): string {
    return "User";
  }
}
```

HTTP 메서드 데코레이터의 인자로 API URL을 넘겨줄 수 있다.
또한 Controller의 인자로는 컨트롤러에 고정된 경로를 넘겨줄 수 있다.

## 요청과 함께 온 데이터를 처리하는 방법

클라이언트는 요청을 보낼 때 서버에서 필요한 데이터를 보내기도 하는데 이런 데이터들은 각각 대응하는 데코레이터로 주입받아 사용할 수 있다.

- `@Body()`: Request body
- `@Param()`: Path parameter
- `@Query()`: Querystring

```ts
import { Controller, Get, Param } from "@nestjs/common";

@Controller("users")
export class UserController {
  @Get()
  findUserById(@Param("id") id) {
    return `User: ${id}`;
  }
}
```
