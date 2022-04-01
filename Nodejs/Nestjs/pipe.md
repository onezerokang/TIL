# Pipe

파이프는 요청이 라우터 핸들러로 전환되기 전에 요청 객체를 변환할 수 있다.
파이프는 보통 두가지의 목적으로 사용된다.

- 인풋 데이터를 원하는 타입(형식)으로 변환
- 유효성 검사와 예외 처리

## Built-in pipes

@nestjs/common 패키지에는 다음과 같은 파이프가 내장 돼 있다.

- ValidationPipe
- ParseIntPipe
- ParseFloatPipe
- ParseBoolPipe
- ParseArrayPipe
- ParseUUIDPipe
- ParseEnumPipe
- DefaultValuePipe

`Parse*` 로 시작하는 파이프는 전달된 인자의 타입을 검사하는 파이프이다.
인자의 값은 문자열로 전달되는데 ParseIntPipe은 전달된 인자가 정수인지 검사하고, 정수로 변환이 가능하면 정수로 변환시킨다.
정수가 아닐 시 예외를 발생시킨다.

```ts
@Get('/:id')
findOne(@Param('id', ParseIntPipe) id: number) {
  console.log(typeof id) // number
}
```

클래스를 전달하지 않고 직접 인스턴스를 생성하여 전달할 수 있는데, 이 경우 파이프 내부 동작 방식을 바꾸고 싶을 때 사용한다.

```ts

@Get('/:id')
findOne(@Param('id', new ParseIntPipe({ errorHttpStatusCode: HttpStatus.NOT_ACCEPTABLE })) id: number) {
console.log(typeof id) // number
}

```

`DefaultValuePipe`은 인자에 기본 값을 설정할 때 사용한다.

## Binding pipes

## Custom pipes

## Schema based validation

## Object schema validation

## Binding validation pipes

## Class validator

## Global scoped pipes

## The built-in ValidationPipe

## Transformation use case

## Providing defaults
