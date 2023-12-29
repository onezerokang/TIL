# 6장: AOP

AOP는 IoC/DI, 서비스 추상화와 더불어 스프링의 3대 기반 기술의 하나다. AOP를 바르게 이용하려면 AOP의 등장배경과 스프링이 그것을 도입한 이유, 그 적용을 통해 얻을 수 있는 장점이 무엇인지에 대한 충분한 이해가 필요하다.

스프링에 적용된 가장 인기 있는 AOP의 적용 대상은 선언적 트랜잭션 기능이다. 트랜잭션 경계설정 기능을 AOP를 이용해 더욱 깔끔한 방식으로 바꿔보자.

## 트랜잭션 코드의 분리

서비스 추상화로 UserService가 트랜잭션 기술, 메일 발송 기술에 종속적이지 않고 깔끔한 코드가 되었다.

스프링이 제공하는 깔끔한 트랜잭션 인터페이스를 썼음에도 비즈니스 로직이 주인이어야 할 메소드에 트랜잭션 코드가 더 많은 자리를 차지하고 있는 것은 단일 책임에 위배된다.

### 메소드 분리

UserService를 더 깔끔한 코드로 만들기 위해, 트랜잭션이 적용된 코드를 다시 한번 살펴보자.

```java
public void upgradeLevels() {
    // 트랜잭션 경계 설정 - 시작
    TransactionStatus status = this.transactionManager.getTransaction(new DefaultTransactionDefinition());
    // 트랜잭션 경계 설정 - 시작

    try {
        // 비즈니스 로직
        List<User> users = userDao.getAll();
        for (User user : users) {
            if (canUpgradeLevel(user)) {
                upgradeLevel(user);
            }
        }
        // 비즈니스 로직

        // 트랜잭션 경계 설정 - 끝
        this.transactionManager.commit(status);
    } catch (RuntimeException e) {
        this.transactionManager.rollback(status);
        throw e;
    }
    // 트랜잭션 경계 설정 - 끝
}
```

위 코드를 살펴보면 트랜잭션 경계 설정 코드와, 비즈니스 로직 코드가 완벽하게 독립적인 코드임을 알 수 있다. 그 이유는 다음과 같다.

1. 코드가 섞이지 않고 경계가 명확하다.
2. 서로 주고 받는 정보가 없다.

그렇다면 성격이 다른 코드를 두 개의 메소드로 분리할 수 있을 것 같다.

```java
public void upgradeLevels() {
    TransactionStatus status = this.transactionManager
        .getTransaction(new DefaultTransactionDefinition());

    try {
        upgradeLevelsInternal();
        this.transactionManager.commit(status);
    } catch (RuntimeException e) {
        this.transactionManager.rollback(status);
        throw e;
    }
}

private void upgradeLevelsInternal() {
    List<User> users = userDao.getAll();
    for (User user : users) {
        if (canUpgradeLevel(user)) {
            upgradeLevel(user);
        }
    }
}
```

성격이 다른 로직이 분리되니 이해하기도 편하고, 수정하기에도 부담이 없다.

### DI를 이용한 클래스의 분리

비즈니스 로직을 담당하는 코드를 깔끔하게 분리했지만, 여전히 트랜잭션을 담당하는 코드가 UserService 안에 자리 잡고 있다.

어차피 서로 직접적으로 주고 받는 정보가 없다면 간단하게 트랜잭션 코드를 클래스 밖으로 뽑아낼 수 있다.

#### DI 적용을 이용한 트랜잭션 분리

현재 구조는 클라이언트 오브젝트가 UserService를 직접 참조하기 때문에 클라이언트와 UserService가 강한 결합도로 고정되어 있다. 이 사이를 비집고 트랜잭션 경계설정 같은 다른 무언가를 추가하기는 힘들다.

그래서 UserService를 인터페이스로 만들고 기존 코드는 UserService 인터페이스의 구현 클래스를 만들어넣도록 한다. 그러면 클라이언트와 결합이 약해지고, 유연한 확장이 가능해진다.

트랜잭션 기능을 UserService에서 분리시킬 것이기 때문에 UserService를 구현한 클래스를 2개 만들자.

- UserServiceImpl: 기존 비즈니스 로직이 담긴 UserService 구현 클래스
- UserServiceTx: 트랜잭션 경계 설정를 위한 UserService 구현 클래스

#### UserService 인터페이스 도입

먼저 기존 UserService를 UserServiceImpl로 이름을 변경하고 UserService 인터페이스를 생성하자.

```java
public interface UserService {
    void add(User user);
    void upgradeLevels();
}
```

그리고 UserServiceImpl에서 트랜잭션과 관련된 코드를 제거하고, 비즈니스 로직만 남기자.

```java
public UserServiceImpl implements UserService {
    // ...생략
    public void upgradeLevels() {
        List<User> users = userDao.getAll();
        for (User user : users) {
            if (canUpgradeLevel(user)) {
                upgradeLevel(user);
            }
        }
    }
    // ...생략
}
```

이제 UserServiceImpl은 UserDao라는 인터페이스를 이용하고, User라는 도메인 정보를 가진 비즈니스 로직에만 충실한 깔끔한 코드가 됐다.

#### 분리된 트랜잭션 기능

이제 분리된 트랜잭션 처리를 담은 UserServiceTx를 만들자. UserServiceTx는 UserService를 구현한 후 UserServiceImpl에 작업을 위임하면 된다.

```java
public class UserServiceTx implements UserService {
    UserService userService;

    public void setUserService(UserService userService) {
        this.userService = userService;
    }

    @Override
    public void add(User user) {
        userService.add(user);
    }

    @Override
    public void upgradeLevels() {
        userService.upgradeLevels();
    }
}
```

