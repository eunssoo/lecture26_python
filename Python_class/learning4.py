# Student 클래스 정의
class Student:

    # 생성자 메서드
    # 객체를 만들 때 이름, 학과, 중간점수, 기말점수를 받아 저장한다.
    def __init__(self, name, dept, mid, final):
        self.name = name      # 객체의 이름 속성에 name 저장
        self.dept = dept      # 객체의 학과 속성에 dept 저장
        self.mid = mid        # 객체의 중간점수 속성에 mid 저장
        self.final = final    # 객체의 기말점수 속성에 final 저장

    # 문자열화 메서드
    # print(student)를 했을 때 출력될 문자열을 정한다.
    def __str__(self):
        return f'학과: {self.dept}, 이름: {self.name}, 중간: {self.mid}, 기말: {self.final}'

    # 학점을 계산하는 메서드
    def grade(self):
        # 중간점수와 기말점수의 평균 계산
        avg = (self.mid + self.final) / 2

        # 평균이 90 이상이면 A
        if avg >= 90:
            return 'A'

        # 평균이 80 이상이면 B
        elif avg >= 80:
            return 'B'

        # 평균이 70 이상이면 C
        elif avg >= 70:
            return 'C'

        # 평균이 60 이상이면 D
        elif avg >= 60:
            return 'D'

        # 위 조건에 모두 해당하지 않으면 F
        else:
            return 'F'


# Student 객체 생성
# 이름: 김정철, 학과: 기계학과, 중간점수: 89, 기말점수: 90
student = Student('김정철', '기계학과', 89, 90)

# student 객체 출력
# __str__ 메서드가 자동으로 호출된다.
print(student)

# grade() 메서드를 호출해서 학점을 출력한다.
print('학점:', student.grade())