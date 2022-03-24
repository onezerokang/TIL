# Mongoose와 enum

Object Document Mapping인 Mongoose에서는 Schema를 지정하여 몽고디비 데이터의 일관성을 유지할 수 있다.
오늘은 mongoose 공식 문서를 읽다가 발견한 `enum`에 대해 정리해보겠다.

## enum

몽구스에서 enum은 `유효성 검사`를 위해 사용됩니다.

```js
const foodSchema = new Schema({
  name: {
    type: String,
    required: true,
  },
  price: {
    type: Number,
    required: true,
  },
  category: {
    type: String,
    enum: ["KoreanFood", "Snack", "ChineseFood"],
  },
});
```

위 처럼 `enum`을 사용하면 category에는 KoreanFood, Snack, ChineseFood만 저장될 수 있다.
이를 통해 그냥 문자열 타입을 사용하는 것보다 정확한 데이터를 저장할 수 있게 된다.

그래서 필자는 데이터가 들어올 때 다음과 같이 유효성 검사를 해주었다.

```js
router.post("/api/foods", async (req, res) => {
  try {
    if (!Food.schema.path("category").includes(req.body.category)) {
      return res.status(400).json({ message: "Invalid Category" });
    }
    const food = await new Food(req.body).save();
    res.status(200).json(food);
  } catch (err) {
    console.log(err);
    res.status(500).json({ message: "Internal Server Error" });
  }
});
```
