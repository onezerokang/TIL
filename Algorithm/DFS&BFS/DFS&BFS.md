# DFS&BFS

DFS(Depth-First Search)와 BFS(Breadth-First Search)는 그래프 탐색 알고리즘이다.

## 스택 자료구조

후입선출의 자료구조, DFS에서 사용된다.
삽입과 삭제 기능을 갖는다.
파이썬에서 stack을 사용할 때는 list의 append와 pop 메서드를 사용하면 된다.
둘 다 O(1) 시간 복잡도를 갖기 때문에, 별도 자료구조 없이 list를 스택처럼 사용할 수 있다.

```py
stack = []

stack.append(5)
stack.append(2)
stack.append(3)
stack.pop()

print(stack[::-1])
print(stack)
```

## 큐 자료구조

선입선출의 자료구조, BFS에서 사용된다.
파이썬에서 queue를 구현할 때 deque을 사용할 수 있다.
list를 pop하면 원소를 꺼내고 원소의 위치를 조정함
O(N) 시간복잡도

```py
from collections import deque

queue = deque()

queue.append(5)
queue.append(2)
queue.append(3)
queue.popleft()

print(queue)
queue.reverse()
print(queue)
```

## 재귀 함수

재귀 함수란 자기 자신을 다시 호출하는 함수다.
DFS를 구현할 때 사용한다. 재귀 함수는 무한히 호출되기에 재귀 종료 조건을 반드시 명시해야 한다.

```py
# 무한히 호출되는 재귀 함수
def recursive_function():
    print('재귀 함수 호출')
    recursive_function()

recursive_function()
```

재귀함수에 대한 내용은 칸 아카데미 복습하고 블로그에 정리하자
DP 완전정복 책도 참고하면 좋을 것 같다.

```py
# 팩토리얼 구현하기
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

재귀 함수를 잘 활용하면 복잡한 알고리즘을 간결하게 작성할 수 있다.
모든 재귀 함수는 반복문을 이용하여 동일한 기능을 구현할 수 있다.
컴퓨터가 함수를 연속적으로 호출하면 컴퓨터 메모리 내부의 스택 프레임에 쌓인다. 그래서 스택을 사용해야 할 때 구현상 스택 라이브러리 대신에 재귀 함수를 이용하는 경우가 많다.

## DFS

깊이 우선 탐색, 그래프에서 깊은 부분을 우선적으로 탐색

1. 탐색 시작 노드를 스택에 삽입하고 방문 처리를 한다.
2. 스택의 최상단 노드에 방문하지 않은 인접 노드가 있다면 그 노드를 스택에 넣고 방문처리 한다. 방문하지 않은 인접 노드가 없다면 스택에서 최상단 노드를 꺼낸다.
3. 더 이상 2번의 과정을 수행할 수 없을 때까지 반복한다.

```py
def dfs(graph, v, visited):
    visited[v] = True
    print(v, end = ' ')

    for i in graph[v]:
        if not visited[i]:
            dfs(graph, v, visited)

graph = [
    [],
    [2, 3, 8],
    [1, 7],
    [1, 4, 5],
    [3, 5],
    [3, 4],
    [7],
    [2, 6, 8],
    [1, 7]
]

visited = [false] * 9
dfs(graph, 1, visited)
```

## BFS

너비 우선 탐색이라고도 부르며, 그래프에서 가까운 노드부터 우선적으로 탐색하는 알고리즘

1. 탐색 시작 노드를 큐에 삽입하고 방문 처리
2. 큐에서 노드를 꺼낸 뒤에 해당 노드의 인접 노드 중에서 방문하지 않은 노드를 모두 큐에 삽입하고 방문 처리
3. 더 이상 2번의 과정을 수행할 수 없을 때까지 반복

간선의 가중치가 모두 동일한 상황에서 최단 거리을 구하는 알고리즘으로 사용되기도 한다.

```py
from collections import deque

def bfs(graph, start, visited):
    queue = deque([start])
    visited[start] = True

    while queue:
        v = queue.popleft()
        print(v, end = ' ')

        for i in graph[v]:
            if not visited[i]:
                queue.append(i)
                visited = True

graph = [
    [],
    [2, 3, 8],
    [1, 7],
    [1, 4, 5],
    [3, 5],
    [3, 4],
    [7],
    [2, 6, 8],
    [1, 7]
]

visited = [false] * 9
bfs(graph, 1, visited)
```
