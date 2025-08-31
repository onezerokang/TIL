# 이펙티브 코틀린/6장 클래스 설계

## 아이템 36: 상속보다는 컴포지션을 사용하라

> 컴포지션: 객체를 프로퍼티로 갖고, 메서드를 호출하는 것

상속은 'is-a' 관계의 객체 계층 구조를 만들기 위해 설계되었다.

```kt
ArrayList is a List // ArrayList는 List다.
LinkedList is a List // LinkedList는 List다.
```

슈퍼클래스를 상속하는 모든 서브클래스는 슈퍼클래스로도 동작할 수 있어야 한다. 즉 슈퍼클래스의 모든 단위 테스트는 서브클래스로도 통과할 수 있어야 한다. 이런 명확한 관계일 때 상속을 활용하면 OOP의 특징인 다형성을 활용할 수 있다.

하지만 상속은 아래와 같은 단점을 갖고 있으므로 is-a 관계가 명확하지 않은데 단순하게 코드 추출 또는 재사용을 위해 상속을 사용하는 것은 좋지 않다.

- 하나의 부모만 상속 가능하기에 기능을 추가할 때 거대한 Base 클래스가 만들어지거나 복잡한 계층 구조로 이어질 수 있다.
- 필요 없는 기능까지 물려받아 불필요한 메서드가 생길 수 있다(ISP 위반)
- 동작 방식을 확인하려면 슈퍼 클래스르 계속 확인해야 한다.

### 1. 간단한 행위 재사용

예제: progress bar를 어떤 로직 처리 전에 출력하고, 처리 후에 숨기는 유사한 동작을 하는 두 개의 클래스가 있다.

```kt
class ProfileLoader {
  fun load() {
    // 프로그레스 바를 보여 줌
    // 프로파일을 읽어 들임
    // 프로그레스 바를 숨김
  }
}

class ImageLoader {
  fun load() {
    // 프로그레스 바를 보여 줌
    // 이미지를 읽어 들임
    // 프로그레스 바를 숨김
  }
}
```

많은 개발자가 슈퍼클래스를 만들어 공통되는 행위를 추출한다.

```kt
abstract class LoaderWithProgress {

  fun load() {
    // 프로그레스 바를 보여 줌
    innerLoad()
    // 프로그레스 바를 숨김
  }

  abstract fun innerLoad()
}

class ProfileLoader: LoaderWithProgress {

  override fun innerLoad() {
    // 프로파일을 읽어 들임
  }
}

class ImageLoader: LoaderWithProgress {

  override fun innerLoad() {
    // 이미지를 읽어 들임
  }
}
```

이를 컴포지션으로 구현한 코드는 아래와 같다.

```kt
class Progress {
  fun showProgress() { /* show progress */}
  fun hideProgress() { /* hide progress */}
}

class ProfileLoader {
  val progress = Progress()

  fun load() {
    progress.showProgress()
    // 프로파일을 읽어 들임
    progress.hideProgress()
  }
}

class ImageLoader {
  val progress = Progress()

  fun load() {
    progress.showProgress()
    // 이미지를 읽어 들임
    progress.hideProgress()
  }
}
```

두 코드를 비교했을 때 상속을 사용한 코드는 progress bar가 출력되고 사라진다는 것을 알기 위해서 슈퍼클래스를 읽어봐야 하지만 컴포지션을 사용한 코드는 ~Loader 클래스 내부에서 Progress를 갖고 있고 직접 호출하기에 코드의 실행 흐름을 예측하기 쉽다.

또한 컴포지션을 활용하면, 보다 유연하게 기능을 확장할 수 있다. 예를 들어 이미지를 읽어들이고 나서 경고창을 출력한다면 다음과 같은 형태로 컴포지션을 활용할 수 있다.

```kt
class ImageLoader {
  private val progress = Progress()
  private val finishedAlert = FinishedAlert()


  fun load() {
    progress.showProgress()
    // 이미지를 읽어 들임
    progress.hideProgress()
    finishedAlert.show()
  }
}
```

하나 이상의 클래스를 상속할 수 없기에 상속으로 이를 구현하려면 두 기능을 하나의 슈퍼클래스에 배치해야 한다. 또한 ImageLoader가 아닌 클래스는 경고창을 띄우면 안되기에 분기처리도 해야 한다.

```kt
abstract class InternetLoader(val showAlert: Boolean) {

  fun load() {
    // 프로그레스 바를 보여 줌
    innerLoad()
    // 프로그레스 바를 숨김
    if (showAlert) {
        // 경고창 출력
    }
  }

  abstract fun innerLoad()
}
```

