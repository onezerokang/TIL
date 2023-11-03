# Lombok이란

## 1. 개요

Lombok이란 getter, setter, toString 같이 자주 사용되는 메소드를 어노테이션으로 간단하게 작성할 수 있는 자바의 라이브러리다. Lombok을 사용하여 반복되는 코드를 줄이고, 가독성과 유지보수성을 높일 수 있다.

다음과 같이 getter와 setter를 모두 구현할 경우 코드가 길어지고 가독성이 떨어지지만, 롬복을 사용하면 보다 핵심 로직에 집중할 수 있게 된다.

```java
// lombok 사용
@Getter
@Setter
public class Member {
    private String email;
    private String password;
    private String username;
    private int age;
}
```

## 참조

- [Project Lombok](https://projectlombok.org/)
- [더 자바, 코드를 조작하는 다양한 방법](https://www.inflearn.com/course/the-java-code-manipulation#reviews)
