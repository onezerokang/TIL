# Nest.js/Guard

가드은 인가를 할 때 사용되며 `CanActivate` 인터페이스룰 구현하여 정의할 수 있다.

```ts
import { Injectable, CanActivate, ExecutionContext } from "@nestjs/common";
import { Observable } from "rxjs";

export class AuthGuard implements CanActivate {
  canActivate(
    context: ExectionContext
  ): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    return this.validateRequest(request);
  }

  private validateRequest(request: any) {
    // ...validate 조건
    return true;
  }
}
```

`canActivate` 함수는 `ExectionContext`를 인자로 받아 가드가 실행컨텍스트에 대한 정보를 바탕으로 인가를 진행한다.

## 가드 적용

가드를 적용할 때는 `@UseGuard()` 데코레이터에 가드를 넘겨준다.

```ts
@UseGuards(AuthGuard)
@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @UseGuards(AuthGuard)
  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}
```

전역으로 가드를 적용하고 싶다면 main.ts에서 `useGlobalGuards()`로 설정한다.
