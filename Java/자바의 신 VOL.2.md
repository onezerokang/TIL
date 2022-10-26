# 자바의 신 VOL.2

## 가장 많이 쓰는 패키지는 자바랭

`java.lang`은 자바에서 공통적으로 자주 사용하는 기능을 모아둔 패키지로 별도로 import를 하지 않아도 사용할 수 있다.
다음은 자바랭에서 자주 사용하고 꼭 알아두어야 하는 기능들이다.

### 래퍼 클래스(Wrapper Class)

자바에서 간단한 계산을 할 때는 기본 자료형을 사용한다.
기본 자료형은 자바의 Heap이 아닌 Stack에 저장, 관리되는데 이로 인해 계산할 때 보다 빠른 처리가 가능하다.
하지만 다음과 같은 상황에서는 숫자를 처리할 때 기본 자료형이 아닌 참조자료형을 사용해야 한다.

- 매개변수를 참조자료형으로만 받는 메서드 처리
- 제네릭과 같이 기본자료형을 사용하지 않는 기능처리
- 클래스에 선언된 상수값을 사용하기 위함
- 문자열을 숫자로 숫자를 문자열로 쉽게 바꾸거나 진수변환을 하기 위함

이처럼 기본자료형의 데이터를 객체로 변환해야 할 때 사용하는 클래스를 래퍼 클래스라고 한다.
래퍼 클래스는 각 타입에 해당하는 데이터를 인자로 전달받아 객체로 만들어준다.

다음은 래퍼클래스의 종류이다.

- `Byte`
- `Short`
- `Integer`
- `Long`
- `Float`
- `Double`
- `Character`
- `Boolean`

다음은 래퍼클래스를 사용한 예시코드이다.

```java
public class Wrapper {
  public static void main(String args[]) {
    String value1 = "1";
    String value2 = "2";

    // parseInt는 기본자료형을 리턴하고 valueOf는 객체를 리턴한다.
    int int1 = Integer.parseInt(value1);
    int int2 = Integer.parseInt(value2);
    System.out.println(int1 + int2); // 3

    short short1 = Short.valueOf(value1);
    short short2 = Short.valueOf(value2);
    System.out.println(short1 + short2); // 3

    System.out.println(Byte.MAX_VALUE);
    System.out.println(Byte.MIN_VALUE);
  }
}
```

래퍼클래스는 참조자료형이지만 컴파일러에서 자동으로 형변환을 해주기 때문에 기본자료형 처럼 사용할 수 있다. 그렇기 때문에 위 예제에서 `Short.valueOf()`의 값이 객체임에도 더하기 연산자를 사용할 수 있는 것이다.

### System 클래스

System 클래스는 시스템에 대한 정보를 확인하는 클래스로 생성자가 없다.
다음은 System 클래스에서 사용할 수 있는 기능들이다.

- 시스템 속성관리
  - 설명: java.util 패키지에는 Hashtable을 상속받은 Properties 클래스가 있다. 자바 프로그램을 실행하면 Properties객체가 생성되며 그 값은 JVM내에서 꺼내서 사용할 수 있다.
  - `clearProperty(String key)`
    - 리턴 타입: static String
  - `getProperties()`
    - 리턴 타입 static Properties
  - `getProperty(String key)`
    - 리턴 타입: static String
  - `getProperty(String key String def)`
    - 리턴 타입: static String
  - `setProperties(Properties props)`
    - 리턴 타입: static void
  - `setProperty(String key, String value)`
    - 리턴 타입: static String
- 시스템 환경(Environment) 값 조회
  - 설명: 환경값은 OS나 장비에 관련된 값으로 값을 변경하지 못하고 읽기만 가능하다.
  - `getenv()`
    - 리턴 타입: static Map<String, String>
  - `getenv(String name)`
    - 리턴 타입: static String
- 현재 시간 조회
  - 설명: `currentTimeMillis()`는 현재 시간 조회를 위해 `nanoTime()`은 시간의 차이를 측정하기 위해 사용한다.
  - `currentTimeMillis()`
    - 리턴 타입: static long
  - `nanoTime()`
    - 리턴 타입: static long

이외에도 GC를 수행하거나 JVM을 종료하는 기능이 있지만 다룰일이 거의 없기 때문에 생략한다.

## 실수를 방지하기 위한 제네릭이라는 것도 있어요

제네릭(Generic)이란 클래스, 인터페이스, 메서드의 타입을 선언할 때 정의하는 것이 아닌 사용할 때 타입을 파라미터처럼 넘겨주는 것을 말한다.
제네릭을 사용했을 때 장점은 다음과 같다.

1. 잘못된 타입에러를 컴파일 단계에서 발견할 수 있다
2. 따로 타입체크와 형변환을 하지 않아도 된다.
3. 코드의 재사용이 쉬워진다.

다음은 타입 파라미터 컨벤션이다.

- T: Type
- E: Element
- K: Key
- V: Value
- N: Number

다음은 제네릭의 문법이다.

- 제네릭 클래스 & 제네릭 인터페이스 생성

```java
public class GenericClass<T>{}
public class GenericInterface<T, E>{}
```

- 제네릭 클래스와 제네릭 메서드

```java
public class GenericClass<T> {
  private T data;

  public void setData(T data) {
    this.data = data;
  }

  public T getData() {
    return data;
  }
}
```

제네릭 메서드는 클래스의 타입과는 별개의 타입을 갖는 메서드로 주로 정적 메서드에 사용된다.

### 와일드카드

와일드카드는 제네릭으로 들어올 수 있는 타입을 제한할 때 사용한다.

- `<?>`
  - 어떤 타입이든 들어올 수 있다
- `<? extends T>`
  - T혹은 T를 상속받은 자식타입이 들어올 수 있다
- `<? super T>`
  - T혹은 T의 부모타입이 들어올 수 있다.

## 자바랭 다음으로 많이 쓰는 애들은 컬렉션 - Part1(List)
