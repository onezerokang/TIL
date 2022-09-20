# Nest.js/Controller

컨트롤러는 API를 정의하고 요청을 받아들인 후 처리 결과를 응답하는 프로그램의 구성요소다.
Nest.js에서는 `@Controller()` 데코레이터를 사용하여 정의할 수 있다.

```ts
import { Controller, Get, Post, Body } from "@nestjs/common";
import { UserService } from "./users.service";
import { CreateUserDto } from "./dto/users.dto";

@Controller("users")
export class UserController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  createUser(@Body() createUserDto: CreateUserDto) {
    return this.usersService.createUser(createUserDto);
  }

  @Get()
  findAll() {
    return this.usersService.findAll();
  }
}
```

## 요청과 함께 온 데이터를 처리하는 방법

클라이언트에는 요청을 보낼 때 서버에서 필요한 데이터를 보내기도 하는데 `@Body()`, `Param()`, `@Query()`와 같은 데코레이터로 주입받아 사용할 수 있다. 또한 DTO(Data Transfer Object)를 정의하여 어떤 데이터가 입력되어야 하는지를 정의하고 데이터를 쉽게 다룰 수 있다.

- **users.dto.ts**

```ts
export class CreateUserDto {
  name: string;
  age?: number;
}

export class FindUsersDto {
  skip: number;
  limit: number;
}
```

- **users.controller.ts**

```ts
import { Controller, Get, Post, Body } from "@nestjs/common";
import { UserService } from "./users.service";
import { CreateUserDto, FindUsersDto } from "./dto/users.dto";

@Controller("users")
export class UserController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  createUser(@Body() createUserDto: CreateUserDto) {
    console.log(createUserDto); // {name: "minsu", age: 26}
    return this.usersService.createUser(createUserDto);
  }

  @Get()
  findAll(@Query() findUsersDto: FindUsersDto) {
    console.log(findUsersDto); // {skip: 200, limit: 20}
    return this.usersService.findAll(findUsersDto);
  }
}
```
