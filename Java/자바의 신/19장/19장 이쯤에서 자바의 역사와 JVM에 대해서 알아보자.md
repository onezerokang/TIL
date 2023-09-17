# 19장 이쯤에서 자바의 역사와 JVM에 대해서 알아보자

## JDK의 플랫폼에 따른 차이

자바는 Oracle에서만 만드는 것이 아니다. 각 Java 버전에서 제공되어야 하는 표준 문서가 만들어지면 그 기준에 해당하는 각 벤더에 맞는 JDK가 별도로 만들어지는 것이다. 따라서 HP나 IBM도 JDK를 만든다.

어떤 OS에서 개발하든지 JDK의 버전만 맞으면 적용할 OS에서 컴파일만 하면 애플리케이션 실행에 문제가 없다.
즉, Oracle JDK로 개발하고, HP의 JDK에서 컴파일하더라도 전혀 문제가 발생하지 않는다.

## JDK, J2SE, Java SE 외에 자바에서 사용되는 다른 용어들

- JDK: Java Development Kit
- J2SE: Java 2 Standard Edition
- Java SE: Java Standard Edition

Java 2에서 2가 빠진 것은 Java SE 6가 출시되면서부터이며, 마케팅을 위해서 Java로 통칭한 것이다.

자바를 개발하기 위해서 설치를 하다 보면, JDK와 JRE로 분리되어 있는 것을 확인할 수 있다. 여기서 각각의 용어는 다음을 의미한다.

- JDK: Java Development Kit
- JRE: Java Runtime Environment

JRE는 자바를 실행할 수 있는 환경의 집합이다. 따라서, 이 JRE만 설치하면 자바를 컴파일하는 각종 프로그램이 제외된 상태로 설치된다.

## 자바 언어의 특징

1. It should be "simple, object-oriented and familiar"
2. It should be "robust and secure"
3. It should be "architecture-neutral and portable"
4. It should be execute with "high performance"
5. It should be "interpreted, threaded, and dynamic"

## 자바의 버전별 차이

JDK 1.0 ~ 1.3버전까지 차이는 그리 중요하지는 않다.

### JDK 1.0

최초의 버전이다.

### JDK 1.1

JDK 1.1에서 추가된 주요 기능은 다음과 같다.

- AWT의 이벤트 모델의 확장 및 변경
  - AWT: Abstract Window Toolkit의 약어로 자바를 이용하여 UI를 구성할 때 사용되는 기술
- 내부 클래스(inner class) 추가
- JavaBeans, JDBC, RMI 등 추가

  - JavaBeans: 자바에서 제공하는 컴포넌트 모델 중 하나
  - JDBC: Java Database Connectivity의 약자로, 자바에서 DB에 데이터를 담기 위한 API
  - RMI: Remote Method Invocation: JVM에 있는 메소드가 아닌, 원격 JVM에 있는 메소드를 호출하기 위한 기술

### JDK 1.2

JDK 1.2 ~ 1.5까지는 J2SE로 불렸으며, 새로운 버전의 자바라는 의미에서 Java 2라는 이름이 생겼다.

다음은 JDK 1.2에서 추가된 사항이다.

- strictfp 예약어 추가
- 자바에서 GUI를 제공하기 위한 Swing이 코어 라이브러리에 추가
- JIT라는 컴파일러가 Sun JVM에 처음 추가
  - JIT: Just-In-Time의 약자로 에떤 메소트의 일부 혹은 전체 코드를 native code로 변환하여 JVM에 의해 변역되지 않으로 함으로써 보다 빠른 성능을 제공하는 기술
- 자바 플러그인 추가
- CORBA라는 지금은 별로 사용하지 않는 기술과 데이터를 주고 받기 위한 IDL 추가
- 자바에서 각종 자료 구조를 쉽게 처리하기 위한 Collections라는 프레임워크 추가

### JDK 1.3

JDK 1.3에서는 다음과 같은 사항들이 추가되었다.

