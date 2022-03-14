# cookie-parser 사용법

cookie-parser는 클라이언트에서 넘어온 쿠키를 해석해서 req.cookies 객체로 만들어 편하게 꺼내 쓸 수 있게 해준다.
cookie-parser는 쿠키를 해석하는 것뿐만 아니라 쿠키를 만들어 클라이언트로 보내거나, 쿠키를 삭제할 수 있다. 우선 `cookie-parser`를 설치해보자.

```
npm i cookie-parser
```

설치한 cookie-parser를 불러온 후 미들웨어로 등록해준다.

```js
app.use(cookieParser(process.env.COOKIE_SECRET));
```

cookie-parser의 첫번째 인수로 **비밀 키**를 넣을 수 있는데, sign(서명)된 쿠키가 있을 때 이 쿠키가 위조되지 않은, 즉 우리 서버에서 만들어진 쿠키인지 검증할 수 있다. 참고로 서명된 쿠키는 req.signedCookies 객체에서 사용할 수 있다.

cookie-parser로 쿠키를 만드는 방법은 다음과 같다.

```js
res.cookie("key", "value", {
  expires: new Date(Date.now() + 36000),
  httpOnly: true,
  secure: true,
  signed: true,
});
```

res.cookie의 첫번째 인자에는 key, 두번째 인자에는 value를 넣고, 세번째 인자로는 옵션 객체를 넣는다.

cookie-parser로 쿠키를 지우는 방법은 다음과 같다.

```js
res.clearCookie("key", "value", { httpOnly: true, secure: true, signed: true });
```

쿠키의 key와 value, 옵션이 정확히 일치해야 쿠키가 지워진다. 단 expires나 maxAge 옵션은 일치하지 않아도 된다.

> 출처: Nodejs 교과서
> https://www.npmjs.com/package/cookie-parser
