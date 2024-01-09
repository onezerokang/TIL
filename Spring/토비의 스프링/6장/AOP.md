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

## 고립된 단위 테스트

테스트는 작은 단위로 하면 좋은 데, 단위가 작을수록 테스트가 실패했을 때 원인을 찾기 쉽기 때문이다. 하지만 테스트 대상이 다른 오브젝트와 환경에 의존하고 있다면 작은 단위로 테스트하기 힘들다.

### 복잡한 의존관계 속의 테스트

현재 UserService의 구현 클래스가 동작하려면 세 가지 타입의 의존 오브젝트가 필요하다.

1. UserDao 타입의 오브젝트
2. MailSender를 구현한 오브젝트
3. 트랜잭션 처리를 위한 PlatformTransactionManager

현재 UserServiceTest는 UserService만 테스트하는 것처럼 보이지만 UserService가 의존하고 있는 오브젝트들도 테스트가 진행 되는 동안 같이 실행된다. 더 큰 문제는 그 세 가지 의존 오브젝트들도 자신의 코드만 실행되고 마는 게 아니다.

복잡한 의존관계 속의 테스트가 갖는 문제점은 다음과 같다.

1. 테스트 수행 속도가 느리다.
2. 환경이 달라지면 동일한 테스트 결과를 내지 못할 수 있다.
3. 의존 오브젝트에 문제가 있어도 UserService의 테스트가 실패하여 문제를 찾기 힘들다.

### 테스트 대상 오브젝트 고립시키기

테스트 대상이 환경이나 외부 서버, 다른 클래스의 코드에 종속되고 영향을 받지 않도록 고립시킬 필요가 있다. 이때 테스트 대역인 테스트 스텅빙나 목 오브젝트를 사용하할 수 있다.

#### 테스트를 위한 UserServiceImpl

UserService를 구현한 UserServiceImpl에서 트랜잭션 코드를 독립시켰기 때문에, 해당 클래스로 테스트를 진행하면 PlatformTransactionManager에 의존하지 않는 테스트를 작성할 수 있다.

또한 MockUserDao와 MockMailSender를 만들어서 UserServiceImpl을 고립시키고, UserServiceImpl 사이에서 주고 받은 정보를 저장해뒀다가, 테스트 검증에 사용할 수 있도록 하자.

#### 고립된 단위 테스트 활용

다음은 기존 UserServiceTest의 upgradeLevels() 테스트 코드다.

```java
@Test
@DirtiesContext // 컨텍스트의 DI 설정을 변경하는 테스트라는 것을 알려준다.
public void upgradeLevels() throws Exception {
    // DB 테스트 데이터 준비
    userDao.deleteAll();
    for (User user: users) userDao.add(user);

    // 메일 발송 여부 확인을 위해 목 오브젝트 DI
    MockMailSender mockMailSender = new MockMailSender();
    userServiceImpl.setMailSender(mockMailSender);

    // 테스트 대상 실행
    userService.upgradeLevels();

    // DB에 저장된 결과 확인
    checkLevelUpgraded(users.get(0), false);
    checkLevelUpgraded(users.get(1), true);
    checkLevelUpgraded(users.get(2), false);
    checkLevelUpgraded(users.get(3), true);
    checkLevelUpgraded(users.get(4), false);

    // 목 오브젝트를 이용한 결과 확인
    List<String> requests = mockMailSender.getRequests();
    assertThat(requests).hasSize(2);
    assertThat(requests.get(0)).isEqualTo(users.get(1).getEmail());
    assertThat(requests.get(1)).isEqualTo(users.get(3).getEmail());
}

private void checkLevelUpgraded(User user, boolean upgraded) {
    User userUpdate = userDao.get(user.getId());
    // ... 생략
}
```

#### UserDao 목 오브젝트

이제 실제 UserDao와 DB까지 의존하고 있는 부분도 목 오브젝트를 만들어서 적용해보자. 목 오브젝트는 기본적으로 스텁과 같은 방식으로 테스트 대상을 통해 사용될 때 필요한 기능을 지원해줘야 한다.

UserServiceImpl.upgradeLevels() 메소드를 호출할 때 userDao.getAll()과 userDao.update(user) 메소드를 호출하고 있다.

```java
public void upgradeLevels() {
    List<User> users = userDao.getAll();
    for (User user : users) {
        if (canUpgradeLevel(user)) {
            upgradeLevel(user);
        }
    }
}

protected void upgradeLevel(User user) {
    user.upgradeLevel();
    userDao.update(user);
    sendUpgradeEmail(user);
}
```

- getAll(): DB에서 읽어온 것처럼 미리 준비된 사용자 목록을 제공해줘야 한다. 스텁으로 만든다.
- updateUser(user): 리턴 값은 없지만 '레벨 변경'을 검증할 수 있는 기능이다. 목 오브젝트로 만든다.

MockUserDao의 코드는 다음과 같이 만들 수 있다.

```java
static class MockUserDao implements UserDao {
    private List<User> users; // 레벨 업그레이드 후보 User 오브젝트 목록
    private List<User> updated = new ArrayList<>(); // 업그레드 대상 오브젝트를 지정해둘 목록

    private MockUserDao(List<User> users) { this.users = users; }

    public List<User> getUpdated() {
        return this.updated;
    }

    // 스텁 기능 제공
    public List<User> getAll() { return this.users; }

    // 목 오브젝트 기능 제공
    public void update(User user) { updated.add(user); }

    // 테스트에 사용되지 않는 메소드
    public void add(User user) { throw new UnsupportedOperationException(); }
    public User get(String id) { throw new UnsupportedOperationException(); }
    public void deleteAll() { throw new UnsupportedOperationException(); }
    public int getCount() { throw new UnsupportedOperationException(); }
}
```

이제 upgradeLevels() 테스트가 MockUserDao를 사용하도록 수정해보자.

