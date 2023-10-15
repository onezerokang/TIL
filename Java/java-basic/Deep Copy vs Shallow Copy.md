# Deep Copy vs Shallow Copy

깊은 복사와 얕은 복사는 참조 타입 데이터를 복사하는 방식들이다.

- **깊은 복사**: 객체의 상태 값을 복사하여 새로운 객체를 생성한다. 두 변수는 다른 객체를 가리킨다.
- **얕은 복사**: 객체의 주소 값을 복사한다. 두 변수는 같은 객체를 가리킨다.

## 1. 얕은 복사

얕은 복사는 객체의 메모리 주소값만 복사하여 변수나 매개변수로 전달하는 것을 의미한다.

주소값만 복사하기 때문에 같은 객체를 가리키고, 한 곳에서 수정하면 다른 곳에서도 반영된다.

```java

public class ShallowCopy {
    public static void main(String[] args) {
        Person p1 = new Person("민수", 20);
        Person p2 = p1;

        // 두 주소는 같은 값이 출력된다.
        System.out.println("p1의 주소값 = " + p1);
        System.out.println("p2의 주소값 = " + p2);

        p2.setName("철수");
        System.out.println("p1의 이름 = " + p1.getName()); // 철수
        System.out.println("p2의 이름 = " + p2.getName()); // 철수

    }
}


class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Getter & Setter 생략
}
```

## 2. 깊은 복사

깊은 복사는 객체의 상태 값까지 복사하여 새로운 객체를 만드는 복사다. 깊은 복사를 구현하는 방법은 다음과 같다.

- Cloneable 인터페이스 구현
- 복사 생성자 or 복사 팩터리

### 2.1. Cloneable 인터페이스 구현

Cloneable 인터페이스를 구현하게 되면 Object.clone() 메서드를 오버라이딩 해야 한다.

```java
public class CloneableCopy {
    public static void main(String[] args) {
        Person p1 = new Person("민수", 20);
        Person p2 = null;

        try {
            p2 = (Person) p1.clone();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }

        System.out.println("p1 = " + p1);
        System.out.println("p2 = " + p2);
    }
}

class Person implements Cloneable {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }

    // Getter & Setter 생략
}
```

### 2.2. 복사 생성자 or 복사 팩터리

복사 생성자나 복사 팩터리를 사용하는 방식은 말 그대로 복사할 객체를 생성자나 팩터리에 넘기면 객체의 상태를 가져와 새로운 객체를 만들 때 사용하는 방식을 의미한다.

```java
public class DeepCopy {
    public static void main(String[] args) {
        Person p1 = new Person("민수", 20);
        Person p2 = new Person(p1);
        Person p3 = Person.copy(p1);

        // p1, p2, p3 변수는 모두 다른 Person 객체를 가리킨다.
        System.out.println("p1 = " + p1);
        System.out.println("p2 = " + p2);
        System.out.println("p3 = " + p3);

    }
}

class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 복사 생성자
    public Person(Person person) {
        this.name = person.getName();
        this.age = person.getAge();
    }

    // 복사 팩터리
    public static Person copy(Person person) {
        return new Person(person);
    }

    // Getter & Setter 생략
}
```

## 3. 주의사항

객체를 깊은 복사할 때, 해당 객체의 인스턴스 변수가 다른 객체를 참조하고 있다면 해당 객체 또한 깊은 복사해줘야 한다.

만약 그렇지 않을 경우 해당 인스턴스 변수를 통해 참조하고 있는 원본 객체를 수정할 위험이 생긴다.

## 참조

- [[Java] - 깊은 복사(Deep Copy) vs 얕은 복사(Shallow Copy)](https://zzang9ha.tistory.com/372)
- [☕ 자바 clone 메서드 재정의 (얕은 복사 & 깊은 복사)](https://inpa.tistory.com/entry/JAVA-%E2%98%95-Object-%ED%81%B4%EB%9E%98%EC%8A%A4-clone-%EB%A9%94%EC%84%9C%EB%93%9C-%EC%96%95%EC%9D%80-%EB%B3%B5%EC%82%AC-%EA%B9%8A%EC%9D%80-%EB%B3%B5%EC%82%AC)
