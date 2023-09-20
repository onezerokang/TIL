# 33장 Java 8에서 변경된 것들은?

> 추가할 내용들
>
> - 매개 변수와 타입 추론
> - effectively final
> - 람다 표현식에서 예외가 발생하면
> - Method Reference
> - 자바에서 제공하는 함수형 인터페이스들
> - Stream 내용 추가하기
> - 자바에서 함수형 인터페이스를 사용해야 하는 이유

## 1. 함수형 인터페이스

함수형 인터페이스란 추상 메소드가 단 하나만 있는 인터페이스를 말한다.
이런 함수형 인터페이스는 @FunctionalInterface 어노테이션으로 선언할 수 있다.

```java
@FunctionalInterface
interface Calculate {
    int operation(int a, int b);
}
```

## 2. Lambda 표현식

람다 표현식은 함수형 인터페이스를 익명 클래스로 구현할 경우 가독성이 떨어지고, 불편하다는 단점을 보완하기 위해 만들어졌다.
때문에 람다 표현식은 익명 클래스로 전환이 가능하며, 익명 클래스는 람다 표현식으로 전환이 가능하다.

람다 표현식은 3 부분으로 구성되어 있다.

| 매개 변수 목록 | 화살표 토큰 | 처리 식 |
| -------------- | ----------- | ------- |
| (int x, int y) | ->          | x + y   |

스레드의 매개 변수로 넘겨지는 Runnable 인터페이스는 run 추상 메소드만을 갖는 함수형 인터페이스다.

```java
@FunctionalInterface
public interface Runnable {
    public abstract void run();
}
```

Runnable 인터페이스의 구현체를 만들 때, 해당 클래스를 재사용하지 않을 경우 아래와 같이 익명 클래스로 만들 수 있다.

```java
Runnable runnable = new Runnable() {
    @Override
    public void run() {
        System.out.println(Thread.currentThread().getName());
    }
}

new Thread(runnable).start();
```

위의 익명 클래스는 가독성이 떨어진다.
람다 표현식을 사용하면 보다 간결하게 작성할 수 있다.

```java
new Thread(() -> System.out.println(Thread.currentThread().getName())).start();
```

Thread 생성자의 매개 변수로 Runnable의 구현체를 넘겨야 하는데, 이를 람다 표현식을 활용하여 넘긴 것이다.

## 3. java.util.function 패키지

Java 8부터 java.util.function에서 함수형 인터페이스를 제공한다. 따라서 함수형 인터페이스가 필요할 때마다 일일이 구현하지 않아도 된다.

- **Predicate**: test() 메소드가 있으며, 두 개의 객체를 비교하고 boolean을 리턴한다. 추가로 and(), negate(), or()이라는 default 메소드가 구현되어 있으며, isEqual()이라는 static 메소드도 존재한다.
- **Supplier**: get() 메소드가 있으며, 리턴값은 generic으로 선언된 타입을 리턴한다.
- **Consumer**: accept()라는 매개 변수를 하나 갖는 메소드가 있으며, 리턴 값이 없다. 그래서 출력을 할 때처럼 작업을 수행하고 결과를 받을 일이 없을 때 사용한다. 추가로 andThen()이라는 default 메소드가 있는데, 순차적인 작업을 할 때 유용하게 사용될 수 있다.
- **Function**: apply()라는 하나의 매개 변수를 갖는 메소드가 있으며, 리턴 값도 존재한다. 이 인터페이스는 Function<T, R>로 정의되어 있어, Generic 타입을 두개 갖고 있다. T는 입력 타입, R은 리턴 타입을 의미한다. 즉, 변환을 할 때 이 인터페이스를 사용한다.
- **UnaryOperator**: apply()라는 하나의 매개 변수를 갖는 메소드가 있으며, 리턴 값도 존재한다. 단, 한 가지 타입에 대하여 결과도 같은 타입일 경우 사용한다.
- **BinaryOperator**: apply()라는 두개의 매개 변수를 갖는 메소드가 있으며, 리턴 값도 존재한다. 단, 한가지 타입에 대하여 결과도 같은 타입일 경우 사용한다.

## 4. Stream

자바에서 스트림은 컬렉션(연속된 정보)를 순차적으로 처리하는 데 사용한다.
만약 배열에서 스트림을 사용하려면 Arrays.stream() 메소드의 매개 변수로 배열을 넘겨주면 된다.

