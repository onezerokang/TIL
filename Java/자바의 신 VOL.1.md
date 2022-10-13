# 자바의 신 VOL.1

## 1장 프로그래밍이란 무엇인가?

- 자바의 가장 작은 단위는 Class로 메서드나 변수는 반드시 클래스 안에 포함되어야 한다.
- 자바 코드에서 한줄이 끝날 때 세미콜론(;)을 적어줘야 자바가 다른 줄로 인식한다.

## 2장 Hello God Of Java

자바로 프로그래밍을 하기 위해선 JDK(Java Development Kit)와 개발 에디터를 설치해야 한다.
.java 확장자로 되어 있는 소스를 컴파일하면 .class 확장자를 가진 파일이 생성되어 디스크에 저장된다.
컴파일을 마친 클래스 파일은 JVM에서 읽어서 운영체제에서 실행된다.

자바를 컴파일하기 위해서는 클래스의 이름과 파일이름이 같아야 한다.
실행을 목적으로 한 자바 클래스는 메인 메소드가 필요하다.
클래스 파일을 실행하면 메인 메서드가 실행된다.

```java
class HelloWorld {
  public static void main(String args[]) {
    System.out.println("Hello World");
  }
}
```

## 3장 자바를 제대로 알려면 객체가 무엇인지를 알아야 해요

자바는 객체 지향 언어이다.
객체는 클래스의 복제본인데 인스턴스라고 하기도 한다.
클래스는 대부분 그 자체로 동작할 수 없기 때문에 인스턴스를 생성하여 일을 시킨다.
인스턴스는 `new` + `생성자`로 생성할 수 있다.

```java
public class Constructor {
  public static void main(String args[]) {
    // Constructor 생성자로 instance를 생성했다.
    Constructor instance = new Constructor();
  }
}
```

자바는 생성자는 따로 만들지 않으면 클래스를 컴파일 할 때 매개변수가 없는 기본 생성자를 자동으로 만든다.

## 4장 정보를 어디에 넣고 싶은데

### 자바의 변수 종류

- 지역 변수
  - 중괄호 내에서 선언된 변수로 중괄호 내에서만 유효하다.
- 매개 변수
  - 메소드에 넘겨주는 변수로 메소드를 호출할 때 생명이 시작되고 메소드가 끝나면 소멸된다.
- 인스턴스 변수
  - 메소드 밖에, 클래스 안에 선언된 변수로 객체가 시작할 때 생명이 시작되고, 그 객체를 참조하고 있는 다른 객체가 없으면 소멸한다.
- 클래스 변수
  - 메소드 밖에, 클래스 안에 static 예약어와 함께 선언된 변수로 클래스가 처음 호출될 때 생명이 시작되고, 자바 프로그램이 끝날 떄 소멸된다.

```java
public class VariableType {
  int instanceVariable;
  static int classVariable;

  public void method(int parameter) {
    int localVariable;
  }
}
```

### 자바의 자료형

자바의 자료형은 원시형(primitive type)과 참조형(reference type)이 있다.

#### 기본 자료형

- 정수형 타입
  - byte
    - 설명: -2<sup>7</sup> ~ 2<sup>7</sup>-1의 정수를 담는 자료형
    - 기본 값: 0
  - short
    - 설명: -2<sup>15</sup> ~ 2<sup>15</sup>-1의 정수를 담는 자료형
    - 기본 값: 0
  - int
    - 설명: -2<sup>31</sup> ~ 2<sup>31</sup>-1의 정수를 담는 자료형
    - 기본 값: 0
  - long
    - 설명: -2<sup>63</sup> ~ 2<sup>63</sup>-1의 정수를 담는 자료형. 만약 long의 값이 int를 초과한다면 수 뒤에 L을 붙여줘야 한다.
    - 기본 값: 0
  - char
    - 설명: 유니코드로 0('\u0000') ~ 65535('\uffff')의 정수를 담는 자료형
    - 기본 값: '\u0000'
- 소수형 타입
  - 설명: 32비트와 64비트로 제공할 수 있는 범위를 넘어서면 값의 정확성을 보장할 수 없기에 정확한 계산이 요구될 때는 `java.math.BigDecimal`이라는 클래스를 사용해야 한다.
  - double
    - 설명: 64비트로 표현된 소수
    - 기본 값: 0.0
  - float
    - 설명:32비트로 표현된 소수
    - 기본 값: 0.0
