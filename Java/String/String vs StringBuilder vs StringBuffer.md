# String vs StringBuilder vs StringBuffer

## 1. String 클래스

자바의 String 클래스는 문자열을 생성하고 다루는 클래스다.

String 객체는 변경 불가능(immutable)하여 문자열에 값을 더할 때 기존 객체에 문자열을 추가하는 것이 아닌, 새로운 객체를 생성한다(기존 문자열 객체는 더 이상 참조되지 않는다면 GC에 의해 제거된다).

다음 코드를 보자.

```java
public static void main(String[] args) {
    String firstName = "철수";
    String lastName = "김";

    String fullName = firstName + lastName;
}
```

위 코드에서는 "철수" 객체에 "김" 객체를 더하는 것이 아닌 "철수김"이라는 객체를 새로 생성하게 된다.

## 2. StringBuilder & StringBuffer 클래스

StringBuilder와 StringBuffer는 변경 가능(mutable)한 객체다.

문자열을 더 하더라도 새로운 객체를 만드는 것이 아닌, 기존 객체에 문자열을 더한다. 때문에 String과 비교했을 때 메모리 효율과 시간 효율이 더 좋다.

다음은 StringBuilder를 사용하여 문자열을 더하는 예시다.

```java
public static void main(String[] args) {
    StringBuilder fullName = new StringBuilder();
    fullName.append("철수").append("김");
}
```

StringBuilder와 StringBuffer는 생성자와 메서드가 같은데,StringBuilder는 thread-safe하지 않은 반면 StringBuffer는 동기화되어 있어 thread-safe하다는 차이점이 있다.

JDK 5이상에서는 String 더하기 연산을 할 경우, 컴파일 시 해당 연산을 StringBuilder로 변환해준다. 하지만 for 루프와 같이 반복 연산을 할 때는 일일이 변환해주지 않으므로 StringBuilder나 StringBuffer 클래스를 사용해야만 한다.

### 2.2. equals

StringBuilder와 StringBuffer는 String과 다르게 equals 메서드가 오버라이딩되지 않아 등가비교연산자(==)로 비교한 것과 같은 결과를 얻는다.

```java
public static void main(String[] args) {
    StringBuilder sb1 = new StringBuilder("hello");
    StringBuilder sb2 = new StringBuilder("hello");
    System.out.println(sb1 == sb2); // false
    System.out.println(sb1.equals(sb2)); // false
}
```

## 3. 정리

- **String**: 짧은 문자열을 더할 때 사용한다.
- **StringBuffer**: 다중 스레드가 하나의 문자열 객체를 다룰 때 사용한다(애매할 때 사용해도 좋다).
- **StringBuilder**: thread-safe 여부와 상관 없는 프로그램을 개발할 때 사용한다.

## 4. 참조

- 자바 성능 튜닝 이야기 3장
- 자바의 신 15장
