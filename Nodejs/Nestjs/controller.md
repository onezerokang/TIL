# Controller

컨트롤러는 요청을 받고 처리된 결과를 응답하는 인터페이스다.
직접 컨트롤러를 하나하나 만들 수 있지만, nest cli에서는 빠르게 만들 수 있는 커맨드를 제공한다.

```
nest g co [controller-name]
```

만약 co대신 resource를 입력하면 module, controller, service, entity, dto까지 생성해준다.

```
nest g resource [name]
```

## Routing

컨트롤러는 `@Controller` 데코레이터를 클래스에 사용하여 생성할 수 있다.

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

`@Controller` 데코레이터 안에 경로를 지정할 수 있는데 그럴 경우, 해당 경로는 컨트롤러의 basePath가 된다.
컨트롤러에서 HTTP method를 `@Get`, `@Post`, `@Put`, `@Patch`, `@Delete` 등의 데코레이터를 함수와 함께 선언하면
라우터가 만들어진다. 해당 데코레이터의 인자로는 경로를 넣어줄 수 있다.

_참고: Nestjs의 라우터 경로에서는 와일드카드를 사용할 수 있다._

## Request

Nest.js에서는 다음 데코레이터로 요청에 대한 정보를 가져올 수 있다.
`@Req`: Request 객체를 가져온다. Express를 기반해서 사용할 경우 express의 req객체와 같다.
`@Body`: request body를 가져온다.
`@Param(key?: string)`: path 파라미터를 가져온다.
`@Query`: querystring 값을 가져온다.

`@Param(key: string)`데코레이터를 사용할 때 key를 지정해주면 객체가 아닌 정확한 값을 가져올 수 있다.
파라미터가 여러개일 경우 한번에 객체로 받으면 Param의 타입이 any로 지정되기에 정확히 하나하나 가져오는 것이 일반적이다.

_객체로 받을 때_

```ts
@Get(':id/stories/:storyId')
getUserStory(@Param() params) {
  return params
}
```

_하나하나 받을 때_

```ts
@Get(':id/stories/:storyId')
getUserStory(@Param('id') userId: string, @Param('storyId') storyId: string) {
  return {userId, storyId}
}
```

## Response

Nestjs에서 객체, 배열을 return 하면 JSON으로 자동변한하여 응답합니다.
원시형 데이터를 return할 경우 JSON으로 변환하지 않습니다.
HTTP status code의 경우 기본적으로는 200을, Post요청일 경우 201을 반환합니다.

Express에서는 `res.status(200).json(result)`로 작성해주었던 부분을 return 키워드를 사용하는 것으로 줄일 수 있습니다.
그럼에도 express의 res 객체를 사용하고 싶은 경우 `@Res` 데코레이터를 사용하면 됩니다.

Response Header도 기본적으로 설정되어있지만 `@Header` 데코레이터를 사용하여 커스텀 할 수 있습니다.

## Redirect

`@Redirect(url: string, statusCode: number)` 데코레이터를 이용하여 리다이렉트를 할 수 있습니다.
status code를 설정하지 않았을 경우 기본 값은 302입니다.

```ts
@Get()
@Redirect('https://nestjs.com', 301)
```

만약 요청처리 결과에 따라 동적으로 리다이렉트를 하고 싶다면 `{"url": string, "statusCode": number}`를 반환해주면 됩니다.

```ts
@Get('docs')
@Redirect('https://docs.nestjs.com', 302)
getDocs(@Query('version') version) {
  if (version && version === '5') {
    return { url: 'https://docs.nestjs.com/v5/' };
  }
}
```

위 코드는 version이 5일 때 https://docs.nestjs.com/v5/로 이동합니다.

## Sub-domain routing

http://example.com
http://account.example.com
이라는 도메인을 운영하고 싶을 때는 `@Controller()`데코레이터의 인자로 host를 설정해주고, param이 필요할 경우 `@HostParam` 데코레이터를 사용하면 됩니다.

```ts
@Controller({ host: ":account.example.com" })
export class AccountController {
  @Get()
  getInfo(@HostParam("account") account: string) {
    return account;
  }
}
```

그리고 AppModule에서 먼저 처리할 컨트롤러를 앞 인덱스의 위치로 넣어주면 됩니다.

```ts
@Module({
  controllers: [AccountController, AppController]
})
```

## Payload

요청 시에 함께 오는 데이터(payload)는 **DTO(Data Transfer Object)**를 스키마를 생성해서 처리해주어야 합니다(TS를 사용하는 경우)
DTO는 데이터가 네트워크를 통해 전송되는 방법을 정의하는 개체이며 class로 정의하는 것이 좋습니다.
사실 인터페이스를 사용해도 좋지만 인터페이스는 컴파일 시 사라지기 때문에 Nestjs 런타임에서 이를 참조할 수 없습니다.

```ts
export class CreateUserDto {
  email: string;
  password: string;
}
```

이제 이 dto를 controller에서 사용할 수 있습니다.

```ts
@Post()
async create(@Body() createUserDto: CreateUserDto) {
  return 'This action adds a new user'
}
```

> _참조_
> 나중에 ValidationPipe와 함께 사용할 경우 수신되면 안되는 데이터를 필터링할 수 있습니다.
> 현재 예시의 경우 email과 password 데이터만 수신하게 됩니다.
