# 24장 자바랭 다음으로 많이 쓰는 애들은 컬렉션 - Part3(Map)

Map은 java.util 패키지의 Map이라는 인터페이스로 선언되어 있다.

다음은 Map 인터페이스에 선언되어 있는 메소드다. put(), get(), remove()는 꼭 기억하자.

- put(K key, V value)
- putAll(Map<? extends K, ? extends V> m)
- get(Object key)
- remove(Object key)
- keySet()
- values()
- entrySet()
- size()
- clear()

## Map을 구현한 클래스들

- HashMap
- TreeMap
- LinkedHashMap
- Hashtable

Hashtable은 Map 인터페이스를 구현하기는 했지만 일반적인 Map 인터페이스를 구현한 클래스들과는 다르다. 이 두 종류의 다른 점을 간단하게 정리하자면 다음과 같다.

- Map은 Collection view를 사용하지만, Hashtable은 Enumeration 객체를 통해서 데이터를 처리한다
- Map은 키, 값, 키-값 쌍으로 데이터를 순환하여 처리할 수 있지만, Hashtable은 키-값 쌍으로 데이터를 순환하여 처리할 수 없다.
- Map은 이터레이션을 처리하는 도중에 데이터를 삭제하는 안전한 방법을 제공하지만, Hashtable은 그러한 기능을 제공하지 않흔다.

HashMap과 Hashtable 클라스는 다음과 같은 차이가 있다.

- 키나 값에 null 저장 여부
  - HashMap: 가능
  - Hashtable: 불가능
- thread safe 여부
  - HashMap: 불가능
  - Hashtable: 가능

Hashtable은 JDK 1.0부터 만들어졌지만 Collection 인터페이스는 JDK 1.2에 추가되었다.
이미 만들진 Hashtable이 Map에 맞추어 보완되었기 때문에 이런 차이가 발생한다.

Hashtable을 제외한 Map 구현 클래스들은 다중 스레드에서 사용될 때 다음과 같이 선언하여 사용해야만 한다.

```java
Map m = Collections.synchronizedMap(new HashMap(...))
```

## HashMap

다음은 HashMap의 상속 관계다.

```
java.lang.Object
    ㄴ java.util.AbstractMap<K, V>
        ㄴ java.util.HashMap<K, V>
```

구현한 인터페이스는 다음과 같다.

- Serializable
- Cloneable
- Map<E>

생성자는 다음과 같다.

- HashMap()
- HashMap(int initialCapacity)
- HashMap(int initialCapacity, float loadFactor)
- HashMap(Map<? extends K, ? extends V> m)

대부분 매개 변수가 없는 생성자를 사용하지만, HashMap에 담을 데이터가 많은 경우에는 초기 크기를 지정해주는 것이 좋다.

HashMap의 키는 기본 자료형과 참조 자료형 모두 될 수 있다. **만약 어떤 클래스를 만들어 그 클래스를 키로 사용할 때는 equals()와 hashCode() 메소드를 잘 구현해 놓아야 한다.**

HashMap에 객체가 들어가면 hashCode() 결과 값에 따른 bucket이라는 list 형태의 바구니가 만들어진다. 만약 서로 다른 키가 저장되었는데, hashCode() 메소드의 결과가 동일하다면, 이 버켓에 여러 개의 값이 들어갈 수 있다. 따라서 get() 메소드가 호출되면 hashCode()의 결과를 확인하고, 버켓에 들어간 목록에 데이터가 여러 개일 경우 equals() 메소드를 호출하여 동일한 값을 찾게 된다. 따라서 키가 되는 객체를 직접 작성할 때는 hashCode()와 equals()를 반드시 오버라이딩하자.

get() 메소드로 없는 키를 찾을 때는 null을 리턴한다.

put() 메소드로 존재하는 키를 넣을 때는 새로운 값으로 덮어쓴다.

## 정렬된 key 목록을 원한다면 TreeMap을 사용하자

TreeMap에 데이터를 저장하면 '숫자 > 알파벳 대문자 > 알파벳 소문자 > 한글' 순으로 키를 정렬한다.

