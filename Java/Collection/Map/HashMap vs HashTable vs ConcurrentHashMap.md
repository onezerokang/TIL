# HashMap vs HashTable vs ConcurrentHashMap

## 개요

- 자바에서 Map 자료구조가 필요할 때 주로 HashMap을 사용했었는데, HashTable과 ConcurrentHashMap과의 차이점이 궁금해져서 공부하고 정리하게 되었다.

## HashMap

- Key-Value로 데이터를 저장한다.
- Key와 Value 모두 null 값을 허용한다.
- 스레드 세이프하지 않아, 동시에 같은 키에 대해 업데이트가 발생하면 예상치 못한 결과가 발생할 수 있다.

## HashTable

- Key-Value로 데이터를 저장한다.
- Key와 Value 모두 null 값을 허용하지 않는다.
- HashTable의 메서드에는 synchronized 키워드가 붙어있어 한번에 하나의 스레드만 HashTable에 접근할 수 있다.
- 스레드 세이프 하지만 후술할 ConcurrentHashMap에 비해 성능이 좋지 않아, 레거시 코드 외에는 사용되지 않는다.

## ConcurrentHashMap

- Key-Value로 데이터를 저장한다.
- Key와 Value 모두 null 값을 허용하지 않는다.
- key-value 쌍을 저장하는 Entry 객체 단위로 잠금(lock)이 걸린다.
- 따라서 여러 스레드가 동시에 접근하더라도, 접근하는 Entry가 다르면 락을 해제할 때까지 대기하지 않아도 된다.

## 결론

- 싱글 스레드 환경에서는 HashMap을 사용하자.
- 멀티 스레드 환경에서는 ConcurrentHashMap을 사용하자.

## 참조

- 자바의신, 이상민, 24장 자바랭 다음으로 많이 쓰는 애들은 컬렉션 - Part3(Map)
- <a href="https://tecoble.techcourse.co.kr/post/2021-11-26-hashmap-hashtable-concurrenthashmap/" target="_blank">HashMap vs HashTable vs ConcurrentHashMap</a>
