# 1 문자열 '30f'를 실수(float)로 바꾸려고 시도
try:
    f = float('30f')

# 오류가 발생하면 Exception 객체를 e에 저장
except Exception as e:
    print(type(e))   # 발생한 예외 클래스 출력

# 실행결과는 <class 'ValueError'>
# '30f'는 숫자 형태가 아니므로 float() 변환이 불가능하다.

# 2 딕셔너리에서 'foot'이라는 key로 값을 찾으려고 시도
try:
    {'fb': 11, 'bb': 9, 'vb': 6}['foot']

# 오류가 발생하면 Exception 객체를 e에 저장
except Exception as e:
    print(type(e))   # 발생한 예외 클래스 출력

# 실행결과는 <class 'KeyError'>
# 딕셔너리에 'foot'이라는 key가 없다.

# 3 리스트에서 index 3 위치의 값을 꺼내려고 시도
try:
    [1, 2, 3][3]

# 오류가 발생하면 Exception 객체를 e에 저장
except Exception as e:
    print(type(e))   # 발생한 예외 클래스 출력

# 실행결과는 <class 'IndexError'>
# 리스트 [1, 2, 3]의 인덱스는 0, 1, 2까지만 있다. 3번 인덱스는 없다.

# 4 문자열과 정수를 더하려고 시도
try:
    pl = 'python' + 3

# 오류가 발생하면 Exception 객체를 e에 저장
except Exception as e:
    print(type(e))   # 발생한 예외 클래스 출력

# 실행결과는 <class 'TypeError'>
# 문자열 'python'과 정수 3은 +로 바로 더할 수 없다.