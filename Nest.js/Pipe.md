# Nest.js/Pipe

파이프는 컨트롤러에 요청이 전달되기전 데이터의 타입을 변경하거나 유효성 검사를 할 때 사용된다.
클라이언트의 요청이 파이프의 유효성 검사를 통과하지 못한다면 예외를 일으켜 비즈니스로 로직이 실행되지 않는다.

Nest.js에 내장된 파이프는 다음과 같다.

- ValidatePipe
  - 주어진 조건으로 유효성 검사를 한다.
- ParseIntPipe
  - 데이터가 정수로 변환되는 값일 경우 변환하고 아닐 경우 예외를 일으킨다.
- ParseBoolPipe
  - 데이터가 불리언으로 변환되는 값일 경우 변환하고 아닐 경우 예외를 일으킨다.
- ParseArrayPipe
  - 데이터가 배열로 변환되는 값일 경우 변환하고 아닐 경우 예외를 일으킨다.
- ParseUUIDPipe
  - 데이터가 UUID로 변환되는 값일 경우 변환하고 아닐 경우 예외를 일으킨다.
- DefaultValuePipe
  - 기본 값을 지정한다.

```ts
import {
  Controller,
  Post,
  Get,
  DefaultValuePipe,
  ParseIntPipe,
} from "@nestjs/common";
import { UsersService } from "./users.service";

export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  findAll(
    @Query("limit", new DefaultValuePipe(10), ParseIntPipe) limit: number,
    @Query("skip", new DefaultValuePipe(0), ParseIntPipe) skip: number
  ) {
    return this.usersService.findAll(limit, skip);
  }
}
```

파이프를 사용할 때는 클래스를 넘겨도되고 옵션을 설정하고 싶을 때는 위 예시에 나온 `DefaultValuePipe`처럼 직접 인스턴스화 하여 넘겨도 된다.

## Class validator

`class-validator`와 `class-transform` 패키지를 사용하면 유효성 검사 파이프를 만들 수 있다.

```
npm i class-validator class-transform
```

먼저 `ValidationPipe`을 전역으로 등록한다.

- **main.ts**

```ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe());
  await app.listen(3000);
}
bootstrap();
```

정의된 DTO에 `class-validator`로 유효성 검사 로직을 추가한다.

```ts
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  password: string;

  @IsString()
  name: string;

  @IsInt()
  age: number;
}
```

이제 요청이 왔을 때 전역에 적용되는 `ValidationPipe`가 class-validator의 유효성 검사 조건으로 값을 검사한다.

```ts
import { Controller, Post, Get, Body, ValidationPipe } from "@nestjs/common";
import { UsersService } from "./users.service";
import { CreateUserDto } from "./users.dto";

export class UsersController {
  constructor(private readonly usersService: UsersService) {}
  @Post()
  createUser(@Body() createUserDto: CreateUserDto) {
    return this.usersService.createUser(createUserDto);
  }
}
```

## 참조

- [파이프(Pipe)](https://wikidocs.net/158588)
- [Pipes](https://docs.nestjs.com/pipes)
