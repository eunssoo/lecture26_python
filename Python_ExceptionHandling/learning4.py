# 학년 번호를 key로, 영어 학년명을 value로 저장한 딕셔너리
uyear = {
    1: 'freshman',
    2: 'sophomore',
    3: 'junior',
    4: 'senior'
}

try:
    # 사용자에게 학년을 입력받고 정수로 변환
    year = int(input('대학교 몇 학년이지요? '))

    # 1~4 사이가 아니면 직접 예외 발생
    if year < 1 or year > 4:
        raise Exception('1~4 정수를 입력하세요.')

    # 정상 입력이면 딕셔너리에서 해당 학년명 출력
    print(f'{year}학년: {uyear[year]}')

except Exception as e:
    # 예외 클래스 이름 출력
    print('예외 발생 이름:', type(e))

    # 예외 메시지 출력
    print('예외 발생 이유:', e)

finally:
    # 예외 발생 여부와 상관없이 항상 실행
    print('예외 처리가 잘되는군요!')