```java
@Test
public void upgradeLevels() throws Exception {
    // 고립된 테스트에서는 테스트 대상 오브젝트를 직접 생성하면 된다.
    UserServiceImpl userServiceImpl = new UserServiceImpl();

    // 목 오브젝트로 만든 UserDao를 직접 DI 해준다.
    MockUserDao mockUserDao = new MockUserDao(this.users);
    userServiceImpl.setUserDao(mockUserDao);

    MockMailSender mockMailSender = new MockMailSender();
    userServiceImpl.setMailSender(mockMailSender);

    userServiceImpl.upgradeLevels();

    // MockUserDao로부터 업데이트 결과를 가져오고 검증한다.
    List<User> updated = mockUserDao.getUpdated();
    assertThat(updated).hasSize(2);
    checkUserAndLevel(updated.get(0), "j_oner", Level.SILVER);
    checkUserAndLevel(updated.get(1), "m_gumayusi", Level.GOLD);

    List<String> requests = mockMailSender.getRequests();
    assertThat(requests).hasSize(2);
    assertThat(requests.get(0)).isEqualTo(users.get(1).getEmail());
    assertThat(requests.get(1)).isEqualTo(users.get(3).getEmail());
}
```

이전에는 UserService 오브젝트가 많은 의존 오브젝트와 서비스, 외부 환경에 의존하고 있었기에 스프링 컨테이너에서 @Autowired를 통해 가져왔었다. 이제는 완전히 고립돼서 테스트만을 위해 독립적으로 동작하는 테스트 대상을 사용할 것이기 때문에 스프링 컨테이너에서 빈을 가져올 필요가 없다.

#### 테스트 수행 성능의 향상

워낙 간단한 테스트인지라 전체 진행 시간의 차이를 못 느끼겠지만, upgradeLEvels()의 테스트 수행 시간은 이전보다 훨씬 빨라졌다.

UserServiceTest를 실행했을 때 DB에 의존하고 있는 add()와 upgradeAllNoting() 테스트는 각각 100ms ~ 700ms로 측정됐지만, 고립된 upgradeLevels()는 4ms만에 완료 됐다.

고립된 테스트를 하면 테스트가 다른 의존 대상에 영향을 받을 경우를 대비해 복잡하게 준비할 필요가 없을 뿐만 아니라, 테스트 수행 성능도 크게 향상된다. 테스트가 빨리 돌아가면 부담 없이 자주 테스트를 돌려볼 수 있다.

### 단위 테스트와 통합 테스트

- **단위 테스트**: 테스트 대상 클래스를 테스트 대역을 이용해 의존 오브젝트나 외부의 리소스를 사용하지 못하도록 고립시켜서 테스트 하는 것
- **통합 테스트**: 두 개 이상의 성격이나 계층이 다른 오브젝트가 연동하도록 만들어 테스트하거나, 외부의 DB나 파일 서비스 등의 리소스가 참여하는 테스트

다음은 단위 테스트와 통합 테스트 중에서 어떤 방법을 쓸지 결정하는 몇 가지 가이드라인이다.

- 항상 단위 테스트를 먼저 고려한다.
- 외부의 리소스를 사용해야만 가능한 테스트는 통합 테스트로 만든다.
- DAO 같이 로직을 담기보다는 DB를 통해 로직을 수행하는 인. SQL을 JDBC를 통해 실행하는 코드만으로는 고립된 테스트 어려움. DB를 사용하는 테스트는 DB에 테스트 데이터를 준비하고, DB에 직접 확인을 하는 부가 작업 필요
- 단위 테스트를 만들기 너무 복잡하다고 판단되는 코드는 처음부터 통합 테스트를 고려해본다.
- 스프링 테스트 컨텍스트 프레임워크를 이용하는 테스트는 통합 테스트다. 가능하면 스프링의 지원 없이 코드 레벨의 DI를 사용하면서 단위 테스트를 하는 게 좋겠지만, 스프링의 설정 자체도 테스트 대상이고, 스프링을 이용해 좀 더 추상적인 레벨에서 테스트해야 할 경우도 종종 있다. 이럴 땐 스프링 테스트 컨텍스프 프레임워크를 이용해 테스트

테스트는 코드가 작성되고 빠르게 진행되는 편이 좋다.

코드를 작성하면서 테스트를 어떻게 만들 수 있을지 고민 좋다. 테스트하기 편한 코드는 깔끔하고 좋은 코드.

### 목 프레임워크

단위 테스트를 만들기 위해서는 목 오브젝트와 스텁의 사용이 필수적이다.

다행히도, 번거로운 목 오브젝트를 편리하게 작성하도록 도와주는 다양한 목 오브젝트 지원 프레임워크가 있다.

#### Mockito 프레임워크

Mockito는 목 오브젝트 프레임워크로 간단한 메소드 호출만으로 다이내믹하게 특정 인터페이스를 구현한 테스트용 목 오브젝트를 만들 수 있다.

UserDao 인터페이스를 구현한 목 오브젝트는 다음과 같이 Mockito의 스태틱 메소드를 한 번 호출해주면 만들어진다.

```java
UserDao mockUserDao = mock(UserDao.class);
```

이렇게 만들어진 목 오브젝트는 아직 아무런 기능이 없다. 여기에 getAll() 메소드가 호출될 때 사용자 목록을 리턴하도록 스텁 기능을 추가해줘야 한다.

```java
when(mockUserDao.getAll()).thenReturn(this.users);
```

다음은 update() 호출이 있었는지를 검증하는 부분이다. Mockito를 통해 만들어진 목 오브젝트는 메소드 호출과 관련된 모든 내용을 자동으로 저장해두고, 이를 간단한 메소드로 검증할 수 있게 해준다.

테스트를 진행하는 동안 mockUserDao의 update() 메소드가 두 번 호출됐는지 확인하고 싶다면, 다음과 같이 검증 코드를 넣어주면 된다.

```java
verify(mockUserDao, times(2)).update(any(User.class));
```

Mockit 목 오브젝트는 다음의 네 단계를 거쳐서 사용하면 된다. 두 번째와 네 번째는 각각 필요한 경우에만 사용할 수 있다.