대신 HashMap보단느 느리다.

TreeMap이 키를 정렬하는 것은 SortedMap 인터페이스를 구현했기 때문이다.

키를 검색하기 좋기 떄문에, 키를 검색하는 프로그램을 작성할 때 매우 도움이 된다.

## Map을 구현한 Properties 클래스

Properties는 Hashtable을 상속한 클래스다. 따라서 Map 인터페이스에서 제공하는 모든 메소드를 사용할 수 있다.

```java
public class PropertiesSample {
    public static void main(String[] args) {
        Properties prop = System.getProperties();
        Set<Object> keySet = prop.keySet();
        for(Object tempObject: keySet) {
            System.out.println(tempObject + "=" + prop.get(tempObject));
        }
    }
}

```

```shell
java.specification.version=17
sun.jnu.encoding=UTF-8
java.class.path=/Users/wonyoung/dev/godofjava/out/production/godofjava
java.vm.vendor=Oracle Corporation
sun.arch.data.model=64
java.vendor.url=https://java.oracle.com/
java.vm.specification.version=17
os.name=Mac OS X
sun.java.launcher=SUN_STANDARD
user.country=KR
sun.boot.library.path=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home/lib
sun.java.command=chap24.PropertiesSample
http.nonProxyHosts=local|*.local|169.254/16|*.169.254/16
jdk.debug=release
sun.cpu.endian=little
user.home=/Users/wonyoung
user.language=ko
java.specification.vendor=Oracle Corporation
java.version.date=2023-04-18
java.home=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home
file.separator=/
java.vm.compressedOopsMode=Zero based
line.separator=

java.vm.specification.vendor=Oracle Corporation
java.specification.name=Java Platform API Specification
sun.management.compiler=HotSpot 64-Bit Tiered Compilers
ftp.nonProxyHosts=local|*.local|169.254/16|*.169.254/16
java.runtime.version=17.0.7+8-LTS-224
user.name=wonyoung
path.separator=:
os.version=13.3.1
java.runtime.name=Java(TM) SE Runtime Environment
file.encoding=UTF-8
java.vm.name=Java HotSpot(TM) 64-Bit Server VM
java.vendor.url.bug=https://bugreport.java.com/bugreport/
java.io.tmpdir=/var/folders/ff/0wknmmj139b2fkcmtmpqrn180000gn/T/
java.version=17.0.7
user.dir=/Users/wonyoung/dev/godofjava
os.arch=aarch64
java.vm.specification.name=Java Virtual Machine Specification
native.encoding=UTF-8
java.library.path=/Users/wonyoung/Library/Java/Extensions:/Library/Java/Extensions:/Network/Library/Java/Extensions:/System/Library/Java/Extensions:/usr/lib/java:.
java.vm.info=mixed mode, sharing
java.vendor=Oracle Corporation
java.vm.version=17.0.7+8-LTS-224
sun.io.unicode.encoding=UnicodeBig
socksNonProxyHosts=local|*.local|169.254/16|*.169.254/16
java.class.version=61.0
```

그렇다면 왜 HashMap이나 Hashtable을 사용하지 않고 Properties 클래스를 사용하는 것일까?
그 이유는 Properties 클래스에서 추가로 제공하는 메소드들을 보면 알 수 있다.

- load(InputStream inStream)
- load(Reader reader)
- loadFromXML(InputStream in)
- store(OutputStream out, String comments)
- store(Writer writer, String comments)
- storeToXML(OutputStream os, String comment)
- storeToXML(OutputStream os, String comment, String encoding)

Properties 클래스의 객체에 시스템 속성만 저장할 수 있는게 아니다.

어플리케이션에서 사용할 여러 속성값들을 Properties 클래스를 사용하여 데이터를 넣고, 빼고, 저장하고, 읽어들일 수 있다.

이 클래스가 없다면 직접 파일을 읽는 메소드를 만들고, 파일에 쓰는 메소드도 만들어야만 한다.