위와 같은 방법은 굉장히 나쁜 해결 방법이다. 서브 클래스가 필요하지도 않은 기능을 갖고, 단순하게 이를 차단할 뿐이다. 상속은 슈퍼클래스의 모든 것을 가져오고 필요한 것만 가져올 수 없다.

### 2. 모든 것을 가져올 수밖에 없는 상속

상속은 슈퍼클래스의 모든 것을 가져온다. 이는 객체 계층 구조를 표현할 땐 좋지만, 일부 기능만 재사용하고 싶을 때는 적합하지 않다.

```class
abstract class Dog {
  open fun bark() {/*...*/}
  open fun sniff() {/*...*/}
}

// 냄새를 맡지 못하는 로봇 강아지를 만들고 싶음
class RobotDog: Dog() {
    override fun sniff() {
        throw Error("Operation not supported")
    }
}
```

- RobotDog는 필요 없는 sniff()를 강제로 가지게 됨 -> 인터페이스 분리 원칙 위반
- 슈퍼클래스의 동작을 깨뜨림 -> 리스코프 치환 원칙 위반

### 3. 캡슐화를 깨는 상속

상속은 슈퍼클래스의 내부 구현에 영향을 받기에, 내부 구현을 알아야 한다.

```kt
class CounterSet<T>: HashSet<T>() {
  val elementsAdded: Int = 0
    private set

  override fun add(element: T): Boolean {
    elementsAdded++
    return super.add(element)
  }

  override fun addAll(elements: Collection<T>): Boolean {
    elementsAdded += elements.size
    return super.addAll(elements)
  }
}
```

위 클래스는 문제 없어보이지만 잘 동작하지 않는다.

```kt
val counterList = CounterSet<String>()
counterList.addAll(listOf("A", "B", "C"))
print(counterList.elementAdded) // 6
```

HashSet의 addAll 내부에서 add를 사용하기에 addAll과 add에서 추가한 요소 개수를 중복해서 센다. addAll를 제거하면 문제를 해결할 수 있지만, 이런 방식은 위험하다. 자바 HashSet.addAll 최적화하려고 내부적으로 add를 호출하지 않는다면?

라이브러리의 구현이 변경되는 일은 자주 있다. 슈퍼 클래스의 구현 변경은 서브 클래스에 영향을 미친다. 컴포지션은 내부 구현이 아닌 외부에서 관찰되는 동작에만 의존하므로 비교적 안전한다.

```kt
class CounterSet<T> {
  private val innerSet = HashSet<T>()
  val elementsAdded: Int = 0
    private set

  override fun add(element: T): Boolean {
    elementsAdded++
    return innserSet.add(element)
  }

  override fun addAll(elements: Collection<T>): Boolean {
    elementsAdded += elements.size
    return innserSet.addAll(elements)
  }
}
```

- 단점: 다형성이 사라짐, CounterSet은 Set이 아님.
  - 유지하고 싶으면 위임 패턴 사용
  - 위임 패턴: 클래스가 인터페이스를 상속받게 하고, 포함한 객체의 메서드들을 활용해서, 인터페이스에서 정의한 메서드를 구현하는 패턴.
  - 이렇게 구현된 메서드를 포워딩 메서드라고 한다.

```kt
class CounterSet<T>: MutableSet<T> {
  private val innserSet = HashSet<T>()
  val elementsAdded: Int = 0
    private set

  override fun add(element: T): Boolean {
    elementsAdded++
    return innserSet.add(element)
  }

  override fun addAll(elements: Collection<T>): Boolean {
    elementsAdded += elements.size
    return innserSet.addAll(elements)
  }

  override val size: Int
    get() = innerSet.size

  override fun contains(element: T): Boolean =
    innerSet.contains(element)

  override fun containsAll(elements: Collection<T>): Boolean =
    innerSet.containsAll(elements)

  // 생략
}
```

- 구현해야 하는 포워딩 메서드 많음.
- 코틀린 위임 패턴 쉽게 구현 가능한 문법 제공
- 컴파일 시점에 포워딩 메서드들이 자동으로 만들어짐

```kt
class CounterSet<T>(
  private val innserSet: MutableSet<T> = mutableSetOf()
): MutableSet<T> by innerSet {
  val elementsAdded: Int = 0
    private set

  override fun add(element: T): Boolean {
    elementsAdded++
    return innserSet.add(element)
  }

  override fun addAll(elements: Collection<T>): Boolean {
    elementsAdded += elements.size
    return innserSet.addAll(elements)
  }
  // override 하지 않은 나머지 메서드들은 자동으로 포워딩 메서드가 생성됨
}
```

