# JIT 컴파일러

JIT(Just-In-Time) 컴파일러란 프로그램을 실행하기 전, C/C++ 처럼 전체를 컴파일 하는 대신, 인터프리터가 실행하다가, 인터프리터가 자주 사용하는 코드의 정보를 캐시에 담아두었다가 미리 꺼내서 실행하는 것이다.

초기 JVM은 바이트코드를 인터프리터 방식을 이용하여 실행했기에 속도가 느렸지만 JIT 컴파일 방식을 도입해 속도를 보완했다.

JVM은 내부적으로 어떤 메서드가 얼마나 자주 수행되는지를 확인하고 HotSpot이라고 판단하면 컴파일을 수행해놓는다.

## 참조

- 자바의 신 2권
- [JIT 컴파일 - 위키백과](https://ko.wikipedia.org/wiki/JIT_%EC%BB%B4%ED%8C%8C%EC%9D%BC)
- [[Java] JIT 컴파일러란?](https://velog.io/@mooh2jj/JIT-%EC%BB%B4%ED%8C%8C%EC%9D%BC%EB%9F%AC%EB%9E%80)
- [[Java] JIT 컴파일러란?](https://hyeinisfree.tistory.com/26)
