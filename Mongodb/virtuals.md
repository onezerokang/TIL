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

## Virtual 프로퍼티로 populate 하기

몽고디비에서 다큐먼트의 관계가 1:N(일대다)일 때 '1'의 ObjectId를 '다'에 저장한다.
'다'의 ObjectId를 '1'에 저장할 경우 '다'가 늘어나 16mb 제한을 넘어버릴 수 있기 때문이다.

문제는 이 경우 '1'의 '다'의 값을 populate할 수 없다는 것인데 virtual 프로퍼티를 만들어 해결할 수 있다.

```js
const userSchema = new Schema({ name: String });

const blogPostSchema = new Schema({
  title: String,
  author: { type: ObjectId, ref: "User" },
});

const User = mongoose.model("User", userSchema);
const BlogPost = mongoose.model("BlogPost", blogPostSchema);
```

위 코드에서는 virtual 프로퍼티를 사용하지 않았다. 이 때 유저가 자신이 작성한 블로그 포스트를 가져오려면 다음과 같이 해야 한다.

```js
// 가져올 유저가 하나일 때
const user = await User.findOne({ name: "suzi" }).lean();
const blogPosts = await BlogPost.find({ author: user._id });
user.blogPosts = blogPosts;

// 가져올 유저가 여럿일 때
const users = await User.find().lean();
const usersWithBlogPosts = await Promise.all(
  users.map(async (user) => {
    const blogPosts = await BlogPost.find({ author: user._id });
    user.blogPosts = blogPosts;
    return user;
  })
);
```

위 코드에서는 쿼리를 나눠서 해야 하고 효율적이지 않다. virtual field를 만들어서 간편하게 populate 할 수 있다.

```js
const userSchema = new Schema({ name: String });

const blogPostSchema = new Schema({
  title: String,
  author: { type: ObjectId, ref: "User" },
});

userSchema.virtuals("blogPosts", {
  ref: "BlogPost",
  localField: "_id",
  foreignField: "author",
});

// 'console.log()'나 다른 'toObject()'를 사용하는 함수가 virtual 프로퍼티를 포함한다.
userSchema.set("toObject", { virtuals: true });

// 'res.json'이나 `JSON.stringify()` 함수가 virtual 프로퍼티를 포함한다.
userSchema.set("toJSON", { virtuals: true });

const User = mongoose.model("User", userSchema);
const BlogPost = mongoose.model("BlogPost", blogPostSchema);
```

이제 user에서 blogPosts를 populate 할 수 있다.

```js
// 가져올 유저가 하나일 때
const user = await User.findOne({ name: "suzi" }).populate("blogPosts");

// 가져올 유저가 여럿일 때
const users = await User.find().populate("blogPosts");
```
