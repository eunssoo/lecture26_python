class Student:
    def info(self):
        print('대학: ' + self.univ + ' 이름: ' + self.name)


student = Student()

student.name = '이성실'
student.univ = '한국대학교'

student.info()