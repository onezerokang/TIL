# MySQL과 MongoDB의 차이점

MySQL은 관계형 데이터베이스 관리 시스템이고, MongoDB는 NoSQL 데이터베이스 관리 시스템이다. 다음은 두 DBMS의 주요 차이점이다.

- **데이터 모델**:
  - **MySQL**: 데이터를 테이블, 행, 열에 저장하는 관계형 데이터베이스 시스템이다. primary key와 foreign key로 관계를 정의한다.
  - **MongoDB**: 데이터를 BSON(Binary JSON) 문서로 저장하는 문서 지향 데이터 베이스다. BSON 문서를 사용하면 비정형, 반정형, 정형 데이터를 저장할 수 있다.
- **확장성**:
  - **MySQL**: 확장에 사용할 수 있는 옵션이 제한적이다. scale-up을 하거나 읽기 전용 복사본을 최대 5개까지 만들 수 있다. 복제본은 기존 복제본보다 성능이 뒤쳐질 수 있어, 대규모 성능 문제의 원인이 발생할 수 있다.
  - **MongoDB**: scale-up하여 성능을 대규모로 최적화하기 좋다. 복제본 세트(동일한 데이터를 보유하는 MongoDB 서버 그룹)와 샤딩(데이터를 여러 머신으로 분산)을 지원한다.
- **성능**:
  - **MySQL**: 고성능 join을 수행하도록 설계됐다.
  - **MongoDB**: 계층적 데이터 모델을 따르기 떄문에 join이 필요하지 않다. $lookup 작업이 가능하지만 MySQL의 join과 비교했을 떄 성능이 밀린다.
- **유연성**:
  - **MySQL**: 고정된 스키마를 사용한다.
  - **MongoDB**: 다양한 데이터 구조를 갖는 문서를 하나의 콜렉션에 저장할 수 있다.

## 사용 시기

- MySQL:
  - 이커머스, 금융 서비스
  - 데이터 일관성이 중요하고, 복잡한 조인, 트랜잭션 처리 등의 연산을 필요로 하는 전통 어플리케이션
- MongoDB
  - 빅데이터, 실시간 분석, 사물 인터넷, 단순 로그
  - 비정형 데이터를 저장해야 할 때, 끊임없이 변화하고 확장되는 데이터를 처리해야 하는 상황

## 추가 예정

구체적인 도메인과 예시

## 참조

- [MongoDB와 MySQL의 차이점은 무엇인가요?
  ](https://aws.amazon.com/ko/compare/the-difference-between-mongodb-vs-mysql/)
- [mongoDB Story 1: mongoDB 정의와 NoSQL
  ](https://meetup.nhncloud.com/posts/274)
