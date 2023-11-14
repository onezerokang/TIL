# ThreadLocal

## 개요

ThreadLocal이란 스레드마다 각각의 로컬 변수를 사용할 수 있게 하는 클래스다.

멀티 스레드 환경에서 동시에 객체의 상태를 변경하거나, 접근할 때 동기화 문제가 발생할 수 있다.

이를 해결하기 위해 synchronized 키워드를 사용하여 해당 공유 자원을 임계 구역으로 만들어 동기화하는 방법도 있지만, 이는 성능 하락의 원인이 되기도 한다. ThreadLocal을 이용해서 같은 객체에 접근하더라도 다른 로컬 변수를 사용하도록하면 동기화 문제를 해결할 수 있다.

ThreadlLocal이 동기화 문제를 해결하는데만 사용되는가?

## ThreadLocal의 내부 구조

## 참조

- [Thread의 개인 수납장 ThreadLocal](https://dev.gmarket.com/62)
- [ThreadLocal을 알아보자](https://catsbi.oopy.io/3ddf4078-55f0-4fde-9d51-907613a44c0d)
