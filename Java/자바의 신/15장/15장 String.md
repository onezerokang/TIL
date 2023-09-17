# String

자바에서 String 클래스는 정말 많이 사용되는 VVIP 클래스다.

## String 클래스의 선언부

다음은 String 클래스의 선언부이다.

```
public final class String extends Object
    implements Serializable, Comparable<String>, CharSequence
```

- public final: 다른 클래스는 String 클래스를 확장할 수 없다.
- Object: 모든 클래스의 부모 클래스
- Serializable: 추상 메소드가 하나도 없는 특이한 인터페이스. 해당 인터페이스를 구현현한다고 선언해 놓으면, 해당 객체를 파일로 저장하거나 다른 서버에 전송 가능한 상태가 된다.
- Comparable: compareTo() 메소드 하나만 선언된 인터페이스. equals() 메소드와 비슷해보이지만 int를 리턴한다. 같으면 0, 순서 상으로 앞에 있으면 -1, 뒤에 있으면 1을 리턴한다.
- CharSequence: 해당 클래스가 문자열을 다루기 위한 클래스임을 명시적으로 나타낸다. StringBuilder와 StringBuffer 클래스도 CharSequence 인터페이스를 구현했다.

## String의 생성자

일반적으로 문자열은 아래와 같이 만들지만, String의 생성자는 매우 많다.

```java
String name = "GodOfJava";
```

String 생성자 중에서 그나마 많이 사용하는 생성자는 다음과 같다(대부분 String 객체는 따옴표로 묶어 생성할 수 있기 때문이다).

- String(byte[] bytes)
  - 현재 사용중인 플랫폼의 캐릭터 셋을 사용하여 제공된 byte 배열을 디코딩한 String 객체를 생성한다.
- String(byte[] bytes, String charsetName)
  - 지정된 캐릭터 셋을 사용하여 제공된 byte 배열을 디코딩한 String 객체를 생성한다.

## String 문자열을 byte로 변환하기

다음은 문자열을 byte 배열로 반환하는 메소드들이다.

- getBytes()
  - 기본 캐릭터 셋의 바이트 배열을 생성한다.
- getBytes(Charset charset)
  - 지정된 캐릭터 셋 객체 타입으로 바이트 배열을 생성한다.
- getBytes(String charsetName)
  - 지정한 이름의 캐릭터 셋을 갖는 바이트 배열을 생성한다.

## 객체의 Null check

모든 객체를 처리할 때는 널 체크를 반드시 해야 한다.

객체가 널이라는 의미는 초기화가 되어 있지 않으며, 클래스에 선언된 어떤 메소드도 사용할 수 없다는 것을 의미한다. 만약 널인 객체의 메소드가 속성에 접근하려고 하면 런타임 예외인, NullPointerException이 발생한다.

널 체크를 할 때는 ==이나 != 연산자를 사용할 수 있다.

메소드의 매개 변수로 넘어오는 객체가 널이 될 확률이 조금이라도 있다면 반드시 한 번씩 확인하는 습관을 갖고 있어야 장애를 예방할 수 있다.

## 문자열 비교와 Constant Pool

다음은 문자열을 비교하는 메소드들이다.

- equals(Object anObject)
- equalsIgnoreCase(String anotherStr)
- compareTo(String anotherStr)
- compareToIgnoreCase(String str)
- contentEquals(CharSequence cs)
- contentEquals(StringBuffer sb)

다음 코드를 봤을 때 어떤 결과가 나올지 예측해보자.

```java
public class StringCompare {
    public static void main(String[] args) {
                String text = "Check value";
        String text2 = "Check value";


        if (text == text2) {
            System.out.println("text==text2 result is same");
        } else {
            System.out.println("text==text2 result is different");
        }

        if (text.equals(text2)) {
            System.out.println("text.equals(text2) result is same");
        }
    }
}
```

== 비교 연산자로 객체를 비교할 때는 메모리 주소 값을 비교하기 때문에 Constant Pool에 대한 이해가 없다면 다음과 같은 결과를 예측했을 것이다.

```
text==text2 result is different
text.equals(text2) result is same
```

하지만 실제로 출력된 값은 다음과 같다.

```
text==text2 result is same
text.equals(text2) result is same
```

자바에는 Constant Pool이라는 것이 있는데, 이는 객체를 재사용하는 용도이다. String의 경우 동일한 값을 갖는 객체가 있을 경우 먼저 만든 객체를 재사용한다.

쌍따옴표가 아닌 서로 다른 생성자로 문자열을 생성한다면 Constant Pool은 값을 재활용하지 않아 우리가 예측한 결과가 출력된다.

## StringBuffer와 StringBuilder

String은 immutable한 객치다. immutable는 '불변의'라는 의미다. 다시 말해서 한 번 만들어지면 더 이상 그 값을 바꿀 수 없다.

예를 들어 String 객체에 다른 값을 더하면 기존 객체가 변하는 것이 아닌 새로운 객체를 만들고, 기존 객체를 버리는 방식이다. 그러므로 계속 하나의 String을 만들어 계속 더하는 작업을 한다면, 계속 쓰레기를 만들게 되는 것이다.

이런 String 클래스의 단점을 보완하기 위해서 나온 클래스가 StringBuffer와 StringBuilder다. 두 클래스에서 제공하는 메소드는 동일하다. 하지만 StringBuffer는 Thread safe하지만, StringBuilder는 Thread safe하지 않다(당연히 속도는 StringBuilder가 더 빠르다).

두 클래스는 문자열을 더하더라도 새로운 객체를 생성하지 않는다.

```java
StringBuilder sb = new StringBuilder();
sb.append("Hello").append(" world");
```

JDK 5이상에서는 String 더하기 연산을 할 경우, 컴파일 시 해당 연산을 StringBuilder로 변환해준다. 하지만 for 루프와 같이 반복 연산을 할 때는 일일이 변환해주지 않으므로 꼭 처리해줘야 한다.
