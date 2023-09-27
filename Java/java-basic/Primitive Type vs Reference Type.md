# Primitive Type vs Reference Type

## Primitive Type

기본형 데이터는 byte, short, int, long, boolean, char, float, double이다.
해당 데이터들은 메모리의 stack 영역에 저장된다(참고로 데이터를 저장하는 변수도 stack 영역에 저장된다).
메소드가 종료되면 stack에서 스택 프레임이 pop되며 제거된다.

## Reference Type

참조형 데이터는 객체와 배열이다. 해당 데이터들은 메모리의 heap 영역에 동적으로 생성된다(단 Reference Type의 변수는 heap 영역의 메모리 주소를 stack에 저장하는 방식으로 동작한다). 더 이상 객체의 메모리 주소를 참조하는 변수가 없을 때 GC에 의해 제거된다.

## 비교

- **null 저장 여부**:
  - Primitive Type: 저장 불가
  - Reference Type: 저장 가능
- **제네릭 타입에서 사용 여부**:
  - Primitive Type: 사용 불가
  - Reference Type: 사용 가능
- **접근 속도**:
  - Primitive Type: Stack에서 바로 값을 읽어오기 때문에 일반적으로 Reference Type보다 빠르다.
  - Reference Type: Heap에서 데이터를 읽어와야 하며, Wrapper 클래스를 사용할 경우 unboxing 과정의 오버헤드가 있을 수 있다.
- **메모리 양(JVM 구현에 따라 실제 크기는 다를 수 있다)**:
  - Primitive Type: 1byte ~ 8byte의 크기를 갖는다.
  - Wrapper Class: 128bits ~ 192bits의 크기를 갖는다.

## 결론

성능과 메모리 효율성 면에서는 Primitive Type을 우선적으로 고려해야 한다. 그러나 null 값 처리나 제네릭 타입이 필요한 경우에는 Reference Type을 사용하는 것이 적절하다.

## 참조

- 자바의신
- [JAVA 변수의 기본형 & 참조형 타입 차이 이해하기](https://inpa.tistory.com/entry/JAVA-%E2%98%95-%EB%B3%80%EC%88%98%EC%9D%98-%EA%B8%B0%EB%B3%B8%ED%98%95-%EC%B0%B8%EC%A1%B0%ED%98%95-%ED%83%80%EC%9E%85)
- [[Java] Primitive vs Wrapper class 기본형 타입과 래퍼클래스](https://shanepark.tistory.com/449)
