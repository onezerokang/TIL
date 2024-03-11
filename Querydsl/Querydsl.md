# Querydsl

## 개요

- Querydsl은 복잡한 쿼리, 동적 쿼리를 작성할 때 유용하다.
- 쿼리를 자바 코드로 작성하기에 문법 오류를 컴파일 시점에 체크한다.

## Querydsl 설정

- Querydsl 환경 설정은 개발 환경(버전)마다 다르기 때문에 사용하는 환경에 맞는 버전을 사용해야 한다.

### Java 17 & Spring Boot 3.X 설정

```groovy
// dependencies 추가
dependencies {
	implementation 'com.querydsl:querydsl-jpa:5.0.0:jakarta'
	annotationProcessor "com.querydsl:querydsl-apt:${dependencyManagement.importedProperties['querydsl.version']}:jakarta"
	annotationProcessor "jakarta.annotation:jakarta.annotation-api"
	annotationProcessor "jakarta.persistence:jakarta.persistence-api"
}
```

- 이후 gradle tab → Tasks → other → compileJava 수행
- /build/generated/annotationProcessor 경로에 Q-Type 클래스 생성

## JPQL vs Querydsl

- JPQL은 문자로 작성되어 있어서 실행하기 전까지 오류를 알 수 없다.
- Querydsl은 컴파일 시점에 오류를 잡아준다(QType을 만들어서 코드로 풀어내기 때문이다).
- 다음 예시는 회원을 조회하는 JPQL과 Querydsl이다.

```java
@SpringBootTest
@Transactional
class QueryTest {
  @Autowired
  EntityManager em;

  @Test
  void jpql() {
      // member1를 찾아라.
      String qlString = "select m from Member m where m.username = :username";
      Member findMember = em.createQuery(qlString, Member.class)
              .setParameter("username", "member1")
              .getSingleResult();

      assertThat(findMember.getUsername()).isEqualTo("member1");
  }

  @Test
  void querydsl() {
      JPAQueryFactory queryFactory = new JPAQueryFactory(em); // entity manager를 넘겨야 한다.
      QMember m = new QMember("m"); // alias

      Member findMember = queryFactory
              .selectFrom(m)
              .from(m)
              .where(m.username.eq("member1"))
              .fetchOne();

      assertThat(findMember.getUsername()).isEqualTo("member1");
  }
}
```

## 기본 Q-Type 활용

- new QMember("m"): alias 활용
  - 같은 테이블을 조인하는 경우, alias가 겹치기 때문에 위 방법대로 alias를 선언해서 사용해야 한다.
- QMember.member: 내부 인스턴스 활용 방법
  - alais가 겹치지 않는 상황에서는 Q-Type을 static import해서 사용하는 것을 권장한다.

## 동적 쿼리 작성방법

- 동적 쿼리를 작성하는 방법은 크게 BooleanBuilder를 사용하는 방법과, Where를 사용하는 방법이 있다.

### BooleanBuilder

- BooleanBuilder의 사용흐름은 다음과 같다.
  1. 검색 파라미터가 null인지 검사한다.
  2. null이 아니라면 검색 조건을 BooleanBuilder에 추가한다.
  3. BooleanBuilder를 .where() 체이닝 메서드에 넘긴다.
- 다음은 BooleanBuilder를 사용하는 예시 코드다.

```java
@Repository
public class MemberJpaRepository {
    private final EntityManager em;
    private final JPAQueryFactory queryFactory;

    public MemberJpaRepository(EntityManager em) {
        this.em = em;
        this.queryFactory = new JPAQueryFactory(em);
    }

    public List<MemberTeamDto> searchByBuilder(MemberSearchCondition condition) {
        BooleanBuilder builder = new BooleanBuilder();
        if (hasText(condition.getUsername())) {
            builder.and(member.username.eq(condition.getUsername()));
        }
        if (hasText(condition.getTeamName())) {
            builder.and(team.name.eq(condition.getTeamName()));
        }
        if (condition.getAgeGoe() != null) {
            builder.and(member.age.goe(condition.getAgeGoe()));
        }
        if (condition.getAgeLoe() != null) {
            builder.and(member.age.loe(condition.getAgeLoe()));
        }

        return queryFactory
                .select(new QMemberTeamDto(
                        member.id.as("memberId"),
                        member.username,
                        member.age,
                        team.id.as("teamId"),
                        team.name.as("teamName")))
                .from(member)
                .leftJoin(member.team, team)
                .where(builder)
                .fetch();
    }
}
```

### Where

- Where절은 조건을 검사하는 메서드를 조합해서 사용할 수 있기 때문에 깔끔하고 강력하다.

