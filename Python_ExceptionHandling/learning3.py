# 나눗셈을 수행하는 함수 정의
def divide(x, y):
    try:
        # x를 y로 나눈 결과를 result에 저장
        # y가 0이면 여기서 ZeroDivisionError 발생
        result = x / y

    except ZeroDivisionError:
        # 0으로 나누려고 했을 때 실행
        print('0으로는 나눌 수 없습니다.')

    else:
        # 예외가 발생하지 않았을 때만 실행
        print('결과:', result)


# 정상적인 나눗셈
divide(3.2, 2)

# 0으로 나누는 경우
divide(5.4, 0)

# 결과: 1.6
# 0으로는 나눌 수 없습니다.