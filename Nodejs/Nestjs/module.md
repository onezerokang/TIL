# Modules

모듈: 한가지 일만 수행하는 컴포넌트가 아닌, 유사한 기능을 모아서 작성한 좀 더 큰 작업을 수행하는 단위이다.
예를 들면 로그인 함수, 로그 아웃 함수, 회원 가입 함수들은 User에 대한 작업이라는 공통점이 있기 때문에 UserModule로 묶을 수 있다.
Nestjs는 하나의 루트 모듈(AppModule)이 존재하고 다른 모듈들로 구성되어 있다.

`@Module` 데코레이터를 사용해서 모듈을 만들 수 있다. `@Module` 데코레이터의 인자로 `ModuleMetadata`를 받는다.

## Shared Modules

import: 이 모듈에서 사용하기 위한 프로바이더를 가지고 있는 다른 모듈을 가져온다.
controllers/providers: 모듈 전반에서 사용할 컨트롤러와 프로바이더를 가져온다.
export: 이 모듈에서 제공하는 컴포넌트를 다른 모듈에서 import 해야 할 때 export 해주어야 한다. export를 선언해주면 public 인터페이스 또는 API로 간주된다.

## Module re-exporting

가져온(import)한 모듈을 다시 내보낼 수 있다(export).
아래 예시에서는 CommonModule, CoreModule, AppModule이 존재한다.
AppModule에서 CommonModule과 CoreModule를 사용하기 위해서는 둘다 imports 해야 하지만
CoreModule에서 CommonModule을 imports 한뒤 re-exports하면 AppModule에서는 CoreModule만 imports해도 CommonModule를 사용할 수 있다.

**CommonModule.ts**

```ts
@Module({
  providers: [CommonService],
  exports: [CommonService],
})
export class CommonModule {}
```

**CommonService.ts**

```ts
@Injectable()
export class CommoneService {
  hello(): string {
    return "Hello World";
  }
}
```

**CoreModule.ts**

```ts
@Module({
  imports: [CommonModule],
  exports: [CommonModule],
})
export class CoreModule {}
```

**AppModule.ts**

```ts
@Module({
  imports: [CoreModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

_모듈은 프로바이더 처럼 주입해서 사용할 수 없다. 모듈간 순환 종속성이 발생하기 때문이다_

## Global Modules

Nest.js는 모듈 범위에서 프로바이더를 캡슐화 한다. 따라서 어떤 모듈안에 있는 프로바이더를 주입받기 위해서는
먼저 모듈을 가져와야 한다. 허나 전역적으로 사용해야 하는 모듈이 있을 경우 `@Global` 데코레이터를 사용하면 된다.
전역 모듈은 루트모듈이나 코어모듈에서 한 번만 등록해야 한다.

```ts
@Global()
@Module({
  providers: [CommonService],
  exports: [CommonService],
})
export class CommonModule {}
```

허나 전역 모듈을 많이 만들면 응집도가 떨어지기에 꼭 필요한 모듈만 전역으로 만들어야 한다.

## Dynamic Modules

Consuming Module에서 Host Module을 생성할 때 동적으로 값을 결정하는 모듈.
ex) 로컬 서버, 테스트 서버, 배포 서버에서 다른 환경변수를 사용하게 한다.

먼저 동적 모듈을 먼저 만들 것이다. 데이터베이스 모듈을 만들고, forRoot이라는 정적 메서드를 만들어준다.
forRoot의 인자로는 Consuming Module에서 설정할 수 있는 값을 받아준다.
그리고 해당 설정을 적용한 후 데이터 베이스 모듈을 리턴해주면 App Module에서 다이나믹 모듈을 사용할 수 있다.

**Database Module**

```ts
import { Module, DynamicModule } from "@nestjs/common";
import { createDatabaseProviders } from "./database.providers";
import { Connection } from "./connection.provider";

@Module({
  providers: [Connection],
})
export class DatabaseModule {
  static forRoot(entities = [], options?): DynamicModule {
    const providers = createDatabaseProviders(options, entities);
    return {
      module: DatabaseModule,
      providers: providers,
      exports: providers,
    };
  }
}
```

**App Module**

```ts
import { Module } from "@nestjs/common";
import { DatabaseModule } from "./database/database.module";
import { User } from "./users/entities/user.entity";

@Module({
  imports: [DatabaseModule.forRoot([User])],
  exports: [DatabaseModule],
})
export class AppModule {}
```
