# ArrayList의 내부 구현

## 1. 개요

ArrayList는 내부적으로 배열을 기반으로 한 자료구조로, 동적으로 크기가 조절될 수 있는 특징을 갖는다.

일반적인 배열은 한번 크기가 정해지면 그 크기를 변경할 수 없다. 따라서, 정해진 크기를 초과하여 데이터를 추가하려고 하면 `ArrayIndexOutOfBoundsException`이 발생한다. 이런 유연하지 못한 특징으로 인해 배열은 사용에 제약이 발생한다.

반면 ArrayList는 배열의 장점을 살리면서 이런 제약을 극복하였다. 요소가 추가될 때 현재 용량이 부족하면 자동으로 용량을 확장한다. 즉, 더 큰 크기의 배열을 새롭게 생성하고 기존의 데이터를 그곳에 복사한다. 이런 방식으로 ArrayList는 배열의 고정된 크기라는 제한 없이 데이터를 유연하게 관리할 수 있게 되었다.

ArrayList가 실제로 어떻게 구현되어있는지 확인해보겠다.

## 2. 클래스 변수

- **serialVersionUID**: 직렬화 버전의 고유값으로 직렬화/역직렬화 시 해당 클래스의 버전을 판단한다.
- **DEFAULT_CAPACITY**: 내부 배열의 용량을 지정하지 않고 ArrayList를 초기화 시 설정될 용량이다.
- **EMPTY_ELEMENTDATA**: 빈 인스턴스에 사용되는 공유 빈 배열 인스턴스로 초기 용량을 0으로 설정했을 시 elementData가 참조하는 대상이 된다.
- **DEFAULTCAPACITY_EMPTY_ELEMENTDATA**: 기본 크기의 빈 인스턴스에 사용되는 공유 빈 배열 인스턴스. 첫 번째 요소가 추가될 때 얼마나 확장할지 알기 위해 EMPTY_ELEMENTDATA와 구분한다.

```java
@java.io.Serial
private static final long serialVersionUID = 8683452581122892189L;

private static final int DEFAULT_CAPACITY = 10;

private static final Object[] EMPTY_ELEMENTDATA = {};

private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};
```

## 3. 인스턴스 변수

- **elementData**: ArrayList의 요소들이 저장되는 배열 버퍼다. ArrayList의 용량은 이 배열 버퍼의 길이와 같다. 만약 `elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA` 인 빈 ArrayList가 있으면 첫 번째 요소가 추가될 때 DEFAULT_CAPACITY로 확장한다.
- **size**: ArrayList에 들어가 있는 요소의 개수이다.

```java
transient Object[] elementData; // non-private to simplify nested class access

private int size;
```

## 4. 생성자

- 초기 용량 설정: 인자로 넘긴 용량을 갖는 배열을 초기화 한다.

```java
public ArrayList(int initialCapacity) {
    if (initialCapacity > 0) {
        // 초기 용량이 양수
        this.elementData = new Object[initialCapacity];
    } else if (initialCapacity == 0) {
        // 초기 용량이 0
        this.elementData = EMPTY_ELEMENTDATA;
    } else {
        throw new IllegalArgumentException("Illegal Capacity: "+ initialCapacity);
    }
}
```

- 기본 용량 사용: 초기 용량이 10인 빈 배열을 초기화 한다.

```java
public ArrayList() {
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}
```

- 인자로 컬렉션 넘기기:
  - 넘긴 값이 빈 배열일 경우: elementData가 EMPTY_ELEMENTDATA를 가리키도록 한다.
  - 넘긴 값이 ArrayList일 경우: elementData가 넘긴 ArrayList를 가리키도록 한다.
  - 넘긴 값이 다른 자료구조 일 경우: 자료구조를 배열로 복사하여 elementData가 가리키도록 한다.

