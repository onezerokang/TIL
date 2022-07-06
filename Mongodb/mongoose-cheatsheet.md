# 몽구스 치트시트

몽구스란 node.js에서 사용할 수 있는 몽고디비의 ODM이다.
ODM은 Object Data Mapping의 약자로 몽고디비의 데이터를 자바스크립트의 객체로 mapping 시켜준다. 이를 통해 몽고디비의 데이터를 보다 쉽고 편하게 다룰 수 있다.

## 설치

```
npm install mongoose
```

## 연결

```js
const mongoose = require("mongoose");

mongoose.connect("mongodb_uri", {});
```

## 스키마

몽고디비는 테이블이 없기 때문에 다큐먼트에 어떤 값을 넣어도 문제가 없다.
이런 문제를 방지하기 위해 몽구스는 사용자가 작성한 스키마로 몽고디비에 저장하기 전에 필터링한다.

mongoose에서 사용할 수 있는 타입

- String
- Number
- Date
- Buffer
- Boolean
- Mixed
- ObjectId
- Array
- Decimal128
- Map

```js
const mongoose = require("mongoose");

const user = new mongoose.Schema(
  {
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
    },
    age: {
      type: Number,
      default: 1,
      required: true,
    },
    isAdult: {
      type: Boolean,
      default: false,
      required: true,
    },
    name: {
      first: String,
      last: String,
    },
    friends: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
      },
    ],
    any: [mongoose.Schema.Types.Mixed],
  },
  {
    timestamps: true,
  }
);

userSchema.index({ email: 1 });

const User = mongoose.model("User", userSchema);
module.exports = { User };
```

### 인스턴스 메서드

```js

```

### 스태틱 메서드

```js

```

### 인덱스

### 옵션

###

## Create

### Document.prototype.save()

```js
const user = new User({
  email: "",
  age: 20,
  name: { first: "kaka", last: "kim" },
});

await user.save();
```

### Model.create()

```js
await User.create({ email: "", age: 20, name: { first: "kaka", last: "kim" } });

await User.create([
  { email: "", age: 20, name: { first: "kaka", last: "kim" } },
  { email: "", age: 20, name: { first: "kaka", last: "kim" } },
]);
```

### Model.insertMany()

```js
const users = [{}, {}];
await User.insertMany(users);
```

## Read

### Model.findOne()

```js
const user = await User.findOne({});
```

### Model.findById()

```js
const user = await User.findById({});
```

### Model.find()

```js
const users = await User.find({});
```

## Update

### Model.findOneAndUpdate()

```js

```

## Delete

### Model.findOneAndDelete()

```js
const user = User.findOneAndDelete();
```

### Model.findByIdAndDelete()

```js

```

### Model.deleteOne()

```js
const result = await User.deleteOne();
```

### Model.deleteMany()

```js
const result = await User.deleteMany();
```

## 쿼리빌더

## 고급기술
