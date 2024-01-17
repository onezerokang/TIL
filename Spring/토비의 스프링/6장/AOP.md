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

## 스프링의 프록시 팩토리 빈

지금까지 기존 코드 수정없이 트랜잭션 부가기능을 추가해줄 수 이는 다양한 방법을 살펴봤다. 스프링은 이런 문제에 어떤 해결책을 제시하는지 살펴보자.

### ProxyFactoryBean

스프링은 일관된 방법으로 프록시를 만들수 있게 도와주는 추상 레이어를 제공한다. 생성된 프록시는 스프링 빈으로 등록돼야 한다. 스프링은 프록시 오브젝트를 생성해주는 기술을 추상화한 팩토리 빈을 제공한다.

스프링의 ProxyFactoryBean은 프록시를 생성해서 빈 오브젝트로 등록하게 해주는 팩토리 빈이다. ProxyFactoryBean은 순수하게 프록시를 생성하는 작업만을 담당하고 프록시를 통해 제공해줄 부가기능은 별도의 빈에 둘 수 있다.

ProxyFactoryBean이 생성하는 프록시에서 사용할 부가기능은 MethodInterceptor 인터페이스를 구현해서 만든다.

앞에서 만들엇던 다이내믹 프록시 학습 테스트를 스프링의 ProxyFactoryBean을 이용하도록 수정해보자.

```java
@Test
public void proxyFactoryBean() {
    ProxyFactoryBean pfBean = new ProxyFactoryBean();
    pfBean.setTarget(new HelloTarget()); // 타깃 설정
    pfBean.addAdvice(new UppercaseAdvice());; // 부가기능을 담은 어드바이스. 여러 개 추가 가능

    Hello proxiedHello = (Hello) pfBean.getObject(); // FactoryBean이므로 getObject()로 생성된 프록시를 가져온다.

    assertThat(proxiedHello.sayHello("Toby")).isEqualTo("HELLO TOBY");
    assertThat(proxiedHello.sayHi("Toby")).isEqualTo("HI TOBY");
    assertThat(proxiedHello.sayThankYou("Toby")).isEqualTo("THANK YOU TOBY");
}

static class UppercaseAdvice implements MethodInterceptor {
    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {
        // 리플렉션의 Method와 달리 메소드 실행 시 타깃 오브젝트를 전달할 필요가 없다. MethodInvocation은 메소드 정보와 함께 타깃 오브젝트를 알고 있기 때문이다.
        String ret = (String) invocation.proceed();
        return ret.toUpperCase(); // 부가기능 적용
    }
}
```

#### 어드바이스: 타깃이 필요 없는 순수한 부가기능

ProxyFactoryBean을 적용한 코드를 기존의 JDK 다이내믹 프록시를 사용했던 코드와 비교해보면 몇 가지 차이점이 있다.

- InvocationHandler를 구현했을 때와 달리 MethodInterceptor를 구현한 UppercaseAdvice에는 타깃 오브젝트가 등장하지 않는다. MethodInterceptor로는 메소드 정보와 함께 타깃 오브젝트가 담긴 MethodInvocation 오브젝트가 전달된다. MethodInvocation은 타깃 오브젝트의 메소드를 실행할 수 있는 기능이 있기 때문에 MethodInterceptor는 부가기능을 제공하는 데만 집중할 수 있다.
- MethodInvocation은 일종의 콜백 오브젝트로 proceed()를 실행하면 타깃 오브젝트의 메소드를 실행한다. ProxyFactoryBean은 작은 단위의 템플릿/콜백 구조를 응용해 적용했기 땜누에 템플릿 역할을 하는 MethodInvocation을 싱글톤으로 두고 공유할 수 있다(JDK 다이내믹 프록시 코드와 가장 큰 차이)
- ProxyFactoryBean에 이 MethodInterceptor를 추가해줄 때 수정자 메소드 대신 addAdvice()를 사용한다는 점도 주목. ProxyFactoryBean 하나만으로 여러 개의 부가 기능을 제공해주는 프록시를 만들 수 있다는 뜻이다. 따라서 앞에서 살펴봤던 프록시 팩토리 빈의 단점 중 하나였던, 새로운 부가기능을 추가할 때마다 프록시와 프록시 팩토리 빈도 추가해줘야 한다는 문제를 해결할 수 있다.
- MethodInterceptor를 추가하는 메소드 이름은 addAdvice다. 스프링은 단순히 메소드 실행을 가로채는 방식 외에도 부가기능을 추가하는 여러 가지 방법을 제공한다. MethodInterceptor처럼 타깃 오브젝트에 적용하는 부가기능을 담은 오브젝트를 스프링에서는 어드바이스라고 부른다.
- 마지막 차이점은 프록시가 구현해야 하는 Hello 인터페이스를 제공해주지 않았다. ProxyFactoryBean에 인터페이스 자동검출 기능을 사용해 타깃 오브젝트가 구현하고 있는 인터페이스 정보를 알아낸다. 그리고 알아낸 인터페이스를 모두 구현하는 프록시를 만들어준다.
- **어드바이스는 타깃 오브젝트에 종속돼지 않는 순수한 부가기능을 담은 오브젝트라는 사실을 잘 기억해두자.**

#### 포인트 컷: 부가기능 적용 대상 메소드 선정 방법

- 기존 InvocationHandler는 메소드 이름을 가지고 부가기능 적용 대상 메소드를 선정하는 것이 가능했다(pattern 필드 사용)
- ProxyFactoryBean의 MethodInterceptor 오브젝트는 여러 프록시가 공유해서 사용할 수 있다. 그러기 위해서 MethodInterceptor는 타깃 정보를 가지고 있으면 안된다. 그 덕분에 MethodInterceptor를 스프링의 싱글톤 빈으로 등록 가능. 그런데 여기에다가 트랜잭션 적용 대상 메소드 이름 패턴을 넣어주는 것은 곤란.
- 기존 다이내믹 프록시는 모든 메소드 요청이 InvocationHandler로 넘겨졌고, invoke() 메소드에서 부가기능을 적용할 메소드를 구분했다.
  - 이 경우 부가기능을 가진 InvocationHandler가 타깃과 메소드 선정 알고리즘 코드에 의존하고 있다는 문제가 있다.
  - 만약 타깃이 다르고 메소드 선정 방식이 다르다면 InvocaitonHandler 오브젝트를 여러 프록시가 공유할 수 없다.
