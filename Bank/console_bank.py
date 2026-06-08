# 회원 관련 클래스 import
from member.member import Member
from member.member_dao import MemberDAO
from member.member_service import MemberService

# 계좌 관련 클래스 import
from account.account import Account
from account.account_dao import AccountDAO
from account.account_service import AccountService


# ConsoleBank 클래스
# 역할:
# 1. 메뉴 출력
# 2. 사용자 입력 받기
# 3. MemberService / AccountService 호출
# 4. 결과 메시지 출력
#
# 실제 회원/계좌 규칙 판단은 Service 클래스가 담당한다.
class ConsoleBank:
    # 시작 메뉴
    start_menu = ['종료', '로그인', '회원가입']

    # 일반 회원 로그인 후 은행 업무 메뉴
    banking_menu = ['로그아웃', '계좌목록', '입금', '출금', '계좌생성', '계좌해지', '내정보']

    # 일반 회원의 내 정보 메뉴
    member_myinfo_menu = ['돌아가기', '내정보조회', '비밀번호수정', '회원탈퇴']

    # 관리자 메뉴
    admin_menu = ['로그아웃', '회원관리', '계좌관리']

    # 관리자 계좌 관리 메뉴
    admin_account_menu = ['돌아가기', '전체계좌목록', '회원별계좌목록']

    # 관리자 회원 관리 메뉴
    admin_member_menu = ['돌아가기', '회원목록', '회원정보조회', '회원강퇴']

    # 생성자
    def __init__(self):
        # 회원 기능 처리 서비스
        self.msv = MemberService(MemberDAO())

        # 계좌 기능 처리 서비스
        self.asv = AccountService(AccountDAO())

    # 프로그램 시작 함수
    def main(self):
        self.show_welcome()
        self.run_start_menu()
        self.say_goodbye()

    # 시작 문구 출력
    def show_welcome(self):
        print('=' * 50)
        print(f'{"Sungsoo Console Bank":^50}')
        print('=' * 50)

    # 종료 문구 출력
    def say_goodbye(self):
        print('>> Sungsoo Console Bank를 이용해 주셔서 감사합니다.')

    # 메뉴 출력 후 사용자 선택값 반환
    def select_menu(self, menu_list):
        print('-' * 40)

        # 리스트의 1번 인덱스부터 실제 메뉴로 출력한다.
        for index in range(1, len(menu_list)):
            print(f'{index}. {menu_list[index]}')

        # 리스트의 0번 인덱스는 종료/로그아웃/돌아가기 역할이다.
        print(f'0. {menu_list[0]}')
        print('-' * 40)

        # 사용자가 숫자가 아닌 값을 입력할 수 있으므로 예외 처리
        try:
            menu = int(input('>> 메뉴 : '))
            return menu
        except ValueError:
            return -1

    # 금액 입력 전용 보조 함수
    # 입금액, 출금액, 최초 입금액처럼 숫자로 입력해야 하는 곳에서 사용한다.
    def input_amount(self, message):
        try:
            amount = int(input(message))
            return amount
        except ValueError:
            print('금액은 숫자로 입력해야 합니다.')
            return None

    # =========================
    # 시작 메뉴
    # =========================
    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)

            if menu == 0:
                break
            elif menu == 1:
                self.menu_login()
            elif menu == 2:
                self.menu_join()
            else:
                print('없는 메뉴입니다.')

    # 회원가입
    def menu_join(self):
        print('===== 회원가입 =====')

        user_id = input('>> 아이디 : ')
        password = input('>> 비밀번호 : ')
        name = input('>> 이름 : ')

        # 입력받은 정보로 Member 객체 생성
        member = Member(user_id, password, name)

        # 회원가입 처리는 MemberService에게 맡긴다.
        if self.msv.join(member):
            print('회원가입이 완료되었습니다.')
        else:
            print('회원가입에 실패하였습니다. 이미 존재하는 아이디일 수 있습니다.')

    # 로그인
    def menu_login(self):
        print('===== 로그인 =====')

        user_id = input('>> 아이디 : ')
        password = input('>> 비밀번호 : ')

        # 로그인 처리는 MemberService에게 맡긴다.
        if self.msv.login(user_id, password):
            member = self.msv.view_member_info(user_id)

            if member:
                print(f'{member.get_name()}님 환영합니다.')

            # 관리자 로그인
            if self.msv.current_user == MemberService.ADMIN_ID:
                self.run_admin_menu()

            # 일반 회원 로그인
            else:
                self.run_banking_menu()

        else:
            print('로그인에 실패하였습니다.')

    # 로그아웃
    def menu_logout(self):
        self.msv.logout()
        print('로그아웃되었습니다.')

    # =========================
    # 일반 회원 은행 메뉴
    # =========================
    def run_banking_menu(self):
        print('===== 은행 업무 메뉴 =====')

        while True:
            menu = self.select_menu(ConsoleBank.banking_menu)

            if menu == 0:
                self.menu_logout()
                break
            elif menu == 1:
                self.menu_list_my_accounts()
            elif menu == 2:
                self.menu_deposit()
            elif menu == 3:
                self.menu_withdraw()
            elif menu == 4:
                self.menu_create_account()
            elif menu == 5:
                self.menu_delete_account()
            elif menu == 6:
                self.menu_myinfo()
            else:
                print('없는 메뉴입니다.')

            # 회원탈퇴가 성공하면 current_user가 None이 되므로 회원 메뉴 종료
            if self.msv.current_user is None:
                break

    # 현재 로그인한 회원의 계좌 목록 출력
    def menu_list_my_accounts(self):
        account_list = self.asv.get_members_accounts(self.msv.current_user)

        if not account_list:
            print('등록된 계좌가 없습니다.')
        else:
            print('===== 내 계좌 목록 =====')
            for account in account_list:
                print(account)

    # 입금
    def menu_deposit(self):
        print('===== 입금 =====')

        self.menu_list_my_accounts()

        account_no = input('>> 계좌번호 : ')
        amount = self.input_amount('>> 입금액 : ')

        # 금액 입력이 잘못되면 함수 종료
        if amount is None:
            return

        try:
            # 계좌 소유자 확인과 입금 가능 여부 판단은 AccountService에서 처리한다.
            result = self.asv.deposit(self.msv.current_user, account_no, amount)

        except LookupError:
            print('없는 계좌번호입니다.')

        except PermissionError:
            print('본인의 계좌가 아닙니다.')

        except ValueError:
            print('입금 금액은 0원보다 커야 합니다.')

        else:
            if result:
                print(f'{amount:,}원이 입금되었습니다.')
                print(f'잔액 : {self.asv.get_account_balance(account_no):,}원')
            else:
                print('입금에 실패하였습니다.')

    # 출금
    def menu_withdraw(self):
        print('===== 출금 =====')

        self.menu_list_my_accounts()

        account_no = input('>> 계좌번호 : ')
        amount = self.input_amount('>> 출금액 : ')

        if amount is None:
            return

        password = input('>> 계좌 비밀번호 : ')

        try:
            # 계좌 존재 여부, 소유자 확인, 비밀번호 확인, 잔액 확인은 AccountService에서 처리한다.
            result = self.asv.withdraw(self.msv.current_user, account_no, amount, password)

        except LookupError:
            print('없는 계좌번호입니다.')

        except PermissionError:
            print('본인의 계좌가 아닙니다.')

        except KeyError:
            print('계좌 비밀번호가 일치하지 않습니다.')

        except ValueError:
            print('출금 금액이 잘못되었거나 잔액이 부족합니다.')

        else:
            if result:
                print(f'{amount:,}원이 출금되었습니다.')
                print(f'잔액 : {self.asv.get_account_balance(account_no):,}원')
            else:
                print('출금에 실패하였습니다.')

    # 계좌 생성
    def menu_create_account(self):
        print('===== 계좌 생성 =====')

        password = input('>> 계좌 비밀번호 : ')
        balance = self.input_amount('>> 최초 입금액 : ')

        if balance is None:
            return

        # 계좌번호는 AccountService에서 자동으로 부여하므로 0으로 넣는다.
        account = Account(0, self.msv.current_user, balance, password)

        try:
            result = self.asv.create_account(account)

        except ValueError:
            print('최초 입금액은 0원 이상이어야 합니다.')

        else:
            if result:
                print('계좌가 생성되었습니다.')
                self.menu_list_my_accounts()
            else:
                print('계좌 생성에 실패하였습니다.')

    # 계좌 해지
    def menu_delete_account(self):
        print('===== 계좌 해지 =====')

        self.menu_list_my_accounts()

        account_no = input('>> 해지할 계좌번호 : ')
        password = input('>> 계좌 비밀번호 : ')

        try:
            # 계좌 존재 여부, 소유자 확인, 비밀번호 확인은 AccountService에서 처리한다.
            result = self.asv.delete_account(self.msv.current_user, account_no, password)

        except LookupError:
            print('없는 계좌번호입니다.')

        except PermissionError:
            print('본인의 계좌가 아닙니다.')

        except KeyError:
            print('계좌 비밀번호가 일치하지 않습니다.')

        except ValueError:
            print('잔액이 남아 있어 계좌를 해지할 수 없습니다.')

        else:
            if result:
                print('계좌가 해지되었습니다.')
            else:
                print('계좌 해지에 실패하였습니다.')

    # 내 정보 메뉴 이동
    def menu_myinfo(self):
        self.run_my_info_menu()

    # =========================
    # 내 정보 메뉴
    # =========================
    def run_my_info_menu(self):
        print('===== 내 정보 메뉴 =====')

        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)

            if menu == 0:
                break
            elif menu == 1:
                self.menu_view_myinfo()
            elif menu == 2:
                self.menu_update_password()
            elif menu == 3:
                if self.menu_delete_membership():
                    break
            else:
                print('없는 메뉴입니다.')

            if self.msv.current_user is None:
                break

    # 내 정보 조회
    def menu_view_myinfo(self):
        member = self.msv.view_member_info(self.msv.current_user)

        if member:
            print(member)
        else:
            print('회원 정보를 찾을 수 없습니다.')

    # 비밀번호 수정
    def menu_update_password(self):
        print('===== 비밀번호 수정 =====')

        org_password = input('>> 기존 비밀번호 : ')
        new_password = input('>> 새 비밀번호 : ')

        if self.msv.update_member_password(self.msv.current_user, org_password, new_password):
            print('비밀번호가 변경되었습니다.')
        else:
            print('비밀번호 변경에 실패하였습니다.')

    # 회원 탈퇴
    def menu_delete_membership(self):
        print('===== 회원 탈퇴 =====')

        # 현재 구조에서는 회원 탈퇴 전 계좌가 남아 있는지 ConsoleBank에서 확인한다.
        # 더 정교한 구조에서는 BankService 같은 통합 서비스로 옮길 수 있다.
        account_list = self.asv.get_members_accounts(self.msv.current_user)

        if account_list:
            print('계좌가 남아 있어 회원탈퇴를 할 수 없습니다.')
            print('계좌를 모두 해지한 뒤 다시 시도하세요.')
            return False

        password = input('>> 비밀번호 확인 : ')

        member = self.msv.view_member_info(self.msv.current_user)

        if not member:
            print('회원 정보를 찾을 수 없습니다.')
            return False

        if member.get_password() != password:
            print('비밀번호가 일치하지 않습니다.')
            return False

        if self.msv.remove_member(self.msv.current_user):
            print('회원탈퇴가 완료되었습니다.')
            return True

        print('회원탈퇴에 실패하였습니다.')
        return False

    # =========================
    # 관리자 메뉴
    # =========================
    def run_admin_menu(self):
        print('===== 관리자 메뉴 =====')

        while True:
            menu = self.select_menu(ConsoleBank.admin_menu)

            if menu == 0:
                self.menu_logout()
                break
            elif menu == 1:
                self.menu_manage_members()
            elif menu == 2:
                self.menu_manage_accounts()
            else:
                print('없는 메뉴입니다.')

    # 관리자 회원관리 메뉴 이동
    def menu_manage_members(self):
        self.run_admin_member_menu()

    # 관리자 계좌관리 메뉴 이동
    def menu_manage_accounts(self):
        self.run_admin_account_menu()

    # =========================
    # 관리자 계좌 관리 메뉴
    # =========================
    def run_admin_account_menu(self):
        print('===== 관리자 계좌 관리 메뉴 =====')

        while True:
            menu = self.select_menu(ConsoleBank.admin_account_menu)

            if menu == 0:
                break
            elif menu == 1:
                self.menu_list_all_accounts()
            elif menu == 2:
                self.menu_list_member_accounts()
            else:
                print('없는 메뉴입니다.')

    # 전체 계좌 목록
    def menu_list_all_accounts(self):
        account_list = self.asv.get_all_accounts()

        if not account_list:
            print('등록된 계좌가 없습니다.')
        else:
            print('===== 전체 계좌 목록 =====')
            for account in account_list:
                print(account)

    # 특정 회원 계좌 목록
    def menu_list_member_accounts(self):
        user_id = input('>> 조회할 회원 아이디 : ')

        account_list = self.asv.get_members_accounts(user_id)

        if not account_list:
            print('등록된 계좌가 없습니다.')
        else:
            print(f'===== {user_id} 회원의 계좌 목록 =====')
            for account in account_list:
                print(account)

    # =========================
    # 관리자 회원 관리 메뉴
    # =========================
    def run_admin_member_menu(self):
        print('===== 관리자 회원 관리 메뉴 =====')

        while True:
            menu = self.select_menu(ConsoleBank.admin_member_menu)

            if menu == 0:
                break
            elif menu == 1:
                self.menu_list_members()
            elif menu == 2:
                self.menu_view_member_info()
            elif menu == 3:
                self.menu_delete_member()
            else:
                print('없는 메뉴입니다.')

    # 전체 회원 목록
    def menu_list_members(self):
        member_list = self.msv.list_members()

        if not member_list:
            print('가입한 회원이 없습니다.')
        else:
            print('===== 회원 목록 =====')
            for member in member_list:
                print(member)

    # 특정 회원 정보 조회
    def menu_view_member_info(self):
        user_id = input('>> 조회할 회원 아이디 : ')

        member = self.msv.view_member_info(user_id)

        if member:
            print(member)
        else:
            print('회원 정보를 찾을 수 없습니다.')

    # 관리자 회원 강퇴
    def menu_delete_member(self):
        user_id = input('>> 강퇴할 회원 아이디 : ')

        # 관리자 계정 삭제 금지는 MemberService에도 들어 있어야 한다.
        # 여기서는 사용자에게 명확한 메시지를 보여주기 위해 한 번 더 확인한다.
        if user_id == MemberService.ADMIN_ID:
            print('관리자 계정은 삭제할 수 없습니다.')
            return

        member = self.msv.view_member_info(user_id)

        if not member:
            print('존재하지 않는 회원입니다.')
            return

        # 현재 구조에서는 계좌가 남아 있는 회원은 강퇴하지 못하게 한다.
        account_list = self.asv.get_members_accounts(user_id)

        if account_list:
            print('해당 회원의 계좌가 남아 있어 강퇴할 수 없습니다.')
            print('계좌를 먼저 정리해야 합니다.')
            return

        if self.msv.remove_member(user_id):
            print('강퇴 처리되었습니다.')
        else:
            print('강퇴 처리에 실패하였습니다.')


# 이 파일을 직접 실행했을 때만 실행된다.
if __name__ == '__main__':
    app = ConsoleBank()
    app.main()