1. 인터페이스를 이용해 목 오브젝트를 만든다.
2. 목 오브젝트가 리턴할 값이 있다면 지정한다. 메소드 호출 시 강제로 예외를 던지게 만들 수도 있다.
3. 테스트 대상 오브젝트에 DI 해서 목 오브젝트가 테스트 중에 사용되도록 만든다.
4. 테스트 대상 오브젝트를 사용한 후에 목 오브젝트의 특정 메소드가 호출됐는지, 어떤 값을 가지고 몇 번 호출됐는지를 검증한다.

다음은 Mockito를 적용해 만든 테스트 코드다.

```java
@Test
public void mockUpgradeLevels() {
    UserServiceImpl userServiceImpl = new UserServiceImpl();

    UserDao mockUserDao = mock(UserDao.class);
    when(mockUserDao.getAll()).thenReturn(this.users);
    userServiceImpl.setUserDao(mockUserDao);

    MailSender mockMailSender = mock(MailSender.class);
    userServiceImpl.setMailSender(mockMailSender);

    userServiceImpl.upgradeLevels();

    // mockUserDao가 몇번 호출됐는지, 어떤 매개변수를 가지고 호출됐는지 검증
    verify(mockUserDao, times(2)).update(any(User.class));
    verify(mockUserDao, times(2)).update(any(User.class));
    verify(mockUserDao).update(users.get(1));
    assertThat(users.get(1).getLevel()).isEqualTo(Level.SILVER);
    verify(mockUserDao).update(users.get(3));
    assertThat(users.get(3).getLevel()).isEqualTo(Level.GOLD);

    // ArgumentCaptor를 사용해 실제 MailSender 목 오브젝트에 전달된 파라미터를 가져와 내용을 검증
    // 파라미터를 직접 비교하기보다는 파라미터의 내부 정보를 확인해야 할 때 유용하다.
    ArgumentCaptor<SimpleMailMessage> mailMessageArg =
            ArgumentCaptor.forClass(SimpleMailMessage.class);
    verify(mockMailSender, times(2)).send(mailMessageArg.capture());
    List<SimpleMailMessage> mailMessages = mailMessageArg.getAllValues();
    assertThat(mailMessages.get(0).getTo()[0]).isEqualTo(users.get(1).getEmail());
    assertThat(mailMessages.get(1).getTo()[0]).isEqualTo(users.get(3).getEmail());
}
```

## 다이내믹 프록시와 팩토리 빈

### 프록시와 프록시 패턴, 데코레이터 패턴

트랜잭션 경계설정 코드를 비즈니스 로직 코드에서 분리해낼 때 적용했던 기법을 다시 검토해보자.

- 서비스에 트랜잭션과 핵심 로직이라는 성격이 다른 두 개의 책임이 있어 각각 UserServiceTx와 UserServiceImpl로 분리했다.
- UserServiceTx를 사용해야 할 서비스가 UserServiceImpl을 직접 사용할 경우, 부가기능이 적용될 기회가 없는 문제가 있었다.
- 이를 해결하려면 부가기능은 핵심기능 클래스가 구현한 인터페이스를 구현하여 핵심 기능을 가진 클래스인 것처럼 사용하게 했다.
- 그러기 위해서는 클라이언트는 인터페이스를 통해 핵심 기능을 제공받기 때문에 UserServiceTx를 통해 UserServiceImpl을 사용하게 되었다.

이렇게 마치 자신이 클라이언트가 사용하려고 하는 실제 대상인 것처럼 위장해서 클라이언트의 요청을 받아주는 것을 **프록시(proxy)**, 그리고 프록시를 통해 최종적으로 요청을 위임받아 처리하는 실제 오브젝트를 타깃(target) 또는 실체(real subject)라고 부른다.

**프록시의 특징은 타깃과 같은 인터페이스를 구현했다는 것과 프록시가 타깃을 제어할 수 있는 위치에 있다는 것이다.**

프록시는 사용 목적에 따라 두 가지로 구분할 수 있다.

1. 클라이언트가 타깃에 접근하는 방법을 제어하기 위함
2. 타깃에 부가적인 기능을 부여해주기 위함

두 가지 모두 대리 오브젝트라는 개념의 프록시를 두고 사용한다는 점은 동일하지만, 목적에 따라서 디자인 패턴에서는 다른 패턴으로 구분한다.

### 데코레이터 패턴

데코레이터 패턴은 타깃에 부가적인 기능을 런타임에 다이내믹하게 부여하기 위해 프록시를 사용하는 패턴을 말한다. 다이내믹하게 기능을 부가한다는 의미는 컴파일 시점, 즉 코드상에서 어떤 방법과 순서로 프록시와 타깃이 연결되어 사용되는지 정해져 있지 않다는 뜻이다.

UserService 인터페이스를 구현한 UserServiceImpl에 트랜잭션 부가 기능을 제공해주는 UserServiceTx를 추가한 것도 데코레이터 패턴을 적용한 것이라고 불 수 있다.

인터페이스를 통한 데코레이터 정의와 다이내믹한 구성 방법은 스프링의 DI 방법을 이용하면 아주 편리하다. 데코레이터 빈의 프로퍼티로 같은 인터페이스를 구현한 다른 데코레이터 또는 타깃 빈을 설정하면 된다.

데코레이터 패턴은 인터페이스를 통해 위임하는 방식이기 때문에 어느 데코레이터에서 타깃으로 연결될지 코드레벨에서는 미리 알 수 없다. 구성하기에 따라서 여러 데코레이터를 적용할 수도 있다.

데코레이터 패턴은 타깃의 코드를 손대지 않고, 클라이언트가 호출하는 방법도 변경하지 않은 채로 새로운 기능을 추가할 때 유용한 방법이다.

### 프록시 패턴

프록시라는 용어와 프록시 패턴은 구분할 필요가 있다.

- **프록시**: 클라이언트와 타깃 사이에 대리 역할을 맡은 오브젝트를 두는 방법을 총칭
- **프록시 패턴**: 프록시를 사용하는 방법 중에 타깃에 대한 접근 방법을 제어하려는 목적을 가진 경우

