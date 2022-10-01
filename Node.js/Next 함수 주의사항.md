# Next 함수 주의사항

> 이 문서에서는 next()를 호출할 때의 주의사항을 다루고 있지만 res 객체를 이용하여 응답할 때도 같은 문제가 발생합니다.

express.js의 미들웨어에서 다음 미들웨어로 넘어갈 때 `next()`를 호출한다.

```js
app.use((req, res, next) => {
  console.log("A");
  next();
});

app.use((req, res, next) => {
  console.log("B");
  next();
});
```

위 코드를 실행하면 아래와 같이 출력된다.

```
A
B
```

문제는 `next()`를 호출한 다음에 또 다른 코드가 있을 때 발생한다.

```js
app.use((req, res, next) => {
  console.log("A");
  next();
  console.log("C");
});

app.use((req, res, next) => {
  console.log("B");
  next();
  console.log("D");
});
```

위 코드를 실행하면 아래와 같이 출력된다.

```
A
B
D
C
```

이런 문제를 해결하기 위해선 `next()`를 `return`을 함께 사용해줘야 한다.

```js
app.use((req, res, next) => {
  console.log("A");
  return next();
  console.log("C");
});

app.use((req, res, next) => {
  console.log("B");
  return next();
  console.log("D");
});
```
