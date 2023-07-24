# DTO

DTO(Data Transfer Object)란 서로 다른 계층간 데이터를 주고 받거나, 클라이언트와 서버가 데이터를 교환할 때 사용하는 객체.

## Entity

Entity는 RDS의 테이블과 매핑되는 클래스로, Entity를 기준으로 테이블이 생성되고 변경된다.
이런 엔티티 덕분에 애플리케이션을 테이블 중심이 아닌 객체 중심 설계를 할 수 있게 된다.

## Entity가 아닌 DTO로 데이터를 교환하는 이유

1. Entity는 Table과 매핑되는 객체기 때문에 여기 저기서 사용되다가 속성 변경될 수도 있음
2. Entity의 모든 속성이 외부에 노출될 수 있음

## DTO와 toEntity, of 메서드

```java
@Getter
@Builder
@NoArgsConstructor
@AllArgsContructor
public class MemberRequest {
    private String name;
    private Integer age;

    public Member toEntity() {
        return Member.builder()
            .name(this.name)
            .age(this.age)
            .build();
    }
}
```

```java
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MemberResponse {
    private String name;
    private Integer age;

    public static MemberResponse of(Member member) {
        return MemberResponse.builder()
            .name(member.getName())
            .age(member.getAge())
            .build();
    }
}
```
