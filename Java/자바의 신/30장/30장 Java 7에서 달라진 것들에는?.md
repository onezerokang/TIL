# 30장 Java 7에서 달라진 것들에는?

!제네릭 파트 보완 필요

## 숫자 표시 방법 보완

- 숫자 앞에 '0b'를 붙여 2진수 표현 추가
- 숫자 사이에 '\_'를 넣어 가독성 개선

```java
// 진법
int decVal = 1106; // 10진수
int octVal = 02122; // 8진수
int hexVal = 0x452; // 16진수
int binVal = 0b10001010010; // 2진수(java 7부터 추가)

// '_'를 넣어 가독성 개선
int jdk6 = 1000000000
int jdk7 = 1_000_000_000
```

## switch문에서 String 사용

Java 6까지는 swtich-case 문에 정수형만 사용가능했지만, Java 7부터 문자열을 넣을 수 있게 되었다.
단 문자열이 null인 경우 NullPointerException이 발생하니 꼭 null 체크를 해야 한다.

## 제네릭을 쉽게 사용할 수 있는 Diamond

제네릭을 사용할 때 생성자에 타입을 명시하지 않고 '<>'(Diamon)를 사용해주면 된다.

```java
// Java 6
HashMap<String, Integer> map = new HashMap<String, Integer>();

// Java 7
HashMap<String, Integer> map = new HashMap<>();
```

## 예외 처리시 다중 처리 가능

Java 7부터 catch 블록에서 처리하는 방식이 동일하다면 하나의 catch 블록에서 다중 예외를 처리할 수 있게 되었다.

```java
// Java 6
Scanner scanner = null;
try {
    scanner = new Scanner(new File(fileName), encoding);
    System.out.println(scanner.nextLine());
} catch(IllegalArgumentException iae) {
    iae.printStackTrace();
} catch(FileNotFoundException ffe) {
    ffe.printStackTrace();
} catch(NullPointerException npe) {
    npe.printStackTrace();
} catch(Exception e) {
    e.printStackTrace();
} finally {
    if(scanner != null) {
        scanner.close;
    }
}

// Java 7
Scanner scanner = null;
try {
    scanner = new Scanner(new File(fileName), encoding);
    System.out.println(scanner.nextLine());
} catch(IllegalArgumentException | FileNotFoundException | NullPointerException exception) {
    exception.printStackTrace();
} finally {
    if(scanner != null) {
        scanner.close;
    }
}
```

try-with-resource. Java 7에는 AutoCloseable 인터페이스 추가.
이 인터페이스를 구현한 클래스는 별도로 close()를 호출해 줄 필요가 없다.

```java
try (Scanner scanner = new Scanner(new File(fileName), encoding)) {
    System.out.println(scanner.nextLine());
} catch(IllegalArgumentException | FileNotFoundException | NullPointerException exception) {
    exception.printStackTrace();
}
```

finally 블록에서 scanner.close()를 해주지 않아도 된다.

AutoCloseable 인터페이스를 구현한 클래스는 try-with-resource 문장에서 사용할 수 있다.
많이 사용하는 클래스 중 AutoCloseable과 관련있는 클래스들은 다음과 같다.

- java.nio.channels.FileLock
- java.beans.XMLEncoder
- java.beans.XMLDecoder
- java.io.ObjectInput
- java.io.ObjectOutput
- java.util.Scanner
- java.sql.Connection
- java.sql.ResultSet
- java.sql.Statement
