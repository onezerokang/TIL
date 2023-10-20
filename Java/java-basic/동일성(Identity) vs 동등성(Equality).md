# 동일성(Identity) vs 동등성(Equality)

동일성과 동등성에 대해서 알고는 있었는데 정확히 어떤 개념이 어떤 특성인지 헷갈려서 정리하게 되었다.

- **동일성(Identity)**: 두 객체의 메모리 주소가 같은 것을 의미한다.
- **동등성(Equality)**: 두 객체의 논리적인 값(상태)이 같은 것을 의미

## 동일성

동일성은 두 객체의 메모리 주소가 같은 것을 의미한다. 자바에서 동일성은 비교 연산자(`==`)로 확인할 수 있다.

다음과 같은 객체가 있다고 가정하자.

```java
public class Car {
    private final String name;

    public Car(String name) {
        this.name = name;
    }
}
```

다음 car1과 car2는 동일한 객체의 주소를 가리키고 있기에 동일하다.

```java
Car car1 = new Car("테슬라");
Car car2 = car1;

System.out.println(car1 == car2); // true
```

## 동등성

동등성은 두 객체가 논리적으로 동일한 값을 갖고 있음을 의미한다. 자바에서 동등성은 equals() 메서드와 hashCode() 메서드를 오버라이드 해야 한다(자세한 내용은 [equals와 hashCode](/Java/java-lang/equals와%20hashCode.md) 문서를 참고).

```java
public class Car {
    private final String name;

    public Car(String name) {
        this.name = name;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Car car = (Car) o;
        return Objects.equals(name, car.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }
}
```

이제 두 객체가 논리적으로 같은 값을 같는다면 동등하다고 할 수 있다.

```java
Car car1 = new Car("테슬라");
Car car2 = new Car("테슬라");

System.out.println(car1.equals(car2)); // true
```
