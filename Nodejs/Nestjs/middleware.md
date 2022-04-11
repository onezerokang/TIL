# Middleware

미들웨어는 라우트 핸들러 전에 호출되는 함수다. Express와 마찬가지로 Request, Response 객체에 접근할 수 있으며 next() 함수를 갖는다.
아래는 미들웨어를 만드는 예시다.

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

미들웨어는 `NestMiddleware`를 구현(implements)하고 `use()` 메서드에 미들웨어 로직을 프로그래밍 할 수 있다.

## Dependency injection

Nest.js 미들웨어는 Dependency Injection을 지원한다. 컨트롤러나 프로바이더에 주입이 가능하며 constructor를 통해 주입한다.

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
`forRoutes()` 메서드는 와일드카드를 지원하며, 특정 메서드에만 적용되도록 설정할 수 있다.

```ts
forRoutes({ path: "ab*cd", method: RequestMethod.ALL });
```

## Middleware consumer

`MiddlewareConsumer`는 helper class로, 미들웨어 관리에 필요한 메서드를 제공한다.

## Excluding routes

exclude 메서드를 사용하면 미들웨어가 적용되지 않을 라우터를 지정할 수 있다.

```ts
consumer
  .apply(LoggerMiddleware)
  .exclude(
    { path: "cats", method: RequestMethod.GET },
    { path: "cats", method: RequestMethod.POST },
    "cats/(.*)"
  )
  .forRoutes(CatsController);
```

## Functional middleware

의존성 주입을 하지 않는 간단한 미들웨어의 경우 함수로 만들 수 있다.

```ts
import { Request, Response, NextFunction } from "express";

export function logger(req: Request, res: Response, next: NextFunction) {
  console.log(`Request...`);
  next();
}
```

## Multiple middleware

순차적으로 실행되는 여러 미들웨어를 등록하기 위해서는 `apply()` 메서드 내부에 쉼표로 구분된 목록을 제공해주면 된다.

```ts
consumer.apply(cors(), helmet(), logger).forRoutes(CatsController);
```

## Global middleware

전역 미들웨어를 등록하고 싶을 경우 main.ts에서 등록해줄 수 있다.

```ts
const app = await NestFactory.create(AppModule);
app.use(logger);
await app.listen(3000);
```

단 전역 미들웨어에서는 DI container에 접근할 수 없다.
이 때 AppModule에서 `forRoutes('*')`로 설정하여 사용해주면 해결된다.
