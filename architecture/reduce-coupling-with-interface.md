# 도메인 간 결합도를 낮추는 방법: 인터페이스

프로젝트에서 회원 가입을 할 경우 포인트 잔액(PointBalance)을 함께 생성해줘야 하는 요구사항이 추가되었다. 즉 Member 엔티티를 생성할 때 PointBalance 엔티티도 함께 생성해줘야 했다. 먼저 회원가입 로직이 어떻게 구성되어 있는지 확인해보자.

```kt
@Service
class MemberService(
    private val memberRepository: MemberRepository,
) {

    @Transactional
    fun signUp(newMember: NewMember) {
        val member = memberRepository.save(
            Member(
                email = newMember.email,
                password = newMember.password,
                nickname = newMember.nickname,
                role = newMember.role,
            )
        )
    }
}
```

간단하게 생각해보면 MemberService에 PointBalanceRepository를 추가하고 함께 생성해주면 될 것 같다.

```kt
@Service
class MemberService(
    private val memberRepository: MemberRepository,
    private val pointBalanceRepository: PointBalanceRepository,
) {

    @Transactional
    fun signUp(newMember: NewMember) {
        val member = memberRepository.save(
            Member(
                email = newMember.email,
                password = newMember.password,
                nickname = newMember.nickname,
                role = newMember.role,
            )
        )

        pointBalanceRepository.save(
            PointBalance(
                memberId = member.id,
            )
        )
    }
}
```

즉 Member 도메인이 PointBalance 도메인을 의존하게 되는 구조다. 이 경우 PointBalance가 변경될 경우 PointBalance뿐만 아니라 Member도 수정이 필요해진다.

나는 Member와 PointBalance의 관계에 대해 먼저 정의했다.

1. Member는 PointBalance보다 더 많은 곳에서 범용적으로 사용된다.
2. Member가 PointBalance를 의존할 경우 PointBalance가 변경될 때마다 Member도 영향을 받는다는 의미다.
3. 영향을 받은 Member가 변경되면 Member를 의존하는 수많은 도메인들도 영향을 받는다. 즉 변경이 전파된다.
4. 따라서 PointBalance가 Member를 의존해야 하고, Member는 PointBalance를 모르는 게 더 변경에 유연한 구조다.

앞서 본 코드처럼 MemberService가 PointBalance를 아는 구조에서, pointBalance에 member의 nickname을 기록해야 하는 요구사항이 추가된다면 어떻게 될까? PointBalance에 nickname 필드가 추가되면서 변경사항이 생기고, 이를 의존하는 MemberService에서도 nickname을 넣어줘야 한다. 즉 하나의 요구사항으로 두 곳을 수정하게 된다.

```kt
@Transactional
fun signUp(newMember: NewMember) {
    val member = memberRepository.save(
        Member(
            email = newMember.email,
            password = newMember.password,
            nickname = newMember.nickname,
            role = newMember.role,
        )
    )

    pointBalanceRepository.save(
        PointBalance(
            memberId = member.id,
            // +닉네임 추가
            nickname = member.nickname,
        )
    )
}
```

이처럼 덜 중요한 도메인을 변경할 때 더 중요한 도메인에 영향을 주는 것을 막으려면 PointBalance가 Member를 아는 구조가 되어야 한다. 그러기 위해서 인터페이스를 이용한 방법과 이벤트를 사용한 방법이 있는데, 필자는 다음과 같은 이유로 인터페이스를 선택했다.

1. 프로젝트의 규모가 작다(단일 서버).
2. PointBalance 생성은 반드시 되어야 함(한 트랜잭션으로 묶고 싶음).

MemberSignedUpHandler 인터페이스를 만들고, 회원가입할 때 다른 도메인이 수행해야 하는 작업이 있다면 이를 구현하도록 하였다.

```kt
fun interface MemberSignedUpHandler {
    fun onSignedUp(member: Member)
}
```

```kt
@Component
class PointBalanceInitializer(
    private val pointBalanceRepository: PointBalanceRepository,
) : MemberSignedUpHandler {

    override fun onSignedUp(member: Member) {
        pointBalanceRepository.save(
            PointBalance(
                memberId = member.id,
            )
        )
    }
}
```

```kt
@Service
class MemberService(
    private val memberRepository: MemberRepository,
    private val memberSignedUpHandlers: List<MemberSignedUpHandler>,
) {

    @Transactional
    fun signUp(newMember: NewMember) {
        val member = memberRepository.save(
            Member(
                email = newMember.email,
                password = newMember.password,
                nickname = newMember.nickname,
                role = newMember.role,
            )
        )
        memberSignedUpHandlers.forEach { it.onSignedUp(member) }
    }
}
```

이렇게 하면 PointBalance의 요구사항이 추가/변경되어도 Member는 PointBalance를 모르기 때문에 변경되지 않는다. 도메인의 의존 방향을 역전시킴으로써 변경이 전파되는 문제를 해결했다. 도메인 간 결합도를 낮추는 방법 중 이벤트를 활용하는 방법도 있는데 이는 다음에 다루도록 하겠다.