프록시 패턴은 타깃의 기능을 확장하거나 추가하지 않는다. 대신 클라이언트가 타깃에 접근하는 방식을 변경해준다.

- 예시 1:
  - 타깃 오브젝트 생성이 복잡하거나 당장 필요하지 않은 경우, 필요한 시점까지 생성하지 않는 것이 좋다.
  - 그런데 타깃 오브젝트에 대한 레퍼런스가 미리 필요할 때 프록시 패턴을 샤용한다.
  - 프록시 메소드를 통해 메소드에 접근하려고 하면 그때 타깃 오브젝트를 생성하고 요청을 위임하는 것이다.
- 예시 2:
  - 특별한 상황에서 타깃에 대한 접근권한을 제어하기 위해 프록시 패턴을 사용
  - 수정 가능한 오브젝트가 존재할 때, 특정 레이어로 넘어가서는 읽기전용으로만 동작하게 강제할 때 프록시를 사용

프록시는 데코레이터와 유사하지만, 프록시는 코드에서 자신이 만들거나 접근할 타깃 클래스 정보를 알고 있는 경우가 많다. 생성을 지연하는 프록시라면 구체적인 생성 방법을 알아야 하기 때문에 타깃 클래스에 대한 직접적인 정보를 알아야 한다.

프록시 패턴은 아킷의 기능 자체에는 관여하지 않으면서 접근하는 방법을 제어해주는 프록시를 이용하는 것이다.

## 다이내믹 프록시

프록시는 기존 코드에 영향을 주지 않으면서 타깃의 기능을 확장하거나 접근 방법을 제어할 수 있는 유용한 방법이다. 하지만 프록시를 만드는 것은 번거롭다. 매번 새로운 클래스를 정의하고, 인터페이스의 구현을 일일히 구현해서 위임하는 코드를 넣어야 하기 때문이다.

자바에는 java.lang.reflect 패키지 안에 프록시를 손쉽게 만들 수 있도록 지원해주는 클래스가 있다. 기본적인 아이디어는 목 프레임워크와 비슷하다. 일일이 프록시 클래스를 정의하지 않고도 몇 가지 API를 이용해 프록시처럼 동작하는 오브젝트를 다이내믹하게 생성하는 것이다.

#### 프록시의 구성과 프록시 작성의 문제점

프록시의 역할은 위임과 부가작업으로 구분할 수 있다.

프록시를 만들기가 번거로운 이유는 다음과 같다.

1. 인터페이스를 구현하고 위임하는 코드를 작성하기 번거롭다.
2. 부가기능 코드가 중복될 가능성이 많다. 예를 들어 트랜잭션은 DB를 사용하는 대부분 로직에 적용될 필요가 있는 데, 트랜잭션 경계를 설정하는 코드가 프록시 메소드에 중복될 것이다.

#### 리플렉션

다이내믹 프록시는 리플랙션 기능을 이용해서 프록시를 만들어준다. 리플랙션은 자바의 코드 자체를 추상화해서 접근하도록 만든 것이다.

자바의 모든 클래스는 그 클래스 자체의 구상정보를 담은 Class 타입의 오브젝트를 하나씩 갖고 있다. `클래스이름.class`라고 하거나 오브젝트의 getClass() 메소드를 호출하면 클래스 정보를 담은 Class 타입의 오브젝트를 가져올 수 있다. 클래스 오브젝트를 이용하면 클래스 코드에 대한 메타정보를 가져오거나, 오브젝트를 조작할 수 있다.

리플렉션 API 중에 메소드에 대한 정의를 담은 Method라는 인터페이스를 이용해 메소드를 호출하는 방법을 살펴보자.

```java
Method lengthMehtod = String.class.getMethod("length");
```

스트링이 가진 메소드 중에서 "length" 이름을 갖고, 파라미터는 없는 메소드의 정보를 가져온 것이다. 이를 이용해 특정 오브젝트의 메소드를 실행할 수도 있다. Method 인터페이스에 정의된 invoke() 메소드를 사용하면 된다.

```java
Stirng name = "Spring";
int length = lengthMethod.invoke(name);
```

학습 테스트를 만들어 Method를 이용해 메소드를 호출하는 방법을 익혀보자.

```java
public class ReflectionTest {
    @Test
    public void invokeMethod() throws Exception {
        String name = "Spring";

        // length()
        assertThat(name.length()).isEqualTo(6);

        Method lengthMethod = String.class.getMethod("length");
        assertThat((Integer) lengthMethod.invoke(name)).isEqualTo(6);


        // charAt()
        assertThat(name.charAt(0)).isEqualTo('S');

        Method charAtMethod = String.class.getMethod("charAt", int.class);
        assertThat((Character) charAtMethod.invoke(name, 0)).isEqualTo('S');
    }
}
```

#### 프록시 클래스

다이내믹 프록시르르 이용한 프록시를 만들어보자. 프록시를 적용할 간단한 타깃 클래스와 인터페이스를 정의한다.

구현할 인터페이스는 다음과 같다.

```java
public interface Hello {
    String sayHello(String name);
    String sayHi(String name);
    String sayThankYou(String name);
}
```

이를 구현한 타깃 클래스는 다음과 같다.

```java
public class HelloTarget implements Hello {
    @Override
    public String sayHello(String name) {
        return "Hello " + name;
    }

    @Override
    public String sayHi(String name) {
        return "Hi " + name;
    }

    @Override
    public String sayThankYou(String name) {
        return "Thank You " + name;
    }
}
```

이제 Hello 인터페이스를 통해 HelloTarget 오브젝트를 사용하는 클라이언트 역할을 하는 테스트를 만들자.

```java
@Test
public void simpleProxy() {
    Hello hello = new HelloTarget(); // 타깃은 인터페이스를 통해 접근하는 습관을 들이자.
    assertThat(hello.sayHello("Toby")).isEqualTo("Hello Toby");
    assertThat(hello.sayHi("Toby")).isEqualTo("Hi Toby");
    assertThat(hello.sayThankYou("Toby")).isEqualTo("Thank You Toby");
}
```