- 반면 ProxyFactoryBean 방식은 두 가지 확장기능인 부가기능(Advice)와 선정 알고리즘(Pointcut)을 활용하는 유연한 구조를 제공한다.
  - Advice: 부가기능을 제공하는 오브젝트
  - Pointcut: 선정 알고리즘을 담은 오브젝트
  - 어드바이스와 포인트컷은ㅁ 모두 프록시에서 DI로 주입돼서 사용된다.
  - 두 가지 모두 여러 프록시에서 공유가 가능하도록 만들어지기 때문에 스프링의 싱글톤 빈으로 등록이 가능하다.
- 프록시는 클라이언트로 요청 받으면 포인트컷에게 부가기능을 부여할 메소드인지 확인해달라고 요청
- 포인트컷은 Pointcut 인터페이스를 구현해서 만들면 된다.
- 프록시는 포인트컷으로부터 확인받으면 MethodInterceptor 타입의 어드바이스 호출
- 어드바이스는 JDK의 다이내믹 프록시의 InvocationHandler와 달리 직접 타깃을 호출하지 않는다. 자신이 공유되어야 하므로 타깃 정보라는 상태를 가질 수 없다. 어드바이스가 부가기능을 부여하는 중에 타깃 메소드 호출이 필요하면 전달받은 MethodInvocation 타입 콜백 오브젝트의 proceed() 메소드를 호출해주기만 하면 된다.
- 어드바이스가 일종의 템플릿이 되고 타깃을 호출하는 기능을 갖고 있는 MethodInvocation 오브젝트가 콜백이 되는 것이다.
- 템플릿은 한번 만들면 재사용이 가능하고 여러 빈이 공유해서 사용할 수 있듯이, 어드바이스도 독립적인 싱글톤 빈으로 등록하고 DI를 주입해서 여러 프록시가 사용하도록 만들 수 있다.
- 프록시로부터 어드바이스와 포인트컷을 독립시키고 DI를 사용하게 한 것은 전형적인 전략 패턴 구조다. 덕분에 여러 프록시가 공유해서 사용할 수도 있고, 또 구체적인 부가기능 방식이나 메소드 선정 알고리즘이 바뀌면 구현 클래스만 바꿔서 설정에 넣어주면 된다. 프록시와 ProxyFactoryBean 등의 변경 없이도 기능을 자유롭게 확장할 수 있는 OCP를 충실히 지키는 구조가 된 것이다.

다음은 MethodInterceptor로 만들었던 어드바이스와 함께 포인트컷까지 적용하는 학습테스트 코드다.

```java
@Test
public void pointcutAdvisor() {
    ProxyFactoryBean pfBean = new ProxyFactoryBean();
    pfBean.setTarget(new HelloTarget());

    NameMatchMethodPointcut pointcut = new NameMatchMethodPointcut();
    pointcut.setMappedName("sayH*");

    pfBean.addAdvisor(new DefaultPointcutAdvisor(pointcut, new UppercaseAdvice()));

    Hello proxiedHello = (Hello) pfBean.getObject();

    assertThat(proxiedHello.sayHello("Toby")).isEqualTo("HELLO TOBY");
    assertThat(proxiedHello.sayHi("Toby")).isEqualTo("HI TOBY");
    assertThat(proxiedHello.sayThankYou("Toby")).isEqualTo("Thank You Toby");
}
```

포인트컷이 필요없을 때는 ProxyFactoryBean의 addAdvice() 메소드를 호출해서 어드바이스만 등록했다.

포인트 컷을 함께 등록할 때는 어드바이스와 포인트컷을 Advisor 타입으로 묶어서 addAdvisor() 메소드로 추가해야 한다.

그렇다면 왜 어드바이스와 포인트컷을 묶어서 등록해야 할까? 그 이유는 ProxyFactoryBean에는 여러 개의 어드바이스와 포인트컷을 등록할 수 있는 데, 이들을 따로 등록하면 어떤 어드바이스에 대해 어떤 포인트컷을 적용할지 애매해지기 때문이다.

이렇게 어드바이스와 포인트컷을 묶은 오브젝트를 인터페이스 이름을 따서 어드바이저(Advisor)라고 부른다.

### ProxyFactoryBean 적용

JDK 다이내믹 프록시의 구조를 그대로 이용해서 만들었던 TxProxyFactoryBean을 이제 스프링의 ProxyFactoryBean을 이용하도록 수정해보자.

#### TransactionAdvice

먼저 트랜잭션 부가기능을 처리할 어드바이스를 만들자.

```java
public class TransactionAdvice implements MethodInterceptor {
    PlatformTransactionManager transactionManager;

    public void setTransactionManager(PlatformTransactionManager transactionManager) {
        this.transactionManager = transactionManager;
    }

    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {
        TransactionStatus status = this.transactionManager.getTransaction(new DefaultTransactionDefinition());
        try {
            Object ret = invocation.proceed();
            this.transactionManager.commit(status);
            return ret;
        } catch (RuntimeException e) {
            // JDK 다이내믹 프록시가 제공하는 Method와 달리 스프링의 MethodInvocation을 통한 타깃 호출은 예외가 포장되지 않고 타깃에서 보낸 그대로 전달된다.
            this.transactionManager.rollback(status);
            throw e;
        }
    }
}
```

JDK 다이내믹 프록시의 InvocationHandler를 이용했을 때보다 코드가 간결하다. 리플렉션을 통한 타깃 메소드 호출작업의 번거로움은 MethodInvocation 타입의 콜백을 이용한 덕분에 대부분 제거할 수 있다.

#### 스프링 XML 설정파일

학습 테스트에서 직접 DI해서 사용했던 코드를 XML 설정으로 바꿔주자.

먼저 어드바이스를 스프링 빈으로 등록하자.

```xml
<bean id="transactionAdvice" class="kang.onezero.tobyspring.user.service.TransactionAdvice">
    <property name="transactionManager" ref="transactionManager" />
</bean>
```

다음은 포인트 컷 빈으로 등록하자.

```xml
<bean id="transactionPointcut" class="org.springframework.aop.support.NameMatchMethodPointcut">
    <property name="mappedName" value="upgrade*" />
</bean>
```

이제 어드바이스와 포인트 컷을 담을 어드바이저를 빈으로 등록하자.

```xml
<bean id="transactionAdvisor" class="org.springframework.aop.support.DefaultPointcutAdvisor">
    <property name="advice" ref="transactionAdvice" />
    <property name="pointcut" ref="transactionPointcut" />
</bean>
```

이제 ProxyFactoryBean을 등록하자. 다음과 같이 프로퍼티에 타깃 빈과 어드바이저 빈을 지정해주면 된다.

