# Overview

Nestjs는 Nodejs은 Noejs를 기반으로 한 웹 API 프레임워크다.
Nestjs는 Express 또는 Fastify 프레임워크를 래핑하여 동작하며 기본으로 설치할 시 Express를 사용한다.
Nodejs와 그를 기반으로 하는 많은 프레임워크는 자유도가 높아 유연하지만, 프로젝트의 구조가 커질 수록 유지보수 하기 어려워진다.
실제로 필자도 Express로 프로젝트를 1년 가까이 했는데 작업하는 사람과, 코드가 늘어날수록 서로의 코딩 스타일을 이해하는데 어려움이 있었다.
하지만 Nest.js는 아키텍쳐를 제공하기에 일관된 프로그래밍을 할 수 있다.

## Module

Nest.js는 비슷한 기능, 자원을 처리하는 코드를 모듈로 캡슐화한다.
모듈은 API를 제공하는 `controller`와 비즈니스로직이 있는 `service`로 구성 돼 있다.
또한 모듈은 다른 모듈의 기능이 필요할 때 import하여 사용할 수 있다.

```ts
@Module({
  imports: [ProductModule],
  controllers: [SellerController],
  provider: [SellerService],
})
export class SellerModule {}
```

## Controller

컨트롤러는 express로 치면 `router`와 비슷하다.
REST API로 경로를 정의하고, 해당 경로로 요청이 왔을 때 비즈니스 로직을 실행시키고 응답을 보낸다.

```ts
@Controller("seller")
export class SellerController {
  constructor(private readonly sellerService: SellerService) {}

  @Get()
  async findAll() {
    return await this.sellerService.findAll();
  }

  @Post()
  async create(@Body sellerDto: CreateSellerDto) {
    return await this.sellerService.create(sellerDto);
  }
}
```

## Provider

프로바이더에 `@Injectable` 데코레이터를 붙이면 해당 객체는 Nestjs에 의해 다른 모듈로 주입될 수 있다.
Nestjs는 Provider 객체를 인스턴스화 하고 필요할 때 인스턴스를 주입시킨다. 따라서 개발자는 객체를 관리하지 않고
필요한 객체를 주입받아 사용할 수 있다.

> 출처
> https://medium.com/daangn/typescript%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EC%84%9C%EB%B9%84%EC%8A%A4%EA%B0%9C%EB%B0%9C-73877a741dbc > https://wikidocs.net/147787
