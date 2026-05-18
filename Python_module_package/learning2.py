# 수학 관련 기능을 사용하기 위해 math 모듈 가져오기
import math

# 난수, 즉 랜덤한 숫자를 만들기 위해 random 모듈 가져오기
import random


# 원의 면적을 계산하는 함수 정의
# r은 원의 반지름을 의미한다.
def get_area(r):
    # 원의 면적 공식: 반지름 * 반지름 * 원주율
    area = r * r * math.pi

    # 계산한 면적을 함수 밖으로 반환
    return area


# random.random()은 0 이상 1 미만의 랜덤 실수를 만든다.
# 여기에 10을 곱하면 0 이상 10 미만의 랜덤 반지름이 된다.
radius = random.random() * 10

# 반지름을 소수점 둘째 자리까지 반올림한다.
radius = round(radius, 2)

# get_area 함수에 반지름을 넣어 원의 면적을 계산한다.
area = get_area(radius)

# 원의 반지름 출력
print('원의 반지름:', radius)

# math.pi에 저장된 원주율 출력
print('원주율 pi:', math.pi)

# 원의 면적을 소수점 둘째 자리까지 출력
print(f'반지름 {radius}인 원의 면적은 {area:.2f}')