# Provider

프로바이더란 앱의 핵심 기능, 즉 비즈니스 로직을 수행하는 역할이다.
프로바이더는 서비스, 레포지토리, 팩토리, 헬퍼 등 여러가지 형태로 구현이 가능하며 Nestjs 컴포넌트에 의존성 주입이 가능하다.
(사실 컨트롤러에 비즈니스 로직을 같이 작성해도 에러가 발생하지는 않지만, 단일 책임 원칙에 위반되기에 분리하는 것이다)

## Services

프로바이더는 `@Injectable` 데코레이터를 사용하여 생성할 수 있다.

**users.service.ts**

```ts
import { Injectable } from "@nestjs/common";
import { Cat } from "./interfaces/cat.interface";

@Injectable()
export class CatsService {
  private readonly cats: Cat[] = [];

  create(cat: Cat) {
    this.cats.push(cat);
  }

  findAll(): Cat[] {
    return this.cats;
  }
}
```

**interfaces/user.interface.ts**

```ts
export interface Cat {
  name: string;
  age: number;
  breed: string;
}
```

**users.controller.ts**

```ts
import { Controller, Get, Post, Body } from "@nestjs/common";
import { CreateCatDto } from "./dto/create-cat.dto";
import { CatsService } from "./cats.service";
import { Cat } from "./interfaces/cat.interface";

@Controller("cats")
export class CatsController {
  constructor(private catsService: CatsService) {}

  @Post()
  async create(@Body() createCatDto: CreateCatDto) {
    this.catsService.create(createCatDto);
  }

  @Get()
  async findAll(): Promise<Cat[]> {
    return this.catsService.findAll();
  }
}
```

CatsService는 생성자를 통해서 된다.. 이때 `private` 문법을 사용해야 한다.
이 단축문법은 `catsService`를 선언하고 동시에 초기화 시켜준다.

## Dependency Injection

의존성 주입(Dependency Injection)이란:

Nest는 의존성주입이 가능한 디자인 패턴을 기반으로 구축되었습니다.
아래 예에서 Nest는 catsService의 인스턴스를 생성하고 반환하여 사용합니다.

```ts
constructor(private catsService: CatsService) {}
```

## Scope

## Custom Provider

## Optional Provider

## Property-based injection

## Provider registration

서비스를 컨트롤러에서 주입하여 사용하기 위해서는 모델에 서비스를 등록해야 한다.
모듈 파일에 있는 `@Module` 데코레이터의 providers 배열에 등록해주면 된다.

```ts
import { Module } from "@nestjs/common";
import { CatsController } from "./cats/cats.controller";
import { CatsService } from "./cats/cats.service";

@Module({
  controllers: [CatsController],
  providers: [CatsService],
})
export class AppModule {}
```
