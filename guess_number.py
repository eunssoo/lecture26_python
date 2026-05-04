# 1. random 기능 준비
import random
# 2. 컴퓨터가 1~50 사이 숫자 정하기
limit = 50
num_try = 7

answer = random.randint(1, limit)
# 3. 성공 여부 변수 만들기
success = False
# 4. 최대 7번 반복하기
for attempt in range (1, num_try +1):
    # 4-1. 사용자 숫자 입력받기
    user_num = int(input(f"{attempt}번째 시도 - 숫자를 맞춰보세요: "))
    # 4-2. 정답과 비교하기
    if user_num == answer:
        # 맞으면 사용자 승리 후 종료
        print("WIN")
        success = True
        break
        # 작으면 up 출력
    elif user_num < answer:
        print("UP")
        # 크면 down 출력
    else:
        print("DOWN")
# 5. 7번 안에 못 맞혔으면 컴퓨터 승리
if success == False:
    print("computer win")