```xml
<bean id="userService" class="org.springframework.aop.framework.ProxyFactoryBean">
    <property name="target" ref="userServiceImpl" />
    <!--
    어드바이스와 어드바이저를 동시에 설정해줄 수 있는 프로퍼티.
    리스트에 어드바이스나 어드바이저의 빈 아이디를 값으로 넣어주면 된다.
    기존의 ref 속성을 사용하는 DI와는 방식이 다름에 주의해야 한다.    -->
    <property name="interceptorNames">
        <list>
            <value>transactionAdvisor</value>
        </list>
    </property>
</bean>
```

어드바이저는 interceptorNames에 넣는다. 프로퍼티 이름이 Advisor가 아닌 이유는 어드바이스와 어드바이저를 혼합해서 설정할 수 있도록 하기 위해서다. 그렇기 때문에 <property>의 ref가 아닌 <list>로 여러 개의 값을 넣을 수 있게 하고 있다.

#### 테스트

트랜잭션이 적용됐는지를 확인하는 하기 위해 만든 upgradeAllOrNoting()을 수정할 것이다.

이번에는 간단한 수정으로 충분하다. 스프링의 ProxyFactoryBean도 팩토리 빈이므로 기존 TxProxyFactoryBean과 같은 방법으로 테스트할 수 있기 때문이다.

```java
@Test
@DirtiesContext // 컨텍스트 설정을 변경하기 때문에 여전히 필요하다.
public void upgradeAllOrNoting() throws Exception {
    TestUserService testUserService = new TestUserService(users.get(3).getId());
    testUserService.setUserDao(this.userDao);
    testUserService.setMailSender(mailSender);

    // TxProxyFactoryBean으로 생성했던 것을 ProxyFactoryBean으로 수정
    ProxyFactoryBean txProxyFactoryBean = context.getBean("&userService", ProxyFactoryBean.class);
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

#### 어드바이스와 포인트컷의 재사용

ProxyFactoryBean은 스프링 DI와 템플릿/콜백 패턴, 서비스 추상화 등의 기법이 모두 적용됐다. 그 덕분에 독립적이며, 여러 프록시가 공유할 수 있는 어드바이스와 포인트컷으로 확장 기능을 분리할 수 있었다. 이제 UserService 외에 새로운 비즈니스 로직을 담은 서비스 클래스가 만들어져도 이미 만들어둔 TransactionAdvice를 그대로 재사용할 수 있다.

## 스프링 AOP

지금까지 비즈니스 로직의 반복적으로 작성된 트랜잭션 코드를 깔끔하게 분리하는 작업을 했다.

### 자동 프록시 생성

부가기능을 제공하는 과정에서 타깃 코드는 깔끔해졌고, 부가기능은 한 번만 만들어 모든 타깃과 메소드에 재사용이 가능하며, 타깃의 적용 메소드를 선정하는 방식도 독립적으로 작성할 수 있도록 분리되었다.

하지만 한 가지 더 해결해야 할 문제가 남아 있다. 부가기능의 적용이 필요한 타깃 오브젝트마다 거의 비슷한 내용의 ProxyFactoryBean 빈 설정정보를 추가해주는 부분이다.

```xml
<bean id="userService" class="org.springframework.aop.framework.ProxyFactoryBean">
    <property name="target" ref="userServiceImpl" />
    <property name="interceptorNames">
        <list>
            <value>transactionAdvisor</value>
        </list>
    </property>
</bean>
```

target 프로퍼티를 제외하면 빈 클래스의 종류, 어드바이스, 포인트컷의 설정이 중복된다. 이런 류의 중복은 제거할 수 없을까?

#### 빈 후처리기를 이용한 자동 프록시 생성기

스프링은 OCP의 가장 중요한 요소인 유연한 확장이라는 개념을 스프링 컨테이너 자신에게도 다양한 방법으로 제공하고 있다. 그래서 스프링은 컨테이너로서 제공하는 기능 중 변하지 않는 핵심적인 부분외에는 대부분 확장할 수 있도록 확장 포인트를 제공한다.

그중 관심을 가질 만한 확장 포인트는 BeanPostProcessor 인터페이스를 구현해서 만든 빈 후처리기다. 빈 후처리기는 스프링 빈 오브젝트로 만들어지고 난 후에, 빈 오브젝트를 다시 가공할 수 있게 해준다.

DefaultAdvisorAutoProxyCreator: 어드바이저를 이용한 자동 프록시 생성기로 스프링이 제공하는 빈 후처리기 중 하나다.

빈 후처리기를를 스프링에 적용하려면 후처리기 자체를 빈으로 등록하면 된다. 스프링은 빈 후처리기가 빈으로 등록되어 있으면 빈 오브젝트가 생성될 때마다 빈 후처리이게 보내서 후처리 작업을 요청한다. 빈 후처리기는 빈의 프로퍼티를 수정하거나, 별도의 초기화 작업을 진행할 수 잆다. 심지어 만들어진 빈 오브젝트를 바꿔치기할 수도 있다.

이를 잘 이용하면 스프링이 생성하는 빈 오브젝트 일부를 프록시로 포정하고, 프록시를 빈으로 대신 등록할 수도 있다. 바로 이것이 자동 프록시 생성 빈 후처리기다.

1. 스프링은 빈 오브젝트가 만들어질 때마다 이를 빈 후처리기에 보낸다.
2. DefaultAdvisorAutoProxyCreator는 전달받은 빈이 프록시 적용 대상인지 확인한다.
3. 프록시 적용 대상이면 내장된 프록시 생성기에 현재 빈에 대한 프록시를 만들게 하고, 만들어진 프록시에 어드바이저를 연결한다.
4. 빈 후처리기는 생성된 프록시를 컨테이너에게 돌려준다.
5. 컨테이너는 빈 후처리가 돌려준 오브젝트를 빈으로 등록하고 사용한다.

#### 확장된 포인트컷

포인트 컷은 다음 두 가지 기능을 갖는다.

1. 타깃 오브젝트의 메소드 중 어떤 메소드에 부가기능을 적용할지 선정
2. 어떤 빈에 프록시를 적용할지를 선택

```java
public interface Pointcut {
    ClassFilter getClassFilter(); // 프록시를 적용할 클래스인지 확인
    MethodMatcher getMethodMatcher(); // 어드바이스를 적용할 메소드인지 확인
}
```

ProxyFactoryBEan에서는 굳이 클래스 레벨의 필터를 필요 없었지만, 모든 빈에 대해 프록시 자동 적용 대상을 선별해야 하는 빈 후처리기인 DefaultAdvisorAutoProxyCreator는 클래스와 메소드 선정 알고리즘을 모두 갖고 있는 포인트컷이 필요하다(기존 사용한 NameMatchMethodPointcut은 클래스 필터 기능이 없다.)

#### 포인트컷 테스트

포인트컷의 기능을 간단한 학습 테스트로 확인해보자.

Hello 인터페이스와 이를 구현한 HelloTarget, 그리고 부가기능인 HelloAdvice를 사용했던 DynamicProxyTest에 테스트 메소드를 추가한다.

```java
@Test
public void classNamePointcutAdvice() {
    NameMatchMethodPointcut classMethodPointcut = new NameMatchMethodPointcut() {
        @Override
        public ClassFilter getClassFilter() {
            return new ClassFilter() { // 익명 내부 클래스 방식으로 클래스 정의
                @Override
                public boolean matches(Class<?> clazz) {
                    return clazz.getSimpleName().startsWith("HelloT"); // 클래스 이름이 HelloT로 시작하는 것만 선정한다.
                }
            };
        }
    };

    classMethodPointcut.setMappedName("sayH*"); // sayH로 시작하는 메소드 이름을 가진 메소드만 선정한다.

    // 테스트
    checkAdvice(new HelloTarget(), classMethodPointcut, true);

    class HelloWorld extends HelloTarget {};
    checkAdvice(new HelloWorld(), classMethodPointcut, false);

    class HelloToby extends HelloTarget {};
    checkAdvice(new HelloToby(), classMethodPointcut, true);

}

