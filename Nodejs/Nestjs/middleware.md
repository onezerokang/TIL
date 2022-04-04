# Middleware

Nest.js에서 미들웨어는 Express의 미들웨어와 같다. 컨트롤러에 요청이 들어오기전에 미들웨어를 거쳐 프로그래머가 정해둔 로직을 실행한다.
logger 미들웨어를 간단하게 구현하는 것을 통해 미들웨어를 익힐 수 있도록 하겠다.

```ts
import { Injectable, NestMiddleware } from "@nestjs/common";
import { Request, Response, NextFunction } from "express";

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log("Request...");
    next();
  }
}
```

미들웨어는 `NestMiddleware`를 구현(implements)해야 한다. 그로인해 use 메서드를 구현해야 하고, 인자로 req, res, next를 갖게 되어 express와 같은 미들웨어를 구현할 수 있게 된다.

## Dependency injection

Nest.js 미들웨어는 Dependency Injection을 지원한다.

## Applying middleware

미들웨어는 `@Module()` 데코레이터에서 등록할 수 없다. 대신 `NestModule`을 구현한 Module 클래스에서 configure 메서드를 통해 연결할 수 있다.

```ts
import { Module, NestModule, MiddlewareConsumer } from "@nestjs/common";
import { LoggerMiddleware } from "./common/middleware/logger.middleware";
import { CatsModule } from "./cats/cats.module";

@Module({
  imports: [CatsModule],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(LoggerMiddleware).forRoutes("cats");
  }
}
```

위 코드는 cats 라우터로 들어오는 모든 요청은 LoggerMiddleware를 거치도록 미들웨어를 등록해준 것이다.

## Route wildcards

미들웨어가 적용될 routes를 지정할 때 와일드카드를 사용할 수 있다.

```ts
forRoutes({ path: "ab*cd", method: RequestMethod.ALL });
```

## Middleware consumer

## Excluding routes

## Functional middleware

## Multiple middleware

## Global middleware

전역 미들웨어를 등록하고 싶을 경우 main.ts에서 등록해줄 수 있다.

```ts
const app = await NestFactory.create(AppModule);
app.use(logger);
await app.listen(3000);
```