- boolean
  - 설명: true or false
  - 기본 값: false

## 5장 계산을 하고 싶어요

### 형 변환

형 변환은 변수 또는 리터럴의 타입을 다른 타입으로 변환시키는 것이다.

#### 묵시적 형변환

범위가 작은타입을 큰 타입으로 옮길 때는 암묵적으로 타입을 바꿔준다.

```
byte byteValue = 127;
short shortValue = byte;
```

#### 명시적 형변환

범위가 큰 타입을 작은타입으로 바꿀 때는 명시적으로 바꿔줘야 한다.

```
short shortValue = 128;
byte byteValue = (byte)shortValue;
```

범위가 큰 타입을 작은 타입으로 바꾸면 생각지도 모한 값이 나올 수 있으므로 신중히 형 변환을 해야 한다.

## 6장 제가 조건을 좀 따져요

### if

```
if(boolean){
  statement;
}else if(boolean){
  statement;
}else {
  statement;
}
```

### switch

하나의 값이 여러 범위에 걸쳐서 비교되어야 할 때는 하나의 값으로 분기하여 비교하는 switch 구문을 사용하는 것이 좋다.

```
switch(비교 대상 변수) {
  case 점검값1:
  처리문장1;
  break;
  case 점검값2:
  case 점검값3:
  case 점검값4:
  처리문장2;
  default:
  기본처리문장;
  break;
}
```

### while

```
while(boolean) {
  반복문장;
}
```

### for

```
for(초기화; 종료조건; 조건 값 증가) {
  반복문장;
}
```

## 7장 여러 데이터를 하나에 넣을 수는 없을까요?

### 배열

배열이란 한 변수에 한가지 타입에 대한 여러 데이터를 저장할 수 있는 자료구조이다.

```java
int [] lottoNumbers = new int(6); //권장 문법
int lottoNumbers[] = new int(6);  // 비권장 문법

int[] lottoNumbers = {1,2,3,4,5,6}; // 절대 변경되지 않는 값을 저장할 때 사용하는 방식

// 2차원 배열
int[][] twoDim = new int[2][3]; // 권장 문법
int twoDim[][] = new int[2][3]; // 비권장 문법

// 2차원 배열의 크기를 서로 다르게 지정하는 방법
int[][] twoDim = new int[2][];
twoDim[0] = new int[2];
twoDim[1] = new int[4];

// 배열과 Collection을 처리할 때 편한 for 루프
for(int number: lottoNumbers) {
  System.out.println(number);
}

```

## 8장 참조 자료형에 대해서 더 자세히 알아봅시다

### 생성자

생성자는 인스턴스를 생성한다. 특징으로는 리턴타입이 없고 클래스와 이름이 같다.
기본 생성자는 클래스에서 따로 생성자를 정의하지 않았을 경우 컴파일 단계에서 만들어지는 매개변수가 없는 생성자다. 즉 기본 생성자는 다른 생성자가 있으면 만들어지지 않는다.

```java
class Constructor {
  String data;
  public Constructor(){};
  public Constructor(String data){
    this.data = data;
  };
}
```

생성자의 개수 제한은 없으나 너무 많으면 관리가 힘들어 꼭 필요한 생성자만 만들어야 한다.
this는 인스턴스 변수와 매개변수의 이름을 구분할 때 인스턴스 변수를 구분하기 위해 사용한다.

### 오버로딩(Overloading)

오버로딩(overloading)이란 메서드의 이름은 같지만 매개변수의 타입, 개수, 위치가 다를 때 다른 메서드로 간주하는 것을 말한다.

```java
public class ReferenceOverloading {
  public static void main(String args[]){
    ReferenceOverloading reference = new ReferenceOverloading();
    reference.print(1);
    reference.print("hello");
    reference.print(1,"hello");
    reference.print("hello", 1);
  }
  public void print(int data){
    System.out.println(data);
  }
  public void print(String data){
    System.out.println(data);
  }
  public void print(String stringData, int intData){
    System.out.println(stringData + " " + intData);
  }
  public void print(int intData, String stringData){
    System.out.println(intData + " " + stringData);
  }
}
```

### 스테틱 메서드(static method)

스테틱 메서드는 인스턴스를 생성하지 않고 클래스에서 바로 사용이 가능한 메서드다. `System.out.println()`이 대표적인 스테틱 메서드다.

