# Checked Exception vs Unchecked Exception

## Exception이란

Exception(예외)란 프로그램 실행 중 발생할 수 있는 예상하지 못한 상황이나 조건을 말한다.
예외를 제대로 처리하지 못하면 프로그램이 비정상적으로 종료될 수 있다.

## Error

## Checked Exception

Checked Exception이란 컴파일러가 체크하는 예외를 말한다. 만약 Checked Exception에 대해 예외 처리하지 않았다면 컴파일 에러가 발생한다.

다음은 자주 발생하는 Checked Exception이다.

- FileNotFoundException
- SQLException

## Unchecked Exception

Unchekced Exception이란 런타임(프로그램 실행 중)에서 발생할 수 있는 예외를 말한다. 예외 처리를 해주지 않아도 컴파일 에러는 발생하지 않지만, 프로그램이 비 정상적으로 종료될 수 있다.

다음은 자주 발생하는 Unchecked Exception이다.

- NullPointerException
- ArrayIndexOutOfBoundsException

## Exception handling

## 참조

- 자바의 신 14장
- [즐거운 자바: 예외(Exception) 처리하기](https://www.inflearn.com/course/%EC%A6%90%EA%B1%B0%EC%9A%B4-%EC%9E%90%EB%B0%94)
