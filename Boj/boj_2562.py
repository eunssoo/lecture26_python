data = []

for i in range(9):
    num = int(input())
    data.append(num)

max_num = max(data)
print(max_num)

for i in range(9):
    if data[i] == max_num:
        print(i + 1)
