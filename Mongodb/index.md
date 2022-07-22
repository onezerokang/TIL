# Index

## 인덱스란?

데이터베이스의 인덱스는 책의 인덱스(색인, 목차)와 유사하다. 때문에 DB의 인덱스에 대해 이야기 하기전 사전으로 먼저 예시를 들어보도록 하겠다. 다음은 사람이 사전에서 글자를 찾는 과정이다.

0. '라면'이라는 글자를 찾고 싶은 상황
1. 'ㄹ'로 시작하는 글자가 적힌 범위를 확인하기 위해서 목차, 혹은 인덱스를 확인한다.
2. 인덱스를 통해 'ㄹ'로 시작하는 글자가 적힌 범위로 이동한다.
3. 'ㄹ' 영역에서 '라면'이라는 글자를 찾는다.

이처럼 데이터베이스에서 데이터 쿼리를 할 때 전체 내용을 살펴보는 대신 특정 내용을 가르키는 정렬된 리스트를 확인한다. 따라서 엄청난 양의 명령을 더 빠르게 쿼리할 수 있다.
인덱션을 사용하지 않는 쿼리를 컬렉션 스캔(collection scan)이라 하며, 서버가 쿼리 결과를 찾으려면 '전체 내용을 살펴봐야 함'을 의미한다. 몽고DB에서는 원하는 데이터 필드를 인덱스로 지정하여 검색 결과를 빠르게 가져오는 것이 가능하다.

## 인덱스의 원리

인덱스는 DB의 검색을 빠르게 하기 위하여 데이터의 순서를 미리 정리해두는 과정이다. 몽고DB에서는 원하는 데이터 필드를 인덱스로 지정하여 검색 결과를 빠르게 가져오는 것이 가능하다.

몽고DB의 필드에 인덱스를 걸면 해당 필드를 중복없이 복사, 정렬한 다음 각각 해당 도큐먼트의 주소를 저장한다. 그래서 쿼리를 할 때 index에서 일치하는 조건을 찾고 해당 index와 매칭되는 도큐먼트를 찾는다. 이런 원리로 문서가 100,000개일 때 탐색을 하려면 100,000개의 문서를 모두 조회해야 하지만, index를 사용하면 수십번~수천번안에 탐색이 끝나 탐색 속도가 매우 빨라진다.

## 인덱스의 종류

### 단일 필드 인덱스(Single Field Index)

하나의 필드 인덱스를 사용하는 것을 단일 필드 인덱스라고 한다. 몽고DB에서는 기본적으로 컬렉션에 `_id`라는 단일 필드 인덱스가 생성된다. 단일 필드 인덱스를 설정하는 방법은 다음과 같다.

```
db.userSchema.index({age: 1})
```

단일 필드 인덱스에서 1은 오름차순, -1은 내림차순을 의미한다. 하지만 단일 필드 인덱스에서는 오름차순, 내림차순인지 중요하지 않다. 어떤 방향으로 가도 동일하게 접근하기 때문이다.

### 복합 인덱스(Compound Index)

두 개 이상의 필드를 사용하는 인덱스를 복합 인덱스라고 한다. 다음은 복합 인덱스를 설정하는 방법이다.

```
db.userSchema.index({age: 1, username: -1 })
```

위 예제처럼 인덱스를 설정하면 age는 오름차순으로 정렬한다. 그리고 같은 age를 갖을 경우 username으로 내림차순 정렬하게 된다.
복합 인덱스를 사용할 때는 아래의 특징을 고려하며 생성한다.

#### sort 연산 시 인덱스의 순서를 고려하며 생성하자

#### 단일 인덱스와 다르게 복합 인덱스는 정렬 방향을 고려하자

#### Prefixes

#### sort 연산은 non-prefix를 지원한다.

#### Index Intersection

### TTL 인덱스

TTL(Time to live) Index란 특정 시간 이후 또는 특정 시간에 컬렉션에서 문서를 자동으로 제거하는데 사용할 수 있는 특수 단일 필드 인덱스로, 한정된 시간 동안에만 데이터베이스에 유지해야 하는 이벤트 데이터, 로그 및 세션 정보와 같은 유형의 정보 관리에 유용하다.

```
db.coupon.createIndex({createdAt: 1}, {expireAfterSeconds: 60 * 60 * 24})
```

