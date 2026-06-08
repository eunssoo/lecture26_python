# 계좌 한 개의 정보를 저장하는 클래스
class Account:
    # 생성자
    # Account 객체를 만들 때 계좌번호, 계좌주, 잔액, 비밀번호를 받아서 저장한다.
    def __init__(self, account_no, owner, balance, password):
        self.__account_no = account_no  # 계좌번호
        self.__owner = owner            # 계좌주, 보통 회원 id 또는 이름
        self.__balance = balance        # 계좌 잔액
        self.__password = password      # 계좌 비밀번호

    # 계좌번호를 반환하는 메서드
    def get_account_no(self):
        return self.__account_no

    # 계좌주를 반환하는 메서드
    def get_owner(self):
        return self.__owner

    # 잔액을 반환하는 메서드
    def get_balance(self):
        return self.__balance

    # 계좌 비밀번호를 반환하는 메서드
    # 출금이나 계좌해지 때 비밀번호 확인용으로 사용할 수 있다.
    def get_password(self):
        return self.__password

    # 계좌번호를 수정하는 메서드
    # AccountService에서 계좌번호를 자동 발급할 때 사용할 수 있다.
    def set_account_no(self, account_no):
        self.__account_no = account_no

    # 잔액을 수정하는 메서드
    # 입금, 출금 후 잔액을 변경할 때 사용한다.
    def set_balance(self, balance):
        self.__balance = balance

    # 비밀번호를 수정하는 메서드
    # 나중에 계좌 비밀번호 변경 기능이 생기면 사용할 수 있다.
    def set_password(self, password):
        self.__password = password

    # Account 객체를 print() 했을 때 출력될 문자열을 정한다.
    # 비밀번호는 보안상 출력하지 않는 것이 좋다.
    def __str__(self):
        return f'계좌번호 = {self.__account_no} 계좌주 = {self.__owner} 잔액 = {self.__balance}'


# 이 파일을 직접 실행했을 때만 아래 테스트 코드가 실행된다.
# 다른 파일에서 import할 때는 실행되지 않는다.
if __name__ == '__main__':
    # Account 객체 생성
    ac = Account('111111', '은성수', 10000, '1234')

    # 잔액 변경 테스트
    ac.set_balance(20000)

    # 계좌번호 변경 테스트
    ac.set_account_no('222222')

    # 비밀번호 변경 테스트
    ac.set_password('5678')

    # Account 객체 출력
    print(ac)

    # getter 메서드 테스트
    print(ac.get_account_no())
    print(ac.get_owner())
    print(ac.get_balance())
    print(ac.get_password())
    print(ac)