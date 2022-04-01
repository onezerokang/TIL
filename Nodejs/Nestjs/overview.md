# Overview

Nestjs는 Noejs를 기반 웹 API 프레임워크다.
Nestjs는 Express 또는 Fastify 프레임워크 위에서 동작하며 기본으로 설치할 시 Express를 사용한다.
Nodejs와 그를 기반으로 하는 많은 프레임워크는 자유도가 높아 유연하지만, 프로젝트의 구조가 커질 수록 유지보수 하기 어려워진다는 단점이 있다.
실제로 필자도 Express로 프로젝트를 1년 가까이 했는데 서로 코딩스타일이 달라, 서로의 코드를 읽고 유지보수하는데 어려움을 겪었다.
하지만 Nest.js는 정해진 구조와 규칙을 제공하기에 일관되게 프로그래밍을 할 수 있다.

## Module

Nest.js는 비슷한 기능, 자원을 처리하는 코드를 모듈로 캡슐화한다.
모듈은 API를 제공하는 `controller`와 비즈니스로직이 있는 `service`로 구성 돼 있다.
또한 모듈은 다른 모듈의 기능이 필요할 때 import하여 사용할 수 있다.

```ts
@Module({
  imports: [ProductModule],
  controllers: [SellerController],
  provider: [SellersService],
})
export class SellerModule {}
```

## Controller

컨트롤러는 express로 치면 `router`와 비슷하다.
REST API로 경로를 정의하고, 해당 경로로 요청이 왔을 때 비즈니스 로직을 실행시키고 응답을 보낸다.

```ts
@Controller("seller")
export class SellersController {
  constructor(private readonly sellersService: SellersService) {}

  @Get()
  async findAll() {
    return await this.sellersService.findAll();
  }

  @Post()
  async create(@Body sellerDto: CreateSellersDto) {
    return await this.sellersService.create(sellerDto);
  }
}
```

## Provider

프로바이더는 다른 컨트롤러나 프로바이더에 의존성 주입을 할 수 있다.
`@Injectable()` 데코레이터를 사용하면 해당 인스턴스는 Nestjs에 의해 다른 모듈로 주입될 수 있다.
Nestjs는 Provider 객체를 인스턴스화 하고 필요할 때 인스턴스를 주입시킨다.
이로 인해 개발자는 코드의 재사용성을 높일 수 있다.

```ts
@Injectable()
export class SellersService {
  async findAll(): sellersDto[] {
    return await Seller.find();
  }
  async create(sellerDto: CreateSellersDto) {
    const seller = await new Seller(sellerDto).save();
    return seller;
  }
}
```

> 출처
> https://medium.com/daangn/typescript%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EC%84%9C%EB%B9%84%EC%8A%A4%EA%B0%9C%EB%B0%9C-73877a741dbc > https://wikidocs.net/147787
