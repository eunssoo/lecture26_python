# 팩토리얼 함수를 사용하기 위해 math 모듈 가져오기
import math

# 중앙값, 평균, 분산, 표준편차 함수를 사용하기 위해 statistics 모듈 가져오기
import statistics


# 이 파일을 직접 실행했을 때만 아래 코드가 실행된다.
# 다른 파일에서 import될 때는 실행되지 않는다.
if __name__ == '__main__':

    # 1, 6, 11, 16의 팩토리얼 출력
    print('1! =', math.factorial(1))
    print('6! =', math.factorial(6))
    print('11! =', math.factorial(11))
    print('16! =', math.factorial(16))

    # 한 줄 띄우기
    print()

    # 점수 리스트 생성
    st = [80, 99, 77, 65, 92, 74, 82]

    # 리스트 그대로 출력
    print(st)

    # 중앙값 출력
    # median은 데이터를 정렬했을 때 가운데에 있는 값
    print('중앙값: %.2f' % statistics.median(st))

    # 평균 출력
    # mean은 모든 값을 더한 뒤 개수로 나눈 값
    print('평균: %.2f' % statistics.mean(st))

    # 분산 출력
    # variance는 데이터가 평균에서 얼마나 흩어져 있는지 나타내는 값
    print('분산: %.2f' % statistics.variance(st))

    # 표준편차 출력
    # stdev는 분산에 제곱근을 씌운 값
    print('표준편차: %.2f' % statistics.stdev(st))