```java
/**
 * Constructs a list containing the elements of the specified
 * collection, in the order they are returned by the collection's
 * iterator.
 *
 * @param c the collection whose elements are to be placed into this list
 * @throws NullPointerException if the specified collection is null
 */
public ArrayList(Collection<? extends E> c) {
    Object[] a = c.toArray();
    if ((size = a.length) != 0) {
        if (c.getClass() == ArrayList.class) {
            elementData = a;
        } else {
            elementData = Arrays.copyOf(a, size, Object[].class);
        }
    } else {
        // replace with empty array.
        elementData = EMPTY_ELEMENTDATA;
    }
}
```

## 5. 주요 메서드

### 5.1. add

add() 메서드를 호출하면 요소를 배열의 끝에 추가한다.

```java
public boolean add(E e) {
    modCount++;
    add(e, elementData, size);
    return true;
}
```

`add(E e)` 메서드는 오버로드된 `add(e, elementData, size)` 메서드를 호출한다.
해당 메서드는 현재 배열의 용량이 꽉 찼다면 grow() 메서드를 호출하여 배열을 키우고 요소를 추가한다.

```java
private void add(E e, Object[] elementData, int s) {
    if (s == elementData.length)
        elementData = grow();
    elementData[s] = e;
    size = s + 1;
}
```

`add(int index, E element)` 메서드를 호출하여 요소가 삽입될 index를 지정할 수 있다.

다만 기존 요소들을 한칸씩 밀어야 하기에 O(n)의 시간복잡도를 갖는다.

```java
/**
 * 지정된 요소를 이 목록의 지정된 위치에 삽입합니다.
 * 해당 위치에 있는 요소(있는 경우) 및
 * 그 이후의 요소들을 오른쪽으로 이동시킵니다
 * (그들의 인덱스에 하나를 더합니다).
 *
 * @param index 지정된 요소가 삽입될 인덱스
 * @param element 삽입될 요소
 * @throws IndexOutOfBoundsException {@inheritDoc}
 */
public void add(int index, E element) {
    rangeCheckForAdd(index);
    modCount++;
    final int s;
    Object[] elementData;
    if ((s = size) == (elementData = this.elementData).length)
        elementData = grow();
    System.arraycopy(elementData, index,
                        elementData, index + 1,
                        s - index);
    elementData[index] = element;
    size = s + 1;
}
```

### 5.2. grow

내부 배열의 용량이 꽉 찼다면 `grow()` 메서드를 호출한다.

```java
private Object[] grow() {
    return grow(size + 1);
}
```

`grow()` 메서드는 내부적으로 `grow(int minCapacity)`를 호출한다.
해당 메서드는 배열을 기존 용량의 1.5배에서 ~ 2배로 늘린다. 이때 늘린 용량이 minCapacity보다 작다면 minCapacity만큼 용량을 늘린다.

```java
private Object[] grow(int minCapacity) {
    int oldCapacity = elementData.length;
    if (oldCapacity > 0 || elementData != DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        int newCapacity = ArraysSupport.newLength(oldCapacity,
                minCapacity - oldCapacity, /* 최소 성장 */
                oldCapacity >> 1           /* 비트를 오른쪽으로 한칸 시프트하는 연산으로 정수를 2로 나누는 것과 같다  */);
        return elementData = Arrays.copyOf(elementData, newCapacity);
    } else {
        return elementData = new Object[Math.max(DEFAULT_CAPACITY, minCapacity)];
    }
}
```

## 6. 결론

ArrayList의 동작 방식은 다음과 같다.

0. `add(E e)` 메서드를 호출하여 데이터를 추가하려고 한다.
1. `add(E e)`는 내부적으로 `add(E e, Object[] elementData, int s)`를 호출한다.
2. `add(E e, Object[] elementData, int s)` 메서드에서는 현재 배열의 용량과, 저장된 요소의 개수가 같을 경우 `grow()` 메서드를 호출한다.
3. `grow()` 메서드는 `grow(int minCapacity)`를 호출한다.
4. `grow(int minCapacity)`는 기존 데이터를 복사한, 더 큰 배열을 리턴한다.
