# Car 클래스 정의
class Car:

    # 생성자 메서드
    # 객체를 만들 때 회사명, 연식, 색상을 받아 저장한다.
    def __init__(self, company, year, color):
        self.company = company  # 자동차 회사 저장
        self.year = year        # 자동차 연식 저장
        self.color = color      # 자동차 색상 저장

    # 문자열화 메서드
    # print(mycar)를 했을 때 출력될 문자열을 정한다.
    def __str__(self):
        return f'자동차 회사: {self.company}, 년식: {self.year}, 색상: {self.color}'

    # 동등 비교 메서드
    # mycar == yourcar 를 실행했을 때 호출된다.
    def __eq__(self, other):
        # 회사, 연식, 색상이 모두 같으면 True
        # 하나라도 다르면 False
        return self.company == other.company and self.year == other.year and self.color == other.color


# Car 객체 생성
# mycar는 현대, 2020년식, 검정색 자동차
mycar = Car('현대', 2020, '검정')

# yourcar는 기아, 2021년식, 백색 자동차
yourcar = Car('기아', 2021, '백색')

# mycar 객체 출력
# 내부적으로 mycar.__str__()이 호출된다.
print(mycar)

# yourcar 객체 출력
# 내부적으로 yourcar.__str__()이 호출된다.
print(yourcar)

# 두 객체가 같은지 비교
# 내부적으로 mycar.__eq__(yourcar)가 호출된다.
print(mycar == yourcar)