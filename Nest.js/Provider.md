# Nest.js/Provider

프로바이더란 주입 가능한 비즈니스 로직으로 `@Injectable()` 데코레이터로 정의가 가능하다.
프로바이더는 서비스(Service), 레포지토리(Repository), 팩토리(Factory), 헬퍼(Helper) 등 여러가지 형태로 구현할 수 있다.

- **users.service.ts**

```ts
import { Injectable } from "@nestjs/common";
import { User } from "./user.interface";
import { CreateUserDto } from "./dto/users.dto";

@Injectable()
export class UsersService {
  private readonly users: User[] = [];

  createUser(createUserDto: CreateUserDto) {
    this.users.push(createUserDto);
    return { success: true };
  }

  findAll(): User[] {
    return this.users;
  }
}
```

- **user.interface.ts**

```ts
export interface User {
  name: string;
  age?: number;
}
```

비즈니스 로직을 컨트롤러에 작성해도 되지만 이는 단일 책임 원칙에 위배 되기에 따로 분리한 후 컨트롤러에 주입하여 사용한다.

## 프로바이더 등록과 주입

프로바이더를 사용하기 위해서는 프로바이더를 사용할 모듈에 프로바이더를 등록해야 한다.

```ts
import { Module } from "@nestjs/common";
import { UsersController } from "./users.controller";
import { UsersService } from "./users.service";

@Module({
  controllers: [UsersController],
  providers: [UsersService],
})
export class UsersModule {}
```

이후 컨트롤러나 프로바이더에서 등록한 프로바이더를 주입하여 사용할 수 있다.

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

이렇게 Nest.js는 의존성 주입(Dependency Injection)을 제공하기 때문에 개발자는 읽기 쉽고 재사용 가능한 코드를 짤 수 있다.