스트림은 다음과 같은 구조를 갖는다.

```java
list
    .stream() // 스트림 생성
    .filter(x -> x > 10) // 중개 연산
    .count(); // 종단 연산
```

- **스트림 생성**: 컬렉션의 목록을 스트램 객체로 변환한다. 여기서 스트림 객체는 java.util.stream 패키지의 Stream 인터페이스를 말한다.
- **중개 연산**: 생성된 스트림 객체를 사용하여 중개 연산 부분에서 처리한다. 하지만, 이 부분에서는 아무런 결과를 리턴하지 못한다.
- **종단 연산**: 중개 연산에서 작업된 내용을 바탕으로 결과를 리턴한다.

스트림에서 제공하는 연산의 종류는 다음과 같다.

- filter(pred): 데이터를 조건으로 거를 때 사용
- map(mapper): 데이터를 특정 데이터로 변환
- forEach(block): for 루프를 수행하는 것처럼 순회
- flatMap(flat-mapper): 스트림의 데이터를 잘게 쪼개서 새로운 스트림 제공
- sorted(comparator): 데이터 정렬
- toArray(array-factory): 배열로 변환
- any / all / noneMatch(pred): 일치하는 것을 찾음
- findFirst / Any(pred): 맨 처음이나 순서에 상관없는 것을 찾음
- reduce(binop) / reduce(base, binop): 결과를 취합
- collect(collector): 원하는 타입으로 데이터를 리턴

### 3.1. forEach()

```java
public class StudentForEachSample {
    public static void main(String[] args) {
        StudentForEachSample sample = new StudentForEachSample();

        List<StudentDto> students = new ArrayList<>();
        students.add(new StudentDto("요다", 43, 99, 10));
        students.add(new StudentDto("만두", 30, 71, 85));
        students.add(new StudentDto("건빵", 32, 81, 75));

        sample.printStudentNames(students);
    }

    private void printStudentNames(List<StudentDto> students) {
        students.stream().forEach(student -> System.out.println(student.getName()));
    }
}
```

### 3.2. map()

### 3.3. filter()

## 4. Method Reference

앞 절의 예제에서 forEach의 출력문장은 다음과 같이 처리할 수도 있다.

```java
forEach(System.out::println)
```

더블 콜론은 Method Reference라고 부른다.

- static 메소드 참조: ContainingClass::staticMethodName
- 특정 객체의 인스턴스 메소드 참조: containingObject::instanceMethoddName
- 특정 유형의 임의의 객체에 대한 인스턴스 메소드 참조: ContainingType::methodName
- 생성자 참조: ClassName:new

#### static 메소드 참조

다음 예제에서는 String의 스트림이기 때문에 forEach() 문장 안에서 String을 제공한다.
그래서 printResult() 메소드에서는 String 값을 매개 변수로 받기 때문에 이처럼 참조해서 사용할 수 있다.

```java
public class MethodReferenceSample {
    public static void main(String[] args) {
        MethodReferenceSample sample = new MethodReferenceSample();
        String[] stringArray = {"요다", "만두", "건빵"};
        sample.staticMethodReference(stringArray);
    }
    private static void printResult(String s) {
        System.out.println(s);
    }

    private void staticMethodReference(String[] stringArray) {
        Stream.of(stringArray).forEach(MethodReferenceSample::printResult);
    }
}
```

## 특정 객체의 인스턴스 메소드 참조

인스턴스 참조는 System.out::println과 같이 System 클래스에 선언된 out 변수가 있고, 그 out 변수에 있는 println 메소드를 호출하는 것처럼 "변수에 선언된 메소드 호출"을 의미한다.

## 특정 유형의 임의의 객체에 대한 인스턴스 메소드 참조

```java
private void objectReference(String[] stringArray) {
    Arrays.sort(stringArray, String::compareToIgnoreCase); // 임의 객체 참조
    Arrays.asList(stringArray).stream().forEach(System.out::println); // 인스턴스 메소드 참조
}
```

## 생성자 참조

생성자도 임의의 인터페이스를 통해서 만들 수 있다.

```java
interface MakeString {
    String fromBytes(char[] chars);
}

private void createInstance() {
    MakeString makeString = String::new;
    char[] chars = {'g', 'o', 'd', 'o', 'f', 'j', 'a', 'v', 'a'};
    String madeString = makeString.fromBytes(chars);
    System.out.println(madeString);
}
```
