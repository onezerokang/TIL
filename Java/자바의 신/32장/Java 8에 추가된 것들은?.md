# 32장 Java 8에 추가된 것들은?

Java 8에서 추가되거나 변경된 것은 매우 많다. 그 중 꼭 알아야 하는 것은 다음과 같다.

- Lambda 표현식
- Functional 인터페이스
- Stream
- Optional
- 인터페이스의 기본 메소드(Default method)
- 날짜 관련 클래스들 추가
- 병렬 배열 정렬
- StringJoiner 추가

## Optional

Optional 클래스는 값을 포함할 수도 있고, 않을 수도 있는 컨테이너 객체다.
Opitonal의 목적은 null 값에 대한 대안을 제공하여 NullPointerException을 방지하는 것에 있다.

Optional 클래스는 new + 생성자로 인스턴스를 만들지 않는다.

다음은 Optional 클래스에서 인스턴스를 생성하는 방법이다.

```java
Optional<String> emptyString = Optional.empty(); // 데이터가 없는 Optional 객체 생성

String common = null;
Optional<String> nullableString = Optional.ofNullable(common); // 데이터에 null이 추가될 수 있는 상황

common = "common";
Optional<String> commonString = Optional.of(common); // 반드시 데이터가 들어갈 수 있는 상황
```

isPresent() 메소드를 사용하여 Optional 클래스가 비어 있는지 확인할 수 있다.

```java
System.out.println(Optional.of("present").isPresent()); // true
System.out.println(Optional.ofNullable(null).isPresent()); // false
```

get(), orElse(), orElseGet(), orElseThrow() 메소드를 활용하여 Optional 클래스의 값을 꺼낼 수 있다.

```java
String defaultValue = "default";
String result1 = data.get(); // 데이터가 없으면 null이 리턴된다.
String result2 = data.orElse(defaultValue); // 없을 경우 기본 갑을 리턴한다.
Supplier<String> stringSupplier = new Supplier<>() {
    @Override
    public String get() {
        return "GodOfJava";
    }
};

String result3 = data.orElseGet(stringSupplier); // Supplier<T> 인터페이스를 활용하는 방법으로 orElseGet() 메소드를 사용할 수 있다.

Supplier<Exception> exceptionSupplier = new Supplier<>() {
    @Override
    public Exception get() {
        return new Exception();
    }
};

String result4 = data.orElseThrow(exceptionSupplier); // 데이터가 없을 때 예외를 발생시킬 수 있다.
```

## Default method

인터페이스에 default 키워드와 함께 구현된 메소드를 default method라고 한다. default 메소드를 만든 이유는 하위 호환성 때문이다.

인터페이스에 선언된 메소드를 구현하지 않으면 오류가 발생하는데, 많은 사람들이 사용하고 있는 인터페이스에 새로운 메소드를 추가한다고 생각해보자. 그러면 해당 인터페이스를 사용하는 모든 프로그램에 오류가 발생할 것이다.

허나 default 메소드를 사용하여 메소드를 추가하면, 해당 인터페이스를 구현하는 모든 클래스가 해당 메소드를 구현하지 않아도 되도록 지원된다.

다음은 default 메소드를 갖는 인터페이스다.

```java
public interface DefaultStaticInterface {
    static final String name = "GodOfJavaBook";
    static final int since = 2023;
    String getName();
    int getSince();
    default String getEmail() {
        return name + "@godofjava.com";
    }
}
```

```java
public class DefaultImplementedChild implements DefaultStaticInterface {
    @Override
    public String getName() {
        return name;
    }

    @Override
    public int getSince() {
        return since;
    }
}
```

## 날짜 관련 클래스들

Java 8 이전에는 Date나 SimpleDateFormatter 클래스를 이용하여 날짜를 처리했다.
하지만 이 클래스들은 스레드 세이프하지 않고, 불변하지 않아 지속적으로 값이 변경 가능했다.
이러한 이슈로 Java 8부터는 java.time 패키지가 추가되었다.

시간을 나타내는 클래스는 Local, Offset, Zoned로 3가지 종류가 존재한다.

- Local: 시간대가 없는 시간. 예를 들어 '1시'는 어느 지역의 1시인지 구분되지 않는다.
- Offset: UTC(그리니치 시간대)와이ㅡ 오프셋을 가지는 시간. 한국은 "+09:00"
- Zoned: 시간대("한국 시간"과 같은 정보)를 갖는 시간, 한국의 경우 "Asia/Seoul"

요일을 표현할 수 있는 DayOfWeek enum 클래스가 생겼다.
MONDAY부터 SUNDAY까지 상수로 선언되어 있다.

getDisplayName() 메소드에 TextStyle과 Locale(지역정보)를 전달하여 해당 요일을 출력할 수 있다.

```java
public class DateSample {
    public static void main(String[] args) {
        DayOfWeek[] dayOfWeeks = DayOfWeek.values();
        Locale locale = Locale.getDefault();

        for (DayOfWeek day : dayOfWeeks) {
            System.out.print(day.getDisplayName(TextStyle.FULL, locale) + " ");
            System.out.print(day.getDisplayName(TextStyle.SHORT, locale) + " ");
            System.out.println(day.getDisplayName(TextStyle.NARROW, locale) + " ");
        }
    }
}
```

출력 결과는 다음과 같다.

```
월요일 월 월
화요일 화 화
수요일 수 수
목요일 목 목
금요일 금 금
토요일 토 토
일요일 일 일
```

## 병렬 배열 정렬(Parallel array sorting)

Java 8부터 Arrays 클래스에 parallelSort() static 메소드가 추가되었다.
parallelSort는 내부적으로 Fork-Join 프레임워크를 사용한다.
정렬해야 할 요소가 5000개를 넘는다면 일반 Arrays.sort() 보다 빠르다. CPU 더 사용한다.

```java
int[] intValues = new int[10];
// 배열 값 지정
Arrays.parallelSort(intValue);
```

## StringJoiner

StringJoiner는 문자열의 조인 작업을 보다 효율적으로 처리하기 위해 추가되었다.
문자열을 구분하는 구분자와, 접두사(prefix), 접미사(suffix)를 설정할 수 있다.

```java
String[] stringArray = new String[]{"StudyHard", "GodOfJava", "Book"};
StringJoiner joiner = new StringJoiner(",", "{", "}");

for (String s: stringArray) {
    joiner.add(s);
}
System.out.println(joiner); // {StudyHard,GodOfJava,Book}
```