- 다형성 필요한데, 상속을 사용하고 싶지 않다면 위임 패턴을 사용할 수 있다.
- 근데 일반적으로 다형성이 그렇게까지 필요한 경우 잘 없기에 컴포지션을 사용하는 것이 낫다.

### 4. 오버라이딩 제한하기

만약 상속은 허용하되, 오버라이드할 수 있는 메서드를 제한하고 싶다면 open 키워드를 사용한다. open 클래스는 open 메서드만 오버라이드할 수 있다.

```kt
open class Parent {
    fun a() {}
    open fun b() {}
}

class Child: Parent() {
    override fun a() {} // 오류
    override fun b() {}
}
```

### 5. 정리

- 명확한 is-a 관계가 아니라면 컴포지션이 상속보다 안전하고 유연하다.
- 상속을 꼭 써야 하는 이유가 없고 로직 재사용 목적이라면 컴포지션을 사용하자.

# 아이템 37: 데이터 집합 표현에 data 한정자를 사용하라

데이터를 한번에 전달해야 할 때 data 한정자를 붙인 클래스를 사용한다.

```kotlin
data class Player(
    val id: Int,
    val name: String,
    val points: Int
)

val player = Player(0, "Gecko", 9999)
```

data 한정자를 붙이면 toString, equals와 hashCode, copy, componentN 함수가 자동으로 생성된다.

copy는 기본 생성자 프로퍼티가 같은 새로운 객체를 복제한다. 새로 만들어진 객체의 값은 이름이 있는 아규먼트를 활용해 변경할 수 있다. copy 메서드는 객체를 얕은 복사하지만 객체가 불변하다면 상관 없다.

```kotlin
val newObject = player.copy(name = "Thor")
print(newObject) // Player(id=0, name=Thor, points=9999)
```

componentN(component1, component2) 함수는 위치를 기반으로 객체를 해제할 수 있게 해준다.

```kotlin
val (id, name, points) = player
// 내부적으로 componentN 함수를 사용하는 다음과 같은 코드로 변환한다.
val id: Int = player.component1()
val name: String = player.component2()
val pts: Int = player.component3()
```

- 장점:
  - 변수 이름 마음대로 지정 가능.
  - List와 Map.Entry 등의 원하는 형태로도 객체 해제 가능

```kotlin
val visited = listOf("China", "Russia", "India")
val (first, second, third) = visited
println("$first $second $thrid") // China Russia India

val trip = mapOf(
    "China" to "Tianjin",
    "Russia" to "Petersburg",
    "India" to "Rishikesh"
)
for ((country, city) in trip) {
    println("We loved $city in $country")
}
```

- 단점:
  - 위치 잘못 지정 시 위험함.
  - 객체를 해제할 때는 주의해야 하므로 데이터 클래스의 기본 생성자에 붙어 있는 프로퍼티 이름을 쓰는 게 좋다.
    - 순서 잘못 지정하면 인텔리제이가 관련된 경고를 줄 것

참고:

- 값이 하나인 데이터 클래스는 해제하지 말자.
- 읽는 사람에게 혼동을 줄 수 있고, 특히 람다 표현식과 함께 활용될 때 문제가 된다.

```kotlin
data class User(val name: String)

fun main() {
  	val user = User("John")
    user.let { a -> println(a) } // User(name=John)
    // 이렇게 하지 말자.
    // 자바에선 문제가 없지만 코틀린에서는 객체가 분해된다.
    user.let { (a) -> println(a) } // John
}
```

### 튜플 대신 데이터 클래스 사용하기

- 코틀린의 튜플은 Serializable을 기반으로 만들어지며, toString을 사용할 수 있는 제네릭 데이터 클래스.

```kt
public data class Pair<out A, out B>(
    public val first: A,
    public val second: B
) : Serializable {

    public override fun toString(): String =
        "($first, $second)"
}

public data class Triple<out A, out B, out C>(
    public val first: A,
    public val second: B,
    public val third: C
) : Serializable {

    public override fun toString(): String =
        "($first, $second, $third)"
}
```

- 튜플은 데이터 클래스와 같은 역할을 하지만 훨씬 가독성이 나빴다. 튜플만 보고 어떤 타입을 나타내는지 예측할 수 없다.
- Pair과 Triple만 남고 나머지는 모두 사라졌다.
- 다음 경우를 제외하고 튜플 대신 data 클래스를 쓰는 것이 명확하고 가독성이 좋다.
  - 값에 간단한 이름을 붙일 때
  ```kt
    val (description, color) = when {
      degrees < 5 -> "cold" to Color.BLUE
      degrees < 23 -> "mild" to Color.YELLOW
      else -> "hot" to Color.RED
    }
  ```
  - 표준 라이브러리에서 볼 수 있는 것처럼 미리 알 수 없는 aggregate(집합)를 표현할 때
  ```kt
  val (odd, even) = numbers.partition { it % 2 == 1 }
  val map = mapOf(1 to "San Francisco", 2 to "Amsterdam")
  ```

