# Mongodb에서 TTL설정하기

TTL이란 Time To Live의 약자로 컴퓨터나 네트워크에서 데이터의 유효기간을 나타내기 위한 방법이다.

## Mongodb에서 TTL 설정하기

Mongodb에서 TTL을 설정하기 위해서는 TTL index를 걸어줘야 한다. 문법은 다음과 같다.

```
db.collection.createIndex({expiredAt: 1}, {expireAfterSeconds: 3600})
```

위 코드는 expiredAt으로부터 1시간이 지나면 해당 document를 제거하는 TTL index를 설정해준 것이다.
TTL인덱스를 거는 필드가 꼭 expiredAt이 아니어도 된다.

## Mongoose에서 TTL 설정하기

Nodejs에서 Mongodb를 사용할 때는 주로 Mongoose를 사용하는데, 여기서 TTL index를 설정하는 법을 알아보겠다.

```js
const mongoose = require("mongoose");
const { Schema } = mongoose;

const verifyCodeSchema = new Schema({
  email: {
    type: String,
    required: true,
  },
  code: {
    type: String,
    required: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
    expires: 60 * 60 * 2,
  },
});

const VerifyCode = mongoose.model("VerifyCode", verifyCodeSchema);
module.exports = VerifyCode;
```

위 코드처럼 이메일 인증코드를 저장하는 Schema를 만들었다.
그리고 이메일 인증코드의 유효기간을 2시간으로 설정했기 때문에
createdAt 필드에 expires를 2시간으로 설정해준 것이다.(7,200초)
이렇게 하면 새로운 verifyCode document를 만든 시간을 기준으로 2시간 후에 해당 document를 제거한다.
참고로 mongodb는 1분마다 제거할 document가 없는지 탐색하기 때문에 정확한 시간에 삭제되는 것이 아닌 1분간의 오차범위가 있을 수 있다.

## 주의사항

필자의 경우 테스트용으로 expires를 1분으로 설정했었다.
이후 정상적으로 삭제되는 것을 확인하자 이를 3,600초로 조정하였는데 여전히 1분만 유지되고 document가 삭제되는 것을 확인했다.
그래서 DB에 접속하여 getIndexes()를 사용해 확인해봤는데 기존에 mongoose에서 1분으로 설정한 경우 덮어쓰지 못하는 것을 확인했다.
이 경우 dropIndex()를 사용하여 기존 인덱스를 지워주고 다시 mongoose를 통해 mongodb에 접속하면 해결된다.
