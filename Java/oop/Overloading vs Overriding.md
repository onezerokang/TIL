# Overloading vs Overriding

자바를 공부하다보면 오버로딩과 오버라이딩이라는 개념을 접하게 된다.
이름이 비슷한 두 개념을 헷갈리지 않는 것이 중요하기 때문에 어떤 차이점을 갖고 왜 사용하는지 정리해보겠다.

## 메소드 시그니쳐

메소드 시그니쳐는 **메소드 매개변수의 순서와 타입**을 의미한다. 만약 두 메소드가 매개변수의 순서와 타입이 같다면, 해당 메소드들의 시그니쳐는 같다고 할 수 있다.

- **오버로딩**: 메소드 시그니쳐가 다를 경우 메소드 이름이 같더라도 다른 메소드로 취급하는 것을 의미한다.
- **오버라이딩**: 은 메소드 시그니쳐가 같은 부모 클래스의 메소드를 재정의하는 것이다.

## Overloading

오버로딩은 메소드 시그니쳐가 다를 경우 메소드 이름이 같더라도 다른 메소드로 취급하는 것을 의미한다. 이를 통해 같은 이름의 메소드를 여러개 정의할 수 있다. 만약 자바에서 오버로딩을 지원하지 않았다면 매개변수의 타입이나 개수를 신경쓰며 메소드를 호출해야 했을 것이다.

println() 메소드는 같은 메소드명으로 여러개의 매개변수 타입을 처리할 수 있다.

- println()
- println(boolean x)
- println(char x)
- println(char[] x)
- println(double x)
- println(float x)
- println(int x)
- println(long x)
- println(Object x)
- println(String x)

오버로딩된 메소드는 컴파일 시 명시된 인자의 타입의 기준으로 호출된다.

## Overriding

오버라이딩은 부모 클래스의 메소드를 재정의하는 것을 의미한다. 오버라이딩을 하기 위해서는 메소드명과 메소드 시그니쳐가 동일해야 한다. 접근제어자의 경우 범위가 더 넓어질 수는 있지만 좁아질 수는 없다.

오버라이딩된 메소드는 런타임 단계에서 부모 메소드와 시그니처 동일성을 검증한다.

@Override 어노테이션을 활용하여 컴파일러에게 해당 메소드가 부모 메소드를 오버라이딩했다는 것을 알리며, 잘못된 오버라이딩을 시도할 경우 컴파일 에러를 발생시킬 수있다.

## 참조

- 자바의신
- [[java] 오버로딩과 오버라이딩](https://colinch4.github.io/2021-06-09/%EC%98%A4%EB%B2%84%EB%A1%9C%EB%94%A9%EA%B3%BC_%EC%98%A4%EB%B2%84%EB%9D%BC%EC%9D%B4%EB%94%A9/)