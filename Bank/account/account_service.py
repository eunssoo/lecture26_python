# account/account.py 파일의 Account 클래스를 가져온다.
# AccountService는 Account 객체를 생성하거나 수정할 때 사용한다.
from account.account import Account

# account/account_dao.py 파일의 AccountDAO 클래스를 가져온다.
# 실제 계좌 저장, 조회, 수정, 삭제는 DAO에게 맡긴다.
from account.account_dao import AccountDAO


# 계좌 서비스 클래스
# 역할:
# 1. 계좌 생성
# 2. 전체 계좌 조회
# 3. 회원별 계좌 조회
# 4. 입금
# 5. 출금
# 6. 계좌 해지
# 7. 잔액 조회
#
# DAO는 단순 저장/조회 담당이고,
# Service는 "이 작업을 해도 되는지" 규칙을 판단한다.
class AccountService:
    # 계좌번호 자동 발급용 클래스 변수
    # 계좌를 만들 때마다 이 번호를 계좌번호로 사용하고 1씩 증가시킨다.
    account_no_seq = 111111

    # 생성자
    # AccountService 객체를 만들 때 AccountDAO 객체를 받아서 저장한다.
    def __init__(self, account_dao):
        # 실제 계좌 데이터 접근은 DAO가 담당한다.
        self.__dao = account_dao

    # 계좌 생성
    def create_account(self, account):
        # 최초 입금액이 음수이면 계좌 생성 불가
        # ValueError는 "값이 잘못되었다"는 의미로 사용한다.
        if account.get_balance() < 0:
            raise ValueError

        # 현재 account_no_seq 값을 계좌번호로 설정한다.
        # 계좌번호는 문자열로 저장한다.
        account.set_account_no(str(AccountService.account_no_seq))

        # 다음 계좌 생성을 위해 계좌번호를 1 증가시킨다.
        AccountService.account_no_seq += 1

        # 실제 저장은 DAO에게 맡긴다.
        return self.__dao.insert_account(account)

    # 전체 계좌 목록 조회
    def get_all_accounts(self):
        return self.__dao.select_all_accounts()

    # 특정 회원의 계좌 목록 조회
    def get_members_accounts(self, member_id):
        return self.__dao.select_accounts_by_member_id(member_id)

    # 계좌 소유자 확인
    # 특정 계좌가 특정 회원의 계좌인지 검사한다.
    def is_owner(self, member_id, account_no):
        # 계좌번호로 계좌를 찾는다.
        account = self.__dao.select_account_by_account_no(account_no)

        # 계좌가 없으면 False
        if account is None:
            return False

        # 계좌의 owner와 member_id가 같으면 True, 아니면 False
        return account.get_owner() == member_id

    # 입금
    # 수정 전: deposit(account_no, amount)
    # 수정 후: deposit(member_id, account_no, amount)
    #
    # 이유:
    # 계좌 소유자 확인은 ConsoleBank가 아니라 AccountService에서 처리해야 한다.
    def deposit(self, member_id, account_no, amount):
        # 계좌번호로 계좌를 찾는다.
        account = self.__dao.select_account_by_account_no(account_no)

        # 계좌가 없으면 LookupError 발생
        if account is None:
            raise LookupError

        # 현재 로그인한 회원의 계좌가 아니면 PermissionError 발생
        if account.get_owner() != member_id:
            raise PermissionError

        # 입금 금액이 0 이하이면 ValueError 발생
        if amount <= 0:
            raise ValueError

        # 기존 잔액 + 입금액
        new_balance = account.get_balance() + amount

        # 계좌 객체의 잔액 수정
        account.set_balance(new_balance)

        # 수정된 계좌를 DAO에 다시 저장
        return self.__dao.update_account(account_no, account)

    # 출금
    def withdraw(self, member_id, account_no, amount, password):
        # 계좌번호로 계좌를 찾는다.
        account = self.__dao.select_account_by_account_no(account_no)

        # 계좌가 없으면 LookupError 발생
        if account is None:
            raise LookupError

        # 현재 로그인한 회원의 계좌가 아니면 PermissionError 발생
        if account.get_owner() != member_id:
            raise PermissionError

        # 계좌 비밀번호가 다르면 KeyError 발생
        # 여기서는 "키/비밀번호가 맞지 않음" 의미로 사용한다.
        if account.get_password() != password:
            raise KeyError

        # 출금 금액이 0 이하이면 ValueError 발생
        if amount <= 0:
            raise ValueError

        # 잔액보다 큰 금액을 출금하려 하면 ValueError 발생
        if account.get_balance() < amount:
            raise ValueError

        # 기존 잔액 - 출금액
        new_balance = account.get_balance() - amount

        # 계좌 객체의 잔액 수정
        account.set_balance(new_balance)

        # 수정된 계좌를 DAO에 다시 저장
        return self.__dao.update_account(account_no, account)

    # 계좌 해지
    def delete_account(self, member_id, account_no, password):
        # 계좌번호로 계좌를 찾는다.
        account = self.__dao.select_account_by_account_no(account_no)

        # 계좌가 없으면 LookupError 발생
        if account is None:
            raise LookupError

        # 현재 로그인한 회원의 계좌가 아니면 PermissionError 발생
        if account.get_owner() != member_id:
            raise PermissionError

        # 계좌 비밀번호가 다르면 KeyError 발생
        if account.get_password() != password:
            raise KeyError

        # 잔액이 남아 있으면 계좌 해지 불가
        # 이 조건은 선택 사항이지만, 은행 프로그램 흐름상 자연스럽다.
        if account.get_balance() > 0:
            raise ValueError

        # 실제 삭제는 DAO에게 맡긴다.
        return self.__dao.delete_account(account_no)

    # 계좌 잔액 조회
    def get_account_balance(self, account_no):
        # 계좌번호로 계좌를 찾는다.
        account = self.__dao.select_account_by_account_no(account_no)

        # 계좌가 있으면 잔액 반환
        if account is not None:
            return account.get_balance()

        # 계좌가 없으면 -1 반환
        return -1