## 아이템 38: 연산 또는 액션을 전달할 때 인터페이스 대신 함수 타입을 사용하라

### 함수 타입이란

코틀린에서 함수 타입(Function Type)은 함수도 하나의 값으로 다룰 수 있는 개념을 표현하기 위해 제공된다. 즉, 함수를 변수에 저장하거나, 다른 함수에 인자로 넘기거나, 함수의 반환값으로 돌려줄 수 있다.

### SAM

대부분의 프로그래밍 언어에는 함수 타입이라는 개념이 없다. 그래서 연산 또는 액션을 전달할 때 메서드가 하나만 있는 인터페이스를 활용한다. 이런 인터페이스를 SAM(Single-Abstract Method)라고 부른다. 예를 들어 다음 코드는 뷰를 클릭했을 때 발생하는 정보를 전달하는 SAM이다.

```kt
interface OnClick {
    fun clicked(view: View)
}
```

인자로 SAM을 받는다면, 이러한 인터페이스를 구현한 객체를 전달 받는다는 의미다.

```kt
fun setOnClickListener(listener: OnClick) {
    // ...
}

setOnClickListener(object : Onclick {
    override fun clicked(view: View) {
        // ...
    }
})
```

이런 코드를 함수 타입을 사용하는 코드로 변경하면, 더 많은 자유를 얻을 수 있다.

```kt
fun setOnClickListener(listener: (View) -> Unit) {
    //...
}
```

예를 들어 다음과 같은 방법으로 파라미터를 전달할 수 잇다.

```kt
// 람다 표현식 또는 익명 함수로 전달
setOnClickListener { /*...*/ }
setOnClickListener(fun(view) { /*...*/ })

// 함수 레퍼런스 또는 제한된 함수 레퍼런스로 전달
setOnClickListener(::println)
setOnClickListener(this::showUsers)

// 선언된 함수 타입을 구현한 객체로 전달
class ClickListener: (View)->Unit {
    override fun invoke(view: View) {
        // ...
    }
}
setOnClickListener(ClickListener())
```

일단 함수 타입에 대한 이해가 필요할 듯

### 언제 SAM을 사용해야 할까?

딱 한가지 경우에 SAM을 사용하는 것이 좋다. 코틀린이 아닌 다른 언어에서 사용할 클래스를 설계할 때.

자바에서는 인터페이스가 더 정확하다. 함수 타입으로 만들어진 클래스는 자바에서 타입 별칭과 IDE 지원등을 제대로 받을 수 없다.

마지막으로 다른 언어(자바 등)에서 코틀린의 함수 타입을 사용하려면, Unit을 명시적으로 리턴하는 함수가 필요하다.

자바에서 사용하기 위한 API를 설계할 때는 함수 타입보다 SAM을 사용하는 것이 합리적이다. 하지만 이외의 경우에는 함수 타입을 사용하는 게 좋다.

## 아이템 39: 태그 클래스보다는 클래스 계층을 사용하라

> 큰 규모의 프로젝트에서는 상수(constant) '모드'를 갖은 클래스들을 꽤 많을 수 있다.
> 이러한 상수 모드를 태그(tag)라고 부르며, 태그를 포함한 클래스를 태그 클래스(tagged class)라고 부른다.

태그 클래스는 서로 다른 책임을 한 클래스에 태그로 구분하여 넣기에 많은 문제를 내포하고 있다. 다음 예제는 테스트에 사용되는 클래스로서 어떤 값이 기준에 만족하는지 확인하기 위해 사용되는 클래스다.

```kt
class ValueMatcher<T> private constructor(
    private val value: T? = null,
    private val matcher: Matcher
) {

    fun match(value: T?) = when(matcher) {
        Matcher.EQUAL -> value == this.value
        Matcher.NOT_EQUAL -> value != this.value
        Matcher.LIST_EMPTY -> value is List<*> && value.isEmpty()
        Matcher.LIST_NOT_EMPTY -> value is List<*> && value.isNotEmpty()
    }

    enum class Matcher {
        EQUAL,
        NOT_EQUAL,
        LIST_EMPTY,
        LIST_NOT_EMPTY
    }

    companion object {
        fun <T> equal(value: T) =
            ValueMatcher<T>(value = value, matcher = Matcher.EQUAL)

        fun <T> notEqual(value: T) =
            ValueMatcher<T>(value = value, matcher = Matcher.NOT_EQUAL)

        fun <T> emptyList(value: T) =
            ValueMatcher<T>(value = value, matcher = Matcher.LIST_EMPTY)

        fun <T> notEmptyList(value: T) =
            ValueMatcher<T>(value = value, matcher = Matcher.LIST_NOT_EMPTY)
    }
}
```

