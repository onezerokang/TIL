# 12장 모든 클래스의 부모는 Object에요

## 1. java.lang.Object

자바에서는 기본적으로 아무런 상속을 받지 않으면, java.lang.Object 클래스를 확장한다.

예를 들어 다음 클래스는 사실 Object를 상속하고 있기 때문에 toString을 메소드를 정의하지 않았음에도 Object의 toString을 호출할 수 있다.

```java
package chap12;

public class InheritanceObject {
    public static void main(String[] args) {
        InheritanceObject object = new InheritanceObject();
        System.out.println(object.toString());
    }
}
```

Object 메소드를 정의하고 이를 상속하게 함으로써 모든 클래스가 가져야 할 최소한의 기능을 설정 하는 것이다.

## 2. Object 클래스의 메소드

Object 클래스에 선언된 메소드는 객체를 처리하기 위한 메소드와 쓰레드를 위한 메소드로 나뉜다.

### 2.1. 객체 처리를 위한 메소드

- protected Object clone()
  - 객체의 복사본을 만들어 리턴한다.
- public boolean equals(Object obj)
  - 현재 객체와 매개변수로 받은 객체가 같은지 확인한다.
  - 기본적으로 Object의 equals() 메소드는 hashCode()를 비교하기 때문에 객체의 속성 값을 기준으로 비교하고 싶다면 오버라이딩 해야 한다.
- protected void finalize()
  - 현재 객체가 더 이상 쓸모 없어졌을 때 가비지 컬렉터에 의해서 호출되는 메소드로 개발자가 다룰 일은 거의 없다.
- public Class<?> getClass()
  - 현재 객체의 Class 객체를 리턴한다.
- public int hashCode()
  - 객체에 대한 해시 코드 값을 리턴한다. 해시 코드는 16진수로 제공되는 객체의 메모리 주소를 말한다.
  - equals()의 결과가 true인 경우 hashCode()의 결과 값은 반드시 같아야 한다.
  - 따라서 equals()를 오버라이딩 했다면 hashCode() 또한 오버라이딩 해야 한다.
- public String toString()
  - 객체를 문자열로 표현하는 값을 리턴한다.

### 2.2. 쓰레드 처리를 위한 메소드

- public void notify()
  - 이 객체의 모니터에 대기 하고 있는 단일 쓰레드를 깨운다.
- public void notifyAll()
  - 이 객체의 모니터에 대기 하고 있는 모든 쓰레드를 깨운다.
- public void wait()
  - 다른 쓰레드가 현재 객체에 대한 notify() 메소드나 notifyAll() 메소드를 호출할 때까지 현재 쓰레드가 대기하고 있도록 한다.
- public void wait(long timeout)
  - long 매개변수를 넘겨주면 쓰레드의 최대 대기 시간을 지정할 수 있다.
- public void wait(long timeout, int nanos)
  - 나노초를 추가로 넘겨주면 대기 시간을 더 자세하게 지정할 수 있다.

### 2.3. toString()

toString()은 객체를 문자열로 표현한 값을 리턴하는 메소드로 다음과 같은 상황에서 자동으로 호출된다.

- System.out.println() 메소드에 매개 변수로 들어가는 경우
- 객체에 대하여 더하기 연산을 하는 경우

다음 예시를 통해 toString()을 명시적으로 호출하지 않았음에도 toString()이 호출되는 경우를 확인할 수 있다.

```java
package chap12;

public class ToString {
    public static void main(String[] args) {
        ToString thisObject = new ToString();
        thisObject.toStringMethod();
    }
    public void toStringMethod() {
        System.out.println(this); // chap12.ToString@36baf30c
        System.out.println(this.toString()); // chap12.ToString@36baf30c
        System.out.println("plus " + this); // plus chap12.ToString@36baf30c
    }
}
```

실제 Object 클래스에 구현되어 있는 toString() 메소드는 다음과 같다.

```
getClass().getName() + '@' + Integer.toHexString(hashCode())
```

toString()을 구성하는 각 부분에 대해 자세히 알아보자

- getClass().getName()
  - 현재 클래스의 패키지 이름과 클래스 이름이 나온다.
- Integer.toHexString(hashCode())
  - 객체의 메모리 주소를 문자열로 변환

