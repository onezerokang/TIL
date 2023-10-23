# BigDecimal

## 1. 개요

BigDecimal은 금융 관련 연산 같이 오차가 발생해서 안되는 상황에 사용되는 타입이다. float, double과 BigDecimal을 간단하게 비교해보자(float과 double에 대한 자세한 내용은 [여기](/Java/data-type/float%20vs%20double.md)를 참고하세요).

- **내부 표현 방식**:
  - **BigDecimal**: 수를 정수(unscaled value)와 scale로 나눠서 표햔한다. 예를 들어 1.23의 정수는 123이고 scale은 2다.
  - **float & double**: 부동 소수점 표현에 따라 표현한다.
- **정밀도**:
  - **BigDecimal**: 임의 정밀도(메모리의 제한 내에서 원하는 만큼의 정밀도)를 갖는다.
  - **float & double**: 각각 32비트, 64비트 수로 표현하여 값의 범위나 정밀도에 제한이 있다.
- **속도**:
  - **BigDecimal**: 무제한 숫자의 길이와 복잡한 연산 처리로 인해 기본 타입 연산에 비해 느리다.
  - **float & double**: 기본 타입의 데이터기 때문에 연산 속도가 빠르다.

## 2. 예시

예를 들어 1.03 달러에서 42센트만큼 사용했을 때, 남은 돈을 구하는 코드를 작성해보자.

```java
double a = 1.03;
double b = 0.42;

System.out.println(a - b); // 0.6100000000000001
```

하지만 BigDecimal을 사용하면 정확한 계산 결과를 반환한다.

```java
BigDecimal a = new BigDecimal("1.03");
BigDecimal b = new BigDecimal("0.42");

System.out.println(a.subtract(b)); // 0.61
```

## 3. BigDecimal이 정밀도 높은 연산을 할 수 있는 이유

BigDecimal은 정수형인 unscaled value와 소수점 오른쪽의 자리수를 나타내는 32비트 정수인 scale로 구성된다. 예를 들어 1.23의 unscaled value는 123이고 scale은 2가 된다.

BigDecimal가 연산하는 과정은 다음과 같다.

1. 정수 값(unscaled value)과 정밀도(scale)를 나눠서 저장한다. 예를 들어 1.23의 경우 정수 값은 123이고 scale은 2다.
2. 정수 값에 연산을 수행하고 정밀도를 적용하여 최종 결과를 나타내어 정확한 계산을 한다.

## 4. BigDecimal 연산 방법

### 4.1. 사칙 연산

```java
BigDecimal a = new BigDecimal("7");
BigDecimal b = new BigDecimal("3");

// 더하기
System.out.println(a.add(b));

// 빼기
System.out.println(a.subtract(b));

// 곱하기
System.out.println(a.multiply(b));

// 나누기
System.out.println(a.divide(b)); // ArithmeticException

// 나머지
System.out.println(a.remainder(b));

// 절대값
System.out.println(a.abs());

// 최대 값, 최소값
System.out.println(a.max(b));
System.out.println(a.min(b));

// 부호 변환
System.out.println(a.negate());
```

### 4.2. 비교 연산

비교 연산에는 equals()와 compareTo()를 사용할 수 있다. 두 메서드의 차이는 다음과 같다.

- **equals()**: unscaled value와 scale을 모두 비교한다.
- **compareTo()**: 두 객체의 숫자값만 비교한다. 따라서 소수점 맨 끝의 0을 무시하고 비교하고 싶다면 compareTo()를 사용해야 한다.

```java
BigDecimal a = new BigDecimal("1.23");
BigDecimal b = new BigDecimal("1.230");

System.out.println(a == b); // false: 메모리 주소 비교

System.out.println(a.equals(b));; // scale까지 비교

System.out.println(a.compareTo(b) == 0); // 숫자만 비교
```

## 5. 소수점 처리 전략

BigDecimal의 소수점 처리는 java.math 패키지의 RoundingMode Enum 클래스가 사용된다.

```java
public enum RoundingMode {
    // 0에서 멀어지는 방향으로 올림
    UP(BigDecimal.ROUND_UP),

    // 0에서 가까워지는 방향으로 내림
    DOWN(BigDecimal.ROUND_DOWN),

    // 양의 무한대를 향해서 올림
    CEILING(BigDecimal.ROUND_CEILING),

    // 음의 무한대를 향해서 내림
    FLOOR(BigDecimal.ROUND_FLOOR),

    // 반올림(사사오입)
    HALF_UP(BigDecimal.ROUND_HALF_UP),

    // 반올림(오사육입)
    HALF_DOWN(BigDecimal.ROUND_HALF_DOWN),

    // 반올림(오사오입)
    HALF_EVEN(BigDecimal.ROUND_HALF_EVEN),

    // 소수점 처리를 하지 않음
    // 연산의 결과가 소수일 경우 ArithmeticException 발생
    UNNECESSARY(BigDecimal.ROUND_UNNECESSARY);

    // ... 생략
}
```

## 6. 주의 사항

### 6.1. double 생성자 대신 String 생성자 사용하기

double은 근사값을 담고 있어 이를 사용해 BigDecimal 객체를 생성하면 정확한 값이 들어가지 않는다. 따라서 String 생성자나 BigDecimal의 valueOf 메서드를 사용해야 한다.

```java
new BigDecimal(1.12); // wrong
new BigDecimal("1.12"); // 1.12
BigDecimal.valueOf(1.12); // 1.12
```

### 6.2. 소수점 처리 전략 설정하기

소수점 처리를 하지 않을 경우 무한 소수 발생 시 ArithmeticException이 발생한다.

### 6.3. 동등성 비교 시 compareTo()와 equals() 사용을 구분하기

- equals(): 정수값(unscaled value)와 정밀도(scale)을 모두 비교
- compareTo(): 숫자값만 비교

## 7. 참조

- Effective Java - Item 60
- [BigDecimal A to Z: 정확한 계산을 위한 숫자 처리 클래스](https://dev.gmarket.com/75)
- [BigDecimal이라는 라이브러리가 존재하는 이유는 뭘까?](https://golf-dev.tistory.com/84#recentComments)
- [BigDecimal이란?](https://github.com/wjdrbs96/Today-I-Learn/blob/master/Java_God/%EA%B8%B0%ED%83%80/BigDecimal%EC%9D%B4%EB%9E%80%3F.md)
