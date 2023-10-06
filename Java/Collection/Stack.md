# Stack 클래스

## 1. 개요

Stack 클래스는 LIFO 기능을 구현할 때 필요한 클래스다. 하지만 다음과 같은 이유로 Stack 대신 ArrayDeque를 사용하는 것이 좋다.

1. Vector 상속은 자바 설계상 결함이다.
2. Stack의 메소드는 느리다.
3. 초기 크기를 지정할 수 없다.

## 2. 문제점

### 2.1. Vector 상속은 설계상 결함이다

다음은 Stack 클래스의 상속 관계다.

```
java.lang.Object
    ㄴ java.util.AbstractCollection<E>
        ㄴ java.util.AbstractList<E>
            ㄴ java.util.Vector<E>
                ㄴ java.util.Stack<E>
```

Stack은 한쪽에서만 데이터를 삽입/삭제 할 수 있는 LIFO 자료구조이지만 Vector를 상속했기 떄문에 중간에 데이터를 삽입/삭제할 수 있게 되었다. 이는 자바 설계의 결함이다.

### 2.2. Stack의 메소드는 느리다

Stack의 메소드들은 synchronized 키워드로 구현되어있어 thread-safe 하지만 멀티스레드 환경이 아니라면 오버헤드의 발생 원인이 된다.

따라서 LIFO 구조를 만들 때 Deque 인터페이스를 구현한 ArrayDeque 클래스를 사용하는 것이 좋다(ArrayDeque는 thread safe하지 않다).

### 2.3. 초기 크기를 지정할 수 없다

Stack은 생성자가 없어 초기 크기가 고정되어 있다. 만약 큰 값을 저장해야 하는 상황이라면 내부적으로 더 큰 크기의 스택을 만들고 값을 복사하는 작업으로인해 성능 저하가 발생한다.

## 3. 참조

- 자바의 신 22장
- [[Java] Stack보다는 ArrayDeque를 쓰자. Stack과 Vector의 문제점](https://jaehee329.tistory.com/27)
- [Stack 클래스란 무엇인가?](https://github.com/wjdrbs96/Today-I-Learn/blob/master/Java/Collection/Stack%20%ED%81%B4%EB%9E%98%EC%8A%A4%EB%9E%80%3F.md)
