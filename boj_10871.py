N, X = map(int, input().split())
data = list(map(int, input().split()))
for x in data:
    if X > x:
        print(x, end=' ')