UserServiceTx는 사용자 관리 비즈니스 로직을 전혀 갖지 않고 다른 UserService 구현 오브젝트에 기능을 위임한다.

이제 UserServiceTx에 트랜잭션 경계설정이라는 부가적인 작업을 부여해보자.

```java
public class UserServiceTx implements UserService {
    UserService userService;
    PlatformTransactionManager transactionManager;

    public void setTransactionManager(PlatformTransactionManager transactionManager) {
        this.transactionManager = transactionManager;
    }

    public void setUserService(UserService userService) {
        this.userService = userService;
    }

    @Override
    public void add(User user) {
        userService.add(user);
    }

    @Override
    public void upgradeLevels() {
        TransactionStatus status = this
                .transactionManager.getTransaction(new DefaultTransactionDefinition());

        try {
            userService.upgradeLevels();
            this.transactionManager.commit(status);
        } catch (RuntimeException e) {
            this.transactionManager.rollback(status);
            throw e;
        }
    }
}
```

#### 트랜잭션 적용을 위한 DI 설정

이제 남은 것은 설정 파일을 수정하는 부분이다.

스프링 DI 설정에 의해 다음과 같은 의존관계가 만들어져야 한다.

- Client(UserServiceTest) -> UserServiceTx -> UserServiceImpl

다음은 수정한 스프링 설정파일의 내용이다.

```xml
<bean id="userService" class="kang.onezero.tobyspring.user.service.UserServiceTx">
    <property name="userService" ref="userServiceImpl" />
    <property name="transactionManager" ref="transactionManager" />
</bean>
<bean id="userServiceImpl" class="kang.onezero.tobyspring.user.service.UserServiceImpl">
    <property name="userDao" ref="userDao" />
    <property name="mailSender" ref="mailSender" />
</bean>
```

#### 트랜잭션 분리에 따른 테스트 수정

분리된 코드에 대해 테스트를 돌리기 전에 손봐야 할 곳이 제법 있다. 전에는 UserService 클래스를 직접 사용하고, 각종 의존 오브젝트를 테스트용 DI 기법을 이용해서 사용했다. 이제 기존의 UserService 클래스가 인터페이스와 두 개의 클래스로 분리된 만큼 테스트에서도 적합한 타입과 빈을 사용하도록 변경해야 한다.

변경해야 하는 곳은 다음과 같다.

- **@Autowired UserService userService**: @Autowired는 타입으로 빈을 먼저 찾는다. 같은 타입의 빈이 두 개 이상이라면 빈 id로 조회를 진행한다.
- **@Autowired UserServiceImpl userServiceImpl**: MailSender 목 오브젝트를 이용한 테스트에서는 테스트에서 직접 MailSender를 DI 해줘야 했다. MailSender는 DI 해줄 대상을 구체적으로 알고 있어야 하기 떄문에 UserServiceImpl 클래스의 오브젝트를 가져와야 한다.
- **upgradeLevels()**: userService가 아닌 userServiceImpl에 mockMail을 주입해주자.
  ```java
  @Test
  public void upgradeLevels() throws Exception {
    MockMailSender mockMailSender = new MockMailSender();
    // UserService의 구현체인 UserServiceTx는 setMailSender() 메소드가 없다.
    userServiceImpl.setMailSender(mockMailSender);
  }
  ```
- **upgradeAllOrNoting()**: 이 테스트는 사용자 관리 로직이 아닌, 트랜잭션 기술이 바르게 적용됐는지를 확인하기 위해 만든 학습 테스트다. 직접 테스트용 확장 클래스도 만들고 수동 DI도 적용 한 만큼, 바뀐 구조를 모두 반영해줘야 한다.

  - 트랜잭션 테스트용으로 특별히 정의한 TestUserService 클래스는 UserSereviceImpl 클래스를 상속하도록 바꿔준다.

  ```java
  static class TestUserService extends UserServiceImpl
  ```

  - TestUserService 오브젝트를 UserServiceTx 오브젝트에 수동 DI 시킨후에 트랜잭션 기능까지 포함된 UserServiceTx의 메소드를 호출하면서 테스트를 수행하도록 한다.

  ```java
  @Test
  public void upgradeAllOrNoting() throws Exception {
      TestUserService testUserService = new TestUserService(users.get(3).getId());
      testUserService.setUserDao(this.userDao);
      testUserService.setMailSender(mailSender);

      UserServiceTx txUserService = new UserServiceTx();
      txUserService.setTransactionManager(transactionManager);
      txUserService.setUserService(testUserService);

      userDao.deleteAll();
      for(User user: users) userDao.add(user);

      try {
          txUserService.upgradeLevels();
          fail("TestUserServiceException expected");
      } catch (TestUserServiceException e) {
          // TestService가 던지는 예외를 잡아서 계속 진행되도록 한다.
      }
      checkLevelUpgraded(users.get(1), false); // 예외가 발생하기 전에 레벨 변경이 있어ㄸ썬 사용자 레벨이 처음 상태로 바뀌었나 확인
  }
  ```

테스트가 성공하는지 확인하자.

#### 트랜잭션 경계설정 코드 분리의 장점

트랜잭션 경계설정 코드의 분리와 DI를 통한 연결은 지금까지 해왔던 작업 중에서 가장 복잡했다. 이런 수고를 한 결과로 얻을 수 있는 장점은 다음과 같다.

1. 비즈니스 로직을 담당하는 UserServiceImpl의 코드를 작성 시 트랜잭션과 같은 기술적인 내용에 전혀 신경쓰지 않아도 된다.
2. 비즈니스 로직에 대한 테스트를 손쉽게 만들어낼 수 있다(다음 절에서 추가 설명).
