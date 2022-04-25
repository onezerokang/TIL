# Validation

서버에 전송된 데이터가 유효한지 검증하는 작업은 매우 중요하다. 정보를 제대로 검증하지 않으면 잘못된 정보가 저장되어 장애가 발생할 수 있다.
Nest는 class-validator와 class-transformer 패키지를 통해 간단하게 유효성 검사를 할 수 있다.

```
npm i class-validator class-transformer
```

데이터 검증을 하기 위해서는 `ValidationPipe`을 main.ts에 등록해주어 endpoint에서 잘못된 정보를 받지 않도록 한다.

```ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe());
  await app.listen(3000);
}
bootstrap();
```

검증을 위한 DTO class를 하나 만들어보자.

```ts
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsNotEmpty()
  password: string;
}
```

만약 해당 유저를 생성할 때 위 조건을 만족하지 못한다면 Nest는 400 Request를 응답할 것이다.

## ValidationPipeOptions

몇 가지 사용할만한 `ValidationPipeOptions`를 기록해본다.

- transform: DTO 클래스에 따라 유형이 지정된 객체로 자동변환한다. ex: "12" -> 12;
- disableErrorMessages: 오류 메시지를 출력하지 않는다.
- whitelist: 검증 규칙이 정의되지 않은 프로퍼티를 모두 제거하고 데이터를 넘긴다.
- forbidNonWhitelisted: whitelist와 사용되며 검증 규칙이 정의되지 않은 프로퍼티가 있을 경우 에러를 던진다.
- skipMissingProperties: 검증 데코레이터가 있고 IsOptional이 아닌 프로퍼티가 객체에 없어도 에러를 던지지 않는다.
- forbidUnknownValues: 알 수 없는 객체의 유효성을 검사하려는 시도가 즉시 실패합니다.
