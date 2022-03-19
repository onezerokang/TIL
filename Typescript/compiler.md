# Typescript Compiler 설정

타입스크립트의 기본타입을 배울 때는 변경사항이 생길 때마다 `tsc app.js`를 했었다.
이렇게 일일히 컴파일을 하는 방식은 개발 효율이 떨어지기 때문에 오늘은 타입스크립트 컴파일에 대해 정리했다.

## Watch mode

watch모드는 TS 코드에 변화가 생겼을 때마다 컴파일하는 방법이다. 사용예시는 다음과 같다.

```
tsc app.ts --watch
```

혹은

```
tsc app.ts -w
```

## tsconfig.json 설정하기

tsconfig.json은 타입스크립트에 대해 설정하는 파일이다. 아래 명령어로 tsconfig.json 파일을 생성할 수 있다.

```
tsc --init
```

tsc 명령어로 컴파일을 할 때 경로를 지정하지 않으면 tsconfig.json이 있는 폴더를 기준으로 컴파일한다.
tsconfig파일이 없다면 프로젝트 폴더 내에서 상위 폴더의 경로를 검색해 나간다.

```
tsc -w
```

## tsconfig.json 설정하기

tsconfig.json을 보면 대략 다음과 같은 구조를 갖는다.

```json
{
  "compilerOptions": {
    // ...생략
  }
}
```

그리고 추가로 `files`, `include`, `exclude`를 사용할 수 있다.

**files**
타입스크립트 컴파일 명령어를 입력할 때 대상 파일을 지정하지 않고 files에 미리 정의해 놓을 수 있다.

```js
{"files":["app.ts", "analytics.ts"]}
```

**include**
files는 컴파일 할 파일을 정의한다면 include는 디렉터리를 정의한다.

```js
{"include": ["src/**/*"]}
```

**exclude**
변환하지 않을 디렉터리를 지정한다.

```js
{"exclude": ["node_modules"]}
```

위 예제에서는 node_modules를 지정했지만 exclude의 기본값으로 node_modules이 지정되어있기 때문에 굳이 입력할 필요는 없다.

> TIP
> 컴파일 대상 경로를 정의하는 속성의 우선 순위 files > include = exclude

**exclude**

## compilerOptions 옵션 몇개 살펴보기

| 옵션                       | 설명                                                                              |
| -------------------------- | --------------------------------------------------------------------------------- |
| lib                        | 컴파일 시 포함할 라이브러리의 목록.                                               |
| allowJS                    | 컴파일 시 JS파일이 포함될 수 있는지를 지정. TS를 점진적으로 적용할 때 사용한다.   |
| checkJS                    | JS파일의 오류검사 여부를 설정한다.                                                |
| sourceMap                  | 브라우저에서 타입스크립트 그대로를 볼 수 있게 해주는 옵션. 디버깅에 유용하다      |
| rootDir                    | TS파일이 모여있는 디렉터리 경로. 설정 시 해당 디렉터리에서만 컴파일이 진행된다.   |
| outDir                     | 컴파일된 JS 파일이 모여있는 디렉터리 경로. rootDir의 폴더 구조를 그대로 복사한다. |
| removeComments             | 컴파일 시 TS 파일에 작성된 주석 제거 여부                                         |
| noEmit                     | 이 옵션을 true로 설정하면 컴파일이 되지 않는다.                                   |
| downlevelIteration         | 타겟이 'ES5', 'ES3'일 때에도 'for-of', spread 그리고 destructuring 문법 모두 지원 |
| noEmitOnError              | 타입스크립트 컴파일 과정에서 에러가 날 경우 JS파일을 만들지 않는다.               |
| Strict                     | 자바스크립트를 Strict 모드로 컴파일 한다. true로 할경우 아래 옵션 적용            |
| noUnusedLocals             | 타입스크립트에서 사용하지 않는 변수가 있을 시 에러를 던진다.                      |
| noUnusedParameters         | 사용하지 않는 인자가 있을 경우 에러를 던진다.                                     |
| noImplicitReturns          | 함수가 조건에 따라 return 값을 줄 때가 있고 안줄 때가 있을 때 에러를 던진다.      |
| noFallthroughCasesInSwitch | switch문에서 fallthrough 케이스에 대한 에러보고 여부                              |

> 출처
> https://www.udemy.com/course/understanding-typescript

> https://joshua1988.github.io/ts/config/tsconfig.html#%ED%83%80%EC%9E%85%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-%EC%84%A4%EC%A0%95-%ED%8C%8C%EC%9D%BC-%EC%86%8D%EC%84%B1

> https://geonlee.tistory.com/214