```java
public class StaticMethodExam {
  public static void main(String args[]) {
    StaticMethodExam.staticMethod();
  }

  public static void staticMethod() {
    System.out.println("Static method");
  }
}
```

스테틱 메서드는 스테틱 변수(클래스 변수)만 사용할 수 있다.
스테틱 변수는 모든 객체에서 하나의 값만 바라보기 때문에 남발해서는 안된다.

### 스테틱 블록(static block)

스테틱 블록은 객체가 생성되기전에 딱 한번만 호출되고, 그 이후에는 호출할 수 없다.

```java
public class StaticBlockExam {
  static int data = 0;
  static {
    System.out.println("Static block");
    data++;
  }

  public static void main(String[] args) {
    StaticBlockExam staticBlockExam = new StaticBlockExam(); //Static block
    System.out.println("data=" + data); //data=1
    StaticBlockExam staticBlockExam2 = new StaticBlockExam();
    System.out.println("data=" + data); //data=1
  }
}

```

### pass by value vs pass by reference

- pass by value
  - 값을 넘겨줄 때 원본을 복사해서 넘겨주는 것을 의미한다. 복사되어 넘겨진 값을 수정해도 원본의 값이 변경되진 않는다.
  - 기본 자료형은 무조건 pass by value로 데이터를 전달한다.
- pass by reference
  - 참조하는 주소를 넘겨준다. 넘겨진 값을 수정하면 원본이 변경된다.
  - 참조 자료형은 pass by reference로 데이터를 전달한다.
  - 단 참조자료형들도 호출된 메소드에서 다른 객체로 대체하여 처리하면 기존 값은 바뀌지 않는다(new 생성자를 이용하여 아예 새로운 참조형 데이터를 덮어쓸 때)

```java
public class ReferencePass {
  public static void main(String[] args) {
    ReferencePass reference = new ReferencePass();
    reference.callPassByValue();
    reference.callPassByReference();
  }
  public void callPassByValue() {
    int a = 10;
    String b = "b";
    System.out.println("before passByValue");
    System.out.println("a= " + a);
    System.out.println("b= " + b);
    passByValue(a,b);
    System.out.println("after passByValue");
    System.out.println("a= " + a);
    System.out.println("b= " + b);
  }

  public void passByValue(int a, String b) {
    a = 20;
    b = "z";
    System.out.println("in passByValue");
    System.out.println("a= " + a);
    System.out.println("b= " + b);
  }

  public void callPassByReference() {
    MemberDTO member = new MemberDTO("Sangmin");
    System.out.println("before passByReference");
    System.out.println("member.name= " + member.name);
    passByReference(member);
    System.out.println("after passByReference");
    System.out.println("member.name= " + member.name);
  }

  public void passByReference(MemberDTO member) {
    member.name = "Minsu";
  }
}

```

### 가변인자(varargs)

넘겨질 인자의 개수가 정확하지 않을 때 사용한다.

```java
public class VarargsExam {
  public static void main(String args[]) {
    VarargsExam exam = new VarargsExam();
    exam.printArgs("가", "나", "다", "라");
  }

  public void printArgs(String ...args) {
    for(int i = 0; i < args.length; i++) {
      System.out.println(args[i]);
      /*
      가
      나
      다
      라
      */
    }
  }
}
```

## 9장 자바를 배우면 패키지와 접근 제어자는 꼭 알아야 해요

### 패키지

패키지란 클래스의 집합으로 서로 관련있는 클래스를 묶어 파일을 효율적으로 관리하는 방법이다.
자바에서 패키지는 물리적으로 하나의 디렉터리를 의미한다.

패키지는 다음과 같이 선언할 수 있다.

- **문법**

```java
package 패키지이름;
```

- **예시**

```java
// 루트경로 기준으로 c/javapackage 디렉터리에 있는 패키지를 의미한다.
package c.javapackage;

public class Package {
  public static void main(String args[]) {
    System.out.println("Package")
  }
}
```

패키지를 선언할 때는 아래와 같은 규칙을 지켜야 한다.

- 패키지 선언은 소스 가장 첫 줄에 해야 한다.
- 파일 하나에 한번만 선언 되어야 한다.
- `package` 뒤에 오는 패키지 이름은 패키지가 위치한 폴더 이름과 같아야 한다.
- 패키지 이름은 java로 시작해서는 안된다.