이제 Hello 인터페이스를 구현한 프록시를 만들어보자. 추가할 기능은 리턴하는 문자를 모두 대문자로 바꿔주는 것이다.

```java
public class HelloUppercase implements Hello {
    Hello hello;

    public HelloUppercase(Hello hello) {
        this.hello = hello;
    }

    @Override
    public String sayHello(String name) {
        return hello.sayHello(name).toUpperCase();
    }

    @Override
    public String sayHi(String name) {
        return hello.sayHi(name).toUpperCase();
    }

    @Override
    public String sayThankYou(String name) {
        return hello.sayThankYou(name).toUpperCase();
    }
}
```

다음과 같이 테스트 코드를 추가해 프록시가 동작하는지 확인하자.

```java
Hello proxiedHello = new HelloUppercase(hello);
assertThat(proxiedHello.sayHello("Toby")).isEqualTo("HELLO TOBY");
assertThat(proxiedHello.sayHi("Toby")).isEqualTo("HI TOBY");
assertThat(proxiedHello.sayThankYou("Toby")).isEqualTo("THANK YOU TOBY");
```

이전에도 이야기했지만 이 코드는 모든 메소드를 구현해야 하고, 부가적인 기능인 리턴 값을 문자로 바꾸는 기능이 모든 메소드에서 중복되는 문제가 나타난다.

#### 다이내믹 프록시 적용

클래스로 만든 HelloUppercase를 다이내믹 프록시로 만들어보자.

_p.441: 다이내믹 프록시의 동작방식 이미지_

다이내믹 프록시는 프로시 팩토리에 의해 런타임 시 다이내믹하게 만들어지는 오브젝트다. 다이내믹 프록시 오브젝트는 타깃의 인터페이스와 같은 타입으로 만들어진다. 클라이언트는 다이내믹 프록시 오브젝트를 타깃 인터페이스를 통해 사용할 수 있다. 이 덥궁네 프록시를 만들 때 인터페이스를 모두 구현해가면서 클래스를 정의하는 수고를 덜 수 있다. 프록시 팩토리엑게 인터페이스 정보만 제공해주면 해당 인터페이스를 구현한 클래스의 오브젝트를 자동으로 만들어준다.

다이내믹 프록시가 인터페이스 구현 클래스의 오브젝트는 만들어주지만, 프록시로 필요한 부가기능 제공 코드는 직접 작성해야 한다. 부가기능은 프로깃 오브젝트와 독립적으로 InvocationHandler를 구현한 오브젝트에 담는다. InvocationHandler는 다음과 같은 메소드 한 개만 가진 간단한 인터페이스다.

```java
public Object invoke(Object proxy, Method method, Object[] args)
```

다이내믹 프록시 오브젝트는 클라이언트의 모든 요청을 리플랙션 정보로 변환해서 InvocationHandler 구현 오브젝트의 invoke 메소드로 넘기는 것이다. 타깃 인터페이스의 모든 메소드 요청이 하나의 메소드로 집중되기 때문에 중복되는 기능을 효과적으로 제거할 수 있다.

Hello 인터페이스를 제공하면서 프록시 팩토리에게 다이내믹 프록시를 만들어달라고 요청하면 Hello 인터페이스의 모든 메소드를 구현한 오브젝트를 생성해준다.

InvocationHandler를 구현한 오브젝트를 제공해주면 다이내믹 프록시가 받는 모든 요청을 InvocationHandler의 invoke() 메소드로 보내준다. Hello 인터페이스의 메소드가 아무리 많더라도 invoke() 메소드 하나로 처리할 수 있다.

다이내믹 프록시를 만들어보자.

먼저 다이내믹 프록시로부터 메소드 호출 정보를 받아 처리하는 InvocationHandler를 만들어보자.

```java
public class UppercaseHandler implements InvocationHandler {
    Hello target;

    public UppercaseHandler(Hello target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        String ret = (String) method.invoke(target, args); // 타깃으로 위임, 인터페이스의 메소드 호출에 모두 적용된다.
        return ret.toUpperCase(); // 부가기능 제공
    }
}
```

다이내믹 프록시로부터 요청을 전달받으려면 InvocationHandler를 구현해야 한다. 다이내믹 프록시가 받는 모든 요청은 invoke() 메소드로 전달된다. 다이내믹 프록시를 통해 요청이 전달되면 리플렉션 API를 이용해 타깃 오브젝트의 메소드를 호출한다. 타깃 오브젝트는 생성자를 통해 미리 전달 받아둔다.

이젱 InvocationHandler를 사용하고 Hello 인터페이스를 구현하는 프록시를 만들어보자. 다이내믹 프록시 생성은 Proxy 클래스의 newProxyInstance() 스태틱 팩토리 메소드를 이용하면 된다.

```java
@Test
public void dynamicProxy() {
    Hello proxiedHello = (Hello) Proxy.newProxyInstance(
        getClass().getClassLoader(), // 동적으로 생성되는 다이내믹 프록시 클래스의 로딩에 사용할 클래스 로더
        new Class[] { Hello.class }, // 구현할 인터페이스
        new UppercaseHandler(new HelloTarget())); // 부가기능과 위임 코드를 담은 InvocationHandler

    assertThat(proxiedHello.sayHello("Toby")).isEqualTo("HELLO TOBY");
    assertThat(proxiedHello.sayHi("Toby")).isEqualTo("HI TOBY");
    assertThat(proxiedHello.sayThankYou("Toby")).isEqualTo("THANK YOU TOBY");
}
```

다루기 쉽지 않은 리플렉션 API를 이용했고, 기존 HelloUppercase 프록시 클래스보다 더 까다로워진 것 같다. 과연 다이내믹 프록시를 적용했을 때 장점이 있긴 있는 것일까?

#### 다이내믹 프록시의 확장

