# Transaction

> 트랜잭션(Transaction)은 데이터베이스의 논리적 처리 그룹이며 각 그룹과 트랜잭션은 여러 도큐먼트에 대한 읽기, 쓰기와 같은 작업을 하나 이상 포함할 수 있다. 몽고DB는 여러 작업, 컬렉션, 데이터베이스, 도큐먼트 및 샤드에서 ACID 호환 트랜잭션(ACID-compliant transaction)을 지원한다.
>
> 몽고DB 완벽가이드 p.269

## 트랜잭션이란

트랜잭션은 읽기나 쓰기와 같은 데이터베이스 작업을 하나 이상 포함하는 **데이터베이스의 논리적 처리 단위**(unit of processing)다.
트랜잭션의 중요한 특징은 작업이 성공하든 실패하든 부분적으로는 완료되지 않는다는 점이다.
다음은 '송금'을 통해 트랜잭션을 설명하는 예시이다.

**트랜잭션을 사용하지 않을 경우**

0. 상황: 인터넷 뱅킹으로 친구에게 10,000원을 송금해야 한다.
1. 사용자가 송금버튼을 누르면 클라이언트는 서버에 송금 요청을 한다.
2. 사용자의 계좌에서 10,000원을 차감한다.
3. 친구의 계좌에 10,000원을 추가해야 하는데 정전으로 인해 이 작업이 진행되지 못했다.
4. 내 계좌에는 10,000원이 차감 됐지만 친구는 돈을 받지 못해 10,000원이 증발해버렸다.

**트랜잭션을 사용할 경우**

0. 상황: 인터넷 뱅킹으로 친구에게 10,000원을 송금해야 한다.
1. 사용자가 송금버튼을 누르면 클라이언트는 서버에 송금 요청을 한다.
2. 사용자의 계좌에서 10,000원을 차감한다.
3. 친구의 계좌에 10,000원을 추가해야 하는데 정전으로 인해 이 작업이 진행되지 못했다.
4. 모든 작업이 성공되지 못했기 때문에 사용자의 계좌에서 차감된 10,000원을 복구시키고 다시 작업을 진행한다.
5. 정전이 빠르게 해결되어서 송금에 성공하거나 해결이 오래걸려 송금에 실패한다. 하지만 송금에 실패하더라도 내 계좌에서만 10,000원이 차감되는 문제는 발생하지 않는다.

위 예시에서 송금과정을 하나의 트랜잭션이라 볼 수 있다.
송금 트랜잭션에는 내 계좌에서 돈을 차감하는 update 작업과 친구의 계좌에서 돈을 추가하는 update 작업이 있다.
만약 트랜잭션에 있는 여러작업중 하나라도 실패했다면 데이터를 원래 상태로 복구하는데 이를 rollback이라고 한다.
반면 오류 없이 트랜잭션에 있는 모든 작업이 성공했다면 commit한다.

## 트랜잭션 사용 목적

트랜잭션은 **데이터 부정합을 방지**하고자 할 때 사용한다.
부정합이 발생하지 않으려면 프로세스를 병렬로 처리하지 않도록 하여 한 번에 하나의 프로세스만 처리하도록 하면 되는데, 이는 효율이 떨어진다.
즉, 병렬로 처리할 수 밖에 없는 현실적인 상황에서 부정합을 방지하고자 트랜잭션을 사용하는 것이다.

### 트랜잭션의 특성

트랜잭션에는 ACID라는 4가지 특성이 있다.

- 원자성(Atomicity)

  - 트랜잭션 내 모든 작업이 적용되거나 아무 작업도 적용되지 않도록 한다. 즉 트랜잭션은 일부 작업만 실행할 수 없다.
  - 수행되고 있는 트랜잭션에 의해 변경된 내역을 유지하면서, 이전에 commit된 상태를 임시영역에 따로 저장하여 원자성을 보장한다.
  - 이전 데이터들이 임시로 저장되는 영역을 rollback segment라고 한다.

- 일관성(Consistency)

  - 트랜잭션이 성공적으로 완료되면 일관적은 DB 상태를 유지한다.
  - 여기서 말하는 일관성이란 데이터 타입이 바뀌지 않는 것을 말한다.

- 고립성 or 격리성(Isolation)

  - 트랜잭션 수행 시 다른 트랜잭션의 작업이 끼어들지 못하게 보장하는 것이다.
  - 즉 여러 병렬 트랜잭션이 각 트랜잭션을 순차적으로 실행할 때와 동일한 결과를 얻게 된다.

