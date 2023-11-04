# HTTPS

HTTPS(Hyper Text Transfer Protocol Secure)는 HTTP에 보안 레이어를 추가한 것으로, SSL/TSL 프로토콜을 사용하여 통신을 암호화한다.
SSL(Secure Socket Layer)란 비대칭키 암호화 방식과 대칭키 암호화 방식을 적절히 사용한 암호 프로토콜이다.

## 대칭키 암호화

대칭키 암호화란 하나의 키로 암호화/복호화를 수행하는 암호화 방식을 말한다. 대칭키 암호화의 장단점은 다음과 같다.

- **장점**: 비대칭키 암호화보다 간편하여 연산이 덜 복잡하다.
- **단점**: 상대방에게 암호화된 내용을 보내기 위해서는 복호화 할 키를 함께 보내야 한다. 이때 키를 탈취당할 경우 제 3자에 의해 데이터가 복호화될 수 있다.

## 비대칭키 암호화

비대칭키 암호화(또는 공개키 암호화)는 암호화용 키와 복호화용 키를 나누는 방식이다. 이때 상대방에게 전달되는 키를 공개키(public key), 절대 노출되어서는 안되는 키를 개인키(private key)라고 한다. 공개키로 암호화 된 내용은 개인키로만 복호화 할 수 있다.

- **장점**: 상대방에게 공개키만 주고, 개인키는 본인이 갖고 있기 때문에, 공개키를 탈취당하더라도 상대방은 데이터를 복호화할 수 없다. 즉, 키 전송에 이점을 갖는다.
- **단점**: 대칭키 암호화에 비해 연산이 복잡하다.

## HTTPS 인증 방식

HTTPS 인증 시 SSL 프로토콜을 사용하는데, 해당 인증 과정은 다음과 같다.

- HTTPS 프로토콜을 사용하기 위해서는 인증을 받아야 한다.
- 사이트를 만든 사람이 사이트의 정보와 사이트의 공개키를 CA에 보낸다.
- 문제 없는 사이트라는 것이 판단되면 사이트 인증서 서명
- 이 CA는 브라우저에 내장되어 있다.

클라이언트가 서버에 접속할 때 다음과 같은 과정을 거친다.

## 참조

- [단방향 암호화 방식](https://opentutorials.org/module/5250/29713)
- [양방향 암호화 방식 - 대칭키 방식](https://opentutorials.org/module/5250/29714)
- [[10분 테코톡] 🍭 다니의 HTTPS](https://youtu.be/wPdH7lJ8jf0?feature=shared)