다이내믹 프록시를 사용하는 것이 직접 정의한 프록시보다 훨씬 유연하다. Hello 인터페이스의 메소드가 3개가 아니라 30개라고 생각해보자. 프록시를 직접 정의할 경우, 30개의 메소드를 모두 구현해야 하지만, 다이내믹 프록시의 경우 그렇지 않다.

또 하나의 예시를 살펴보자. UppercaseHandler는 모든 메소드의 리턴 타입이 String이라고 가정한다. 그런데 리턴타입이 String이 아닌 메소드가 추가된다면 런타임에 캐스팅 오류가 발생할 것이다. 그래서 Method를 이용한 타깃 오브젝트의 메소드 호출 이후 리턴 타입을 확인해서 String인 경우에만 대문자로 바꿔주고 나머지는 그대로 넘겨주는 방식으로 수정해보자.

```java
public class UppercaseHandler implements InvocationHandler {
    Object target;

    public UppercaseHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        Object ret = method.invoke(target, args);

        if (ret instanceof String) {
            return ((String) ret).toUpperCase();
        }

        return ret;
    }
}
```

리턴 타입뿐만 아니라 메소드의 이름도 조건으로 걸 수 있다. 이름이 say로 시작하는 경우에만 대문자로 바꾸도록 수정해보자.

```java
@Override
public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    Object ret = method.invoke(target, args);

    if (ret instanceof String && method.getName().startsWith("say")) {
        return ((String) ret).toUpperCase();
    }

    return ret;
}
```

이렇게 다이내믹 프록시를 이용하면 InvocationHandler를 구현한 클래스만 수정하여 프록시가 제공할 부가기능을 수정할 수 있다.

### 다이내믹 프록시를 이용한 트랜잭션 부가기능

기존 UserServiceTx는 서비스 인터페이스의 메소드를 모두 구현해야 하고 트랜잭션이 필요한 메소드마다 트랜잭션 처리 코드가 중복돼서 나타나는 비효율적인 방법으로 만들어져있다.

UserServiceTx를 다이내믹 프록시로 만들어보자.

#### 트랜잭션 InvocationHandler

트랜잭션 부가기능을 가진 핸들러의 코드는 다음과 같이 정의할 수 있다.

```java
public class TransactionHandler implements InvocationHandler {
    private Object target; // 부가기능을 제공할 타깃 오브젝트
    private PlatformTransactionManager transactionManager;
    private String pattern; // 트랜잭션 적용할 메소드 이름 패턴

    public void setTarget(Object target) {
        this.target = target;
    }

    public void setTransactionManager(PlatformTransactionManager transactionManager) {
        this.transactionManager = transactionManager;
    }

    public void setPattern(String pattern) {
        this.pattern = pattern;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        if (method.getName().startsWith(pattern)) {
            return invokeInTransaction(method, args);
        } else {
            return method.invoke(method, args);
        }
    }

    private Object invokeInTransaction(Method method, Object[] args) throws Throwable {
        TransactionStatus status = this.transactionManager.getTransaction(new DefaultTransactionDefinition());
        try {
            Object ret = method.invoke(target, args);
            this.transactionManager.commit(status);
            return ret;
        } catch (InvocationTargetException e) {
            this.transactionManager.rollback(status);
            throw e.getTargetException();
        }
    }
}
```

요청을 위임할 타깃을 DI로 제공받도록 한다. 타깃을 저장할 변수는 Object로 선언하여 UserServiceImpl 외에 트랜잭션 적용이 필요한 어떤 타깃 오브젝트에도 적용할 수 있다.

이제 UserServiceTx보다 코드는 복잡하지 않으면서도 UserService뿐만 아니라 모든 트랜잭션이 필요한 오브젝트에 적용 가능한 트랜잭션 프록시 핸들러가 만들어졌다.

#### TransactionHandler와 다이내믹 프록시를 이용하는 테스트

이제 다이내믹 프록시에 사용되는 TransactionHandler가 UserServiceTx를 대신할 수 있는지 확인하기 위해 UserServiceTest에 적용해보자.

```java
@Test
public void upgradeAllOrNoting() throws Exception {
    TestUserService testUserService = new TestUserService(users.get(3).getId());
    testUserService.setUserDao(this.userDao);
    testUserService.setMailSender(mailSender);

    TransactionHandler txHandler = new TransactionHandler();
    txHandler.setTarget(testUserService);
    txHandler.setTransactionManager(transactionManager);
    txHandler.setPattern("upgradeLevels");

    UserService txUserService = (UserService) Proxy.newProxyInstance(
            getClass().getClassLoader(),
            new Class[]{UserService.class},
            txHandler);

    userDao.deleteAll();
    for(User user: users) userDao.add(user);

    try {
        txUserService.upgradeLevels();
        fail("TestUserServiceException expected"); //
    } catch (TestUserServiceException e) {
        // TestService가 던지는 예외를 잡아서 계속 진행되도록 한다.
    }
    checkLevelUpgraded(users.get(1), false); // 예외가 발생하기 전에 레벨 변경이 있어ㄸ썬 사용자 레벨이 처음 상태로 바뀌었나 확인
}
```

### 다이내믹 프록시를 위한 팩토리 빈

이제 TransactionHandler와 다이내믹 프록시를 스프링 DI를 통해 사용할 수 있도록 만들어야 한다.

문제는 DI 대상이 되는 다이내믹 프록시 오브젝트는 일반적인 스프링의 빈으로 등록할 방법이 없는 점이다.

스프링은 내부적으로 리플렉션을 이용해 클래스의 오브젝트를 생성한다. Class의 newInstance() 메소드는 해당 클래스의 파리마터가 없는 생성자를 호출하고, 그 결과 생성되는 오브젝트를 돌려주는 리플렉션 API다.

```java
Date now = (Date) Class.forName("java.util.Date").newInstance();
```

스프링은 리플랙션 API를 이용해 빈 정의에 나오는 클래스 이름을 가지고 빈 오브젝트를 생성한다. 문제는 다이내믹 프록시 오브젝트의 클래스가 어떤 것인이 알 수 없다는 것이다. 다이내믹 프록시는 Proxy 클래스의 newProxyInstance()라는 스태틱 팩토리 메소드를 통해서만 만들 수 있다.