- 영속성 or 지속성(Durability)
  - 트랜잭션이 커밋될 때 시스템 오류가 발생하더라도 모든 데이터가 유지되도록 한다.
  - 성공적으로 수행된 트랜잭션은 문제 없이 영원히 반영되어야 한다.

데이터베이스는 이러한 속성을 모두 충족하고 성공적인 트랜잭션만 처리될 때 ACID를 준수한다고 한다.
트랜잭션이 완료되기 전에 오류가 발생하면 ACID 준수(ACID compliance)는 데이터가 변경되지 않게 한다.

몽고DB는 복제 셋과 샤드 전체에 ACID 호환 트랜잭션이 있는 분산 데이터베이스다.

## Mongoose에서 트랜잭션을 사용하는 법

> Transaction을 사용하기 위해서는 MongoDB 4.2, Mongoose 5.2 이상 버전이어야 한다.

**Account Schema**

```js
const mongoose = require("mongoose");

const accountSchema = new mongoose.Schema({
  name: { type: String, required: true, minlength: 2, maxlength: 20 },
  money: { type: Number, required: true, default: 0 },
});

const Account = mongoose.model("Account", accountSchema);

module.exports = Account;
```

**Account Router**

```js
const express = require("express");
const { startSession } = require("mongoose");
const Account = require("./models/account");

const router = express.Router();

router.post("/", async (req, res) => {
  const session = await startSession();
  try {
    await session.startTransaction();

    const { accountId1, accountId2, money } = req.body;

    const account1 = await Account.updateOne(
      { _id: accountId1 },
      { $inc: { money } },
      { new: true }
    ).session(session);

    const account2 = await Account.updateOne(
      { _id: accountId2 },
      { $inc: { money } },
      { new: true }
    ).session(session);

    await session.commitTransaction();

    res.status(200).json({ account1, account2 });
  } catch (err) {
    console.log(err);
    await session.abortTransaction();
    res.status(500).json({ err: err.message });
  } finally {
    await session.endSession();
  }
});
```

**withTransaction() helper**

`withTransaction()` 헬퍼 함수를 사용하면 `startTransaction()`과 `commitTransaction()`을 생략할 수 있다.

```js
const express = require("express");
const { startSession } = require("mongoose");
const Account = require("./models/account");

const router = express.Router();

router.post("/", async (req, res) => {
  const session = await startSession();

  try {
    await session.withTransaction(async () => {
      const { accountId1, accountId2, money } = req.body;

      const account1 = await Account.updateOne(
        { _id: accountId1 },
        { $inc: { money } },
        { new: true }
      ).session(session);

      const account2 = await Account.updateOne(
        { _id: accountId2 },
        { $inc: { money } },
        { new: true }
      ).session(session);

      res.status(200).json({ account1, account2 });
    });
  } catch (err) {
    console.log(err);
    await session.abortTransaction();
    res.status(500).json({ err: err.message });
  } finally {
    await session.endSession();
  }
});
```

## 마무리

트랜잭션은 일관성을 보장하기 위해 몽고DB에서 유용한 기능을 제공하지만 풍부한 도큐먼트 모델과 함께 사용돼야 한다.
유연성 있는 모델과 스키마 설계 패턴과 같은 모범 사례를 사용하면 대부분의 상황에서 트랜잭션을 사용하지 않아도 된다.
따라서 트랜잭션은 애플리케이션에서 드물게 사용하는 것이 좋은 강력한 기능이다.

## 참조

> [섹션 10. Transaction - 데이터 일관성 보장](https://www.inflearn.com/course/%EB%AA%BD%EA%B3%A0%EB%94%94%EB%B9%84-%EA%B8%B0%EC%B4%88-%EC%8B%A4%EB%AC%B4/dashboard)  
> [ACID 트랜잭션](https://databricks.com/kr/glossary/acid-transactions)  
> [[DB이론] 트랜잭션(transaction)과 ACID 특성을 보장하는 방법](https://victorydntmd.tistory.com/129)  
> [Transactions in Mongoose](https://mongoosejs.com/docs/transactions.html)  
> [해시넷 - 트랜잭션](http://wiki.hash.kr/index.php/%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98)  
> 몽고DB 완벽 가이드 5장: 트랜잭션
