# Populate

> 출처 [https://mongoosejs.com/docs/populate.html](https://mongoosejs.com/docs/populate.html)을 보고 정리한 자료입니다.

몽고디비에는 RDB의 join과 비슷한 `$lookup` aggregation 연산자가 있다.
Mongoose에서도 이와 비슷한 `populate()` 메서드가 있다.
`populate()` 메서드를 호출하여 다른 컬렉션의 문서를 참조할 수 있다.

`populate()`를 호출할 경우, 문서에 저장된 `ObjectId`를 다른 컬렉션의 문서로 자동 교체한다.

아래는 몇가지 예시이다.

```js
const { Schema, model } = require("mongoose");
const { ObjectId } = Schema.Types;

const userSchema = new Schema({
  name: String,
  age: Number,
  stories: [{ ObjectId, ref: "Story" }],
});

const storySchema = new Schema({
  author: { ObjectId, ref: "User" },
  title: String,
  fans: [{ ObjectId, ref: "User" }],
});

const User = model("User", userSchema);
const Story = model("Story", storySchema);
```

위 코드에서는 User Model과 Story Model을 생성했다.
userSchema의 stories 필드와 storySchema의 author 그리고 fans 필드에는 ObjectId가 저장됐다.
그리고 ref를 통해 각 필드가 어떤 모델을 사용할 것인지 몽구스에게 알려주고 있다.

## 참조할 문서 저장하기

참조하고 싶은 다른 문서의 \_id를 할당하면 된다.

```js
const author = await new User({ name: "S H LEE", age: 22 });

const story = await new Story({
  title: "unkillable demon king",
  author: author._id,
}).save();
```

## Population

저장한 \_id를 문서로 변환하기 위해서는 `populate()`을 호출하여야 한다.

```js
const story = await Story.findOne({ title: "unkillable demon king" }).populate(
  "author"
);

console.log(story.author.name); // "S H LEE"
```

## Population 여부 확인

`populated()`함수를 호출하여 해당 필드가 populate 되었는지 확인할 수 있다.
만약 populate된 필드라면 참 같은 값을 리턴한다.

```js
story.populated("author"); // truthy

story.depopulate("author");

story.populated("author"); // undefined
```

## Foreign document가 없을 경우

populate을 한 ObjectId를 갖는 문서가 존재하지 않을 때 해당 필드는 null이 적용된다.

```js
await User.deleteOne({ name: "S H LEE" });

const story = await Story.findOne({ title: "unkillable demon king" }).populate(
  "author"
);

console.log(story.author); // null
```

만약 populate을 한 필드가 array이고, 문서가 존재하지 않을 때 빈 배열이 제공된다.

```js
const storySchema = new Schema({
  authors: [{ type: ObjectId, ref: "User" }],
  title: String,
});

const story = await Story.findOne({ title: "unkillable demon king" }).populate(
  "authors"
);

story.author; // []
```

## 원하는 필드만 가져오기

popalate한 문서에서 특정 필드만 가져오고 싶을 때, `populate()`메서드의 두번째 인자로 가져오고 싶은 싶은 필드를 넘겨준다.

```js
const story = await Story.findOne({ title: "unkillable domon king" }).populate(
  "author",
  "name" // User의 name 필드만 가져온다.
);

console.log(story.author.name); // "S H LEE"
console.log(story.author.age); // null
```

## 여러 ObjectId를 populate 하기

여러 ObjectId를 한번에 populate하고 싶을 때는 아래와 같은 방법을 사용한다.

**방법1**

```js
const story1 = await Story.find().populate("fans").populate("author");

const story2 = await Story.find()
  .populate("fans", "age")
  .populate("author", "name");
```

**방법2**

```js
const story = await Story.find().populate([
  { path: "fans" },
  { path: "author" },
]);

const story = await Story.find().populate([
  { path: "fans", select: "age" },
  { path: "author", select: "name" },
]);
```

## 조건에 맞는 문서만 populate 하기

조건에 맞는 문서만 populate 하고 싶다면 `match` 옵션을 사용하면 된다.

```js
const story = await Story.find().populate({
  path: "fans",
  match: { age: { $gte: 21 } }, // 나이가 21 이상인 User만 가져온다.
});
```

`match`의 조건을 충족하지 못한 데이터는 null 혹은 빈배열을 반환한다.

## limit vs perDocumentLimit

Populate은 `limit`옵션을 지원한다.
하지만

```js
Story.create([
  { title: "Casino Royale", fans: [1, 2, 3, 4, 5, 6, 7, 8] },
  { title: "Live and Let Die", fans: [9, 10] },
]);
```

만약 `populate()`에서 limit 옵션을 사용한다면, 두번째 story의 fans는 가져오지 못할 것이다.

```js
const stories = await Story.find().populate({
  path: "fans",
  options: { limit: 2 },
});

stories[0].name; // 'Casino Royale'
stories[0].fans.length; // 2

// 2nd story has 0 fans!
stories[1].name; // 'Live and Let Die'
stories[1].fans.length; // 0
```

이는 각 다큐먼트에 대해 별도의 쿼리를 실행하지 않기 위해 몽구스가 대신 `numDocuments \* limit`을 제한으로 사용하여 fans를 쿼리하기 때문이다.
올바른 limit이 필요한 경우 `perDocumentLimit` 옵션을 사용해야 한다. populate()은 각 story에 별도의 쿼리를 실행해야 하므로 더 느려질 수 있다.

```js
const stories = await Story.find().populate({
  path: "fans",
  perDocumentLimit: 2,
});

stories[0].name; // 'Casino Royale'
stories[0].fans.length; // 2

stories[1].name; // 'Live and Let Die'
stories[1].fans.length; // 2
```

## 가져온 문서에서 populate 하기

만약 가져온 몽구스 문서에 ppoulate을 하고 싶다면 `Document.prototype.populate()` 메서드를 사용할 수 있다.

```js
const user = await User.findOne({ naem: "S H LEE" });

user.populated("stories"); // null

await user.populate("stories");

user.stories[0].name; // "unkillable demon king"
```

## 중첩 참조된 문서 populate 하기

다음은 user의 친구를 참조하는 user schema다.

```js
const userSchema = new Schema({
  name: String,
  friends: [{ type: ObjectId, ref: "User" }],
});
```

populate을 하여 유저의 친구를 가져올 수 있지만, 가져온 친구의 친구를 populate하고 싶다면 아래와 같이 처리할 수 있다.

```js
const user = await User.findOne({ name: "S H LEE" }).populate({
  path: "friends",
  populate: { path: "friends" },
});
```

## `refPath`를 통한 동적 참조

몽구스는 한 필드에서 여러개의 컬렉션을 참조할 수 있다.
이때 참조하려 하는 모델을 몽구스에게 알려주어야 한다.
평상시에는 `ref`를 사용했지만 여러 컬렉션을 동적으로 참조할 때는 `refPath`를 사용하면 된다.

아래 예시에서 사용자는 이야기와 상품에 댓글을 달 수 있다.

```js
const commentSchema = new Schema({
  contents: { type: String, required: true },
  doc: {
    type: ObjectId,
    required: true,
    refPath: "docModel",
  },
  docModel: {
    type: String,
    required: true,
    enum: ["Story", "Product"],
  },
});

const Product = await model("Product", new Schema({ name: String }));
const Story = await model("Story", new Schema({ title: String }));
const Comment = await model("Comment", commentSchema);
```

몽구스는 refPath에 할당한 필드에 담긴 값을 참조할 모델로 인식한다.

```js
router.post("/products/:id/comments", async (req, res) => {
  try {
    const productId = req.params.id;

    await new Comment({
      contents: "와우",
      doc: productId,
      docModel: "Product",
    }).save();

    res.status(201).json({ success: true });
  } catch (err) {
    console.log(err);
    res.status(500).json({ err: err.message });
  }
});

router.post("/stories/:id/comments", async (req, res) => {
  try {
    const storyId = req.params.id;

    await new Comment({
      contents: "와우",
      doc: storyId,
      docModel: "Story",
    }).save();

    res.status(201).json({ success: true });
  } catch (err) {
    console.log(err);
    res.status(500).json({ err: err.message });
  }
});
```

```js
const comments = await Comment.find().populate("doc");
console.log(comments[0].product.name);
console.log(comments[0].story.name);
```

## Populate Virtuals

자세한 내용은 [Virtuals](https://github.com/newding0to100/TIL/blob/main/Mongodb/virtuals.md)를 참조하십시오.

## 미들웨어에서 Populate하기

`pre` 또는 `post` 후크에서 populate을 사용할 수 있다.
특정 필드를 항상 채우려면 [mongoose-autopopulate 플러그인](https://www.npmjs.com/package/mongoose-autopopulate)을 확인하십시오.

```js
MySchema.pre("find", function () {
  this.populate("user");
});
```

```js
MySchema.post("find", async function (docs) {
  for (const doc of docs) {
    if (doc.isPublic) {
      await doc.populate("user");
    }
  }
});
```

```js
MySchema.post("save", async function (doc, next) {
  doc.populate("user").then(function () {
    next();
  });
});
```

## 마무리

`populate()`은 저장한 다른 컬렉션의 ObjectId를 문서로 변환시켜주는 몽구스의 편한 기능이다.
허나 populate은 $oid로 모두 조회를 해서 자바스크립트 단에서 합쳐주는 것이지 JOIN처럼 DB 자체에서 합쳐주는 것이 아니다.
때문에 populate을 과도하게 중첩해 사용할 경우 성능 문제가 발생할 수 있다.
따라서 populate을 중첩해서 사용하지 않아도 되는 스키마 설계를 하거나 RDB를 사용하는 것을 권장한다.