- 단점
  - 한 클래스에 여러 모드를 처리하기 위한 boilerplate가 추가된다.
  - 여러 목적으로 사용해야 하므로 프로퍼티가 일관적이지 않게 사용될 수 있으며, 더 많은 프로퍼티가 필요하다.
    - 예를 들어 위의 예제에서 value는 모드가 LIST_EMPTY일 때, LIST_NOT_EMPTY일 때 아예 사용되지 않는다.
  - 요소가 여러 목적을 가지고, 요소를 여러 방법으로 설정할 수 있는 경우엥는 상태의 일관성과 정확성을 지키기 어렵다.
  - 팩토리 메서드를 사용해야 하는 경우가 많다. 그렇지 않으면 객체가 제대로 생성되었는지 확인하는 것 자체가 어렵다.

코틀린은 태그 클래스보다 sealed 클래스를 많이 사용한다. 한 클래스에 여러 모드를 만드는 대신에, 각각의 모드를 여러 클래스로 만들고 타입 시스템과 다형성을 활용하는 것이다.

```kt
sealed class ValueMatcher<T> {
    abstract fun match(value: T): Boolean

    class Equal<T>(val value: T) : ValueMatcher<T>() {
        override fun match(value: T): Boolean =
            value == this.value
    }

    class NotEqual<T>(val value: T) : ValueMatcher<T>() {
        override fun match(value: T): Boolean =
            value != this.value
    }

    class EmptyList<T>(val value: T) : ValueMatcher<T>() {
        override fun match(value: T): Boolean =
            value is List<*> && value.isEmpty()
    }

    class Equal<T>(val value: T) : ValueMatcher<T>() {
        override fun match(value: T): Boolean =
            value is List<*> && value.isNotEmpty()
    }
}
```

- 책임이 분산되므로 훨씬 깔끔하다. 각각의 객체들은 자신에게 필요한 데이터만 있으면서, 적절한 파라미터만 갖는다.

### sealed 한정자

sealed 한정자 대신 abstract 한정자를 사용해도 되지만, sealed는 외부 파일에서 서브클래스를 만드는 행위 자체를 모두 제한한다. 외부에서 서브클래스를 만들 수 없으므로, 타입이 추가되지 않을 거라는 게 보장된다. 따라서 when을 만들 때 else 브랜치를 만들 필요가 없다.

### 태그 클래스와 상태 파턴의 차이

태그 클래스와 상태 패턴(state pattern)을 혼동하면 안된다. 상태 패턴은 객체의 내부가 변화할 때, 객체의 동작이 변하는 소프트웨어 디자인이다.

## 아이템 40: equals의 규약을 지켜라

- 코틀린의 Any에는 다음과 같이 잘 설정된 규약을 갖은 메서드들이 있다.
  - equals
  - hashCode
  - toString
- 수 많은 객체와 함수들이 이 규약에 의존하고 있으므로, 규약을 위반하면 일부 객체 또는 기능이 제대로 동작X
- 잘 알아야 한다.

### 동등성

- 코틀린의 두 가지 종류의 동등성(equality)
  - 구조적 동등성(structural equality): equals 메서드와 이를 기반으로 만들어진 == 연산자로 확인하는 동등성
  - a가 nullable이 아니라면 a == b는 a.equals(b)로 변환되고, a가 nullable이라면 a?.equals(b) ?: (b === null)로 변환된다.
  - 레퍼런스적 동등성(referential equality): === 연산자로 확인하는 동등성. 두 피연산자가 같은 객체를 가리키면 true를 반환한다.
- equals는 모든 클래스의 슈퍼클래스인 Any에 구현되어 있으므로, 모든 객체에서 사용 가능하다.
  - 다만 다른 타입의 두 객체를 비교하는 것은 허용되지 않는다.

### equals가 필요한 이유

- Any 클래스에 구현된 equals 메서드는 디폴트로 ===처럼 두 인스턴스가 완전히 같은 객체인지 비교
- 이런 동작은 DB 연결, 리포지토리, 스레드 등의 활동 요소(active element)를 활용할 때 굉장히 유용하다.

