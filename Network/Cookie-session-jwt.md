# Cookie Session JWT

## HTTP의 특징

Client와 Server는 HTTP로 통신을 한다. HTTP는 무상태성(Stateless)한데, 이로 인해 서버는 요청을 보낸 클라이언트를 알지 못하고, 전에 어떤 요청을 했는지도 알 수 없다. 이런 HTTP특성은 다음과 같은 상황을 발생시킨다.

1. 유저가 로그인을 한다.
2. 유저가 글을 작성한다.
3. 글을 수정하려 하는데 서버는 이 유저가 누구인지 모르기 때문에 글을 수정할 수 없으며 다시 로그인하라고 한다.

이런 문제를 해결하기 위해 쿠키와 세션을 이용한다.

## Cookie

쿠키는 서버에서 클라이언트로 보내는 데이터 파일이다. 다음은 쿠키의 예시이다.

### 쿠키의 구성요소

1. key
2. value
3. 0개 이상의 속성(HttpOnly, Max-Age 등..)

### 쿠키의 활용예시

쿠키를 활용하는 방법은 다음과 같다.

1. 유저가 서버에 ID와 비밀번호를 보내 로그인 요청을 한다.
2. 서버는 ID와 비밀번호를 사용하여 유저가 맞는지 검증한다.
3. 서버는 `Set-Cookie` HTTP Header를 사용하여 유저의 정보를 쿠키에 담아 응답한다.
4. 클라이언트에는 유저정보가 담긴 쿠키가 저장된다.
5. 유저가 서버에 어떤 요청을 보낼 때마다 브라우저는 `Cookie HTTP Header`에 쿠키를 담아 함께 보낸다.
6. 서버는 보내진 쿠키를 통해 유저를 인증하고 그에 맞는 응답을 처리한다.

### 쿠키의 장점

- 매 요청시 쿠키를 함께 보내기 때문에 Stateless한 서버에 자신이 누구인지 알려줄 수 있다.

### 쿠키의 단점

- 탈취당할 경우 유저의 정보가 해커에게 통으로 넘어갈 수 있음. 그래서 비밀번호같이 보안이 민감한 데이터는 넣지 않는다.
- 매 요청때마다 쿠키를 보내기 때문에 비용이 발생하게 된다.

쿠키는 유저의 데이터(id, password 등)을 클라이언트에 저장하기 때문에 보안상 취약합니다.
이를 보완하기 위해 서버에 데이터를 저장하는 `Session`을 사용합니다.

## Session

### 세션의 활용예시

1. 유저가 서버에 ID와 비밀번호를 보내 로그인 요청을 한다.
2. 서버는 ID와 비밀번호를 사용하여 유저를 검증한다.
3. 유저의 정보를 Session DB에 저장한다.
4. 저장된 아이디의 식별값인 SessionId를 쿠키에 담아 응답한다.
5. 클라이언트에는 세션 아이디가 담긴 쿠키가 저장된다.
6. 유저가 서버에 어떤 요청을 보낼 때마다 브라우저는 `Cookie HTTP Header`에 쿠키를 담아 보낸다.
7. 서버는 쿠키에 담긴 세션 아이디로 세션 DB를 조회하고, 유저가 있을 시 그에 맞는 응답을 처리한다.

### 세션의 장점

- 유저의 정보를 클라이언트가 아닌 서버에 저장하기 때문에 쿠키가 탈취당해도 유저의 정보를 지킬 수 있다.
- 세션DB를 지워버리면 세션 ID를 탈취당해도 해커는 로그인을 할 수 없다.
- 유저의 계정을 보다 명확하게 관리할 수 있다(로그인 된 디바이스, 인원 수 제한 등)

### 세션의 단점

- 세션 DB를 사용하지 않고 서버에 저장할 경우 서버를 확장하는데 어려움이 생긴다.
- 세션 DB에 세션을 저장하기 때문에 유저가 많아질 수록 많은 비용이 발생한다.

## JWT

`JWT`는 JSON WEB TOKEN의 약자로 JSON을 사인(sign)알고리즘을 통해 사인하고 인코딩한 토큰입니다.
JWT는 Header, Payload, Verify Signature로 이루어져있습니다.

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`

### JWT의 활용예시

### JWT의 장점

### JWT 단점

## 결론

> 출처: Nodejs교과서
> https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/Set-Cookie > https://tecoble.techcourse.co.kr/post/2021-05-22-cookie-session-jwt/