패키지 이름 규칙은 기본적으로 다음과 같다.

- java
  - 자바 기본 패키지(java 벤더에서 개발)
- javax
  - 자바 확장 패키지(java 벤더에서 개발)
- org
  - 비영리 단체의 패키지
- com
  - 영리 단체의 패키지

패키지 이름을 지을 때 유의할 점은 다음과 같다.

- 모두 소문자로 작성한다.
- 자바의 예약어를 사용하지 않는다.
  - ex) com.int.util

#### import

다른 패키지의 클래스를 사용할 때는 `import`를 사용한다.

- **c/javapackage/sub/SubPackage.java**

```java
package c.javapackage.sub;

public class SubPackage {
  public void print() {
    System.out.println("I'm SubPackage");
  }
}
```

- **c/javapackage/Package.java**

```java
package c.javapackage;

import c.javapackage.sub.SubPackage;
// 혹은
import c.javapackage.sub.*;

public class Package {
  public static void main(String args[]) {
    SubPackage sub = new SubPackage();
    sub.print(); // I'm SubPackage;
  }
}
```

#### import static

JDK5에서 추가된 `import static`은 다른 패키지의 스테틱 메서드나 클래스 변수를 가져올 때 사용한다.

```java
package c.javapackage.sub;

public class SubStatic {
    public final static String CLASS_NAME = "SubStatic";

    public static void subStaticMethod(){
        System.out.println("subStaticMethod is called.");
    }
}
```

```java
package c.javapackage;

import c.javapackage.sub.Sub;
import static c.javapackage.sub.SubStatic.subStaticMethod;
import static c.javapackage.sub.SubStatic.CLASS_NAME;
// 혹은
import static c.javapackage.sub.SubStatic.*;

public class Package {
    public static void main(String[] args) {
        System.out.println("Package Class");
        Sub sub = new Sub();
        sub.subClassMethod();
    }
}
```

`import static`으로 가져온 메서드나 변수가 기존 클래스와 중복된다면 기존 클래스에 있는 메서드와 변수를 사용한다.

### 접근 제어자(Access Modifier)

접근 제어자란 클래스, 메서드, 클래스 변수, 인스턴스 변수를 선언할 때 사용한다.
접근 제어자의 종류는 다음과 같다.

- public
  - 누구나 접근 가능하다
- protected
  - 같은 패키지 내에 있거나 상속받은 경우에만 접근 가능하다
- package-private
  - 같은 패키지 내에 있을 때만 접근 가능하다
- private
  - 해당 클래스 내에서만 접근 가능하다

```java
public class MememberDTO {
  private String name;

  public MememberDTO(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }

  public String setName(String name) {
    this.name = name;
    return name;
  }
}
```

위 코드에서 인스턴스 변수, name은 private하게 생성되었기 때문에 반드시 `getName()`메서드와 `setName()` 메서드를 통해야만 조작할 수 있다.

#### 클래스 접근 제어자 선언시 유의점

클래스를 선언할 때 반드시 파일이름과 동일한 `public`으로 선언된 클래스가 있어야 한다.
파일이름과 다른 클래스가 `public`으로 선언되어있다면 그 파일은 컴파일 되지 않는다.

아래 코드는 public으로 선언된 클래스가 파일이름과 달라 컴파일되지 않는 예시 코드이다.

- **Package.java**

```java
package c.javapackage;

public class Package {
  public static void main(String args[]){}
};

// 위의 Package 클래스는 public으로 잘 선언됐지만 SecondPackage 클래스까지
// public으로 선언되어 컴파일 하지 못했다.
public class SecondPackage {}
```

## 10장 자바는 상속이라는 것이 있어요

자바에서 상속을 하면 부모클래스의 `public`, `protected` 메서드와 변수를 사용할 수 있다.
상속은 `extends` 키워드를 이용해서 할 수 있다.

```java
public class Child extends Parent {}
```

자식 클래스의 생성자가 호출되면 부모 클래스의 매개변수 없는 생성자가 실행된다.

## super

`super`는 부모 클래스의 생성자를 명시적으로 지정하는 것이다.
`super`는 두가지 방법으로 사용할 수 있다.

- `super()`
  - 부모 클래스의 생성자를 호출한다.
- `super.method()`
  - 부모 클래스의 메서드를 호출한다.

```java
public class Parent {
  String name;
  public Parent(String name) {
    this.name = name;
  }
  pubilc void introduce(){
    System.out.print("I'm " + name);
  }
}
```

