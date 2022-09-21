# Nest.js/Middleware

미들웨어란 요청이 라우트 핸들러에 닿기전 실행되는 코드다.
Nest.js에서 미들웨어는 `NestMiddleware`를 구현한 클래스에 `@Injectable` 데코레이터로 정의 가능하다.

```ts
import { Injectable, NestMiddleware } from "@nestjs/common";
import { Request, Response, NextFunction } from "express";

@Injectable()
export class Logger implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log(`${req.method} ${req.originalUrl} ${req.ips}`);
    next();
  }
}
```

미들웨어를 사용할 모듈은 `NestModule`을 구현한 후 `configure` 함수를 통해 미들웨어를 등록한다.

```ts
import { Module, NestModule, MiddlewareConsumer } from "@nestjs/common";
import { UsersController } from "./users/users.controller";
import { Logger } from "./common/middlewares/logger";

@Module({
  imports: [UsersController],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): any {
    consumer.apply(Logger).forRoutes(UsersController);
  }
}
```

`MiddlewareConsumer`는 `apply()` 메서드와 `forRoutes()` 메서드를 갖는데 `apply()`에는 등록할 미들웨어를
`forRoutes()`에는 엔드포인트 경로 혹은 미들웨어를 사용할 컨트롤러를 넘긴다. 미들웨어를 적용하고 싶지 않은 컨트롤러는 `exclude()`메서드에 넘겨주면 된다.

## 전역 미들웨어

미들웨어는 전역으로도 사용가능한데 `main.ts`에서 `app.use()`로 등록해주면 된다.
다만 `app.use()`는 인자로 클래스를 받을 수 없어 함수 미들웨어를 사용해야 한다.

```ts
import { Request, Response, NextFunction } from "express";

export const Logger = (req: Request, res: Response, next: NextFunction) => {
  console.log(`${req.method} ${req.originalUrl} ${req.ips}`);
  next;
};
```

다만 함수 미들웨어는 `constructor`를 통한 DI를 할 수 없다.

## 참조

- [미들웨어(Middleware)](https://wikidocs.net/158620)
- [MiddlewareConsumer](https://wikidocs.net/158624)
