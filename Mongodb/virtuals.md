# Virtuals

> 출처 [https://mongoosejs.com/docs/guide.html#virtuals](https://mongoosejs.com/docs/guide.html#virtuals)을 보고 정리한 자료입니다.

Virtuals은 Mongodb에는 저장되지 않지만, get/set할 수 있는 가상 프로퍼티이다.
getter는 프로퍼티를 포맷팅하거나 결합하는데 유용하다.
setter는 하나의 값을 여러 필드로 나눠 저장하는 경우에 유용하다.

```js
// 스키마 정의
const userSchema = new Schema({
  name: {
    first: String,
    last: String,
  },
});

// 모델로 컴파일
const User = mongoose.model("User", userSchema);

// 새로운 다큐먼트 생성
const faker = await new User({ fisrt: "Sang-hyeok", last: "Lee" }).save();
```

다음은 user의 풀 네임을 출력하는 코드이다.

```js
console.log(`${faker.name.first} ${faker.name.last}`);
```

풀 네임을 자주 사용하는 경우 매번 위 코드처럼 풀 네임을 조합해야 하는데 이는 번거롭다.
이때 가상 fullName 프로퍼티를 정의 해주면 유용하다.

```js
userSchema.virtual("fullName").get(function () {
  return `${faker.name.first} ${faker.name.last}`;
});
```

이제 `fullName` 가상 프로퍼티에 접근할 수 있다.

```js
console.log(faker.fullName); // Sang-hyeok Lee
```

마찬가지로 setter를 virtual에 추가할 수 있다.

```js
userSchema.virtual("fullName").get(function () {
  return `${this.name.first} ${this.name.last}`;
});
set(function (v) {
  this.name.first = v.substr(0, v.indexOf(" "));
  this.name.last = v.substr(v.indexOf(" ") + 1);
});

const faker = await new User({ fisrt: "Sang-hyeok", last: "Lee" }).save();

faker.fullName; // "Sang-hyeok Lee"
faker.fullName = "T1 Faker"; // 이제 name.first 는 "T1", name.last는 "Faker"이다.
```

virtual setter는 다른 유효성 검사 전에 적용된다.
따라서 위 예제에서 first와 last 필드가 required 인 경우에도 문제 없이 저장된다.
