# Exception Filter

예외가 발생했을 때 이를 대응하는 예외처리는 소프트웨어를 개발할 때 필수 사항이다.
예외가 발생했을 때 어디다 예외 처리 코드를 넣어야 할까? 예외가 발생할 수 있는 모든 곳에 삽입할 경우 중복 코드 양산 뿐만 아니라 기능 구현과 관려 없는 코드가 삽입되어 핵심 기능 구현에 집중할 수 없다.

예외가 발생했을 때 예외로그와 콜스택을 나며 디버깅에 사용할 수 있도록 한다고 하면, 예외처리기를 따로 만들어 한 고셍서 공통으로 처리해야 한다.

## Exception Handling

Nest는 프레임워크 내에 예외 레이어를 두고 있어 애플리케이션에서 제대로 처리하지 못한 예외를 처리한다. (그래서 try...catch를 사용하지 않아도 서버가 멈추지 않고 에러를 응답한다.)

Nest에는 예외를 처리하는 여러 클래스가 있는데 이 클래스들은 HttpException을 상속하고 HttpException은 Error를 상속하는 구조이다.

**HttpException**

```ts
export declare class HttpException extends Error {
        ...
    constructor(response: string | Record<string, any>, status: number);
        ...
}
```

HttpException은 response라는 JSON응답의 본문과 status라는 HTTP 상태코드를 인자로 받는다.

## Exception Filter

Nest에서 제공하는 전역 예외 필터 외에 직접 예외 필터 레이어를 두어 예외를 다룰 수 있다. 예외가 일어났을 때 로그를 남기거나, 응답 객체를 변경하고자 할 때 사용한다.

```ts
import {
  ArgumentsHost,
  Catch,
  ExceptionFilter,
  HttpException,
  InternalServerErrorException,
} from "@nestjs/common";
import { Request, Response } from "express";

@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: Error, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const res = ctx.getResponse<Response>();
    const req = ctx.getRequest<Request>();

    if (!(exception instanceof HttpException)) {
      exception = new InternalServerErrorException();
    }

    const response = (exception as HttpException).getResponse();

    const log = {
      timestamp: new Date(),
      url: req.url,
      response,
    };

    console.log(log);

    res.status((exception as HttpException).getStatus()).json(response);
  }
}
```

`@Catch()`는 처리되지 않은 예외를 잡을 때 사용한다. HttpException의 인스턴스가 아닌 에러는 InteralServerErrorException으로 처리되도록 한다.

예외 필터는 `@UserFilter()` 데코레이터로 컨트롤러나 전역에 적용할 수 있다. 허나 보통 전역필터를 하나만 갖게 하는 것이 정석이다.

```ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalFilters(new HttpExceptionFilter()); // 전역 필터 적용
  await app.listen(3000);
}
```

의존성 주입을 받고자 하자면 커스텀 프로바이더로 등록한다.

```ts
import { Module } from "@nestjs/common";
import { APP_FILTER } from "@nestjs/core";

@Module({
  providers: [
    {
      provide: APP_FILTER,
      useClass: HttpExceptionFilter,
    },
  ],
})
export class AppModule {}
```

이를 통해 logger를 주입받아 예외필터에서 로그처리를 할 수 있다.
