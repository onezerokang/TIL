# Pipe

파이프는 `Injectable()` 데코레이터와 선언되고, `PipeTransform` 인터페이스를 구현한 클래스다.
파이프는 보통 두가지의 목적으로 사용된다.

- 인풋 데이터를 원하는 타입(형식)으로 변환
- 유효성 검사와 예외 처리

위 두가지 경우 파이프는 컨트롤러의 인자에서 사용된다. Nest는 컨트롤러의 메서드가 호출되기 전 파이프를 실행한다.
파이프는 메서드의 인자를 수신하고 이에 대한 로직을 실행한다. 이후 변환된 인자를 메서드에 넘겨주고 메서드를 호출한다.

## Built-in pipes

`@nestjs/common` 패키지에는 8개의 파이프가 내장 돼 있다.

- ValidationPipe
- ParseIntPipe
- ParseFloatPipe
- ParseBoolPipe
- ParseArrayPipe
- ParseUUIDPipe
- ParseEnumPipe
- DefaultValuePipe

## Binding pipes

파이프를 사용하려면 파이프 클래스의 인스턴스를 적절한 컨택스트에 바인딩해야 한다.
아래 예제는 메서드의 매개변수에 바인딩한다.

```ts
@Get('/:id')
findOne(@Param('id', ParseIntPipe) id: number) {
  console.log(typeof id) // number
}
```

위 예제에서는 인스턴스가 아닌 클래스를 전달하여, 인스턴스화를 프레임워크에 위임하였다.
만약 파이프 내부 동작 방식을 변형해서 사용하고 싶다면 직접 인스턴스를 생성하여 전달하면 된다.

```ts

@Get('/:id')
findOne(@Param('id', new ParseIntPipe({ errorHttpStatusCode: HttpStatus.NOT_ACCEPTABLE })) id: number) {
console.log(typeof id) // number
}

```

## Custom pipes

## Schema based validation

## Object schema validation

## Binding validation pipes

## Class validator

## Global scoped pipes

## The built-in ValidationPipe

## Transformation use case

## Providing defaults
