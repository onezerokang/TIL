# Enum

Enum이란 Enumeration의 약자로 열거 타입이라고도 한다.
열거 타입은 한정된 값만을 갖는 상수를 편리하게 관리하기 위해 사용된다(만약 열거 타입이 없다면?).

열거 타입은 enum 키워드를 사용하여 선언할 수 있다.

```java
public enum Role {
    ADMIN,
    NORMAL,
    VIP
}
```

위의 Role을 열거 타입이라고 하고, ADMIN, NORMAL, VIP를 열거 상수라고 한다.

열거 타입또한 참조형 데이터기에 변수에 저장할 수 있다.

```java
Role role1 = Role.VIP; // 참조 타입이기에 열거 상수는 열거 객체로 생성된다.
Role role2 = null; // 참조 타입이기에 null이 저장될 수 있다.
```

## JVM 메모리에 적재된 열거 타입

자바에서 열거 타입은 클래스고, 상수를 인스턴스로 만들어 public static final 필드로 공개한다.
또한 열거 타입의 인스턴스는 런 타임에 한번만 생성되는 싱글톤 패턴을 사용한다.

이 부분은 JVM에 대해 더 공부해야 할 것 같다.

## 열거 타입 메소드

모든 클래스가 Object 클래스를 상속하는 것처럼, 모든 열거 타입도 java.lang.Enum 클래스를 상속한다.
따라서 모든 열거 타입은 Enum 클래스의 메소드를 사용할 수 있다.

### name

열거 객체가 갖고 있는 문자열을 반환한다.

```java
System.out.println(Role.VIP.name()); // VIP
```

### ordinal

해당 열거 객체가 몇 번째 순서인지 반환한다.

```java
System.out.println(Role.VIP.name()); //
```

### compareTo

두 열거 객체간의 순번을 비교하여 상대적 순번 차이를 반환한다.

### valueOf

열거 객체의 상수명과 동일한 문자열을 입력받아, 일치하는 열거 객체를 반환한다.

### values

열거 타입에 선언된 모든 열거 객체를 순번대로 배열에 담아 반환한다.

## 열거 타입 필드

열거 타입의 열거 객체도 인스턴스이므로 인스턴스 필드를 갖을 수 있다. 이를 통해 상수와 연관된 추가적인 데이터를 상수 자체에 포함하여 관리할 수 있다.

## 참조

- 자바의 신 13장 인터페이스와 추상클래스, enum
- [Enum 클래스](https://www.tcpschool.com/java/java_api_enum)
- [[Java] 열거 타입 (Enum)](https://hudi.blog/java-enum/)
- [Java Enum 활용기](https://techblog.woowahan.com/2527/)
