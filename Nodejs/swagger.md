# Swagger로 Nodejs API 문서만드는 법

swagger는 몇가지 설정과 코드를 이용하여 문서를 작성하면 이를 HTML로 전환해주는 라이브러리입니다.
오늘은 Express서버에서 Swagger를 이용하여 API 스펙을 명시하는 방법을 정리해보았습니다.

## 초기 세팅

우선 필요한 패키지를 설치하겠습니다.

```
npm init -y
```

```
npm i express swagger-ui-express
```

```
npm i swagger-autogen -D
```

swagger-ui-express는 express에서 swagger를 사용할 수 있게 하는 패키지입니다. 이를 통해 swagger 문서를 작성할 수 있습니다.
swagger-autogen은 swagger를 처음부터 작성하는 것이 아닌, 라우터 경로등을 입력하면 자동으로 기본적인 문서작업을 해주는 패키지입니다.
swagger-autogen말고 swagger-jsdoc이라는 패키지를 사용하는 분도 계시던데, 저는 autogen이 훨씬 편하고 유용하다 생각합니다.

## 폴더 구조

프로젝트 폴더 구조는 다음과 같습니다.

```
+-- node_modules
+-- app.js
+-- package.json
+-- package-lock.json
+-- swagger-output.json
+-- swagger.js
```

우선 app.js에 기본적인 서버구조를 만들어주겠습니다.

```js
const express = require("express");
const app = express();
const PORT = 3000;

const users = [
  { id: 0, name: "Haha", height: 169 },
  { id: 1, name: "Minsu", height: 181 },
  { id: 2, name: "YJ", height: 150 },
];

const cars = [
  { id: 0, name: "SM3", owner: 0 },
  { id: 1, name: "benz", owner: 1 },
  { id: 2, name: "BMW", owner: 1 },
];

app.get("/users/:id", (req, res) => {
  const user = users.find((user) => user.id === req.params.id);
  if (!user) {
    return res.staus(404).json({ message: "User not found" });
  }
  res.status(200).json(user);
});

app.post("/users", (req, res) => {
  const user = req.body;
  users.push(users);
  res.status(200).json(user);
});

app.get("/cars/:id", (req, res) => {
  const car = cars.find((car) => car.id === req.params.id);
  if (!car) {
    return res.staus(404).json({ message: "Car not found" });
  }
  car.owner = users.find((user) => user.id === car.owner);
  res.status(200).json(car);
});

app.listen(PORT, () => console.log(`Server listening on port, ${PORT}`));
```

일단 예제에서 DB까지 사용하면 너무 시간이 비효율적으로 사용되기 때문에 users배열과 cars배열을 DB대용으로 사용하였습니다.
car는 owner라는 필드를 가지고 있는데 이는 user의 id값과 연결됩니다.

이제 swagger-autogen을 세팅하도록 하겠습니다. 우선 swagger.js파일을 만듭니다.

```js
const swaggerAutogen = require("swagger-autogen")({ openapi: "3.0.0" });

const doc = {
  info: {
    title: "Example API",
    description: "Swagger autogen학습을 위한 예시문서입니다.",
    version: "1.0.0",
  },
  servers: [{ url: "localhost:3000" }],
  schemes: ["http"],
  securityDefinitions: {
    apiKeyAuth: {
      type: "apiKey",
      in: "cookie",
      name: "auth",
      description: "유저 토큰을 넣어주세요",
    },
  },
  tags: [
    { name: "User", description: "User Endpoint" },
    { name: "Car", description: "Car Endpoint" },
  ],
  components: {
    schemas: {
      User: {
        id: 0,
        name: "Haha",
        height: 169,
      },
      Car: {
        id: 1,
        name: "benz",
        owner: { $ref: "#/components/schemas/User" },
      },
    },
  },
};

const outputFile = "./swagger-output.json";
const endpointsFile = ["./app.js"];

swaggerAutogen(outputFile, endpointsFile, doc).then(() => require("./app.js"));
```

**포인트**

1. swagger-autogen의 인자에 openapi버전을 넣어주기
2. tags를 만들어 같은 경로의 API를 묶어줄 수 있게 하기
3. components로 DB 테이블 구조를 작성하기

그리고 app.js에 express-swagger와 swagger-autogen을 연결해줍니다.

```js
const express = require("express");
const swaggerUi = require("swagger-ui-express");
const swaggerFile = require("./swagger-output.json");
const app = express();
const PORT = 3000;

const users = [
  { id: 0, name: "Haha", height: 169 },
  { id: 1, name: "Minsu", height: 181 },
  { id: 2, name: "YJ", height: 150 },
];

const cars = [
  { id: 0, name: "SM3", owner: 0 },
  { id: 1, name: "benz", owner: 1 },
  { id: 2, name: "BMW", owner: 1 },
];

app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerFile));

app.get("/users/:id", (req, res) => {
  const user = users.find((user) => user.id === req.params.id);
  if (!user) {
    return res.staus(404).json({ message: "User not found" });
  }
  res.status(200).json(user);
});

app.post("/users", (req, res) => {
  const user = req.body;
  users.push(users);
  res.status(200).json(user);
});

app.get("/cars/:id", (req, res) => {
  const car = cars.find((car) => car.id === req.params.id);
  if (!car) {
    return res.staus(404).json({ message: "Car not found" });
  }
  car.owner = users.find((user) => user.id === car.owner);
  res.status(200).json(car);
});

app.listen(PORT, () => console.log(`Server listening on port, ${PORT}`));
```

