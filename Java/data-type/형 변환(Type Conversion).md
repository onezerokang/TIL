# 형 변환(Type Conversion)

## 1. 개요

형 변환이란 데이터 타입을 변경시키는 작업이다. 자바에서는 서로 다른 타입끼리 연산을 수행할 수 없기에 형 변환을 사용하여 자료형을 일치시킨다. 형 변환의 종류로는 Type Promotion과 Type Casting이 있다.

## 2. Type Promotion vs Type Casting

- **Type Promotion**:
  - 묵시적 형 변환, 자동 형 변환
  - 데이터의 허용 범위가 작은 타입에서 큰 타입으로 변환할 때
    ```java
    int a = 10;
    long b = a; // type promotion
    ```
- **Type Casting**:
  - 명시적 형 변환, 강제 형 변환
  - 데이터의 허용 범위가 큰 타입에서 작은 타입으로 변환할 때
    ```java
    long a = 10L;
    int b = (int)a; // type casting
    ```

## 3. Type Promotion의 종류

### 3.1. 정수간의 연산

- 정수간의 연산 시 피연산자의 범위가 모두 int이하라면 int로 자동 형 변환한다.
- 정수간의 연산 시 long 피연산자가 하나라도 있다면 모든 피연산자의 타입을 long으로 자동 형 변환한다.
- 따라서 정수를 int나 long으로 선언해두면 불필요한 형변환을 막아 성능을 향상시킬 수 있다.

실제로 불필요한 형 변환으로 인한 성능차이를 확인해보기 위해 테스트 코드를 작성해봤다. 차이가 엄청나게 크지는 않았지만 형 변환이 발생한 연산이, 발생하지 않은 연산보다 더 많은 시간이 걸리는 것을 확인할 수 있었다.

```java
@DisplayName("int 타입과 long 타입의 연산으로 인한 불필요한 형변환이 발생하는 연산")
@Test
void typePromotion1() {
    long start = System.currentTimeMillis();

    long num = 0;
    for (int i = 0; i < Integer.MAX_VALUE; i++) {
        num += i;
    }

    long end = System.currentTimeMillis();
    System.out.println(end - start); // 661
}

@DisplayName("long 타입간의 연산으로 형 변환이 없는 연산")
@Test
void typePromotion2() {
    long start = System.currentTimeMillis();

    long num = 0;
    for (long i = 0; i < Integer.MAX_VALUE; i++) {
        num += i;
    }

    long end = System.currentTimeMillis();
    System.out.println(end - start); // 610
}
```

### 3.2. 실수간의 연산

- 실수간의 연산 시 모든 피연산자의 타입이 같다면, 해당 타입으로 연산을 진행한다.
- 실수간의 연산 시 double 피연산자가 하나라도 있다면 모든 피연산자의 타입을 double로 자동 형 변환한다.
- 정수 타입과 실수 타입의 연산 시 실수 타입으로 자동 형 변환한다.

### 3.3. 문자열 연산

- '+' 연산 시 String 타입의 피연산자가 하나라도 있다면 모두 String으로 자동 형 변환한다.
- 이때 '+' 연산은 덧셈이 아닌 접합 연산으로 수행된다.
