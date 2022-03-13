# 쿠키, 세션, JWT를 이용하여 로그인 구현예시 만들기

오늘은 Node.js에서 쿠키와 세션을 바탕으로 간단한 로그인 예제를 구현할 것이다.
우선 필요한 패키지를 설치하겠다.

```
npm i express mongoose cookie-parser express-session dotenv
```

`cookie-parser`는 클라이언트가 보낸 쿠키를 해석하여 req.cookies 객체로 만든다. 예를들어 id=yesman 이라는 쿠키를 보냈다면 이를 {id: yesman}같이 객체 형태로 바꿔서 사용하기 편하게 해준다.

```js
app.use(cookieParser(비밀키));
```

cookie-parser 첫번째 인수에는 비밀키를 넣을 수 있다. 서명된 쿠키가 잇는 경우 제공한 비밀키를 통해 해당 쿠키가 내 서버가 만든 쿠키임을 검등할 수 있다. 서명된 쿠키는 `req.cookies`대신 `req.signedCookies` 객체에 들어있다.

```js
res.cookie("id", "yesman", {
  expires: new Date(Date.now() + 36000),
  httpOnly: true,
  secure: true,
  signed: true,
});
```

_.env_

```
MONGO_URI=your_mongodb-uri
COOKIE_SECRET=cookie-secret
```

_./models/user.js_

```js
const mongoose = require("mongoose");
const { Schema } = mongoose;

const userSchema = new Schema({
  email: { type: String, required: true, trim: true },
  password: { type: String, required: true },
});

const User = userSchema("User", userSchema);
module.exports = User;
```

_app.js_

```js
const app = require("app");
const mongoose = require("mongoose");
const cookieParser = require("cookie-parser");
const session = require("express-session");

const app = express();

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("Mongodb Connected..."))
  .catch((err) => console.log(err));

app.use(express.json());
app.use(cookieParser(process.env.COOKIE_SECRET));
app.use(
  session({
    secret: process.env.COOKIE_SECRET,
  })
);

app.use(async (req, res) => {
  try {
  } catch {}
});

app.post("/signUp", async (req, res) => {
  try {
    const user = await new User({
      email: req.body.email,
      password: req.body.password,
    }).save();

    res.status(200).json(user);
  } catch (err) {
    console.log(err);
    res.status(500).json({ message: "Internal Server Error" });
  }
});

app.post("/signIn", (req, res) => {
  try {
  } catch (err) {
    console.log(err);
    res.status(500).json({ message: "Internal Server Error" });
  }
});

app.listen(3000, () => console.log("Server listening on port, 3000"));
```
