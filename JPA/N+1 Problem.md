# N+1 Problem

## 인트로

- 최근 모 회사의 기술과제를 진행하게 되었다.
- 과제는 여러 데이터 샘플과 요구사항을 제공했고, 필자는 해당 요구사항을 기반으로 테이블을 모델링하고, API를 개발해야 했다.
- 총 11개의 테이블이 생성 되었고, 테이블간 연관관계가 맺어져 있다보니 데이터를 조회하는 과정에서 N+1 문제가 발생했다.
- N+1 문제를 해결하기 위해 쿼리를 튜닝하던 중, N+1 문제에 대해 확실히 정리하면 좋을 것 같다고 생각했다.

## N+1 문제란

- N+1 문제란 한 번의 SELECT 쿼리로 데이터를 가져올 것을 기대했으나 N개 쿼리가 추가로 발생하는 문제이다.
- JPA에서 연관관계가 맺어진 데이터를 가져올 때 발생한다.

## 문제 상황

- 기술 과제의 요구사항을 그대로 사용할 수는 없으니, 예제로 사용할 엔티티를 만들겠다.
- 게시글(Post) 엔티티와, 댓글(Comment) 엔티티가 존재한다고 가정하자.

```java
@Getter
@Entity
public class Post {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String content;

    @OneToMany(mappedBy = "post", fetch = FetchType.LAZY)
    private List<Comment> comments;
}
```

```java
@Getter
@Entity
public class Comment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String text;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "post_id")
    private Post post;
}
```

- 이제

## Fetch Join

- Fetch Join은 JPQL의 기능으로, 한번에 연관된 엔티티를 가져올 수 있다.

```java
interface PostRepository extends JpaRepository<Post, Long> {
    @Query("select p from Post p join fetch p.comments")
    public List<Post> findAllFetchJoin();
}
```

## @EntityGraph

- @EnityGraph는 조회 시 한번에 가져올 필드를 지정하는 어노테이션이다.

## 주의 사항

- XXToOne 관계에서는 Fetch Join과 @EntityGraph를 사용해도 괜찮다.
- 하지만 XXToMany 관계에서는 이를 사용하면 중복 데이터를 가져온다.
- 따라서 페이징을 할 수 없다.
- 이 경우 BatchSize를 줘서, where ... in()문을 사용하도록 해야 한다.

## BatchSize

- @BatchSize
-

## 결론

- fetch join으로 쿼리할 수 있는 것은 fetch join으로 최적화한다.
- 글로벌 설정으로 batch size를 설정하여 fetch join으로 할 수 없는 것은 그렇게 처리한다.

## 참조

- <a href="https://www.inflearn.com/course/ORM-JPA-Basic" target="_blank">자바 ORM 표준 JPA 프로그래밍 - 기본편, 김영한</a>
- <a href="https://jojoldu.tistory.com/165" target="_blank">JPA N+1 문제 및 해결방안</a>
- <a href="https://youtu.be/ni92wUkAmQI?feature=shared" target="_blank">[10분 테코톡] 수달의 JPA N+1 문제
  </a>