```java
@Repository
public class MemberJpaRepository {
    private final EntityManager em;
    private final JPAQueryFactory queryFactory;

    public MemberJpaRepository(EntityManager em) {
        this.em = em;
        this.queryFactory = new JPAQueryFactory(em);
    }

    public List<MemberTeamDto> search(MemberSearchCondition condition) {
        return queryFactory
                .select(new QMemberTeamDto(
                        member.id.as("memberId"),
                        member.username,
                        member.age,
                        team.id.as("teamId"),
                        team.name.as("teamName")))
                .from(member)
                .leftJoin(member.team, team)
                .where(
                        usernameEq(condition.getUsername()),
                        teamNameEq(condition.getTeamName()),
                        ageGoe(condition.getAgeGoe()),
                        ageLoe(condition.getAgeLoe())
                )
                .fetch();
    }

    private BooleanExpression usernameEq(String username) {
        return hasText(username) ? member.username.eq(username) : null;
    }

    private BooleanExpression teamNameEq(String teamName) {
        return hasText(teamName) ? team.name.eq(teamName) : null;
    }

    private BooleanExpression ageGoe(Integer ageGoe) {
        return ageGoe != null ? member.age.goe(ageGoe) : null;
    }

    private BooleanExpression ageLoe(Integer ageLoe) {
        return ageLoe != null ? member.age.loe(ageLoe) : null;
    }
}

```

## 사용자 정의 리포지토리

- Spring Data JPA는 인터페이스로 동작한다.
- 하지만 Querydsl은 구현 코드로 동작한다.
- 따라서 Querydsl을 Spring Data JPA와 함께 사용하기 위해서는 사용자 정의 리포지토리를 사용해야 한다.

- 기존 Spring Data Jpa 리포지토리가 존재한다.

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
}
```

- MemberRepository에서 사용할 기능을 사용자 정의 리포지토리 인터페이스에 정의한다.

```java
public interface MemberRepositoryCustom {
  Page<MemberTeamDto> searchPage(MemberSearchCondition condition, Pageable pageable);
}
```

- 사용자 정의 리포지토리 인터페이스를 구현한다.
- 이때 구현체 이름은 [Spring Data Jpa 리포지토리 이름 + Impl]이 되어야 한다.

```java
public class MemberRepositoryImpl implements MemberRepositoryCustom {

    private final JPAQueryFactory queryFactory;

    public MemberRepositoryImpl(EntityManager em) {
        this.queryFactory = new JPAQueryFactory(em);
    }

    @Override
    public Page<MemberTeamDto> searchPage(MemberSearchCondition condition, Pageable pageable) {
        List<MemberTeamDto> content = queryFactory
                .select(new QMemberTeamDto(
                        member.id.as("memberId"),
                        member.username,
                        member.age,
                        team.id.as("teamId"),
                        team.name.as("teamName")))
                .from(member)
                .leftJoin(member.team, team)
                .where(
                        usernameEq(condition.getUsername()),
                        teamNameEq(condition.getTeamName()),
                        ageGoe(condition.getAgeGoe()),
                        ageLoe(condition.getAgeLoe())
                )
                .offset(pageable.getOffset())
                .limit(pageable.getPageSize())
                .fetch();

        JPAQuery<Long> countQuery = queryFactory
                .select(member.count())
                .from(member)
                .leftJoin(member.team, team)
                .where(
                        usernameEq(condition.getUsername()),
                        teamNameEq(condition.getTeamName()),
                        ageGoe(condition.getAgeGoe()),
                        ageLoe(condition.getAgeLoe())
                );
        return PageableExecutionUtils.getPage(content, pageable,
                countQuery::fetchOne);
    }

    private BooleanExpression usernameEq(String username) {
        return hasText(username) ? member.username.eq(username) : null;
    }

    private BooleanExpression teamNameEq(String teamName) {
        return hasText(teamName) ? team.name.eq(teamName) : null;
    }

    private BooleanExpression ageGoe(Integer ageGoe) {
        return ageGoe != null ? member.age.goe(ageGoe) : null;
    }

    private BooleanExpression ageLoe(Integer ageLoe) {
        return ageLoe != null ? member.age.loe(ageLoe) : null;
    }
}
```

- Spring Data Jpa 리포지토리에서 사용자 정의 리포지토리 인터페이스를 상속한다.

```java
public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom {
}
```

- 이제 MemberRepository에서 MemberRepositoryCustom에 정의된 기능을 사용할 수 있다.

```java
@RequiredArgsConstructor
@RestController
public class MemberController {
    private final MemberRepository memberRepository;

    @GetMapping("/api/members")
    public Page<MemberTeamDto> searchMemberV2(MemberSearchCondition condition, Pageable pageable) {
        return memberRepository.searchPageComplex(condition, pageable);
    }
}
```

## 참조

- <a href="https://www.inflearn.com/course/querydsl-%EC%8B%A4%EC%A0%84" target="_blank">실전! Querydsl, 김영한</a>
