# BigInteger

BigInteger는 java.math 패키지에 포함된 클래스로 불변한 임의 정밀도를 갖는 정수를 표현한다. 즉 BigInteger는 메모리가 허락하는한 무한대의 크기를 가진 정수를 표현할 수 있다.

다음은 BigInteger의 주요 특징이다.

1. **불변성(Immutability)**: BigNumber는 불변 객체다. 연산을 수행할 때마다 새로운 BigInteger 객체를 반환한다.
2. **임의 정밀도**: 메모리가 허락하는 한 정수의 크기에 제한이 없다.
3. **성능 고려 사항**: int, long 같은 원시 타입보다 연산이 느릴 수 있다.
4. **사용 사례**: 큰 정수 계산, 암호학적 연산, 고정밀도 수학 연산 등에서 사용한다.

## 사용법

```java
BigInteger bigNumber1 = new BigInteger("10000");
BigInteger bigNumber2 = new BigInteger("100000");

// 덧셈, 뺄셈, 곱셉, 나눗셈, 나머지
bigNumber2.add(bigNumber2);
bigNumber2.subtract(bigNumber2);
bigNumber2.multiply(bigNumber2);
bigNumber2.divide(bigNumber2);
bigNumber2.remainder(bigNumber2);

// 형 변환
BigInteger bigNumber = new BigInteger("10000");

int intBigNum = bigNumber.intValue();
long longBigNum = bigNumber.longValue();
float floatBigNum = bigNumber.floatValue();
double doubleBigNum = bigNumber.doubleValue();
String stringBigNum = bigNumber.toString();

// 값 비교
bigNumber1.compareTo(bigNumber2);
```