swagger-ui-express를 불러오고 미들웨어에 등록하여 /api-docs경로로 접근할 수 있게 합니다.
이후 swagger-autogen으로 만들어질 swagger-output.json을 swagger에 연결해주면 됩니다.

이제 마지막으로 package.json의 script에 swagger-autogen을 실행할 스크립트를 만들어주겠습니다.

```json
{
  "script": { "gendoc": "node ./swagger.js" }
}
```

이제 만든 스크립트를 이용해서 swagger문서를 생성해보겠습니다.

```
npm run gendoc
```

그러면 아래와 같은 swagger-output.json 파일이 생성됩니다. 이 JSON파일이 swagger에 setup되어서 /api-docs를 통해 접근할 수 있게 되는 것입니다.

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Example API",
    "description": "Swagger autogen학습을 위한 예시문서입니다.",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "localhost:3000"
    },
    {
      "url": "http://localhost:3000/"
    }
  ],
  "tags": [
    {
      "name": "User",
      "description": "User Endpoint"
    },
    {
      "name": "Car",
      "description": "Car Endpoint"
    }
  ],
  "paths": {
    "/users/{id}": {
      "get": {
        "description": "",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "OK"
          }
        }
      }
    },
    "/users": {
      "post": {
        "description": "",
        "parameters": [],
        "responses": {
          "200": {
            "description": "OK"
          }
        }
      }
    },
    "/cars/{id}": {
      "get": {
        "description": "",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "OK"
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "User": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number",
            "example": 0
          },
          "name": {
            "type": "string",
            "example": "Haha"
          },
          "height": {
            "type": "number",
            "example": 169
          }
        }
      },
      "Car": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number",
            "example": 1
          },
          "name": {
            "type": "string",
            "example": "benz"
          },
          "owner": {
            "$ref": "#/components/schemas/User"
          }
        }
      }
    },
    "securitySchemes": {
      "apiKeyAuth": {
        "type": "apiKey",
        "in": "cookie",
        "name": "auth",
        "description": "유저 토큰을 넣어주세요"
      }
    }
  }
}
```

다만 swagger-autogen은 기본적으로 API경로와 status code정도만 분석하기 때문에, API 설명, requestBody, reponseBody에 대한 정보들은
주석을 통해 수작업으로 넣어줘야 합니다. 마지막으로 그 작업을 하고 끝내겠습니다.

```js
const express = require("express");
const swaggerUi = require("swagger-ui-express");
const swaggerFile = require("./swagger-output.json");
const app = express();
const PORT = 3000;

const users = [
  { id: 0, name: "Haha", height: 169 },
  { id: 1, name: "Minsu", height: 181 },
  { id: 2, name: "YJ", height: 150 },
];

const cars = [
  { id: 0, name: "SM3", owner: 0 },
  { id: 1, name: "benz", owner: 1 },
  { id: 2, name: "BMW", owner: 1 },
];

app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerFile));

app.get("/users/:id", (req, res) => {
  // #swagger.tags = ["User"]
  // #swagger.summary ="유저를 가져옵니다."
  // #swagger.description = "id와 일치하는 유저를 가져옵니다."

  /*#swagger.responses[200] = {
    description: "여기 설명 넣으시면 됩니다.",
    content: {
        "application/json": {
            schema: {
                $ref: '#/components/schemas/User'
            }
        }
    }
} */
  const user = users.find((user) => user.id === req.params.id);
  if (!user) {
    return res.staus(404).json({ message: "User not found" });
  }
  res.status(200).json(user);
});

app.post("/users", (req, res) => {
  // #swagger.tags = ["User"]
  // #swagger.summary ="유저를 가져옵니다."
  // #swagger.description = "id와 일치하는 유저를 가져옵니다."

  /*#swagger.requestBody = {
      required: true,
      content: {
          "application/json": {
              schema: {
                $ref: "#/components/schemas/User"
              }
          }
      }
  } */

  /*#swagger.responses[200] = {
    description: "여기 설명 넣으시면 됩니다.",
    content: {
        "application/json": {
            schema: {
                $ref: '#/components/schemas/User'
            }
        }
    }
} */
  const user = req.body;
  users.push(users);
  res.status(200).json(user);
});

app.get("/cars/:id", (req, res) => {
  // #swagger.tags = ["Car"]
  // #swagger.summary ="차를 가져옵니다."
  // #swagger.description = "id와 일치하는 차를 가져옵니다."

  /*#swagger.responses[200] = {
    description: "여기 설명 넣으시면 됩니다.",
    content: {
        "application/json": {
            schema: {
                $ref: '#/components/schemas/Car'
            }
        }
    }
} */
  const car = cars.find((car) => car.id === req.params.id);
  if (!car) {
    return res.staus(404).json({ message: "Car not found" });
  }
  car.owner = users.find((user) => user.id === car.owner);
  res.status(200).json(car);
});

app.listen(PORT, () => console.log(`Server listening on port, ${PORT}`));
```

일단 기본적인 튜토리얼을 여기까지고, 400번대 500번대 status code를 처리하고 싶다던가, 인증이 필요한 API를 테스트하고 싶다던가 뭐.. 여러 경우에는 swagger-autogen 공식문서를 읽어보시길 바랍니다. 쉽게 잘 나와있습니다.

전체코드는 이곳에서 확인할 수 있습니다.
[https://github.com/newding0to100/Swagger-tutorial](https://github.com/newding0to100/Swagger-tutorial)

> 출처: https://www.npmjs.com/package/swagger-autogen > https://www.npmjs.com/package/swagger-ui-express
