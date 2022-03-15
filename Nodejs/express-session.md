# express-session 사용법

익스프레스에서 세션을 관리를 도와주는 미들웨어다. 특정 사용자를 임시적으로 저장해둘 때 매우 유용하며, 세션은 사용자 별로 req.session 객체 안에 저장된다. 우선 express-session을 설치하자.

```
npm i express-session
```

해당 미들웨어를 불러온 후 등록해준다.

```js
app.use(
  session({
    resave: false,
    saveUninitalized: false,
    secret: process.env.COOKIE_SECRET,
    cookie: {
      httpOnly: true,
      secure: true,
    },
    name: "session-cookie",
  })
);
```

express-session은 인자로 옵션 객체를 받는다. 자주 사용되는 옵션은 다음과 같다.

- resave: 요청이 올 때 세션에 수정이 생기지 않더라도 세션을 다시 저장할지에 대한 설정
- saveUninitialized: 세션에 저장할 내역이 없더라도 처음부터 세션을 생성할지에 대한 설정
- secret: express-session은 세션 관리 시 클라이언트에 쿠키를 보낸다. 안전하게 쿠키를 보내기 위해 서명을 추가하고, 쿠키와 같은 비밀키를 설정해주어야 한다.
- cookie: 세션 쿠키에 대한 설정이다. 개발시에는 secure를 false로 하고 배포시에는 true로 설정한다.
- store: 세션을 메모리에 저장할지, DB를 연결해 저장할지에 대한 설정. 보통 레디스를 연결한다.

```js
req.session.name = "yesman"; //세션 등록
req.sessionID; //세션 아이디 확인
req.session.distory(); //세션 모두 제거
```

> 출처: https://www.npmjs.com/package/express-session
> Nodejs교과서
