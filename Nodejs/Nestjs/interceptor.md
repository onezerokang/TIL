# Interceptors

인터셉터는 요청과 응답을 가로채서 변형할 수 있는 컴포넌트다.
인터셉터는 AOP의 영향을 많이 받았다. 인터셉터를 이용하면 다음과 같은 기능을 수행할 수 있다.

- 메서드 실행 전/후 추가 로직 바인딩
- 함수에서 반환된 결과를 변환
- 함수에서 던져진 예외를 변환
- 기본 기능의 동작을 확장
- 특정 조건에 따라 기능을 완전히 재정의(예: 캐싱)

예시

```ts
import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
} from "@nestjs/common";
import { Observable } from "rxjs";
import { tap } from "rxjs/operators";

@Injectable()
// NestInterceptor 구현
export class LoggingInterceptor implements NestInterceptor {
  // intercept함수 구현해야 하며 ExecutionContext와 CallHandler를 인자로 받음
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    //   요청 처리 전
    console.log("Before...");

    // 요청 처리 후
    const now = Date.now();
    return next
      .handle()
      .pipe(tap(() => console.log(`After... ${Date.now() - now}ms`)));
  }
}
```