Object의 메소드만으로는 객체의 속성 값을 알 수 없기 때문에 해당 객체가 어떤 객체인지 알기 어렵다. 따라서 실제로 toString 메소드를 사용할 것이라면 오버라이딩을 구현해야 한다.

다음은 DTO에서 toString()을 오버라이딩 한 예시 코드이다(예시를 위해 main 메소드를 사용하였다).

```java
package chap12;

public class MemberDTO {
    public String name;
    public String phone;
    public String email;

    public static void main(String[] args) {
        MemberDTO member = new MemberDTO("james", "01012341234", "james@gmail.com");
        System.out.println(member); // MemberDTO{name='james', phone='01012341234', email='james@gmail.com'}

    }

    public MemberDTO(String name, String phone, String email) {
        this.name = name;
        this.phone = phone;
        this.email = email;
    }

    @Override
    public String toString() {
        return "MemberDTO{" +
                "name='" + name + '\'' +
                ", phone='" + phone + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}
```

### 2.4.equals()

==와 != 연산자는 Primitive 타입에만 사용할 수 있다.

해당 연산자를 Reference 타입에 사용할 경우 객체의 '속성 값'을 비교하는 것이 아닌 '메모리 주소값'을 비교한다.

예를 들어 다음 클래스를 실행하면 두 멤버가 같은 속성 값을 갖고 있음에도 "다른 회원입니다."가 출력된다.

```java
package chap12;

public class Equals {
    public static void main(String[] args) {
        Equals thisObject = new Equals();
        thisObject.equalsMethod();
    }

    public void equalsMethod() {
        MemberDTO member1 = new MemberDTO("james", "01012341234", "james@gmail.com");
        MemberDTO member2 = new MemberDTO("james", "01012341234", "james@gmail.com");

        if (member1 == member2) {
            System.out.println("같은 회원입니다.");
        } else {
            System.out.println("다른 회원입니다."); // 이 부분이 출력된다
        }
    }
}
```

그래서 객체끼리 비교할 때는 equals() 메소드를 사용해야 한다.

이때 java.lang.Object의 equals()는 hashCode()를 비교하도록 구현되었기에 속성값으로 비교하고 싶다면 equals()와 hashCode() 메소드를 오버라이딩 해야 한다.

위 예제 코드를 == 에서 equals로 바꿔보자

```java
package chap12;

public class Equals {
    public static void main(String[] args) {
        Equals thisObject = new Equals();
        thisObject.equalsMethod();
    }

    public void equalsMethod() {
        MemberDTO member1 = new MemberDTO("james", "01012341234", "james@gmail.com");
        MemberDTO member2 = new MemberDTO("james", "01012341234", "james@gmail.com");

        if (member1.equals(member2)) {
            System.out.println("같은 회원입니다."); // 이 부분이 출력된다
        } else {
            System.out.println("다른 회원입니다.");
        }
    }
}
```

equals()와 hashCode()가 오버라이딩 된 MemberDTO는 다음과 같다.

```java
public class MemberDTO {
    public String name;
    public String phone;
    public String email;

    public MemberDTO(String name, String phone, String email) {
        this.name = name;
        this.phone = phone;
        this.email = email;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        MemberDTO memberDTO = (MemberDTO) o;
        return Objects.equals(name, memberDTO.name) && Objects.equals(phone, memberDTO.phone) && Objects.equals(email, memberDTO.email);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, phone, email);
    }
}
```

### 2.4. hashCode()

hashCode() 메소드는 객체의 메모리 주소를 16진수로 리턴한다.

자바에는 두 개의 객체가 서로 동일하다면 hashCode() 값은 무조건 동일 해야 한다는 규칙이 있기에, equals()를 오버라이딩하면 hashCode 메소드도 오버라이딩하여 동일한 값이 나오도록 해야 한다.

객체의 해시 코드를 사용하는 Collection(HashSet, HashMap, HashTable)은 객체가 논리적으로 같은지 비교할 때 먼저 hashCode의 값이 같은지 확인하고, equals() 메소드의 반환 값이 true인지를 확인하기 때문이다.

만약 equals()만 오버라이딩 하고 hashCode()를 오버라이딩 하지 않는다면 중복을 허용하지 않는 Set 자료구조에 속성 값이 같은 객체가 여러 개 저장 되어버린다.