```kotlin
class Name(val name: String)

val name1 = Name("Marcin")
val name2 = Name("Marcin")
val name1Ref = name1

name1 == name1 // true
name1 == name2 // false
name1 == name1Ref // true

name1 === name1 // true
name1 === name2 // false
name1 === name1Ref // true
```

- 객체의 데이터 값이 같으면 같은 객체로 봐야 하는 경우도 있다.
- data를 붙이면 이와 같은 동등성을 보장한다.
- 데이터 클래스는 내부에 어떤 값을 갖는지가 중요하므로 이와 같이 동작하는 게 좋다.
- 데이터 클래스의 동등성은 모든 프로퍼티가 아니라 일부 프로퍼티만 비교해야 할 때도 유용하다.
  - 간단한 예로, 날짜와 시간을 표현하는 객체를 살펴보자.

```kotlin
class DateTime(
    private val millis: Long = 0L,
    private var timeZone: TimeZone? = null
) {
    private var asStringCache = ""
    private var changed = false

    override fun equals(other: Any?): Boolean {
        return other is DateTime &&
                other.millis == millis &&
                other.timeZone == timeZone
    }
}
```

다음과 같은 data 한정자를 사용해도 같은 결과를 낼 수 있다.

```kotlin
data class DateTime(
    private val millis: Long = 0L,
    private var timeZone: TimeZone? = null
) {
    private var asStringCache = ""
    private var changed = false
}
```

- 기본 생성자에 선언되지 않은 프로퍼티는 copy로 복사되지 않는다.
- data 한정자를 기반으로 동등성의 동작을 조작할 수 있으므로, 일반적으로 코틀린에서는 equals를 직접 구현할 필요가 없다.
- 다만 상황에 따라 직접 구현할 때도 있음.
  - 기본적으로 제공되는 동작과 다른 동작을 해야할 때
  - 일부 프로퍼티만 비교할 때
  - data 한정자를 붙이는 것을 원하지 않거나, 비교해야 하는 프로퍼티가 기본 생성자에 없는 경우

### equals의 규약

- 반사적 동작: x가 null이 아니면 x.equals(x)는 true
- 대칭적 동작: x와 y가 null이 아니라면 x.equals(y)는 y.equals(x)와 같은 결과
- 연속적 동작: x, y, z가 null이 아닌 값이고 x.equals(y), y.equals(z)가 true라면 x.equals(z)도 true여야 한다.
- 일관적 동작: x, y가 null이 아니라면 x.equals(y)는 여러 번 실행하더라도 항상 같은 값을 리턴해야 한다.
- 널과 관련된 동작: x가 null이 아니라면 x.equals(null)은 항상 false여야 한다.
- 자세한 예제코드는 일단 생략

### URL과 관련된 equals 문제

- equals를 잘못 설계한 예로는 java.net.URL이 있다. URL 객체 2개를 비교하면 동일한 IP 주소로 해석될 때는 true, 아닐 때는 false가 나온다.
- 문제는 이 결과가 네트워크 상태에 따라서 달라진다는 것이다.

```kotlin
import java.net.URL

fun main() {
    val enWiki = URL("https://en.wikipedia.org/")
    val wiki = URL("https://wikipedia.org/")
    println(enWiki == wiki)
}
```

- 일반적인 상황에서느 두 주소가 같은 IP이므로 true
- 인터넷 연결이 끊겨있으면 false
- 동등성이 네트워크 상태에 의존한다는 것은 잘못됐다.
  - 동작이 일관되지 않다. 네트워크 상태, 설정에 따라 결과가 바뀐다.
  - 일반적으로 equals와 hashCode 처리는 빠를 거라 예상하지만, 네트워크 처리는 굉장히 느리다.
    - 또한 안드로이드 등과 같은 일부 플랫폼에서는 기본 쓰레드에서 네트워크 작업이 금지된다.
    - 이런 환경에서는 URL을 set에 추가하는 기본적인 조작도 쓰레드를 나누어서 해야 한다.
  - 동작 자체에 문제가 있다. 동일한 IP 주소를 갖는 경우 동일한 콘텐츠를 나타내는 것이 아니다.
    - virtual hosting을 사용한다면, 관련 없는 사이트가 같은 IP를 공유할 수 있다.
- 안드로이드는 Android 4.0부터 이런 내용이 수정되었다.
- 코틀린/JVM은 java.net.URL이 아니라 java.net.URI를 사용해서 이런 문제를 해결한다.

### equals 구현하기

