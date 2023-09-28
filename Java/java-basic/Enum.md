# Enum

## 1. 개요

Enum이란 Enumeration의 약자로 열거 타입이라고도 한다.
열거 타입은 한정된 값만을 갖는 상수를 편리하게 관리하기 위해 사용된다.

열거 타입은 enum 키워드를 사용하여 선언할 수 있다.

```java
public enum Role {
    ADMIN,
    NORMAL,
    VIP
}
```

위의 Role을 열거 타입이라고 하고, ADMIN, NORMAL, VIP를 열거 상수라고 한다.

열거 타입 또한 참조형 데이터기에 변수에 저장할 수 있다.

```java
Role role1 = Role.VIP; // 참조 타입이기에 열거 상수는 열거 객체로 생성된다.
Role role2 = null; // 참조 타입이기에 null이 저장될 수 있다.
```

## 2. 꼭 enum을 사용해야 할까?

만약 열거 타입이 없다면 static final 키워드를 사용하여 상수를 하나 하나 만들어 관리해줘야 할 것이다.

```java
public class Role {
    public static final int ADMIN = 0;
    public static final int NORMAL = 1;
    public static final int VIP = 2;
}
```

이 경우 '타입 안정성(type safety)'이 떨어지게 된다(타입 안정성이란 프로그램 내에서 데이터의 타입을 예상한대로 사용하게 보장하는 특성을 말하며, 이를 위해 잘못된 데이터 타입의 사용 시 컴파일 오류를 발생시키는 등의 방법을 통해 잠재적인 오류를 미리 방지한다).

다음은 열거 타입이 아닌 static final로 상수를 관리했을 때 발생할 수 있는 문제다.

1. **잘못된 값 할당**: static final로 선언한 상수의 실제 값은 정수형이기 때문에 Role과 상관 없는 값이 들어올 수 있다.
   ```java
   int USER_ADMIN = 99; // Role과 전혀 상관 없는 값
   ```
2. **메서드 파라미터**: 메서드 파라미터로 role을 받을 때, 정의된 상수가 아닌 모든 정수형을 받을 수 있게 된다.

   ```java
   public void checkAdmin(int role) {
       // ... 검증 로직
   }
   checkAdmin(99); // Role과 전혀 상관 없는 값
   ```

3. **가독성**: 상수의 실제 값은 정수형이기 때문에 이 값을 보고 해당 값이 어떤 Role인지 쉽게 알 수 없다.

하지만 열거 타입을 사용한다면 위 문제점들이 해결된다.

## 3. JVM 메모리에 적재된 열거 타입

자바에서 열거 타입은 클래스이고, 상수를 인스턴스로 만들어 public static final 필드로 공개한다.
또한 열거 타입의 인스턴스는 런 타임에 한번만 생성되는 싱글톤 패턴을 사용한다.

이 부분은 JVM에 대해 더 공부해야 할 것 같다.

## 4. 열거 타입 메소드

모든 클래스가 Object 클래스를 상속하는 것처럼, 모든 열거 타입도 java.lang.Enum 클래스를 상속한다.
따라서 모든 열거 타입은 Enum 클래스의 메소드를 사용할 수 있다.

### 4.1. name

열거 객체가 갖고 있는 문자열을 반환한다.

```java
System.out.println(Role.ADMIN.name()); // ADMIN
```

### 4.2. ordinal

해당 열거 객체가 몇 번째 순서인지 반환한다.

```java
System.out.println(Role.VIP.ordinal()); // 2
```

### 4.3. compareTo

두 열거 객체간의 순번을 비교하여 상대적 순번 차이를 반환한다.

```java
System.out.println(Role.VIP.compareTo(Role.ADMIN)); // 2
```

### 4.4. valueOf

열거 객체의 상수명과 동일한 문자열을 입력받아, 일치하는 열거 객체를 반환한다.

```java
System.out.println(Role.valueOf("NORMAL")); // NORMAL
System.out.println(Role.valueOf("NORMAL2")); // IllegalArgumentException
```

### 4.5. values

열거 타입에 선언된 모든 열거 객체를 순번대로 배열에 담아 반환한다.

```java
System.out.println(List.of(Role.values())); //[ADMIN, NORMAL, VIP]
```

## 5. 열거 타입 필드

열거 타입의 열거 객체도 인스턴스이므로 인스턴스 필드를 갖을 수 있다. 이를 통해 상수와 연관된 추가적인 데이터를 상수 자체에 포함하여 관리할 수 있다.

일반적인 인스턴스 필드를 정의하는 것처럼, 인스턴스 필드를 명시하고 생성자를 정의해주면 된다. 이 때 각 열거 객체의 필드는 상수 옆에 괄호 ()를 사용하여 적어준다.

다음 예시에서는 회원 등급에 따른 UI 표기명과 할인율을 필드로 추가한 코드다.

```java
public enum Role {
    ADMIN("관리자", 10),
    NORMAL("일반 회원", 0),
    VIP("VIP", 20);

    private final String displayName;
    private final int discountRate;

    Role(String displayName, int discountRate) {
        this.displayName = displayName;
        this.discountRate = discountRate;
    }

    public String getDisplayName() {
        return displayName;
    }

    public int getDiscountRate() {
        return discountRate;
    }
}
```

## 6. 참조

- 자바의 신 13장 인터페이스와 추상클래스, enum
- [Enum 클래스](https://www.tcpschool.com/java/java_api_enum)
- [[Java] 열거 타입 (Enum)](https://hudi.blog/java-enum/)
- [Java Enum 활용기](https://techblog.woowahan.com/2527/)
