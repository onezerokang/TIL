# 각 자리가 숫자(0부터 9)로만 이루어진 문자열 S가 주어졌을 때, 왼쪽부터 오른쪽으로 하나씩 모든 숫자를
# 확인하며 숫자 사이에 'x' 혹은 '+'를 연산자를 넣어 결과적으로 만들 수 있는 가장 큰 수를 구하는
# 프로그램을 작성하세요. 단 모든 연산은 왼쪽에서부터 순서대로 이루어진다고 가정합니다.

# 시간 제한: 1초
# 메모리 제한 128MB

# 0, 1이면 더하기를
# 다른 숫자면 곱하기를 하는게 최적의 해
# 두 수 중에서 하나라도 1미만이라면 더하기 수행

S = input()

result = 0

for i in range(len(S)):
    num = int(S[i])
    if num <= 1 or result <= 1:
        result += num
    else:
        result *= num

print(result)
