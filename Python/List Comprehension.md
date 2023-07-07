# List Comprehension

리스트 표현식(list comprehension)을 사용하면 보다 간결하게 리스트를 생성할 수 있다.
다음은 리스트 표현식의 문법이다.

```
new_list = [변수활용 for 변수 in 이터러블 객체 if 조건]
```

1. for 반복문을 사용해 이터러블 객체를 순회하며 값을 변수에 담는다
2. 해당 변수를 활용하여 if 조건문을 확인한다. 조건문을 통과하면 리스트에 값을 담을 수 있다.
3. 조건문을 통과한 변수를 가공하여 새로운 리스트를 생성한다.

다음은 리스트 표현식을 활용하는 예시이다.

```py
a_list = [1, 2, 3, 4, 5]

new_list = [x * 2 for x in a_list if x > 2]
print(new_list) # [6, 8, 10]
```

리스트 표현식을 활용하면 보다 간편하게 다차원 리스트를 생성할 수 있다.

```py
matrix = [[row * col for col in range(1, 4)] for row in range(1, 4)]
print(matrix) # [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

위 코드를 반복문으로 풀면 다음과 같다

```py
matrix = []
for row in range(1, 4):
    column = []
    for col in range(1, 4):
        column.append(row * col)
    matrix.append(column)

print(matrix)
```

## print() 출력 시 줄바꿈 하지 않는 방법

파이썬에서 `print()` 함수로 값을 출력할 때 개행 문자(\n)를 넣어주지 않아도 줄바꿈이 된다.
기본적으로 `print()` 함수를 호출할 때 `print(값, end='\n')` 같이 동작하기 때문이다.
따라서 만약 값 출력시 줄바꿈을 하고 싶지 않다면 `print(값, end='')`와 같이 처리할 수 있다.

## 문자열, 리스트 length 구하기

파이썬에서 문자열과 리스트의 길이는 `len()` 함수로 구할 수 있다.

## range()는 리스트를 반환하는 것이 아니다

어제까지만 해도 `range()` 함수가 정수로 된 list를 반환하는 것으로 착각했다.
찾아보니 이터러블 객체를 반환한다고 한다. 다음은 `range()` 함수를 활용하여 list를 생성하는 예시이다.

```py
a_list = list(range(1, 10, 2))
print(a_list) # [1, 3, 5, 7, 9]
```
