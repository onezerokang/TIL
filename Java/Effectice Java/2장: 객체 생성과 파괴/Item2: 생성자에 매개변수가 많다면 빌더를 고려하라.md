# Item2: 생성자에 매개변수가 많다면 빌더를 고려하라

정적 팩터리 메서드와 생성자의 제약 = 선택적 매개변수가 많을 때 적절히 대응하기 어려움

ex. 식품 포장의 영양정보를 표현하는 클래스. 20개가 넘는 선택 항목으로 이루어진다. 그런데 이 제품중 선택항목 중 대다수의 값이 그냥 0이다.

프로그래머는 이럴 때 점층적 생성자 패턴(telescoping constructor pattern)을 즐겨 쓴다.

```java
public class NutritionFacts {
    private final int servingSize; // 필수
    private final int servings; // 필수
    private final int calories; // 선택
    private final int fat; // 선택
    private final int sodium; // 선택
    private final int carbohydrate; // 선택

    public NutritionFacts(int servingSize, int servings) {
        this(servingSize, servings, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories) {
        this(servingSize, servings, calories, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat) {
        this(servingSize, servings, calories, fat, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat, int sodium) {
        this(servingSize, servings, calories, fat, sodium, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat, int sodium, int carbohydrate) {
        this.servingSize = servingSize;
        this.servings = servings;
        this.calories = calories;
        this.fat = fat;
        this.sodium = sodium;
        this.carbohydrate = carbohydrate;
    }
}
```

문제는 매개변수가 많아지면 클라이언트 코드를 작성하기 어렵거나 읽기 어렵다. 각 값의 의미가 무엇인지 헷갈릴 것이고, 매개변수가 몇 개인지 주의해서 세어 보아야 한다. 타입이 같은 매개변수가 연달아 늘어서 있으면 차직 어려운 버그로 이어질 수 있다.

두번째 대안: JavaBeans pattern

매개변수가 없는 생성자로 객체를 만든 후, setter 메서드를 호출해 매개변수 값을 설정하는 방식

```java
public class NutritionFacts {
    // 기본값이 있다면 기본값으로 초기화
    private int servingSize = -1; // 필수; 기본값 없음
    private int servings = -1; // 필수; 기본값 없음
    private int calories = 0;
    private int fat = 0;
    private int sodium = 0;
    private int carbohydrate = 0;

    public NutritionFacts() {
    }

    public void setServingSize(int val) {
        this.servingSize = val;
    }

    public void setServings(int val) {
        this.servings = val;
    }

    public void setCalories(int val) {
        this.calories = val;
    }

    public void setFat(int val) {
        this.fat = val;
    }

    public void setSodium(int val) {
        this.sodium = val;
    }

    public void setCarbohydrate(int val) {
        this.carbohydrate = val;
    }
}
```

장점: 인스턴스 만들기 쉬워지고, 매개변수 헷갈리지 않음

```java
NutritionFacts coke = new NutritionFacts();
coke.setServingSize(240);
coke.setServings(8);
coke.setCalories(180);
coke.setSodium(35);
coke.setCarbohydrate(27);
```

심각한 단점: 객체 하나 만들려면 여러 메서드 호추랳야 하고, 객체가 완전히 생성되기 전까지는 일관성(consistency)이 무너진 상태에 놓임. 일관성이 무너지는 문제 때문에 자바빈즈 패턴에서는 클래스를 불변으로 만들 수 없으며, 스레드 안정성을 얻으려면 프로그래머가 추가 작업을 해줘야 함.

세번째 대안: 점층적 생성자 패턴의 안정성과 자바빈즈 패턴의 가독성을 겸비한 빌더 패턴

클라이언트는 필용한 객체를 직접 만드는 대신, 필수 매개변수만으로 생성자(혹은 정적 퍁ㄱ터리)를 호출해 빌더 객체를 얻는다. 그 다음 빌더 객체가 제공하는 일종의 세터 메서드들로 원하는 매개변수 설정. 마지막으로 매개변수가 없는 build 메서드를 호출해 필요한 객체를 얻는다.

```java
public class NutritionFacts {
    private final int servingSize;
    private final int servings;
    private final int calories;
    private final int fat;
    private final int sodium;
    private final int carbohydrate;

    public static class Builder {
        // 필수 매개변수
        private final int servingSize;
        private final int servings;

        // 선택 매개변수 - 기본값으로 초기화
        private int calories = 0;
        private int fat = 0;
        private int sodium = 0;
        private int carbohydrate = 0;

        public Builder(int servingSize, int servings) {
            this.servingSize = servingSize;
            this.servings = servings;
        }

        public Builder calories(int val) {
            calories = val;
            return this;
        }

        public Builder fat(int val) {
            fat = val;
            return this;
        }

        public Builder sodium(int val) {
            sodium = val;
            return this;
        }

        public Builder carbohydrate(int val) {
            carbohydrate = val;
            return this;
        }

        public NutritionFacts build() {
            return new NutritionFacts(this);
        }
    }

    private NutritionFacts(Builder builder) {
        servingSize = builder.servingSize;
        servings = builder.servings;
        calories = builder.calories;
        fat = builder.fat;
        sodium = builder.sodium;
        carbohydrate = builder.carbohydrate;
    }
}
```

```java
NutritionFacts coke = new NutritionFacts.Builder(240, 8)
        .calories(100).sodium(35).carbohydrate(27).build();
```

NutritionFacts 클래스는 불변이며, 모든 매개변수의 기본값들을 한 곳에 모아뒀다. 빌더의 세터 메서드들은 빌더 자신을 반환하기 때문에 연쇄적으로 호출할 수 있다.이런 방식을 플루언트 API 혹은 메서드 체이닝이라고 한다.

빌더 패턴은 파이썬과 스칼라에 있는 명명된 선택적 매개변수(named optional parameters)를 흉내낸 것이다.

**빌더 패턴은 계층적으로 설계뙨 클래스와 함께 쓰기 좋다(해당 부분은 나중에 내용 보충)**

빌더 패턴의 단점: 객체를 만들려면 그에 앞서 빌더부터 만들어야 함.점층적 생성자 패턴보다 코드가 장황함. 매개변수가 4개 이상은 되어야 값어치를 한다.

하지만 API는 시간이 지날수록 매개변수가 많아지는 경향이 있다. 생성자나 정적 팩터리 바잇ㄱ으로 시작하다 매개변수가 많아지면 빌더 패턴으로 전환해도 되지만, 이전에 만든 생성자와 정적 팩터리가 도드라져 보일 것. 차라리 빌더로 시작하는 게 나을 만두