- 특별한 이유가 없는 한 직접 구현 ㄴㄴ
  - 기존적으로 제공되는 것을 쓰거나 데이터 클래스로 만들어 사용
  - 그럼에도 직접 만들어야 한다면 반사적, 대칭적, 연속적, 일관적 동작하는지 확인
  - 그리고 이런 클래스는 final로 만드는게 좋다.
  - 서브클래스에서 equals가 작동하는 방식을 변경하면 안된다.
  - 상속을 지원하면서도 완벽한 사용자 정의 equals 함수를 만드는 것은 거의 불가능에 가깝다.

## 아이템 42 compareTo의 규약을 지켜라

- Any 클래스에 있는 메서드가 아니다.
- 수학적인 부등식으로 변환되는 연산자.

```kotlin
obj1 > obj2 // obj1.compareTo(obj2) > 0으로 바뀐다.
obj1 < obj2 // obj1.compareTo(obj2) < 0으로 바뀐다.
obj1 >= obj2 // obj1.compareTo(obj2) >= 0으로 바뀐다.
obj1 <= obj2 // obj1.compareTo(obj2) <= 0으로 바뀐다.
```

- 참고로 compareTo 메서드는 Comparable<T> 인터페이스에도 있다.
- 어떤 객체가 이 인터페이스를 구현하거나 compareTo라는 연선자 메서드를 갖고 있으면 해당 객체가 어떤 순서를 갖고 있으므로 비교할 수 있다는 것이다.
- 다음고 같이 동작해야 한다.
  - 비대칭적 동작:
  - 연속성 동작:
  - 코넥스적 동작:

### compareTo를 따로 정의해야 할까?

- 거의 없음.
- 일반적으로 어떤 프로퍼티 하나를 기반으로 순서를 적용하는 것으로 충분함.

```kotlin
class User(val name: String, val surname: String)
val names = listOf<User> { /*...*/ }

val sorted = names.sortedBy { it.surname }
```

- 여러 프로퍼티를 기반으로 정렬해야 한다면 sortedWith 함수를 사용하면 된다.
  - 사용법
    - compareBy를 활용해서 comparator를 만들어 사용한다.

```kotlin
val sorted = names.sortedWith(compareBy({ it.surname }, { it.name }))
```

- 설명 생략(페이지 참고)

### compareTo 구현하기

compareTo를 구현할 때 유용하게 사용할 수 있는 톱레벨 함수

- 단순히 두 값을 비교하기만 한다면 compareValues 함수를 유용하게 활용 가능
- 더 많은 값을 비교하거나, selector를 활용해서 비교하고 싶다면 compareValuesBy

## 아이템 43: API의 필수적이지 않는 부분을 확장 함수로 추출하라

> 확장 함수(Extension Function): 기존에 정의된 클래스의 소스 코드를 수정하지 않고 새로운 함수를 추가할 수 있는 기능

클래스의 메서드를 정의할 때는 메서드를 멤버로 정의할 것인지 아니면 확장 함수로 정의할 것인지 결정해야 한다.

```kt
// 멤버로 메서드 정의
class Workshop(/*...*/) {
    //...

    fun makeEvent(data: DateTime): Event = //...

    val permalink
        get() = "workshop/$name"
}

// 확장 함수로 메서드 정의
class Workshop(/*...*/) {
    //...
}

fun Workshop.makeEvent(data: DateTime): Event = //...

val Workshop.permalink
    get() = "workshop/$name"
```

두 가지 방법은 호출하는 방법도 비슷하고, 리플렉션으로 레퍼런싱하는 방법도 비슷하다.

```kt
fun useWorkshop(workShop: Workshop) {
    val event = workshop.makeEvent(date)
    val permalink = workshop.permalink

    val makeEventRef = Workshop::makeEvent
    val permalinkPropRef = Workshop::permalink
}
```

둘 다 장단점이 있으니, 상황에 맞게 사용해야 한다.

멤버와 확장의 가장 큰 차이점은 확장은 따로 import한 후 사용해야 한다는 것이다.

또 다른 차이점은 확장은 가상(virtual)이 아니다. 즉, 파생 클래스에서 오버라이드할 수 없다. 확장 함수는 컴파일 시점에 정적으로 선택된다. 따라서 확장 함수는 가상 멤버 함수와 다르게 동작한다. 상속을 목적으로 설계된 함수는 확장 함수로 만들면 안된다.

```kt
open class C
class D: C()
fun C.foo = "c"
fun D.foo = "d"

fun main() {
    val d = D()
    print(d.foo()) // d
    val c: C = d
    print(c.foo()) // c

    print(D().foo()) // d
    print((D() as C).foo()) // c
}
```