# 이 파일을 직접 실행했을 때만 아래 테스트 코드가 실행된다.
# 다른 파일에서 import할 때는 실행되지 않는다.
if __name__ == '__main__':
    # AccountService 객체 생성
    service = AccountService(AccountDAO())

    # 계좌 생성
    # 계좌번호는 AccountService에서 자동으로 부여하므로 0으로 넣는다.
    service.create_account(Account(0, 'sungsoo', 10000, '1234'))
    service.create_account(Account(0, 'sungsoo', 20000, '1234'))
    service.create_account(Account(0, 'sooyaaa', 30000, '1111'))

    # 전체 계좌 목록 출력
    print('--- 전체 계좌 목록 ---')
    for account in service.get_all_accounts():
        print(account)

    # sungsoo 회원의 계좌 목록 출력
    print('--- sungsoo 회원 계좌 목록 ---')
    for account in service.get_members_accounts('sungsoo'):
        print(account)

    # 입금 테스트
    print('--- 입금 테스트 ---')
    try:
        if service.deposit('sungsoo', '111111', 5000):
            print('입금 성공')
            print('잔액:', service.get_account_balance('111111'))
    except Exception as e:
        print(type(e))

    # 출금 테스트
    print('--- 출금 테스트 ---')
    try:
        if service.withdraw('sungsoo', '111111', 3000, '1234'):
            print('출금 성공')
            print('잔액:', service.get_account_balance('111111'))
    except Exception as e:
        print(type(e))

    # 잘못된 비밀번호 출금 테스트
    print('--- 잘못된 비밀번호 출금 테스트 ---')
    try:
        service.withdraw('sungsoo', '111111', 3000, '9999')
    except Exception as e:
        print(type(e))

    # 계좌 해지 테스트
    # 현재 111112 계좌는 잔액이 20000원이므로 바로 해지하면 ValueError가 발생한다.
    print('--- 계좌 해지 테스트 ---')
    try:
        service.delete_account('sungsoo', '111112', '1234')
    except Exception as e:
        print(type(e))

    # 잔액을 0으로 만든 뒤 계좌 해지 테스트
    print('--- 잔액 0원 만든 뒤 계좌 해지 테스트 ---')
    try:
        service.withdraw('sungsoo', '111112', 20000, '1234')

        if service.delete_account('sungsoo', '111112', '1234'):
            print('계좌 해지 성공')
    except Exception as e:
        print(type(e))

    # 최종 전체 계좌 목록 출력
    print('--- 최종 전체 계좌 목록 ---')
    for account in service.get_all_accounts():
        print(account)