```java
public class Child extends Parent {
  public Child(String name){
    super(name);
    super.introduce();
  }
}
```

자식 클래스의 생성자에서 `super()`를 명시적으로 호출하지 않으면 컴파일 시 자동으로 추가된다.
`super()`는 반드시 자식 클래스 생성자의 **첫줄**에서 호출되어야 한다.

## method overriding

메서드 오버라이딩이란 상속받은 메서드를 자식 클래스에서 재정의하여 사용하는 것을 말한다.
이때 재정의된 메서드는 다음과 같은 규칙을 따라야 한다.

- 리턴타입, 메서드 이름, 매개변수 타임 및 개수가 같아야 한다.
- 접근제어자의 범위가 더 넓어질 수는 있지만 좁아질 수는 없다(public한 부모 메서드를 private하게 오버라이딩 할 수 없다).

```java
public class Parent {
  String name;
  public Parent(String name) {
    this.name = name;
  }
  pubilc void introduce(){
    System.out.print("I'm " + name);
  }
}
```

```java
public class Child extends Parent {
  public Child(String name){
    super(name);
  }

  // 상속받은 introduce() 메서드를 오버라이딩 하였다.
  public void introduce(){
    System.out.print("My name is " + name);
  }
}
```

```java
public class MethodOverriding {
  public static void main(String args[]){
    Child child = new Child("Bangwon");
    child.introduce(); // My name is Bandwon
  }
}
```

## 참조자료형의 형변환

상속관계가 성립되면 객체끼리 형변환이 가능하다.
참조자료형의 형변환도 원시자료형의 형변환 같이 암묵적 형변환과, 명시적 형변환이 있다.

자식타입의 객체를 부모타입으로 변경할 때 암묵적 형변환이 이뤄진다.
이때 형변환을 당한 자식타입의 객체는 부모 클래스의 메서드만 사용할 수 있다.
다음은 암묵적 형변환의 예시이다.

```java
Child child = new Child();
Parent parent = child;
```

부모타입의 객체를 자식타입으로 변경할 때는 명시적 형변환을 해야한다.
단 부모타입의 객체는 자식 클래스로 생성된 객체여야 한다.

- **형변환이 되는 예시**

```java
Parent parent = new Child();
Child child = (Child)parent;
```

= **형변환이 안되는 예시**

```java
Parent parent = new Parent();
Child child = parent;

```

여러가지 값을 처리하거나 매개변수로 값을 전달 할 때는 보통 **부모의 클래스** 타입으로 보낸다.
이렇지 않으면 배열과 같이 여러 값을 한번에 본래 때 타입별로 구분하여 메서드를 만들어야 하는 문제가 생길 수 있다.
따라서 부모의 클래스의 타입으로 값을 보낸 후 `instanceof` 예약어를 이용하여 자식 타입으로 형변환 한다.

아래는 형변환에 대한 예시다.

- Computer.java

```java
public class Computer {
  String modelName;
  int battery

  public Computer(String modelName, int battery){
    this.modelName = modelName;
    this.battery = battery;
  }
}
```

- Macbook.java

```java
public class Macbook extends Computer {
  public Macbook(String modelName, int battery) {
    super(modelName, battery);
  }

  public void airDrop(){
    System.out.println("Success");
  }
}
```

- GaluxyBook.java

```java
public class GaluxyBook extends Computer {
  public GaluxyBook(String modelName, int battery) {
    super(modelName, battery);
  }

  public void quickShare(){
    System.out.println("Success");
  }
}
```

- **형변환을 사용하지 않은 예시**

- Charger.java

```java
public class Charger {
  public static void main(String args[]){
    Charger charger = new Charger();

    Macbook [] macbooks = new Macbook[2];
    macbooks[0] = new Macbook("Macbook Air", 130);
    macbooks[1] = new Macbook("Macbook Pro", 300);

    GaluxyBook [] galuxybooks = new GaluxyBook[2];
    galuxybooks[0] =new GaluxyBook("Galuxybook Pro", 180);
    galuxybooks[1] = new GaluxyBook("Galuxybook Go", 110);

    charger.charge(macbooks);
    charger.charge(galuxybookx);
  }

  public void charge(Macbook macbooks) {
    for(Macbook macbook: macbooks) {
      macbook.battery = 100;
      macbook.airDrop();
    }
  }

  public void charge(GaluxyBook galuxybooks) {
    for(GaluxyBook galuxybook: galuxybooks) {
      galuxybook.battery = 100;
      galuxybook.quickshare();
    }
  }
}
```

