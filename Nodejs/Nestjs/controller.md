# Controller

Nest의 컨트롤러는 MVC 패턴의 Controller다. Controller는 요청을 받고 처리된 결과를 응답으로 돌려주는 인터페이스의 역할을 한다.

컨트롤러는 엔드포인트 라우팅(routing) 매커니즘을 통해 각 컨트롤러가 받을 수 있는 요청을 분류한다.

```
nest g co [name]
```

## Routing

**app.controller.ts**

```ts
import { Controller, Get } from "@nestjs/common";
import { AppService } from "./app.service";

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}
```

서버가 수행해야 하는 많고 귀찮은 작업을 데코레이터로 기술하여, 어플리케이션은 핵심 로직에 집중할 수 있게 한다. `@Controller` 데코레이터를 클래스에 선언하는 것으로 컨트롤러의 역할을 하게 한다.

`@Get()` 데코레이터를 함수에 선언하여 해당 함수를 GET 라우터로 사용할 수 있다.

controller 데코레이터에 인자 전달 > 라우팅 경로의 prefix 지정