private void checkAdvice(Object target, Pointcut pointcut, boolean adviced) {
    ProxyFactoryBean pfBean = new ProxyFactoryBean();
    pfBean.setTarget(target);
    pfBean.addAdvisor(new DefaultPointcutAdvisor(pointcut, new UppercaseAdvice()));
    Hello proxiedHello = (Hello) pfBean.getObject();

    if (adviced) {
        // 메소드 선정 방식을 통해 어드바이스 적용
        assertThat(proxiedHello.sayHello("Toby")).isEqualTo("HELLO TOBY");
        assertThat(proxiedHello.sayHi("Toby")).isEqualTo("HI TOBY");
        assertThat(proxiedHello.sayThankYou("Toby")).isEqualTo("Thank You Toby");
    } else {
        // 어드바이스 적용 대상 후보에서 야예 탈락
        assertThat(proxiedHello.sayHello("Toby")).isEqualTo("Hello Toby");
        assertThat(proxiedHello.sayHi("Toby")).isEqualTo("Hi Toby");
        assertThat(proxiedHello.sayThankYou("Toby")).isEqualTo("Thank You Toby");
    }
}
```

- 포인트컷은 NameMatchMethodPointcut을 내부 익명 클래스 방식으로 확장해서 만들었다.
- 클래스 필터를 통과하지 못한 HelloWorld 클래스는 UppercaseAdvice를 제공받지 못한다.

### DefaultAdvisorAutoProxyCreator의 적용

프록시 자동생성 방식에서 사용할 포인트컷을 만드는 방법을 학습 테스트를 만들면서 살펴봤으니, 실제로 적용해보자.

#### 클래스 필터를 적용한 포인트컷 작성

만들어야 할 클래스는 하나뿐이다. 메소드 이름만 비교하던 포인트컷인 NameMatchMethodPointcut을 상속해서 프로퍼티로 주어진 이름 패턴을 가지고 클래스 이름을 비교하는 ClassFilter를 추가하도록 만들 것이다.

```java
public class NameMatchClassMethodPointcut extends NameMatchMethodPointcut {
    public void setMappedClassName(String mappedClassName) {
        // 모든 클래스를 다 허용하던 디폴트 클래스 필터를 프로퍼티로 받은 클래스 이름을 적용해서 필터를 만들어 덮어씌운다.
        this.setClassFilter(new SimpleClassFilter(mappedClassName));
    }

    static class SimpleClassFilter implements ClassFilter {
        String mappedName;

        private SimpleClassFilter(String mappedName) {
            this.mappedName = mappedName;
        }

        public boolean matches(Class<?> clazz) {
            // simpleMatch: 와일드 카드가 들어간 문자열 비교를 지원하는 스프링의 유틸리티 메소드
            return PatternMatchUtils.simpleMatch(mappedName, clazz.getSimpleName());
        }
    }
}
```

#### 어드바이저를 이용하는 자동 프록시 생성기 등록

적용할 자동 프록시 생성기인 DefaultAdvisorAutoProxyCreator는 등록된 빈 중에서 Advisor 인터페이스를 구현한 것들을 모두 찾는다. 그리고 생성되는 모든 빈에 대해 어브다이저의 포인트컷을 적용해보면서 프록시 적용 대상을 선정한다. 빈 클래스가 선정 대상이라면 프록시를 만들어 원리 빈 오브젝트와 바꿔치기한다.

DefaultAdvisorAutoProxyCreator 등록은 다음 한 줄이면 충분하다.

```xml
<bean class = "org.springframework.aop.framework.autoproxy.DefaultAdvisorAutoProxyCreator" />
```

이 빈 정의에는 id 속성이 없는 데, 다른 빈에서 참조하거나 코드에서 빈 이름으로 조회될 필요가 없는 빈이라면 아이디를 등록하지 않아도 되기 때문이다.

#### 포인트컷 등록

다음과 같이 기존 포인트컷 설정을 삭제하고 새로 만든 클래스 필터 지원 포인트컷을 빈으로 등록한다.

```xml
<bean id="transactionPointcut" class="kang.onezero.tobyspring.user.service.NameMatchClassMethodPointcut">
    <property name="mappedClassName" value="*ServiceImpl" /> <!--   클래스 이름 패턴     -->
    <property name="mappedName" value="upgrade*" /> <!--   메소드 이름 패턴     -->
</bean>
```

#### 어드바이스와 어드바이저

어드바이스인 transactionAdvice 빈 설정은 수정할 게 없다.

어드바이저인 transactionAdvisor 빈도 수정할 게 없다. 하지만 어드바이저 사용 방법이 변경되었는 데, 기존 ProxyFactoryBean으로 등록한 빈에서 transactionAdvisor를 명시적으로 DI하지 않고, 어드바이저를 이용하는 자동 프록시 생성기인 DefaultAdvisorAutoProxyCreator에 의해 자동 수집돼고, 생성된 프록시에 다이내믹하게 DI 된다.

#### ProxyFactoryBean 제거와 서비스 빈의 원상 복구

프록시를 도입했을 때부터 아이디를 바꾸고 프록시에 DI 돼서 간접적으로 사용해야 했던 userServiceImpl 빈 아이디를 userService로 되돌려놓을 수 있다ㅏ. 더 이상 명시적인 프록시 팩토리 빈을 등록하지 않기 때문이다. ProxyFactoryBean 타입의 빈도 삭제해버리자.

```xml
<!-- 기존 설정 -->
<bean id="userService" class="org.springframework.aop.framework.ProxyFactoryBean">
    <property name="target" ref="userServiceImpl" />
    <property name="interceptorNames">
        <list>
            <value>transactionAdvisor</value>
        </list>
    </property>
