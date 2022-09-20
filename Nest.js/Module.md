# Nest.js/Module

모듈이란 비슷한 기능을 하는 코드의 모음으로 Nest.js에서는 `@Module()` 데코레이터로 정의할 수 있다.

```ts
import { Module } from "@nestjs/common";
import { UsersController } from "./users.controller";
import { UsersService } from "./users.service";
import { AuthModule } from "../auth/auth.module";

@Module({
  imports: [AuthModule],
  exports: [UsersService],
  controllers: [UsersController],
  providers: [UsersService],
})
export class UsersModule {}
```

- `imports`: 사용하고 싶은 다른 모듈을 등록한다.
- `exports`: 해당 모듈이 다른 모듈에 제공할 프로바이더를 등록한다.
- `controllers`: 해당 모듈의 컨트롤러를 등록한다.
- `providers`: 해당 모듈의 프로바이더를 등록한다.

## 전역 모듈

Nest.js는 모듈 범위내에서 프로바이더를 캡슐화 하기 때문에 프로바이더를 사용하려면 모듈을 먼저 가져와야 한다.
하지만 `@Global()` 데코레이터를 사용하면 전 범위내에서 사용하고 싶은 프로바이더를 모아 전역 모듈을 만들 수 있다.

```ts
@Global()
@Module({
  providers: [CommonService],
  exports: [CommonService],
})
export class CommonModule {}
```

다만 전역모듈을 사용하면 프로그램의 응집도가 떨어지기 때문에 남용하지 않도록 주의해야 한다.

## 동적 모듈

동적 모듈이란 모듈이 생성될 때 동적으로 어떤 변수들이 정해지는 모듈이다.
즉 호스트 모듈을 가져다 쓰는 소비모듈에서 호스트 모듈을 생성할 때 동적으로 값을 생성하는 방식이다.

동적 모듈을 사용하면 인스턴스마다 다르게 결정되어야 하는 것들을 소비 모듈에서 지정할 수 있기에 코드가 간결해진다.

## 참조

- [동적 모듈(Dynamic Module)](https://wikidocs.net/158576)
- [TypeScript를 활용한 서비스개발](https://medium.com/daangn/typescript%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EC%84%9C%EB%B9%84%EC%8A%A4%EA%B0%9C%EB%B0%9C-73877a741dbc)
