# Guards

가드는 주로 인가(Authorization)을 구현할 때 사용한다.
미들웨어는 Execution Context에 접근할 수 없지만 가드는 할 수 있어, 다음 라우터의 정보를 알 수 있기 때문에 인가를 구현하는데 사용되는 것이다.

가드는 `CanActivate`을 구현(implements) 해야 한다.
`CanActivate` 함수는 ExecutionContext의 인스턴스를 인자로 받는다.
ExecutionContext는 ArgumentHost를 상속하고 있어 요청과 응답에 대한 정보를 가지고 있다.

```ts
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(
    context: ExecutionContext
  ): Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    return this.validateRequest(request);
  }

  private validateRequest(request: any) {
    return true;
  }
}
```

가드는 `@useGuards()` 데코리어터로 사용할 수 있다. 가드를 인자로 넘겨주면 되는데, nestjs가 가드의 인스턴스를 생성한다.
만약 여러개의 가드를 사용하고 싶으면 쉼표(,)로 구분해서 넣어주면 된다.

전역 가드를 만들고 싶으면 `useGlobalGurad`를 사용해주면 되고 Dependency Injection을 하고 싶으면 커스텀 프로바이더로 선언해주면 된다.

## Authorization guard

## Execution context

## Role-based authentication

## Binding guards

## Setting roles per handler

## Putting it all together
