# [Spring Boot] 실행 환경별로 application.yml 분리하고 적용하기

## 학습 계기

기존 프로젝트에 통합 테스트를 작성하게되면서, 개발 DB와 테스트용 DB를 분리할 필요가 생겼다.

이를 위해 실행 환경별로 application.yml 설정 파일을 분리하고, 각 환경에 맞는 설정 파일을 적용하는 방법을 정리하게 되었다.

## application.yml이란

application.yml은 스프링 부트의 설정 파일로 DB 연결 정보, 로그 설정 정보 등을 입력하는 설정 파일이다.

예를들어 다음은 DB 연결 정보를 작성해둔 application.yml이다.

```yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/db
    username: admin
    password: 1234
    driver-class-name: com.mysql.cj.jdbc.Driver
```

스프링 애플리케이션의 실행 환경에 따라 다른 설정 값들이 요구될 수 있다. 예를 들어, 개발 환경에서는 로컬 DB, 테스트 환경에서는 인메모리 DB, 프로덕션 환경에서는 AWS RDS에 연결하고 싶을 수 있다.

이럴 경우 각 환경에 맞는 설정 파일을 정의해두고, 해당 환경에서 요구되는 설정 파일을 이용하도록 해야 한다.

### 환경 별 설정 파일 만들기

개발 환경, 테스트 환경, 배포 환경에서 각각 다른 설정 파일이 필요한다고 가정하면 다음과 같이 설정 파일을 만들 수 있다.

- application-dev.yml
- application-test.yml
- application-prod.yml

위 처럼 application-[name].yml 형식으로 설정 파일을 만들면, 해당 파일은[name] profile에서 사용된다.

### 하나의 설정 파일에서 프로필 구분하기

하나의 application.yml 파일에서 여러 프로필별 설정 정보를 작성할 수도 있다.

각 환경은 `---`로 구분해줘야 한다.

```yml
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: # 생략
---
spring:
  config:
    activate:
      on-profile: test
  datasource:
    url: # 생략
---
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: # 생략
```

- spring.config.activate.on-profile: 해당 프로필일 때 적용될 설정의 영역
- spring.profiles.active: 프로필 지정(기본값은 default)

## 프로필 설정하기

환경 별 사용할 설정 파일을 만들었다면 스프링 애플리케이션이 실행될 때 사용할 어떤 환경(프로필)을 사용할지 설정해줘야 한다.

### IntelliJ IDEA에서 프로필 설정하기

현재 필자는 IntelliJ Community Edition을 사용중이기에 CE 기준으로 작성하겠다.

1. IDEA 상단의 Edit Configurations 버튼 클릭
2. Modify options > Add VM options
3. -Dspring.profiles.active=<원하는프로필>

이제 스프링 애플리케이션을 IDEA에서 실행하게 되면, 해당 프로필로 실행될 것이다.

### jar 파일 실행 시 profile 지정 방법

jar 파일을 실행할 때 -Dspring.profiles.active=[프로파일명]을 넣어주면 해당 profile이 적용된다.

```bash
java -Dspring.profiles.active=[프로파일명] -jar example-project-0.0.1-SNAPSHOT.jar
```

### @Profile, @ActiveProfiles 어노테이션

@Profile과 @ActiveProfiles 어노테이션으로 프로필을 지정해줄 수 있다.

@Profile은 스프링 애플리케이션이 실행될 때 사용하고 @ActiveProfiles는 테스트를 할 때 사용된다.

```java
@ActiveProfiles("test")
@SpringBootTest
class MemberServiceTest {
    // ... 생략
}
```

## 마무리

오늘은 이렇게 스프링 애플리케이션 실행 환경별로 설정 정보를 분리하고, 애플리케이션의 프로필을 지정하는 방법을 알아봤다.
