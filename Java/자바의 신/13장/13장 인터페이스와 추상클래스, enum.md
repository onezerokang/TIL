# 13 인터페이스와 추상클래스, enum

## enum 클래스라는 상수의 집합도 있다

enum 클래스는 상수의 집합이다.

```java
public enum OverTimeValues {
    THREE_HOUR,
    FIVE_HOUR,
    WEEKEND_FOUR_HOUR,
    WEEKEND_EIGHT_HOUR;
}
```

enum 클래스에 있는 상수들은 지금까지 살펴본 변수들과 다르게 별도로 타입이나 값을 지정할 필요가 없다.

enum 클래스를 효과적으로 사용하는 방법은 switch문에서 사용하는 것이다.

```java
public class OverTimeManager {
    public static void main(String[] args) {
        OverTimeManager overTimeManager = new OverTimeManager();
        int myAmount = overTimeManager.getOverTimeAmount(OverTimeValues.THREE_HOUR);
        System.out.println(myAmount);
    }

    public int getOverTimeAmount(OverTimeValues value) {
        int amount = 0;
        System.out.println(value);

        switch (value) {
            case THREE_HOUR:
                amount = 18000;
                break;
            case FIVE_HOUR:
                amount = 30000;
                break;
            case WEEKEND_FOUR_HOUR:
                amount = 40000;
                break;
            case WEEKEND_EIGHT_HOUR:
                amount = 60000;
                break;
        }
        return amount;
    }
}
```

별도의 생성자도 필요 없고, 그냥 enum을 넘겨주는 것이 아니다.

enum 타입은 enum 클래스이름.상수이름을 지정함으로써 클래스의 객체 생성이 완료된다고 생각하면 된다.

```java
int myAmount = overTimeManager.getOverTimeAmount(OverTimeValues.THREE_HOUR);
```

위 코드는 아래처럼 풀어쓸 수 있다.

```java
OverTimeValues value = OverTimeValues.THREE_HOUR;
int myAmount = overTimeManager.getOverTimeAmount(value);
```

여기서 value라는 변수는 OverTimeValues라는 enum 클래스의 객체라고 생각하면 된다. enum 클래스는 생성자를 만들 수 있지만, 생성자를 통해 객체를 생성할 수는 없다.

## enum을 보다 제대로 사용하기

enum을 항상 switch로 확인하는 것이 아닌, enum 클래스 선언 시 상수의 값을 지정할 수 있을까?

당연히 enum의 상수값을 지정하는 것은 가능하다. 하지만 값을 동적으로(런타임) 할당하는 것은 불가능하다.

```java
public enum OverTimeValues2 {
    THREE_HOUR(18000),
    FIVE_HOUR(30000),
    WEEKEND_FOUR_HOUR(40000),
    WEEKEND_EIGHT_HOUR(60000);

    private final int amount;
    OverTimeValues2(int amount) {
        this.amount = amount;
    }
    public int getAmount() {
        return amount;
    }
}
```

이제 값을 지정한 enum을 사용해보자

```java
public class OverTimeManager2 {
    public static void main(String[] args) {
        OverTimeValues2 fiveHour = OverTimeValues2.FIVE_HOUR;
        System.out.println(fiveHour);
        System.out.println(fiveHour.getAmount());

    }
}
```

두번째 방법은 선언 자체는 간단하지만 구현이 약간 복잡해진다.

성능은 두번째 방법이 훨씬 좋다.

왜?

## enum 클래스의 부모는 무조건 java.lang.Enum이어야 해요.

enum 클래스는 무조건 java.lang.Enums의 상속을 받는다(당연히 컴파일러가 알아서 추가한다).

따라서 enum을 사용할 때 다른 사람이 만들놓은 enum을 extends를 이용하여 선언하려고 해서는 안된다.

Enum 클래스의 생성자는 다음과 같다.

```java
protected Enum(String name, int ordinal)
```

name은 enum 상수 이름이다. ordinal은 enum의 순서이며, 상수가 선언된 순서대로 0부터 증가한다.

다음은 Enum 클래스에 선언되어 있는 메소드들이다.

- compareTo(E e): 매개 변수로 enum 타입과의 순서 차이를 리턴한다.
- getDeclaringClass(): 클래스 타입의 enum을 리턴한다.
- name(): 상수 이름을 리턴한다.
- ordinal(): 상수의 순서를 리턴한다.
- valueOf(Class<T> enumType, String name): static 메소드. 첫 번째 매개 변수로 클래스 타입의 enum을, 두 번째 매개 변수로 상수의 이름을 넘겨주면 된다.
- values(): enums 클래스에 선언된 모든 상수를 배열로 리턴한다.
