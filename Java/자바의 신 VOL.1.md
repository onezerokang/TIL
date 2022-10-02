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
자바를 실행하면 메인 메서드가 실행된다.

```java
class HelloWorld {
  public static void main(String args) {
    System.out.println("Hello World");
  }
}
```

## 3장 자바를 제대로 알려면 객체가 무엇인지를 알아야 해요

자바는 객체 지향 언어이다.
객체는 클래스의 복제본인데 인스턴스라고 하기도 한다.

생성자란 객체를 생성하는 도구다. 따로 생성하지 않으면 클래스를 컴파일 할 때 매개변수가 없는 기본 생성자를 자동으로 만든다.

인스턴스는 `new` + 생성자로 생성할 수 있다.
클래스는 대부분 그 자체로 동작할 수 없기 때문에 인스턴스를 생성하여 일을 시킨다.

## 4장 정보를 어디에 넣고 싶은데

자바에는 4가지 변수가 있다.

- 지역 변수
- 매개 변수
- 인스턴스 변수
- 클래스 변수

자바의 자료형은 원시형(primitive type)과 참조형(reference type)이 있다.

기본 자료형은 다음과 같다.

- byte
  - 값:
  - 기본 값:
- short
- int
- long
- char
- double
- float
- boolean

## 5장 계산을 하고 싶어요

계산을 할 때는 연산자(operator)를 사용한다.
연산자는 기본 자료형 + String에만 사용할 수 있다.
형 변환에 대한 이야기

## 6장 제가 조건을 좀 따져요

```
if(boolean){

}else if(boolean){

}else {

}
```

```
switch(primitive) {
  case value:

  case value:
  case value:
  case value:

break

  case value:
  default
}
```

```
while(boolean) {
  break, continue
}
```

```
for(?;?;?) {

}
```

## 7장 여러 데이터를 하나에 넣을 수는 없을까요?

배열: 한 변수에 한 가지 타입에 대한 여러 데이터를 저장할 수 있는 자료구조

```java
int [] lottoNumbers = new int(6); //권장 문법
int lottoNumbers[] = new int(6);  // 비권장 문법

int[] lottoNumbers = {1,2,3,4,5,6};

int[][] twoDim = new int[2][3];
```

```java
int [] lottoNumbers = new int(6);
for(int number: lottoNumbers) {
  System.out.println(number);
}
```

## 8장 참조 자료형에 대해서 더 자세히 알아봅시다

기본 생성자는 다른 생성자가 있으면 만들어지지 않는다.

```java
class Constructor {
  String data;
  public Constructor(){};
  public Constructor(String data){
    this.data = data;
  };
}
```

생성자는 인스턴스를 생성한다. 리턴타입이 없고 클래스와 이름이 같아야 한다.
생성자의 개수 제한은 없으나 너무 많으면 관리가 힘들어 꼭 필요한 생성자만 만들어야 한다.
this는 객체의 변수와 매개변수의 이름을 구분할 때 인스턴스 변수를 구분하기 위해 사용한다.

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

스테틱 메서드와 일반 메서드

스테틱 메서드는 인스턴스를 생성하지 않고 클래스에서 바로 사용이 가능하지만 static 변수만 사용 가능하다.
스테틱 변수는 모든 객체에서 하나의 값만 바라보기 때문에 남발해서는 안된다.

static 블록

여러 객체를 생성하지만 클래스를 ...

pass by value vs pass by reference

## 9장 자바를 배우면 패키지와 접근 제어자는 꼭 알아야 해요

## 10장 자바는 상속이라는 것이 있어요
