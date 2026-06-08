# account/account.py 파일의 Account 클래스를 가져온다.
# AccountService는 Account 객체를 생성하거나 수정할 때 사용한다.
from account.account import Account

# account/account_dao.py 파일의 AccountDAO 클래스를 가져온다.
# AccountService는 실제 데이터 저장/조회/수정/삭제를 DAO에게 맡긴다.
from account.account_dao import AccountDAO


# 계좌 서비스 클래스
# 역할: 계좌 생성, 입금, 출금, 계좌 해지 같은 실제 기능 규칙을 처리한다.
class AccountService:
    # 계좌번호 자동 발급용 클래스 변수
    # 새 계좌를 만들 때마다 1씩 증가시켜 계좌번호로 사용한다.
    account_no_seq = 111111

    # 생성자
    # AccountService 객체를 만들 때 AccountDAO 객체를 받아서 저장한다.
    def __init__(self, account_dao):
        self.__dao = account_dao

    # 계좌 생성
    def create_account(self, account):
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

    # 입금
    def deposit(self, account_no, amount):
        # 계좌번호로 계좌를 찾는다.
        account = self.__dao.select_account_by_account_no(account_no)

        # 계좌가 없으면 입금 실패
        if account is None:
            return False

        # 입금 금액이 0 이하이면 실패
        if amount <= 0:
            return False

        # 기존 잔액 + 입금 금액
        new_balance = account.get_balance() + amount

        # 계좌 객체의 잔액 수정
        account.set_balance(new_balance)

        # 수정된 계좌를 DAO에 다시 저장
        return self.__dao.update_account(account_no, account)

    # 출금
    def withdraw(self, member_id, account_no, amount, password):
        # 계좌번호로 계좌를 찾는다.
        account = self.__dao.select_account_by_account_no(account_no)

        # 계좌가 없으면 출금 실패
        if account is None:
            return False

        # 현재 로그인한 회원과 계좌 주인이 다르면 출금 실패
        if account.get_owner() != member_id:
            return False

        # 계좌 비밀번호가 다르면 출금 실패
        if account.get_password() != password:
            return False

        # 출금 금액이 0 이하이면 실패
        if amount <= 0:
            return False

        # 잔액보다 큰 금액을 출금하려 하면 실패
        if account.get_balance() < amount:
            return False

        # 기존 잔액 - 출금 금액
        new_balance = account.get_balance() - amount

        # 계좌 객체의 잔액 수정
        account.set_balance(new_balance)

        # 수정된 계좌를 DAO에 다시 저장
        return self.__dao.update_account(account_no, account)

    # 계좌 해지
    def delete_account(self, member_id, account_no, password):
        # 계좌번호로 계좌를 찾는다.
        account = self.__dao.select_account_by_account_no(account_no)

        # 계좌가 없으면 삭제 실패
        if account is None:
            return False

        # 현재 로그인한 회원과 계좌 주인이 다르면 삭제 실패
        if account.get_owner() != member_id:
            return False

        # 계좌 비밀번호가 다르면 삭제 실패
        if account.get_password() != password:
            return False

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
if __name__ == '__main__':
    # AccountService 객체 생성
    # AccountService는 AccountDAO를 사용해야 하므로 AccountDAO 객체를 넣어준다.
    service = AccountService(AccountDAO())

    # 계좌 생성
    # account_no는 AccountService에서 자동으로 넣어주므로 처음에는 0으로 둔다.
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
    if service.deposit('111111', 5000):
        print('입금 성공')
    else:
        print('입금 실패')

    print(service.get_account_balance('111111'))

    # 출금 테스트
    print('--- 출금 테스트 ---')
    if service.withdraw('sungsoo', '111111', 3000, '1234'):
        print('출금 성공')
    else:
        print('출금 실패')

    print(service.get_account_balance('111111'))

    # 잘못된 비밀번호로 출금 테스트
    print('--- 잘못된 비밀번호 출금 테스트 ---')
    if service.withdraw('sungsoo', '111111', 3000, '9999'):
        print('출금 성공')
    else:
        print('출금 실패')

    # 계좌 해지 테스트
    print('--- 계좌 해지 테스트 ---')
    if service.delete_account('sungsoo', '111112', '1234'):
        print('계좌 해지 성공')
    else:
        print('계좌 해지 실패')

    # 해지 후 전체 계좌 목록 출력
    print('--- 해지 후 전체 계좌 목록 ---')
    for account in service.get_all_accounts():
        print(account)