N = int(input())
data = list(map(int, input().split()))
v  = int(input())

count = 0
for x in data:
    if x == v:
        count += 1
print(count)