#### 팩토리 빈

사실 스프링은 클래스 정보를 가지고 기본 생성자를 통해 오브젝트를 만드는 방법 외에도 빈을 만들 수 있는 여러 가지 방법을 제공한다. 대표적으로 팩토리 빈을 이용한 생성 방법을 들 수 있다. 팩토리 빈이란 스프링을 대신해서 오브젝트의 생성 로직을 담당하도록 만들어진 특별한 빈을 말한다.

팩토리 빈을 만드는 간단한 방법은 FactoryBean이라는 인터페이스를 구현하는 것이다.

```java
package org.springframework.beans.factory;

public interface FactoryBean<T> {
    T getObject() throws Exception; // 빈 오브젝트를 생성해 돌려준다.
    Class<? extends T> getObjectType; // 생성되는 오브젝트 타입을 돌려준다.
    boolean isSingleton(); // getObject()가 돌려주는 오브젝트가 항상 같은 싱글톤 오브젝트인지 알려준다.
}
```

FactoryBean을 구현한 클래스를 스프링 빈으로 등록하면 팩토리 빈으로 동작한다. 팩토리 빈의 동작 원리를 확인하기 위한 학습 테스트를 하나 만들어보자.

```java
// 생성자를 제공하지 않는 클래스
public class Message {
    String text;

    private Message(String text) {
        this.text = text;
    }

    public String getText() {
        return text;
    }

    public static Message newMessage(String text) {
        return new Message(text);
    }
}
```

위 클래스는 생성자를 제공하지 않기 때문에 직접 스프링 빈으로 등록해서 사용할 수 없다.

사실 스프링은 private 생성자를 가진 클래스도 빈으로 등록해주면 리플렉션을 이용해 오브젝트를 만들어준다. 리플렉션은 private으로 선언된 접근 규약을 위반할 수 있는 강력한 기능이 있기 때문이다. 하지만 private으로 선언한 이유는 스태틱 메소드를 통해 오브젝트가 생성되어야 하는 중요한 이유가 있다는 의미이기 때문에 강제로 생성하면 위험하다.

Message 클래스의 오브젝트를 생성해주는 팩토리 빈 클래스를 만들어보자.

```java
public class MessageFactoryBean implements FactoryBean<Message> {
    String text;

    public void setText(String text) {
        this.text = text;
    }

    @Override
    public Message getObject() throws Exception {
        return Message.newMessage(this.text);
    }

    @Override
    public Class<?> getObjectType() {
        return Message.class;
    }

    @Override
    public boolean isSingleton() {
        return false;
    }
}
```

스프링은 FactoryBean을 구현한 클래스가 빈의 클래스로 지정되면, 팩토리 빈 클래스의 오브젝트의 getObject() 메소드를 이용해 오브젝트를 가져오고, 이를 빈 오브젝트로 사용한다. 빈의 클래스로 등록된 팩토리 빈은 빈 오브젝트를 생성하는 과정에서만 사용된다.

#### 팩토리 빈의 설정 방법

위에서 만든 팩토리 빈을 설정하자.

```xml
<bean id="message" class="kang.onezero.tobyspring.learningtest.factorybean.MessageFactoryBean">
    <property name="text" value="Factory Bean" />
</bean>
```

여타 빈 설정과 다른 점은 message 빈 오브젝트의 타입이 MessageFactoryBean이 아니라 Message 타입이라는 것이다. Message 빈 타입은 MessageFactoryBean의 getObjectType() 메소드가 돌려주는 타입으로 결정된다. 또, getObject()가 생성해주는 오브젝트가 message 빈의 오브젝트가 된다.

위 설정을 담은 설정파일을 FactoryBeanTest-context.xml이라는 이름으로 저장하고 테스트를 작성하자.

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(locations = {"classpath:FactoryBeanTest-context.xml"})
public class FactoryBeanTest {
    @Autowired
    ApplicationContext context;

    @Test
    public void getMessageFromFactoryBean() {
        Object message = context.getBean("message");
        assertThat(message).isInstanceOf(Message.class);
        assertThat(((Message) message).getText()).isEqualTo("Factory Bean");
    }
}

```

드물지만 팩토리 빈이 생성하는 빈 오브젝트가 아니라 팩토리 빈 자체를 가져오고 싶을 때가 있다. 이때 '&'를 빈 이름 앞에 붙여주면 팩토리 빈 자체를 돌려준다.

```java
@Test
public void getFactoryBean() throws Exception {
    Object factory = context.getBean("&message");
    assertThat(factory).isInstanceOf(MessageFactoryBean.class);
}
```

#### 다이내믹 프록시를 만들어주는 팩토리 빈

Proxy.newProxyInstance() 메소드로만 생성 가능한 다이내믹 프록시는 일반적인 방법으로 스프링 빈으로 등록할 수 없다. 대신 팩토리 빈을 이용하면 다이내믹 프록시 인스턴스를 스프링 빈으로 등록할 수 있다. 팩토리 빈의 getObject() 메소드에서 다이내믹 프록시 오브젝트를 만들어주는 코드를 넣으면 되기 때문이다.

#### 트랜잭션 프록시 팩토리 빈

다음은 TransactionHandler를 이용하는 다이내믹 프록시를 생성하는 팩토리 빈 클래스다.

```java
public class TxProxyFactoryBean implements FactoryBean<Object> {
    Object target;
    PlatformTransactionManager transactionManager;
    String pattern;
    Class<?> serviceInterface; // 다이내믹 프록시 생성 시 필요하다. UserService 외의 인터페이스를 가진 타깃에도 적용할 수 있다.

    public void setTarget(Object target) {
        this.target = target;
    }

    public void setTransactionManager(PlatformTransactionManager transactionManager) {
        this.transactionManager = transactionManager;
    }

    public void setPattern(String pattern) {
        this.pattern = pattern;
    }

    public void setServiceInterface(Class<?> serviceInterface) {
        this.serviceInterface = serviceInterface;
    }