</bean>
<bean id="userServiceImpl" class="kang.onezero.tobyspring.user.service.UserServiceImpl">
    <property name="userDao" ref="userDao" />
    <property name="mailSender" ref="mailSender" />
</bean>
```

```xml
<!-- 수정된 설정 -->
<bean id="userService" class="kang.onezero.tobyspring.user.service.UserServiceImpl">
    <property name="userDao" ref="userDao" />
    <property name="mailSender" ref="mailSender" />
</bean>
```

#### 자동 프록시 생성기를 사용하는 테스트

다시 테스트다. @Autowired를 통해 컨텍스트에서 가져온 UserService 타입 오브젝트는 트랜잭션이 적용된 프록시여야 한다. 지금까지는 ProxyFactoryBean이 빈으로 등록되어 있어 이를 가져와 타깃을 테스트용 클래스로 바꿔치기하는 방법을 상요했다. 하지만 자동 프록시 생성기를 적용한 후에는 더 이상 팩토리 빈이 존재하지 않는다.

지금까지는 설정 파일에 정상적인 경우의 빈 설정만을 두고 롤백을 일으키는 예외 상황에 대한 테스트는 테스트 코드에서 빈을 가져와 수동 DI로 구성을 바꿔서 사용했다.

하지만 자동 프록시 생성기라는 스플이 컨테이너에 종속적인 기법을 사용했기 때문에 예외상황을 위한 테스트 대상도 빈으로 등록해줘야 한다.

이제 타깃을 코드에서 바꿔치기 할 방법도 없고, 자동 프록시 생성기의 적용이 되는지도 빈을 통해 확인할 필요가 있기 떄문이다.

기존에 만들었떤 TestUserService 클래스를 직접 빈으로 등록하자. 그런데 두 가지 문제가 있다.

1. TestUserService가 UserServiceTest 내부에 정의된 스태틱 클래스라는 점
2. 포인트컷이 트랜잭션 어드바이스를 적용해주는 대상 클래스의 이름 패턴이 \*ServiceImpl이라고 되어 있어 TestUserService는 빈으로 등록해도 포인트컷이 프록시 적용 대상으로 선정해주지 않는다.

위 문제를 해결하기 위해 TestUserService 스태틱 멤버 클래스를 수정하자.

1. 스태틱 클래스 자체는 빈을 등록할 때 이름을 지정하는 방법만 알면 아무런 문제가 없다.
2. TestUserService 클래스 이름을 TestUserServiceImpl로 변경하자.
3. 테스트 코드에서 생성할 것이 아니기에 테스트 픽스처로 만든 users 리스트에서 예외를 발생시킬 기준 id를 가져와 사용할 방법이 없다. 그러므로 아예 예외를 발생시킬 대상인 네 번째 사용자 아이디를 클래스에 넣어버리자.

```java
static class TestUserServiceImpl extends UserServiceImpl {
    private String id = "m_gumayusi"; // 텍스트 픽스쳐의 users(3)의 id 값을 고정

    @Override
    protected void upgradeLevel(User user) {
        if (user.getId().equals(this.id)) throw new TestUserServiceException();
        super.upgradeLevel(user);
    }
}
```

이제 TestUserServiceImpl을 빈으로 등록하자.

```xml
<bean id="testUserService"
    class="kang.onezero.tobyspring.user.service.UserServiceTest$TestUserServiceImpl"
    parent="userService" /> <!-- 프로퍼티 정의를 포함해서 userService 빈의 설정을 상속받는다. -->
```

마지막으로 upgradeAllOrNoting() 테스트를 새로 추가한 testUserService 빈을 사용하도록 수정하자.

```java
public class UserServiceTest {
    @Autowired UserService userService;
    @Autowired UserService testUserService; // 같은 타입의 빈이 두 개 존재하여 필드 이름을 기준으로 주입될 빈이 결정된다.

    // 스프링 컨텍스트의 빈 설정을 변경하지 않으므로 @DirtiesContext 어노테이션은 제거됐다.
    @Test
    public void upgradeAllOrNoting() throws Exception {
        userDao.deleteAll();
        for(User user: users) userDao.add(user);

        try {
            this.testUserService.upgradeLevels();
            fail("TestUserServiceException expected");
        } catch (TestUserServiceException e) {
        }
        checkLevelUpgraded(users.get(1), false);
    }
}
```

이테 테스트를 실해앻서 모든 기능이 정상적으로 동작하는지 확인하자. 특히 upgradeAllOrNoting() 테스트를 통해 자동 프록시 생성기가 평범한 비즈니스 로직만 담고 있는 userService 빈을 자동으로 트랜잭션 부가기능을 제공해주는 프록시로 대체했는지 확인해보자.

#### 자동생성 프록시 확인

이제 실제로 프록시가 자동으로 만들어졌는지 직접 확인해보자.

지금까지 트랜잭션 어드바이스를 적용한 프록시 자동생성기를 빈 후처리기 매커니즘을 통해 적용했다. 최소한 두 가지는 확인해야 한다.

1. 트랜잭션이 필요한 빈에 트랜잭션 부가기능이 적용됐는가(upgradeAllOrNoting() 테스트로 검증)
2. 클래스 필터가 제대로 동작해서 프록시 생성 대상을 선별하고 있는지 여부를 확인
   - 포인트컷 빈의 클래스 이름 패턴을 변경해서 testUserService 빈에 트랜잭션이 적용되지 않게 해보자.

트랜잭션 포인트컷 빈의 클래스 필터용 이름 패턴인 mappedClassName을 수정하고 upgradeAllOrNoting() 테스트가 실패하는지 확인하자.

```xml
<bean id="transactionPointcut" class="kang.onezero.tobyspring.user.service.NameMatchClassMethodPointcut">
    <!-- 클래스 이름 패턴 변경 -->
    <property name="mappedClassName" value="*NotServiceImpl" />
    <property name="mappedName" value="upgrade*" />
