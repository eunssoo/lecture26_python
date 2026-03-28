# N = int(input())
# for i in range(1,10):
#     print(N, "*", i, "=", N * i)

# ,를 빼먹지 말것
# 피드백 f-string 사용하기

N = int(input())

for i in range(1, 10):
    print(f"{N} * {i} = {N * i}")