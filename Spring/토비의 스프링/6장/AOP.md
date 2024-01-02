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

### 데코레이터 패턴

### 프록시 패턴

## 다이내믹 프록시

#### 프록시의 구성과 프록시 작성의 문제점

#### 리플렉션

#### 프록시 클래스

#### 다이내믹 프록시 적용

#### 다이내믹 프록시의 확장

### 다이내믹 프록시를 이용한 트랜잭션 부가기능

#### 프랜잭션 InvocationHandler

#### TransactionHandler와 다이내믹 프록시를 이용하는 테스트

### 다이내믹 프록시를 위한 팩토리 빈

#### 팩토리 빈

#### 팩토리 빈의 설정 방법

#### 다이내믹 프록시를 만들어주는 팩토리 빈

#### 트랜잭션 프록시 팩토리 빈

#### 트랜잭션 프록시 팩토리 빈 테스트

### 프록시 팩토리 빈 방식의 장점과 한계

#### 프록시 팩토리 빈의 재사용

#### 프록시 팩토리 빈 방식의 장점

#### 프록시 팩토리 빈의 한계