- **형변환을 사용한 예시**

- Charger.java

```java
public class Charger {
  public static void main(String args[]){
    Charger charger = new Charger();

    Computer [] computers = new Computer[4];
    computers[0] = new Macbook("Macbook Air", 130);
    computers[1] = new Macbook("Macbook Pro", 300);
    computers[3] = new GaluxyBook("Galuxybook Pro", 180);
    computers[4] = new GaluxyBook("Galuxybook Go", 110);

    charger.charge(computers);
  }

  public void charge(Computer computers) {
    for(Computer computer: computers) {
      computer.battery = 100;
      if(computer instanceof Macbook) {
        Macbook macbook = (Macbook) computer;
        macbook.airDrop();
      }else {
        Galuxybook galuxybook = (Galuxybook) computer;
        galuxybook.quickshare();
      }
    }
  }
}
```

## 모든 클래스의 부모 클래스는 Object에요

자바의 클래스는 아무 상속도 받지 않으면 기본적으로 `java.lang.Object` 클래스를 상속한다.
따라서 모든 클래스는 Object 클래스의 메서드를 호출할 수 있다.
Object 클래스에서 제공하는 메서드는 크게 객체처리를 위한 메서드와 쓰레드를 위한 메소드로 나뉘는데 이번 장에서는 객체 처리를 위한 메서드에 초점을 맞춘다.

다음은 Object 클래스에서 제공하는 메서드다.

- protected Object clone()
  - 객체의 복사본을 만들어 리턴한다.
- public boolean equals(Object obj)
  - 객체가 같은지 확인한다.
- protected void finalize()
  - 현재 객체를 참조하는 곳이 없을 떄 GC에 의해 호출되는 메서드이다.
- public Class<?> getClass()
  - 현재 객체의 Class 클래스의 객체를 리턴한다.
- public int hashCode()
  - 현재 객체의 16진수로 제공되는 메모리 주소를 리턴한다.
- public String toString()
  - 객체를 문자열로 표현하는 값을 리턴한다.

위 메서드 중 자주 사용하는 메서드는 순서대로 `toString()`, `equals()`, `hashCode()` 정도이다.

### toString()

`toString()` 메서드는 객체를 문자열로 표현하는 값을 리턴한다.
자바에서는 `toString()`를 자동으로 호출할 때가 있는데 그 상황은 다음과 같다.

- `System.out.println()` 메소드의 매개변수로 들어갔을 때 `toString()` 메서드가 호출된다.
- String을 제외한 참조형 자료에 연산자를 사용하는 경우 `toString()`.메서드가 호출된다.

```java
Object obj = new Object();
//아래 코드는 System.out.println(obj.toString());과 같다.
System.out.println(obj);
System.out.println(+obj);
```

`toString()` 메서드의 구조는 다음과 같다.

```java
// 패키지 이름 + @ + 16진수 메모리 주소
getClass().getName() + "@" + Integer.toHexString(hashCode());
```

상속받은 `toString()` 메서드를 그대로 사용하면 `"패키지 이름 + @ 16진수 메모리 주소"`를 리턴하기에 객체의 값을 확인하는 용도로는 적합하지 않다.
만약 `toString()`을 사용해야 한다면 해당 메서드를 오버라이딩 해야 한다.

```java
public class UserDTO {
  String name;
  int age;

  public UserDTO(String name, int age) {
    this.name = name;
    this.age = age;
  }

  public String toString() {
    return "name=" + name + " age=" + age;
  }
}
```

위 예시처럼 `toString()`을 오버라이딩하면 다음과 같이 간단하게 사용할 수 있다.

```java
UserDTO user = new UserDTO("이상혁", 26);
// toString()은 자동으로 호출되었다.
System.out.println(user) // "name= 이상혁 age= 26"
```

### equals()

`equals()` 메서드는 객체가 같은지 확인한다.
상속받은 `equals()`를 그대로 사용한다면 `hashCode()` 값을 비교한다.
따라서 클래스의 인스턴스 변수값들이 같다고 하더라도, 해시 코드가 다르면 false를 리턴하게 된다.

