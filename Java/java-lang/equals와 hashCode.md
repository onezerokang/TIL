# equals와 hashCode

equals와 hashCode는 모든 클래스의 부모인 Object 클래스에 정의되어 있는 메소드다. 각 메소드는 다음과 같은 기능을 한다.

- **equals**: 두 객체가 같은지 비교하고 boolean을 리턴한다. 오버라이딩하지 않을 경우 두 객체의 주소값을 비교한다.
- **hashCode**: 객체의 고유값을 리턴한다. 오버라이딩하지 않을 경우 객체의 메모리 주소를 바탕으로 한 해시값을 리턴한다.

따라서 equals와 hashCode를 오버라이딩하지 않고 사용하면 객체의 속성값이 아닌 주소값을 비교한 결과를 리턴하게 된다.

```java
// Person 클래스
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

// Person 인스턴스 비교
public static void main(String[] args) {
    Person p1 = new Person("철수", 20);
    Person p2 = new Person("철수", 20);

    // p1객체와 p2 객체의 속성값이 같지만, equals와 hashCode를 오버라이딩 하지 않았기에 주소값을 비교한다.
    System.out.println(p1.equals(p2)); // false
}
```

객체의 주소값이 아닌 속성값을 비교하고 싶다면 equals와 hashCode를 오버라이딩 해야 한다.
IDE의 기능을 활용하여 equals와 hashCode를 쉽게 오버라이딩 할 수 있다.

```java
// equals와 hashCode를 오버라이딩한 클래스
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}

// Person 인스턴스 비교
public static void main(String[] args) {
    Person p1 = new Person("철수", 20);
    Person p2 = new Person("철수", 20);

    System.out.println(p1.equals(p2)); // true
}
```

## equals를 오버라이딩할 때 hashCode도 오버라이딩 해야 하는 이유

객체의 속성값으로 비교하기 위해 equals를 오버라이딩할 때는 반드시 hashCode의 값도 오버라이딩 해줘야 한다. 위 예제에서는 equals만 오버라이딩 해도 원하는 결과를 받을 수 있는데, 왜 hashCode도 오버라이딩 해야 할까?

그 이유는 hashCode를 사용하는 Collections 때문이다.
HashMap, HashTable, HashSet과 같은 자료구조는 객체의 같음을 판단할 때 hashCode가 같은지 확인하고, equals의 결과가 true인지를 확인한다.

만약 equals만 재정의한다면 hashSet에는 속성값이 같은 객체가 여러개 들어가게 될 것이다.

```java
// hashCode를 오버라이딩 하지 않은 Person 클래스
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }
}


public static void main(String[] args) {
    Set<Person> set = new HashSet<>();
    Person p1 = new Person("철수", 20);
    Person p2 = new Person("철수", 20);
    set.add(p1);
    set.add(p2);

    System.out.println(set.size()); // 1이 출력 돼야 하지만 hashCode를 오버라이딩 하지 않아 2가 출력된다.
}
```

## 참조

- 자바의 신
- [equals와 hashCode는 왜 같이 재정의해야 할까?](https://tecoble.techcourse.co.kr/post/2020-07-29-equals-and-hashCode/)