</bean>
```

### 포인트컷 표현식을 이용한 포인트컷

이번에는 좀 더 편리한 포인트컷 작성 방법을 알아보자.

스프링은 아주 간단하고 효과적인 방법으로 포인트컷의 클래스와 메소드를 선정하는 알고리즘을 작성할 수 있는 방법을 제공한다.

이를 포인트컷 표현식(pointcut expression)이라고 부른다.

#### 포인트컷 표현식

포인트컷 표현식을 지원하는 포인트컷을 적용하려면 AspectJExpressionPointcut 클래스를 사용하면 된다.

Pointcut 인터페이스를 구현하는 스프링의 포인트컷은 클래스 선정을 위한 클래스 필터와 메소드 선정을 위한 메소드 매처 두 가지를 각각 제공해야 했다.

하지만 AspectJExpressionPointcut은 클래스와 메소드의 선정 알고리즘을 포인트컷 표현식을 이용해 한 번에 지정할 수 있게 해준다.

학습 테스트를 만들어서 표현식의 사용 방법을 살펴보자.

- 포인트컷의 선정 후보가 될 여러 개의 메소드를 가진 클래스

```java
public class Target implements TargetInterface {
    @Override
    public void hello() {}

    @Override
    public void hello(String a) {}

    @Override
    public int minus(int a, int b) throws RuntimeException { return 0; }

    @Override
    public int plus(int a, int b) { return 0; }

    public void method() {}
}
```

- 여러 개의 클래스 선정 기능을 확인하기 위해 만든 클래스

```java
public class Bean {
    public void method() throws RuntimeException {}
}
```

#### 포인트컷 표현식 문법

AspectJ 포인트컷 표현식은 포인트컷 지시자를 이용해 작성한다. 대표적으로 사용되는 지시자는 execution()이다.

- execution() 지시자를 사용한 포인트컷 표현식의 문법구조

```
execution([접근제어자 패턴] 리턴타입패턴 [타입패턴.]이름패턴 (타입패턴 | "..", ...) [throws 예외패턴] )
```

- Target 클래스의 minus() 메소드만 선정해주는 포인트컷 표현식 검증 테스트

```java
public class PointcutExpressionTest {
    @Test
    public void methodSignaturePointcut() throws SecurityException, NoSuchMethodException {
        AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
        pointcut.setExpression("execution(public int " +
                "kang.onezero.tobyspring.learningtest.pointcut.Target.minus(int,int) " +
                "throws java.lang.RuntimeException)"); // Target 클래스 minus() 메소드 시그니처

        // Target.minus()
        // 클래스 필터와 메소드 매처를 가져와 각각 비교한다.
        assertThat(pointcut.getClassFilter().matches(Target.class) &&
                pointcut.getMethodMatcher().matches(
                        Target.class.getMethod("minus", int.class, int.class), null)).isTrue();

        // Target.plus()
        // 메소드 매처에서 실패
        assertThat(pointcut.getClassFilter().matches(Target.class) &&
                pointcut.getMethodMatcher().matches(
                        Target.class.getMethod("plus", int.class, int.class), null)).isFalse();

        // Bean.method()
        // 클래스 필터에서 실패
        assertThat(pointcut.getClassFilter().matches(Bean.class) &&
                pointcut.getMethodMatcher().matches(
                        Target.class.getMethod("method", int.class, int.class), null)).isFalse();
    }
}
```

**추가할 라이브러리: runtimeOnly 'org.aspectj:aspectjweaver:1.9.21'**

#### 포인트컷 표현식 테스트

포인트컷 표현식에서 필수가 아닌 '접근제어자 패턴', '클래스 타입 패턴', '예외 패턴'은 생략이 가능하다(대신 좀 더 느슨한 포인트컷이 된다).

```
execution(int minus(int, int))
```

리턴 값의 타입에 대한 제한을 없애고 싶다면 와일드카드를 사용하면 된다.

```
execution(* minus(int, int))
```

파라미터의 개수와 타입을 무시하려면 () 안에 ..를 넣어준다.

```
execution(* minus(..))
```

모든 메소드를 다 허용하는 포인트컷이 필요하다면 메소드 이름도 와일드카드로 바꾸자.

```
execution(* *(..))
```

다양한 활용 방법을 보기 위해 테스트를 보충하자.

- 포인트컷과 메소드를 비교해주는 테스트 헬퍼 메소드

```java
public void pointcutMatches(String expression, Boolean expected, Class<?> clazz,
                            String methodName, Class<?>... args) throws Exception {
    AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
    pointcut.setExpression(expression);

    assertThat(pointcut.getClassFilter().matches(clazz)
            && pointcut.getMethodMatcher().matches(clazz.getMethod(methodName, args), null)).isTrue();
}
```

- 타깃 클래스의 메소드 6개에 대해 포인트컷 선정 여부를 검사하는 헬퍼 메소드

```java
public void targetClassPointcutMatches(String expression, boolean... expected) throws Exception {
    pointcutMatches(expression, expected[0], Target.class, "hello");
    pointcutMatches(expression, expected[1], Target.class, "hello", String.class);
    pointcutMatches(expression, expected[2], Target.class, "plus", int.class, int.class);
    pointcutMatches(expression, expected[3], Target.class, "minus", int.class, int.class);
    pointcutMatches(expression, expected[4], Target.class, "method");
    pointcutMatches(expression, expected[5], Bean.class, "method");
}
```

- 포인트컷 표현식 테스트

```java
@Test
public void pointuct() throws Exception {
    targetClassPointcutMatches("execution(* *(..))", true, true, true, true, true, true);
    // 나머지는 생략
}
```

#### 포인트컷 표현식을 이용하는 포인트컷 적용

AspectJ 포인트컷 표현식은 메소드를 선정하는 데 편리하게 쓸 수 있다.

- AspectJ 포인트컷 표현식 스타일:
  - 메소드의 시그니처를 비교하는 execution()
  - 빈의 이름으로 비교하는 bean()
  - 특정 어노테이션이 적용된 것을 선정하는 @annotation()

이제 포인트컷 표현식을 사용하는 방법을 알았으니 적용해보자.

먼저 앞서 만든 transactionPointcut 빈을 제거고, 기존 포인트컷과 동일한 기준으로 메소드를 선정하는 알고리즘을 가진 포인트컷 표현식을 만들어보자.

```xml
<!-- ServiceImpl로 끝나고 메소드 이름은 upgrade로 시작하는 모든 클래스에 적용되는 표현식 -->
<bean id="transactionPointcut" class="org.springframework.aop.aspectj.AspectJExpressionPointcut">
    <property name="expression" value="execution(* *..*ServiceImpl.upgrade*(..))" />
