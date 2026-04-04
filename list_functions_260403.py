def getIndex(num_list, target):
    """
    리스트에서 target이 처음 등장하는 index를 반환.
    없으면 -1 반환.
    """
    for i in range(len(num_list)):
        if num_list[i] == target:
            return i
    return -1


def getMax(num_list):
    """
    리스트에서 가장 큰 값을 반환.
    """
    max_value = num_list[0]

    for data in num_list:
        if data > max_value:
            max_value = data

    return max_value


def getMin(num_list):
    """
    리스트에서 가장 작은 값을 반환.
    """
    min_value = num_list[0]

    for data in num_list:
        if data < min_value:
            min_value = data

    return min_value


def countGT(num_list, target):
    """
    리스트에서 target보다 큰 값의 개수를 반환.
    GT = Greater Than
    """
    count = 0

    for data in num_list:
        if data > target:
            count += 1

    return count


def sumList(num_list):
    """
    리스트의 모든 값을 더한 합을 반환.
    """
    total = 0

    for data in num_list:
        total += data

    return total


def swapList(num_list):
    """
    리스트를 제자리에서(in-place) 역순으로 바꿈.
    새 리스트를 만들지 않고 양끝 값을 서로 교환.
    """
    left = 0
    right = len(num_list) - 1

    while left < right:
        num_list[left], num_list[right] = num_list[right], num_list[left]
        left += 1
        right -= 1


if __name__ == "__main__":
    number_list = [23, 45, 27, 11, 25, 65, 78]

    print("원본 리스트:", number_list)

    print("getIndex(number_list, 25) =", getIndex(number_list, 25))
    print("getMax(number_list) =", getMax(number_list))
    print("getMin(number_list) =", getMin(number_list))
    print("countGT(number_list, 42) =", countGT(number_list, 42))
    print("sumList(number_list) =", sumList(number_list))

    swapList(number_list)
    print("swapList(number_list) 실행 후 =", number_list)