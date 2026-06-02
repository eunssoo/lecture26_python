# account.py 파일에 있는 Account 클래스를 가져온다.
# AccountDAO는 Account 객체를 저장하고 관리해야 하므로 필요하다.
from XAccount import Account


# 계좌 데이터 접근 클래스
# DAO = Data Access Object
# 역할: 계좌 데이터를 저장, 조회, 수정, 삭제한다.
class AccountDAO:
    def __init__(self):
        # 계좌 정보를 저장할 딕셔너리
        # key   : 계좌번호
        # value : Account 객체
        #
        # 예:
        # {
        #     '111111': Account('111111', 'hyejeong', 10000, '1234'),
        #     '111112': Account('111112', 'curi', 20000, '1234')
        # }
        self.__accountDB = {}

    # 계좌 추가
    def insert_account(self, account):
        # Account 객체에서 계좌번호를 가져온다.
        account_no = account.get_account_no()

        # 같은 계좌번호가 아직 없으면 저장한다.
        if account_no not in self.__accountDB:
            self.__accountDB[account_no] = account
            return True

        # 이미 같은 계좌번호가 있으면 저장 실패
        return False

    # 계좌번호로 계좌 하나 조회
    def select_account_by_account_no(self, account_no):
        # 계좌번호가 딕셔너리에 있으면 해당 Account 객체 반환
        if account_no in self.__accountDB:
            return self.__accountDB[account_no]

        # 없으면 None 반환
        return None

    # 특정 회원 id가 가진 계좌 목록 조회
    def select_accounts_by_member_id(self, member_id):
        # 결과를 담을 리스트
        account_list = []

        # 저장된 모든 계좌 객체를 하나씩 확인한다.
        for account in self.__accountDB.values():
            # 계좌의 owner가 찾는 member_id와 같으면
            if account.get_owner() == member_id:
                # 결과 리스트에 추가한다.
                account_list.append(account)

        # 계좌가 없으면 빈 리스트 []가 반환된다.
        # None보다 []가 안전하다.
        return account_list

    # 전체 계좌 목록 조회
    def select_all_accounts(self):
        # 딕셔너리에 저장된 모든 Account 객체를 리스트로 변환해서 반환한다.
        # 계좌가 하나도 없으면 빈 리스트 []가 반환된다.
        return list(self.__accountDB.values())

    # 계좌 정보 수정
    def update_account(self, account_no, account):
        # 수정하려는 계좌번호가 존재하면
        if account_no in self.__accountDB:
            # 해당 계좌번호 위치에 새로운 Account 객체를 덮어쓴다.
            self.__accountDB[account_no] = account
            return True

        # 계좌번호가 없으면 수정 실패
        return False

    # 계좌 삭제
    def delete_account(self, account_no):
        # 삭제하려는 계좌번호가 존재하면
        if account_no in self.__accountDB:
            # 딕셔너리에서 해당 계좌 삭제
            self.__accountDB.pop(account_no)
            return True

        # 계좌번호가 없으면 삭제 실패
        return False


# 이 파일을 직접 실행했을 때만 아래 테스트 코드가 실행된다.
# 다른 파일에서 import할 때는 실행되지 않는다.
if __name__ == '__main__':
    # AccountDAO 객체 생성
    dao = AccountDAO()

    # 처음에는 계좌가 없으므로 빈 리스트 [] 출력
    ac_list = dao.select_all_accounts()
    print(ac_list)

    # 계좌 3개 추가
    dao.insert_account(Account('111111', 'hyejeong', 10000, '1234'))
    dao.insert_account(Account('111112', 'curi', 20000, '1234'))
    dao.insert_account(Account('111113', 'curi', 200000, '1234'))

    # 전체 계좌 목록 출력
    print('--- 전체 계좌 목록 ---')
    for account in dao.select_all_accounts():
        print(account)

    # 없는 계좌번호 조회
    print('--- 없는 계좌 조회 ---')
    print(dao.select_account_by_account_no('111114'))

    # 특정 회원의 계좌 목록 조회
    print('--- hyejeong 회원의 계좌 목록 ---')
    for account in dao.select_accounts_by_member_id('hyejeong'):
        print(account)

    print()

    # 특정 계좌 조회
    print('--- 수정 전 계좌 조회 ---')
    print(dao.select_account_by_account_no('111112'))

    # 특정 계좌 수정
    dao.update_account('111112', Account('111112', 'curi', 300000, '1234'))

    # 수정 후 계좌 조회
    print('--- 수정 후 계좌 조회 ---')
    print(dao.select_account_by_account_no('111112'))

    print()

    # 특정 계좌 삭제
    dao.delete_account('111113')

    # 삭제된 계좌 조회
    print('--- 삭제 후 계좌 조회 ---')
    print(dao.select_account_by_account_no('111113'))