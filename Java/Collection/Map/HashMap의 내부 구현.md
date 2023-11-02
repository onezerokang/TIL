# HashMap의 내부 구현

## Map 인터페이스

Map은 Key-Value 쌍으로 데이터를 저장하는 자료구조다. Key는 Map 내부에서 중복될 수 없다.

다음은 Map 인터페이스에 선언된 메서드다.

- put(K key, V value)
- putAll(Map<? extends K, ? extends V> m)
- get(Object key)
- remove(Object key)
- keySet()
- values()
- entrySet()
- size()
- clear()

Map 인터페이스를 구현한 클래스로는 HashMap, TreeMap, LinkedHashMap, Hashtable이 있다.

## HashMap이란

HashMap은 Map 인터페이스를 구현한 구현체 중 가장 많이 사용된다.

다음은 HashMap의 생성자다.

- HashMap(): 16개의 저장 공간을 갖는 HashMap 객체를 생성한다.
- HashMap(int initialCapacity): 매개 변수만큼 저장 공간을 갖는 HashMap 객체를 생성한다.
- HashMap(int initialCapacity, float loadFactor): 주어진 크기의 저장 공간과 로드 팩터를 갖는 HashMap 객체를 생성한다.
- HashMap(Map<? extends K, ? extends V> m): 매개 변수로 넘어온 Map을 구현한 객체에 있는 데이터를 갖는 HashMap 객체를 생성한다.

클래스를 키로 사용할 때는 equals와 hashCode를 잘 구횬해야 한다.

HashMap에 객체가 들어가면 hashCode() 메소드의 결과 값에 따른 버켓이라는 list 형태의 바구니가 만들어진다. 만약 다른 키가 저장됐는데 hashCode() 메서드가 동일하다면 해당 버킷에 여러 값이 들어갈 수 있다. 따라서 get() 메서드 호출 시 hashCode()의 결과를 확인하고, 버킷에 들어간 목록에 데이터가 여러 개일 경우 equals() 메소드를 호출하여 동일한 값을 찾는다.

## HashMap 동작 원리

## 출처

- 자바의신, 이상민, 24장 자바랭 다음으로 많이 쓰는 애들을 컬렉션 - Part3(Map)