</bean>
```

포인트컷 표현식을 사용하면 로직이 짧은 문자열에 담겨 코드와 설정이 단순해진다.

반면 문자열 표현식이므로 런타임 시점까지 문법의 검증이나 기능 확인이 되지 않는다.

포인트컷 표현식을 이용하는 포인트컷이 정확히 원하는 빈만 선정했는지 확인하는 일은 만만치 않다. 하지만 스프링 개발팀이 제공하는 지원툴을 사용하면 간단히 포인트컷이 선정한 빈을 한눈에 확인할 수 있다(VOL. 2 내용)

#### 타입 패턴과 클래스 이름 패턴

- 포인트컷 표현식 적용전에는 클래스 이름 패턴을 이용해 타깃 빈을 선정하는 포인트 컷 사용
- 적용할 클래스 이름이 ServiceImpl로 통일되는 단점
- 하지만 단순 클래스 이름 패턴과 포인트컷 표현식의 타입패턴은 중요한 차이점이 있다.
  - 포인트컷 표현식의 클래스 이름에 적용되는 패턴은 클래스 이름 패턴이 아니라 타입 패턴이다.
  - execution(\* *..*ServiceImpl.upgrade\*(..))는 TestUserService도 선정한다.
  - TestUserService의 슈퍼 클래스는 UserServiceImpl이기 때문이다.

### AOP란 무엇인가?

비즈니스 로직을 담은 UserService에 트랜잭션을 적용해온 과정을 정리해보자.

#### 트랜잭션 서비스 추상화

트랜잭션 경계설정 코드를 비즈니스 로직을 담은 코드에 넣으면서 특정 트랜잭션에 종속되는 코드가 돼버렸다.

그래서 트랜잭션 적용이라는 추상적인 작업 내용은 유지하면서 구체적인 구현 방법을 자유롭게 바꿀 수 있도록 서비스 추상화 기법을 적용했다.

트랜잭션 추상화란 결국 인터페이스와 DI를 통해 무엇을 하는지는 남기고, 그것을 어떻게 하는지는 분리한 것이다. 어떻게 할지는 더 이상 비즈니스 로직 코드에는 영향을 주지 않고 독립적으로 변경할 수 있게 됐다.

#### 프록시와 데코레이터 패턴

트랜잭션을 어떻게 다룰 것인가는 추상화를 통해 코드에서 제거했지만, 여전히 비즈니스 로직 코드에는 트랜잭션을 적용하고 있다는 사실이 드러나 있다.

그리고 트랜잭션은 대부분의 비즈니스 로직을 담은 메소드에 필요하고, 트랜잭션의 경계설정을 담당하는 코드의 특성 상 단순한 추상화와 메소드 추출 방법으로는 더 이상 제거할 방법이 없었다.

DI를 이용한 데코레이터 패턴 적용.

클라이언트가 인터페이스와 DI를 통해 비즈니스로직을 담은 클래스에 접근하게 하고, 데코레이터 패턴을 적용해 중간에 트랜잭션이라는 부가기능을 부여.

결국 비즈니스 로직 코드는 트랜잭션과 다른 코드로부터 자유로워졌고, 독립적으로 로직을 검증하는 고립된 테스트를 만들 수도 있게 됐다.

#### 다이내믹 프록시와 프록시 팩토리 빈

프록시를 이용하 비즈니스 로직 코드에서 트랜잭션 코드 제거 성공

허나 비즈니스 로직 인터페이스의 모든 메소드를 구현한 프록시 클래스를 만드는 작업이 큰 짐이 됐다. 또한 트랜잭션 기능이 필요하지 않은 메소드조차 구현해야 했다.

JDK 다이내믹 프록시 기술을 적용해 프록시 오브젝트를 런타임 시에 만들어줌 -> 인터페이스 구현 부담 사라짐, 허나 동일한 기능의 프록시를 여러 오브젝트에 적용할 경우 오브젝트 단위로 중복 발생하는 문제는 해결 못함

JDK 다이내믹 프록시와 같은 프록시 기술을 추상화한 스포링의 프록시 팩토리 빈을 이용해 다이내믹 프록시 생성 방법에 DI 도입. 내부적으로 템플릿/콜백 패턴을 활용하는 스프링의 프록시 팩토리 빈 덕분에 부가기능을 담은 어드바이스와 부가기능 선정 알고리즘을 담음 포인트컷은 프록시에서 분리되고, 여러 프록시에서 공유해서 사용 가능

#### 자동 프록시 생성 방법과 포인트 컷

트랜잭션 적용 대상이 되는 빈마다 일일이 프록시 팩토리 빈을 설정해줘야 하는 부담

스프링 컨테이너의 빈 후처리 기법을 활용해 컨테이너 초기화 시점에 자동으로 프록시를 만들어주는 방법 도입.

프록시 적용 대상을 일일이 지정하지 않고 패턴을 이용해 자동 선정되도록, 클래스 선정 기능을 담은 확장된 포인트컷 사용.

#### 부가기능의 모듈화

지금까지 관심사가 다른 코드를 객체지향 설계 원칙에 따라 분리했다.

하지만 트랜잭션 적용 코드는 기존 방법으로 간단하게 분리해서 독립된 모듈로 만들기 어려웠다.

트랜잭션과 같은 부가기능은 타깃이 존재해야만 의미가 있기에 독립적으로 모듈화하기 어렵다. 타깃과 긴밀하게 연결돼야 하기 때문이다.

많은 개발자는 여기저기 흩어져있는 부가기능을 독립적인 모듈로 만들기 위해 DI, 데코레이터 패턴, 다이내믹 프록시, 오브젝트 생성 후처리, 자동 프록시 생성, 포인트컷과 같은 기법을 적용했다.

덕분에 부가기능인 트랜잭션 경계설정 기능은 TransactionAdvice 이름으로 모듈화 되었고, 적용될 대상을 포인트컷으로 선정할 수 있게 되었다. 독립적으로 모듈화되어 있기 때문에 중복되지 않으며, 변경이 필요할 시 한 곳만 수정하면 된다.

#### AOP: 애스펙트 지향 프로그래밍

전통적인 객체지향 설계 방법으로는 독립적인 모듈화가 불가능한 트랜잭션 경계설정과 같은 부가기능

새로운 특성이 있다고 생각. 오브젝트와 다르게 특별한 이름으로 부름. 바로 aspect. 그 자체로 핵심 기능을 담고 있지는 않지만, 핵심기능에 부가되어 의미를 갖는 특별한 모듈.

애스펙트는 부가 기능을 정의한 어드바이스와, 적용 대상을 결정하는 포인트컷을 함께 갖고 있다.

결국 런타임 시에 부가기능 애스펙트는 자기가 필요한 위치에서 다이내믹하게 참여하게 될 것이다. 하지만 설계와 개발은 독립적인 관점으로 작성할 수 있다.

이렇게 애플리케이션에서 핵심적인 기능에서 부가적인 기능을 분리해서 애스펙트라는 독특한 모듈로 만들어 설계하고 개발하는 방법을 애스펙트 지향 프로그래밍(Aspect Oriented Programming)이라고 한다.

### AOP 적용기술

#### 프록시를 이용한 AOP

스프링은 IoC/DI 컨테이너, 다이내믹 프록시, 데코레이터 패턴, 프록시 패턴, 자동 프록시 생성 기법, 빈 오브젝트의 후처리 조작 기법 등의 다양한 기술을 조합해 AOP를 지원하고 있다. 그 중 핵심은 프록시를 이용했다는 것이다.

독립적으로 개발한 부가기능 모듈을 다양한 타깃 오브젝트의 메소드에 다이내믹하게 적용해주기 위해 가장 중요한 역할을 맡고 있는 게 바로 프록시다. 그래서 스프링 AOP는 프록시 방식의 AOP라고 할 수 있다.

#### 바이트코드 생성과 조작을 통한 AOP

프록시를 사용하지 않고 AOP를 적용하는 방법도 있다. AspectJ는 스프링처럼 다이내믹 프록시 방식을 사용하지 않는다.

AspectJ는 컴파일된 클래스 파일을 수정하거나, 바이트코드를 조작하여 타깃 오브젝트에 직접 부가기능을 넣어준다.

1. 바이트코드를 조작해서 타깃 오브젝트를 직접 수정하면 DI 컨테이너가 사용되지 않는 환경에서도 AOP를 적용할 수 있다.
2. 프록시 방식보다 훨씬 강력하고 유연한 AOP가 가능하다.
   - 오브젝트 생성, 필드 값의 조회와 조작, 스태틱 초기화 등 다양한 부가기능을 부여해줄 수 있다.
   - 허나 일반적인 경우 메소드 호출 시 적용되는 프록시 방식의 AOP로도 충분하다.

### AOP의 용어

- **타깃**: 부가기능을 부여할 대상.
- **어드바이스**: 타깃에게 제공할 부가기능을 담은 모듈
- **조인 포인트**: 어드바이스가 적용될 수 있는 위치. 스프링의 프록시 AOP에서 조인 포인트는 메소드의 실행 단계뿐이다.
- **포인트컷**: 어드바이스가 적용될 조인 포인트를 선별하는 작업 또는 그 기능을 정의한 모듈
- **프록시**: 클라이언트와 타깃 사이에 투명하게 존재하면서 부가기능을 제공하는 오브젝트. DI를 통해 타깃 대신 클라이언트에게 주입된다.
- **어드바이저**: 포인트컷과 어드바이스를 하나씩 갖고 있는 오브젝트. 스프링은 자동 프록시 생성기가 어드바이저를 AOP 작업의 정보로 활용한다(스프링에서만 사용되는 특별한 용어)
- **애스펙트**: AOP의 기본 모듈. 한 개 이상의 포인트컷과 어드바이스의 조합으로 만들어지며 보통 싱글톤 형태의 오브젝트로 존재한다.

### AOP 네임스페이스

스프링 AOP를 적용하기 위해 추가했던 어드바이저, 포인트컷, 자동 프록시 생성기 같은 빈들은 스프링 컨테이너에 의해 자동으로 인식돼서 특별한 작업을 위해 사용된다.

스프링의 프록시 방식 AOP를 적용하려면 최소한 네 가지 빈을 등록해야 한다.

- **자동 프록시 생성기**: 스프링의 DefaultAdvisorAutoProxyCreator 클래스를 빈으로 등록한다. 애플리케이션 컨텍스트가 빈 오브젝트를 생성하는 과정에서 빈 후처리기로 참여한다. 빈으로 등록된 어드바이저를 이용해서 프록시를 자동으로 생성한다.
- **어드바이스**: 부가기능을 구현한 클래스를 빈으로 등록한다.
- **포인트컷**: 스프링의 AspectJExpressionPointcut을 빈으로 등록하고 expression 프로퍼티에 포인트컷 표현식을 넣어준다.
- **어드바이저**: 스프링의 DefaultPointcutAdvisor 클래스를 빈으로 등록해 사용한다. 어드바이스와 포인트컷을 프로퍼티로 참조한다.

#### AOP 네임스페이스

스프링은 이렇게 AOP를 위해 기계적으로 적용하는 빈들을 간편한 방법으로 등록할 수 있다.

스프링은 AOP와 관련된 태그를 정의해둔 aop 스키마를 제공한다.

aop 스키마에 정의된 태그를 사용하려면 설정파일에 다음과 같은 aop 네임스페이스 선언을 추가해줘야 한다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop-3.0.xsd">
<!-- 생략 -->
</beans>
```