이러한 차이는 확장 함수가 첫 번째 아규먼트로 리시버가 들어가는 일반 함수로 컴파일 되기 때문이다.

```kt
fun foo(')
```

### 정리

- 확장 함수는 import해야 한다.
- 확장 함수는 virtual이 아니다.
- 멤버는 높은 우선 순위를 갖는다.
- 확장 함수는 클래스 위가 아니라 타입 위에 만들어진다.
- 확장 함수는 클래스 레퍼런스에 나오지 않는다.

정리하면, 확장 함수는 더 많은 유연성과 자유를 준다. 확장 함수는 상속, 어노테이션 처리 등을 지원하지 않고, 클래스 내부에 없으므로 약간 혼동을 줄 수 있다. API의 필수적인 부분은 멤버로 두는 것이 좋지만 필수적이지 않은 부분은 확장 함수로 만드는 것이 여러모로 좋다.

## 아이템 44: 멤버 확장 함수의 사용을 피하라

어떤 클래스에 대한 확장 함수를 정의할 때, 이를 멤버로 추가하는 것은 좋지 않다. 확장 함수는 첫 번째 인자로 리시버를 받는 단순한 일반 함수로 컴파일된다.

```kt
// 확장 함수 정의
fun String.isPhoneNumber(): Boolean =
    length == 7 && all { it.isDigit() }

// 컴파일
fun isPhoneNumber('$this': String): Boolean =
    '$this'.length == 7 && '$this'.all { it.isDigit() }
```

이렇게 단순하게 변환되는 것이므로, 확장 함수를 클래스 멤버로 정의할 수도 있고, 인터페이스 내부에도 정의할 수 있다.

```kt
interface PhoneBook {
    fun String.isPhoneNumber(): Boolean
}

class Fizz: PhoneBook {
    override fun String.isPhoneNumber(): Boolean =
        length == 7 && all { it.isDigit() }
}
```

이런 코드가 가능하지만, DSL을 만들 때를 제외하면 사용하지 마라. 특히 가시성 제한을 위해 확장 함수를 멤버로 정의하는 것은 좋지 않다.

```kt
// 나쁜 습관. 이렇게 하자 말라
class PhoneBookIncorrect {
    //...

    fun String.isPhoneNumber(): Boolean =
        length == 7 && all { it.isDigit() }
}
```

한가지 큰 이유는 가시성을 제한하지 못함. 이는 단순하게 확장 함수를 사용하는 형태를 어렵게 만들 뿐이다. 이러한 확장 함수를 사용하려면 다음과 같이 사용해야 한다.

```kt
PhoneBookIncorrect().apply { "1234567890".test() }
```

확장 함수의 가시성을 제한하고 싶다면, 멤버로 만들지말고, 가시성 한정자를 붙여줘라.

```kt
class PhoneBookIncorrect {
    //...
}

private fun String.isPhoneNumber(): Boolean =
        length == 7 && all { it.isDigit() }
```

멤버 확장을 피해야 하는 몇 가지 타당한 이유를 정리해보자면 다음과 같다.

- 레퍼런스를 지원하지 않는다.

```kt
val ref = String::isPhoneNumber
val str = "1234567890"
val boundedRef = str::isPhoneNumber

val refX = PhoneBookIncorrect::isPhoneNumber // 오류
val book = PhoneBookIncorrect()
val boundedRefX = book::isPhoneNumber // 오류
```

- 암묵적 접근을 할 때 두 리시버 중에 어떤 리시버가 선택될지 혼동된다.

```kt
class A {
    val a = 10
}

class B {
    val a = 20
    val b = 30

    fun A.test() = a + b // 40일까요? 50일까요?
}
```

- 확장 함수가 외부에 있는 다른 클래스를 리시버로 받을 때, 해당 함수가 어떤 동작을 하는지 명확하지 않다.

```kt
class A {
    //...
}

class B {
    //...

    fun A.update() = ... // A와 B중 어떤 것을 업데이트할까요?
}
```

- 경험이 적은 개발자의 경우 확장 함수를 보면 직관적이지 않거나, 심지어 보기만 해도 겁먹을 수도 있다.

정리: 멤버 확장 함수를 사용하는 것이 의미 있다면 사용해도 된다. 하지만 일반적으로 그 단점을 인지하고, 사용하지 않는 것이 좋다. 가시성을 제한하려면, 가시성관 관련된 한정자를 사용해라. 클래스 내부에 확장 함수를 배치한다고, 외부에서 해당 함수를 사용하지 못하게 제한되는 것이 아니다.