- HotSpot JVM 추가
- CORBA와의 호환성을 위해 RMI tnwjd
- 자바에서 사운드를 처리하기 위한 JavaSound 코어 라이브러리 추가
- JNDI(Java Naming and Directory Interface)가 코어 라이브러리에 추가
- 자바의 디버깅을 보다 쉽게 하기 위한 JPDA(Java Platform Debugger Architecture) 추가
- Synthetic 프록시 클래스 추가

### JDK 1.4

- assert 예약어 추가
- Perl 언어의 정규표현식을 따르는 정규 표현식 추가
- exception chaining을 통해 하위 레벨의 예외의 캡슐화가 가능해짐
- IPv6 지원 시작
- NIO(New I/O)라는 non-blocking 추가
- logging API 추가
- JPEG나 PNG와 같은 이미지를 읽고 쓰기 위한 image I/O API 추가

### Java 5

Java 5에서 매우 많은 변화가 있었다.

- 보다 안전하게 컬렉션 데이터를 처리할 수 있는 제네릭 추가
- 어노테이션이라고 불리는 메타데이터 기능 추가
- 기본 자료형과 그 기본 자료형을 객체로 다루는 클래스 간의 데이터 변환이 자동으로 발생하는 autoboxing과 unboxing 기능 추가
- 상수 타입을 나타내는 enum 추가
- 매개 변수의 개수를 가변적으로 선언할 수 있는 varargs 추가
- 배일이나 컬렉션 타입에 저장된 데이터를 순차적으로 꺼내는 향상된 for 루프 추가
- static import 추가
- 스레드 처리를 쉽게 할 수 있는 java.util.concurrent 패키지 추가
- Scanner 클래스 추가

### Java 6

Java 6는 기능이 많이 추가되지는 않았지만 안정성과 확장성이 증가하였다.

- 스크립팅 언어가 JVM 위에서 수행 가능하게 됨
- 각종 코어 기능의 성능 개선
- Compiler API가 추가되어 프로그램에서 자바 컴파일러 실행이 가능

### Java 7

Java 6가 나오고 5년만에 출시된 Java 7은 향상되고 추가된 부분들이 매우 많다. 이 부분에 대해서는 30장과 31장에서 별도로 살펴보자.

### Java 8

- 람다 표현식 사용이 가능해짐

## JIT 컴파일러란?

Just-In-Time의 약자로, JIT을 사용하는 언어에는 자바와 .NET 등이 있다.
JIT을 좀더 쉬운말로 하면 동적 변환(dynamic translation)이라고 볼 수 있다.
JIT은 컴파일러지만, 실행시 적용되는 기술로 프로그램 실행을 보다 빠르게 하기 위해 존재한다.

JIT은 정적 컴파일 방식과 인터프리터 방식을 혼합한 것이다.
변환 작업은 인터프리터에 의해서 지속적으로 수행되지만, 필요한 코드는 메모리에 올려두었다가 재사용하게 된다.

javac 명령어로 만들어진 class 파일은 bytecode일 뿐이다.
이를 컴퓨터가 알아먹을 수 있도록 하려면 다시 변환 작업이 필요한데 이 변환작업을 JIT 컴파일러에서 한다고 보면 된다.

즉 JVM -> 기계 코드로 변환되는 부분을 JIT에서 수행하는 것이다.

## HotSpot이란?

JDK 1.3부터 제공되는 HotSpot JVM이 제공된다.
HotSpot JVM은 HotSpot 클라이언트 컴파일러, HotSpot 서버 컴파일러의 두 가지 컴파일러를 제공한다.

과거 PC는 지금처럼 하드웨어 성능이 좋지 않았기 때문에 자바를 실행하는 주체가 클라이언트 장비인지, 서버 장비인지를 구분하고 그에 맞는 컴파일러를 사용했다.

다음은 자바에서 클라이언트 장비인지 서버 장비인지 확인하는 기준이다.

- 2개 이상의 물리적 프로세서
- 2GB 이상의 물리적 메모리

이 조건을 만족하면 Oracle JVM은 서버 컴파일러를 선택한다.

명시적으로 지정해주고 싶다면 -client, -server라고 지정해주면 된다.

```shell
java -server Calculator
```
