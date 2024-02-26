# Item1: 생성자 대신 정적 팩터리 메서드를 고려하라

흠... ErrorResponse를 왜 정적 팩터리 메서드로 만들어야 했을까

```java
@Getter
@RequiredArgsConstructor
@AllArgsConstructor
public class ErrorResponse {
    private final int httpStatus;
    private final String message;
    private final String errorCode;

    @JsonInclude(JsonInclude.Include.NON_EMPTY)
    private List<ValidationError> errors;

    @Getter
    @Builder
    @RequiredArgsConstructor
    public static class ValidationError {
        private final String field;
        private final String message;

        public static ValidationError of(final FieldError fieldError) {
            return ValidationError.builder()
                    .field(fieldError.getField())
                    .message(fieldError.getDefaultMessage())
                    .build();
        }
    }

    public static ErrorResponse of(int httpStatus, String message, String errorCode) {
        return new ErrorResponse(httpStatus, message, errorCode);
    }
}

@ExceptionHandler(ApiException.class)
public ResponseEntity<ErrorResponse> handleApiException(ApiException e) {
    return ResponseEntity
    .status(e.getHttpStatus())
    .body(new ErrorResponse(e.getHttpStatus().value(), e.getMessage(), e.getErrorCode()));
}
```

클라이언트가 클래스의 인스턴스를 얻는 방법은 public 생성자를 사용하는 방식과 정적 팩터리 메서드(static factory method)를 사용하는 방식이 있다(팩터리 매서드는 인스턴스를 반환하는 메서드를 의미한다).

예를 들어 박싱 클래스인 Boolean은 기본 타입인 boolean을 받아 Boolean 객체 참조로 변환해준다.

```java
public static Boolean valudOf(boolean b) {
    return b ? Boolean.TRUE : Boolean.FALSE;
}
```

클래스는 public 생성자 대신 정적 팩터리 메서드를 제공할 수 있다. 이의 장단점은 다음과 같다.

- **장점**:
  1. 이름을 가질 수 있다. 생성자에 넘기는 매개변수와 생성자 자체만으로는 반환될 객체의 특성을 제대로 설명하지 못한다. 반면 정적 팩터리 메서드는 이름만 잘 지으면 반환될 객체의 특성을 쉽게 묘사할 수 있다.
  2. 호출될 때마다 인스턴스를 새로 생성하지는 않아도 된다.
  3. 반환 타입의 서브 타입 객체를 반환할 수 있는 능력이 있다. 반환할 객체의 클래스를 자유롭게 선택할 수 있는 엄청난 유연성. 구현 클래스를 공개하지 않고도 그 객체를 반환할 수 있어 API를 작게 유지할 수 있다. 이는 인터페이스를 정적 팩터리 메서드의 반환 타입으로 사용하는 인터페이스 기반 프레임워크(아이템 20)을 만드는 핵심 기술이기도 하다.
  4. 네 번째, 입력 매개변수에 따라 매번 다른 클래스의 객체를 반환할 수 있다. 반환 타입의 서브 타입이기만 하면 어떤 클래스의 객체를 반환하든 상관 없다.
  5. 정적 팩터리 메서드를 작성하는 시점에는 반환할 객체의 클래스가 존재하지 않아도 된다. 이런 유연함은 서비스 제공자 프레임워크(service provider framework)를 만드는 근간이 된다. 대표적으로 JDBC가 있다. 서비즈 제공자 프레임워크에서 제공자는 서비스의 구현체다. 그리소 이 구현체들을 클라이언트에 제공하는 역할을 프레임워크가 통제하여, 클라이언트를 구현체로부터 분리해준다.
- **단점**:

  1. 상속을 하라면 public 이나 protected 생성자가 필요하니 정적 팩터리 메서드만 제공하면 하위 클래스를 만들 수가 없다. 어찌보면 상속보다 컴포지션을 사용하도록 유도하고 불변타입으로 만들려면 이 제약을 지켜야 한다는 점에서 오히려 장점일만두 2.정적 팩터리 메서드는 프로그래머가 찾기 어렵다. 생성자처럼 API 설명에 명확히 드러나지 않아 사용자는 정적 팩터리 메서드 방식 클래스를 인스턴스화 할 방법을 알아내야 한다. 그래서 문서 잘 써야함 ㅅㄱ. 다음은 자주 쓰는 명명 방식

  - from: 매개 변수를 하나 받아서 해당 타입의 인스턴스를 반환하는 형변환 메서드.
  - of: 여러 매개변수를 받아 적합한 타입의 인스턴스를 반환하는 집계 메서드.
  - valueOf: from과 of의 더 자세한 버전
  - instance 혹은 getInstance: 매개변수를 받는다면 매개변수로 명싱한 인스턴스를 반환하지만, 같은 인스턴스임을 보장하지 않는다.
  - create 혹은 newInstance: instance, getInstance와 같지만, 매번 새로운 인스턴스를 생성해 반환함을 보장한다.
  - getType: getInstance와 같으나, 생성한 클래스가 인ㄴ 다른 클래스에 팩터리 메서드를 정의할 때 쓴다.