`createIndex()`의 첫번째 인자에는 TTL 인덱스를 설정할 필드를 지정해주고, 두번째 인덱스에는 TTL 인덱스가 설정된 필드에서 몇초후에 해당 도큐먼트를 삭제할지를 설정해준다.

### Text 인덱스

텍스트에 인덱스를 걸 수 있다. 간단한 검색기능을 구현할 때 사용한다.

```
db.blogPosts.insert([
  { title: "몽고DB 완벽 가이드", content: "몽고DB는 유연하고 확장성 좋은 DB이다...(생략)" },
  { title: "Nest.js로 구현하는 클린 아키텍처", content: "Nest.js는 Express와 비교했을 때...(생략)" },
  { title: "유재석처럼 말하는 법", content: "유재석처럼 말하는 법을 익히면 누구에게나 호감을 살 수...(생략)" }
]);
```

```
db.blogPosts.createIndex({title: "text"})
```

```
db.blogPosts.find({$text: {$search: "몽고DB"}})
```

## Selectivity

## mongoose에서 인덱스 생성하기

### 단일 필드 인덱스 생성

```js
const mongoose = require("mongoose");
const { Schema } = mongoose;

const userSchema = new Schema(
  {
    username: { type: String },
    age: { type: Number },
  },
  { timestamps: true }
);

userSchema.index({ age: 1 });
```

### 복합 인덱스 생성

```js
const mongoose = require("mongoose");
const { Schema } = mongoose;

const userSchema = new Schema(
  {
    username: { type: String },
    age: { type: Number },
  },
  { timestamps: true }
);

userSchema.index({ age: 1, username: -1 });
```

### TTL 인덱스 생성

```js
const mongoose = require("mongoose");
const { Schema } = mongoose;

const userSchema = new Schema(
  {
    username: { type: String },
    age: { type: Number },
  },
  { timestamps: true }
);

userSchema.index({}, {});
```

### 유니크 인덱스 생성

```js
const mongoose = require("mongoose");
const { Schema } = mongoose;

const userSchema = new Schema(
  {
    username: { type: String, unique: true },
    age: { type: Number },
  },
  { timestamps: true }
);
```

### 텍스트 인덱스 설정

```js
const mongoose = require("mongoose");
const { Schema } = mongoose;

const userSchema = new Schema(
  {
    username: { type: String, unique: true },
    age: { type: Number },
  },
  { timestamps: true }
);

userSchema.index({ username: "text" });
```

## 인덱스를 걸 때 고려해야 할 요소

인덱스를 적절하게 사용하면 탐색성능을 올려줄 수 있지만 남용할 경우 큰 효과 없이 자원 낭비만 될 수 있다. 인덱스를 걸 때 고려해야 할 요소는 다음과 같다.

- CUD vs R
  - 인덱스를 지정하면 데이터를 생성, 수정, 삭제를 할 때 인덱스도 변경을 해줘야 해서 CUD 속도가 느려진다. 만약 잘 조회하지는 않고 CUD가 많은 컬렉션은 인덱스를 걸어줄 필요가 없다.
- 메모리
  - 인덱스는 메모리를 많이 차지하기 때문에 남용할 경우 비용이 증가한다.
- query
  - 처음부터 인덱스를 거는 것이 아니 API가 완성되고, 데이터가 어느정도 쌓인 후 인덱스를 걸어줘도 된다.
- selectivity
  - 하나의 인덱스에 여러 도큐먼트가 걸려있을 경우 인덱스에서 탐색을 한 후 다큐먼트에서 또 정렬을 해줘야 한다.

## 마무리

데이터가 적을 때는 인덱스가 탐색속도에 큰 영향을 주지 않는다.
데이터가 쌓여가고 애플리케이션의 방향이 잡히기 시작하면 [Mongo Compass](https://www.mongodb.com/ko-kr/products/compass)의 Explain 기능으로 성능 테스트 해보면서 적절히 인덱스를 걸어주면 된다.

## 참조

> [섹션 8. Index - 많은 데이터 관리하기(빠른 읽기)](https://www.inflearn.com/course/%EB%AA%BD%EA%B3%A0%EB%94%94%EB%B9%84-%EA%B8%B0%EC%B4%88-%EC%8B%A4%EB%AC%B4/dashboard)  
> [[MongoDB] 강좌 6편 Index 설정](https://velopert.com/560)  
> [MongoDB index 개념과 indexing 전략](https://ryu-e.tistory.com/1)  
> 몽고DB 완벽 가이드 5장: 인덱싱