따라서 객체의 변수값만 비교하고 싶다면 `toString()`과 마찬가지로 오버라이딩해야 한다.
다행인 점은 많은 IDE에서 `equals()` 메서드를 자동으로 생성해주는 기능을 제공한다.

### hashCode()

`hashCode()` 메서드는 객체의 메모리주소를 16진법으로 리턴한다.
만약 `equals()` 메서드를 오버라이딩 했다면 `hashCode()` 메서드도 오버라이딩 해주어야 한다.

다행인 점은 많은 IDE에서 `equals()` 메서드를 자동으로 생성해주는 기능을 제공한다.

## 인터페이스와 추상클래스, enum

일반적인 개발절차는 분석, 설계, 개발 및 테스트, 시스템 릴리즈 순서로 진행된다.
인터페이스와 추상클래스는 설계단계에서 클래스가 어떤 메서드와 변수를 갖을지 미리 정의해둘 수 있다.

### 인터페이스

인터페이스의 특징은 다음과 같다.

- 인터페이스를 만들 때는 `interface` 예약어를 사용한다.
- 인터페이스는 클래스와 같이 .java 확장자를 사용하고 컴파일 방식도 같기 때문에 인터페이스 앞에 I를 붙여 구분하는 방식을 사용한다(필수는 아님)
- 클래스 뒤에 `implements` 예약어와 인터페이스가 있으면 해당 클래스는 인터페이스를 구현해야 한다.
- 클래스는 인터페이스에 정의된 메서드를 반드시 구현해야 한다(구현하지 않으면 컴파일 에러가 발생한다).
- 클래스는 여러개의 인터페이스를 구현할 수 있다.

다음은 인터페이스의 예시코드이다.

```java
public interface IMemberManager {
  public boolean addMember(MemberDTO member);
  public boolean deleteMember(number id);
}
```

```java
public class MemberManager implements IMemberManager {
  public boolean addMemeber(MemberDTO member) {
    return false;
  }
  public boolean deleteMember(number id) {
    return false;
  }
}
```

다음은 인터페이스를 만들고 사용할 때 갖는 장점이다

- 개발자 역량에 따른 클래스, 메서드, 변수 네이밍 수준의 격차를 줄일 수 있다.
- 미리 네이밍을 해두면 실제 개발 단계에서 변수명이나 매개변수 구조등을 고민할 필요가 없다.
- 선언과 구현을 구분할 수 있다.

### 추상클래스

추상클래스의 특징은 다음과 같다

- 추상클래스는 `class` 앞에 `abstract` 예약어를 붙여 선언할 수 있다.
- 추상 클래스 안에는 `abstract`로 선언된 메서드가 0개 이상 있어야 한다.
- 클래스에 `abstract` 메서드가 하나라도 있다면 해당 클래스는 반드시 `abstract`으로 선언되어야 한다.
- `abstract` 클래스는 몸통이 있는 메서드가 0개 이상 있어도 괜찮다.
- `abstract` 클래스는 extends로 상속받을 수 있다.

다음은 추상클래스의 예시코드이다.

```java
public abstract class MemberManagerAbstract {
    public boolean addMember(MemberDTO member);
  public boolean deleteMember(number id);
  public void printLog(String data) {
    System.out.println("Data= " + data);
  }
}
```

```java


```

### 인터페이스와 추상클래스의 차이

### final

`final` 예약어는 클래스, 메서드, 변수에 사용할 수 있다.

- final 클래스
  - 다른 클래스가 final 클래스를 상속하지 못하게 한다.
- final 메서드
  - 다른 클래스가 final 메서드를 오버라이딩하지 못하게 한다.
- final 클래스 변수 & 인스턴스 변수
  - 변수를 값을 바꿀 수 없는 상수로 만든다. 선언을 하고 값을 지정하지 않으면 컴파일 에러가 발생한다.
- final 로컬변수 & 매개변수
  - 변수를 값을 바꿀 수 없는 상수로 만든다. 선언을 하고 값을 지정하지 않아도 컴파일 에러가 발생하지는 않는다.
- final 참조 자료형
  - 참조 자료형을 final로 선언하더라도 참조 자료형 안에 있는 변수까지 final 변수가 되진 않는다.

```java
public final finalClass {
  public final printLog(String data) {
    System.out.println("Data= " + data);
  }
}
```

### enum

enum은 상수의 집합을 모아놓은 클래스이다.
다음은 enum을 선언하고 사용하는 예시이다.

