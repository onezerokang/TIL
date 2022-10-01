# req 객체에 user를 저장하는 방법.md

미들웨어를 이용하여 인증을 하는 경우 `req`객체에 유저 데이터를 저장하곤 한다.
자바스크립트를 사용하는 경우 별 문제 없이 저장할 수 있지만 타입스크립트를 사용하는 nest.js의 경우 req 객체에 user를 저장할 수 없다.
이 문제는 타입을 변경하여 해결할 수 있다.

1. src 디렉터리에 types 디렉터리를 생성한다.
2. types 디렉터리 안에 확장할 패키지의 이름으로 디렉터리를 만든다.
3. 해당 폴더에 index.d.ts 파일을 생성한다.

```
 src/
   - types/
    - express/
     - index.d.ts
```

4. 아래 코드를 index.d.ts 파일에 추가한다.

```ts
import express from "express";

declare global {
  namespace Express {
    interface Request {
      user?: Record<string, any>;
    }
  }
}
```

5. tsconfig.json 파일을 수정한다.

```json
{
  "compilerOptions": {
    "typeRoots": ["./src/types", "./node_modules/@types"]
  }
}
```

## 참조

- [Property 'user' does not exist on type 'Request<ParamsDictionary, any, any, ParsedQs, Record<string, any>>'](https://stackoverflow.com/questions/65848442/property-user-does-not-exist-on-type-requestparamsdictionary-any-any-pars)
