# 23장 자바랭 다음으로 많이 쓰는 애들은 컬렉션 - Part2(Set과 Queue)

## Set

Set은 순서에 상관 없이, 어떤 데이터가 존재하는지를 확인하기 위한 용도로 많이 사용된다.

중복되는 것을 방지하고, 원하는 값이 포함되어 있는지를 확인하는 것이 주 용도다.

Set 인터페이스를 구현한 주료 클래스는 HashSet, TreeSet, LinkedHashSet이 있다.

- HashSet: 순서가 전혀 필요 없는 데이터를 해시 테이블에 저장한다. Set 중에 가장 성능이 좋다.
- TreeSet: 저장된 데이터의 값에 따라 정렬되는 셋. red-black tree 구조로 값이 저장되며, HashSet 보다 성능이 약간 느리다.
- LinkedHashSet: LinkedList으로 구현된 해시 테이블에 데이터를 저장한다. 저자오딘 순서에 따라 값이 정렬된다. 성능은 제일 나쁘다.

이런 성능 차이가 발생하는 이유는 데이터 정렬 떄문이다.

## HastSet

다음은 HashSet의 상속 관계다.

```
java.lang.Object
    ㄴ java.util.AbstractCollection<E>
        ㄴ java.util.AbstractSet<E>
            ㄴ java.util.HashSet<E>
```

AbstractSet 클래스는 equals(), hashCode(), removeAll() 메소드만를 구현했다.

Set은 데이터 중복을 허용하지 않으므로, 데이터가 같은지 확인하는 작업이 핵심이다. 따라서 equals()와 hashCode() 메소드를 구현하는 부분은 Set에서 매우 중요하다.

### HashSet의 생성자

- HashSet(): 데이터를 저장할 수 있는 16개의 공간과 0.75의 로드 팩터를 갖는 객체를 생성한다.
- HashSet(Collection<? extends E> c): 매개 변수로 받은 컬렉션 데이터를 HashSet에 담는다.
- HashSet(int initialCapacity): 매개 변수만큼의 저장공간과 0.75의 로드 팩터를 갖는 객체를 생성한다.
- HashSet(int initialCapacity, float loadFactor): 매개변수로 넘겨진만큼의 저장 공간과 로드팩터를 갖는 객체를 생성한다.

로드 팩터(load factor)는 (데이터 개수)/(저장 공간)을 의미한다. 만약 데이터 개수가 증가하여 로드 팩터보다 커지면, 저장 공간의 크기는 증가되고 rehash을 해야 한다.

로드 팩터 값이 클수록 공간은 넉넉해지지만, 데이터를 찾는 시간은 증가한다. 따라서, 초기 공간 개수와 로드 팩터는 데이터의 크기를 고려하여 산정해야 한다.

### HashSet의 주요 메소드

- add(E e)
- clear()
- clone()
- contains(Object o)
- isEmpty()
- iterator
- remove(Object o)
- size()

## Queue

LinkedList는 List 인터페이스뿐만 아니라 Queue와 Deque 인터페이스도 구현하고 있기에, LinkedList 자체가 List이면서도, Queue, Deque도 된다.

Queue는 FIFO 용도로 사용한다.

## LinkedList

다음은 LinkedList의 상속 관계다.

```
java.lang.Object
    ㄴ java.util.AbstractCollection<E>
        ㄴ java.util.AbstractList<E>
            ㄴ java.util.AbstractSequentialList<E>
                ㄴ java.util.LinkedLilst<E>
```

ArrayList 클래스와 비슷하지만 AbstractSequentialList가 부모다.
AbstractList와 AbstractSequentialList의 차이는 add(), set(), remove() 등의 메소드에 대한 구현 내용이 상이하다는 정도다.

- Serializable
- Cloneable
- Iterable<E>
- Collection<E>
- Deque<E>
- List<E>
- Queue<E>

### 생성자

- LinkedList()
- LinkedList(Collection<? extends E> c)

### 메소드

LinkedList는 중복된 기능을 수행하는 메소드가 많은데, 이는 여러 종류의 인터페이스를 구현했기 때문이다.
따라서 여러 메소드를 혼용하여 사용하면 이해하면 힘든 코드가 될 수 있다. add가 붙은 메소드를 사용하는 것이 오해의 소지가 가장 적다.

- addFirst(Object)
- offerFirst(Object)
- push(Object)
- add(Object)
- addLst(Object)
- offer(Object)
- offerLast(Object)
- add(int, Object)
- set(int, Object)
- addAll(Collection)
- addAll(int, Collection)