```java
public enum Role {
  NORMAL,
  ADMIN;
}
```

```java
public class Auth {
  public static void main(String args[]) {
    Auth auth = new Auth();
    auth.checkAdmin(Role.Admin);
  }

  public boolean checkAdmin(Role role) {
    switch(role) {
      case NORMAL:
        return false;
      case ADMIN:
        return true;
    }
  }
}
```

## 다 배운 것 같지만, 예외라는 중요한 것이 있어요

### try...catch 블록

자바에서는 `try..catch 블록`을 이용해서 예외를 처리할 수 있다.
`try...catch 블록`으로 감싸지 않은 곳에서 예외가 발생하면 해당 스레드가 종료된다.

```java
try{
// 예외가 발생할 수 있는 코드
}catch(NullPointerException e) {
  // NullPointer 예외가 발생했을 때 실행할 코드
}catch(ArrayIndexOutOfBoundsException e) {
  // ArrayIndexOutOfBounds 예외가 발생했을 떄 실행할 코드
}catch(Exception e) {
  // 위에 명시한 예외가 아닌 예외가 발생했을 때 실행할 코드
}finally {
  // 예외 발생 여부와 상관없이 실행할 코드
}
```

`try...catch 블록`의 특징은 다음과 같다.

- catch 블록은 여러개를 사용할 수 있다.
- 먼저 선언한 catch 블록의 예외 클래스가 다음에 선언한 catch 블록의 부모에 속하면, 자식에 속하는 catch 블록은 절대 실행될 일이 없으므로 컴파일이 되지 않는다.
- 하나의 try 블록에서 예외가 발생하면 그 예외와 관련있는 catch 블록이 실행된다.
- catch 블록 중 발생한 예외와 관련있는 블록이 없으면, 예외가 발생되면서 해당 쓰레드는 종료된다. 이를 방지하기 위해 마지막 catch ㅂ르록에는 Exception 클래스로 묶어주는 버릇을 갖는게 좋다.

### 예외의 종류

- checked exception
  - 컴파일 시 찾을 수 있는 예외다.
- error
  - 자바 프로그램 밖에서 발생한 예외를 말한다(서버의 디스크가 고장나거나 메인보드가 맛이 간 경우 등)
- runtime exception
  - 컴파일로 잡지 못한 예외이다. 런타임 예외에 해당하는 모든 예외는 `RuntimeException`를 확장한 예외이다.

### Throwable

`Exception` 클래스와 `Error` 클래스는 `Throwable` 클래스를 공통으로 상속한다. `Throwable` 클래스는 다음과 같은 생성자를 갖는다.

- `Throwable()`
- `Throwable(String message)`
- `Throwable(String message Throwable cause)`
- `Throwable(Throwable cause)`

`Throwable` 클래스에 선언되어있고 `Exception` 클래스에서 오버라이딩한 메서드는 10개가 넘는다. 그 중 많이 사용되는 메서드는 다음과 같다.

- `getMessage()`
  - 예외 메시지를 String 형태로 제공받는다.
- `toString()`
  - 예외 메시지와 예외 클래스 이름을 String 형태로 제공받는다.
- `printStackTrace()`
  - 예외 메시지와 스택 트레이스를 출력해준다. printStackTrace는 메시지 량이 많기 때문에 로그가 엄청나게 쌓일 수 있다. 그러므로 꼭 필요한 곳에서만 사용하는 것을 권장한다.

### throw, throws

개발자는 `throw` 이후에 예외 클래스의 객체를 생성하여 예외를 발생시킬 수 있다.

```java
throw new Exception("유효한 이메일이 아닙니다");
```

메서드를 선언할 때 매개 변수 소괄호 뒤에 `throws` 예약어를 적어준 후 예외를 선언하면, 해당 메서드에서 선언한 예외가 발생했을 때 호출한 메서드로 예외처리를 위임할 수 있다. 즉 해당 메서드에서 예외를 `try...catch`로 감싸지 않아도 스레드가 종료되지 않는다.

```java
public void throws() throws NullPointerException, Exception {}
```

### 커스텀 예외

`Throwable`, `Exception` 등을 상속하여 커스텀 예외를 만들 수 있다.

```java
public class MyException extends Exception {
  public MyException() {
    super();
  }
  public MyException(String message) {
    super(message);
  }
}
```