이제 aop 네임스페이스를 이용해 기존 AOP 관련 빈 설정을 변경해보자.

```xml
<aop:config>
    <aop:pointcut id="transactionPointcut" expression=""/>
    <aop:advisor advice-ref="transactionAdvice" pointcut-ref="transactionPointcut"/>
</aop:config>
```

<aop:config>, <aop:pointcut>, <aop:advisor> 세 가지 태그를 정의해두면 세 개의 빈이 자동으로 등록된다.

포인트컷, 어드바이저, 자동 포인트컷 생성기 같은 특별한 기능을 가진 빈들은 별도의 스키마에 정의된 전용 태그를 사용해 정의해주면 편리하다.

애플리케이션을 구상하는 빈과 컨테이너에 의해 사용되는 기반 기능을 지원하는 빈은 구분되는 것이 좋다.

#### 어드바이저 내장 포인트컷

AspectJ 포인트컷 표현식을 활용한 포인트컷은 스트링으로 된 표현식을 담은 expression 프로퍼티 하나만 설정해주면 사용할 수 있다. 또, 포인트컷은 어드바이저에 참조돼야만 사용된다. 그래서 aop 스키마의 전용 태그를 사용하는 경우, 굳이 포인트컷을 독립적인 태그로 두고 어드바이저 태그에서 참조하는 대신 어드바이저 태그와 결합하는 방법도 가능하다.

다음과 같이 포인트컷 표현식을 직접 <aop:advisor> 태그에 담아서 만들 수 있다.

```xml
<aop:config>
    <aop:advisor advice-ref="transactionAdvice" pointcut-ref="execution(* *..*ServiceImpl.upgrade*(..))"/>
</aop:config>
```

태그가 줄어 간결해졌다. 하지만 하나의 포인트컷을 여러 개의 어드바이저에서 공유하려고 할 때는 포인트컷을 독립적인 <aop:pointuct> 태그로 등록해야 한다.