    @Override
    public Object getObject() throws Exception {
        TransactionHandler txHandler = new TransactionHandler();
        txHandler.setTarget(target);
        txHandler.setTransactionManager(transactionManager);
        txHandler.setPattern(pattern);
        return Proxy.newProxyInstance(
                getClass().getClassLoader(),
                new Class[] {serviceInterface},
                txHandler);
    }

    @Override
    public Class<?> getObjectType() {
        return serviceInterface; // 팩토리 빈이 생성하는 오브젝트 타입은 DI 받은 인터페이스 타입에 따라 달라진다. TransactionHandler를 사용하는 다이내믹 프록시를 사용한다.
    }

    @Override
    public boolean isSingleton() {
        return false; // 싱글톤 빈이 아니라는 뜻이 아니라 getObject()가 매번 같은 오브젝트를 리턴하지 않는다는 뜻이다.
    }
}
```

이제 UserServiceTx 빈 설정을 대신해서 userService라는 이름으로 TxProxyFactoryBean 팩토리 빈을 등록한다. UserServiceTx는 더 이상 사용하지 않으니 제거한다.

```xml
<bean id="userService" class="kang.onezero.tobyspring.user.service.TxProxyFactoryBean">
    <property name="target" ref="userServiceImpl" />
    <property name="transactionManager" ref="transactionManager" />
    <property name="pattern" value="upgradeLevels" />
    <property name="serviceInterface" value="kang.onezero.tobyspring.user.service.UserService" />
</bean>
```

#### 트랜잭션 프록시 팩토리 빈 테스트

UserServiceTest의 upgradeAllOrNoting 테스트 코드에 TxProxyFactoryBean을 적용한 후 테스트해보자.

```java
@Test
@DirtiesContext // 다이내믹 프록시 팩토리빈을 직접 만들어 사용할 때는 없앴다가 다시 등장한 컨텍스트 무효화 어노테이션
public void upgradeAllOrNoting() throws Exception {
    TestUserService testUserService = new TestUserService(users.get(3).getId());
    testUserService.setUserDao(this.userDao);
    testUserService.setMailSender(mailSender);

    TxProxyFactoryBean txProxyFactoryBean = context.getBean("&userService", TxProxyFactoryBean.class);
    txProxyFactoryBean.setTarget(testUserService);
    UserService txUserService = (UserService) txProxyFactoryBean.getObject();

    userDao.deleteAll();
    for(User user: users) userDao.add(user);

    try {
        txUserService.upgradeLevels();
        fail("TestUserServiceException expected"); //
    } catch (TestUserServiceException e) {
        // TestService가 던지는 예외를 잡아서 계속 진행되도록 한다.
    }
    checkLevelUpgraded(users.get(1), false); // 예외가 발생하기 전에 레벨 변경이 있어ㄸ썬 사용자 레벨이 처음 상태로 바뀌었나 확인
}
```

### 프록시 팩토리 빈 방식의 장점과 한계

다이내믹 프록시를 생성해주는 프록시를 생성해주는 팩토리 빈을 사용하는 방법은 여러가지 장점이 있다. 한번 부가기능을 가진 프록시를 생성하는 팩토리 빈을 만들어두면 타깃의 타입에 상관없이 재사용할 수 있기 때문이다.

#### 프록시 팩토리 빈의 재사용

TransactionHandler를 이용하는 다이내믹 프록시를 생성해주는 TxProxyFactoryBean은 코드의 수정 없이도 다양한 클래스에 적용할 수 있다. 타깃 오브젝트에 맞는 프로퍼티 정보를 설정해서 빈으로 등록해주기만 하면 된다.

#### 프록시 팩토리 빈 방식의 장점

앞에서 데코레이터 패턴이 적용된 프록시를 사용하면 많은 장점이 있음에도 적극적으로 활용되지 못하는 데는 두 가지 문제가 있다고 설명했다.

1. 프록시를 적용할 타깃이 구현하고 있는 인터페이스를 구현하는 프록시 클래스를 일일이 만들어야 하는 번거로움
2. 부가적인 기능이 여러 메소드에 반복적으로 나타나게 돼서 코드 중복 문제 발생

다이내믹 프록시를 이용하면 타깃 인터페이스를 구현하는 클래스를 일일이 만들 필요가 없고, 하나의 핸들러 메소드를 구현한 것만으로 수많은 메소드의 중복을 제거해줄 수도 있다.

#### 프록시 팩토리 빈의 한계

프로시를 통해 타깃에 부가기능을 제공하는 것은 메소드 단위로 일어나는 일이다. 하나의 클래스 안에 존재하는 여러 개의 메소드에 부가기능을 한번에 제공하는 것은 어렵지 않게 가능했다. 하지만 한 번에 여러 개의 클래스에 공통적인 기능을 제공하는 일은 지금까지 살펴본 방법으로는 불가능하다. 트랜잭션과 같이 비즈니스 로직을 담은 많은 클래스에 적용할 필요가 있다면 거의 비슷한 프록시 팩토리 빈의 설정이 중복되는 것을 막을 수 없다.

하나의 타깃에 여러 개의 부가기능을 적용하려고 할 때도 문제다. XML 설정 은 엄청나게 복잡해질 것이다. 텍스트로 된 빈 설정 작성은 실수하기 쉽고 점점 다루기 힘들어진다. 게다가 타깃과 인터페이스만 다른, 거의 비슷한 설정이 자꾸 반복된 다는 점이 뭔가 찜찜하다.

또 한가지 문제점은 TransactionHandler 오브젝트가 프록시 팩토리 빈 개수만큼 만들어진다는 점이다. TransactionHandler는 타깃 오브젝트를 프로퍼티로 갖고 있다. 따라서 같은 부가기능을 제공하더라도 타깃 오브젝트가 달라지면 새로운 TransactionHandler를 만들어야 한다. TransactionHandler의 중복으을 없애고 모든 타깃에 적용 가능한 싱글톤 빈으로 만들어서 적용할 수는 없을까?
