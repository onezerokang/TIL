# Queue

Queue는 선입선출(First In First Out) 자료구조다. 큐는 터널 같이 생겼으며, 맨 뒤에 데이터를 삽입하거나, 맨 앞의 데이터를 삭제하는 작업을 할 수 있다.

그래프의 너비 우선 탐색(BFS) 알고리즘에 주로 사용되며, 컴퓨터 버퍼, 대기열로도 사용된다.

## 자바의 Queue 선언

자바의 Queue는 Collection을 확장한 인터페이스다.

Queue를 사용하기 위해서는 Queue를 구현한 LinkedList를 사용하면 된다.

```java
import java.util.Queue;
import java.util.LinkedList;
Queue<Integer> queue = new LinkedList<>();
```

## Queue 메소드

Queue는 삽입과 삭제 메소드를 제공하는 데 이러한 각 메소드는 두 가지 형태로 존재한다. 하나는 작업이 실패할 경우 예외를 발생시키고, 다른 하나는 null이나 false를 반환한다.

|      | 예외 발생 | null or false |
| ---- | --------- | ------------- |
| 삽입 | add(e)    | offer(e)      |
| 제거 | remove()  | poll()        |
| 조회 | element() | peek()        |

```java
import java.util.Queue;
import java.util.LinkedList;
Queue<Integer> queue = new LinkedList<>();

// 삽입
queue.add(1);
queue.offer(2);

// 삭제
System.out.println(queue.poll()); // 1
System.out.println(queue.remove()); // 2
System.out.println(queue.poll()); // null

// 참조
queue.add(3);
System.out.println(queue.peek()); // 1(값이 삭제되지는 않는다)
```

각 메소드의 시간 복잡도는 모두 O(1)이다.
