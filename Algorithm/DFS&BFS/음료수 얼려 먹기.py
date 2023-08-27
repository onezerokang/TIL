# N x M 크기의 얼음 틀이 있다. 구멍이 뚫려 있는 부분은 0, 칸막이가 존재하는 부분은 1로 표시된다.
# 구멍이 뚫려 있는 부분끼리 상, 하, 좌, 우로 붙어 있는 경우 서로 연결되어 있는 것으로 간주한다.
# 이때 얼음 틀의 모양이 주어졌을 때 생성되는 총 아이스크림의 개수를 구하는 프로그램을 작성하세요.

# 시간 제한: 1초
# 메모리 제한: 128MB

from collections import deque

N, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def dfs(x, y):
    if x < 0 or x >= N or y < 0 or y >= M or graph[x][y] == 1:
        return
    
    graph[x][y] = 1

    for i in range(4):
        nx = dx[i] + x
        ny = dy[i] + y

        dfs(nx, ny)

def bfs(i, j):
    queue = deque([(i, j)])
    graph[i][j] = 1

    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx = dx[i] + x
            ny = dy[i] + y

            if 0 <= nx < N and 0 <= ny < M and graph[nx][ny] == 0:
                queue.append((nx, ny))
                graph[nx][ny] = 1

result = 0

for i in range(N):
    for j in range(M):
        if graph[i][j] == 0:
            # bfs(i, j)
            dfs(i, j)
            result += 1

print(result)