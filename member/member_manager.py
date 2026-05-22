from member import Member, MemberDAO, MemberService


class MemberManager:
    START_MENU = ['종료', '로그인', '회원가입']
    ADMIN_MENU = ['로그아웃', '회원목록', '회원정보조회', '회원정보수정', '회원탈퇴']
    MEMBER_MENU = ['로그아웃', '내정보조회', '내정보수정', '회원탈퇴']

    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self):
        self.current_user = None
        self.ms = MemberService(MemberDAO())

        # 관리자 계정 기본 등록
        self.ms.join(Member(MemberManager.ADMIN_ID, MemberManager.ADMIN_PASSWORD, '관리자'))

    def main(self):
        self.show_welcome()

        while True:
            menu = self.select_menu(MemberManager.START_MENU)

            if menu == 0:
                break

            elif menu == 1:  # 로그인
                id = input('>> id : ')
                password = input('>> password : ')

                self.current_user = self.ms.login(id, password)

                if self.current_user:
                    if self.current_user == MemberManager.ADMIN_ID:
                        self.start_admin_menu()
                    else:
                        self.start_member_menu()
                else:
                    print('로그인에 실패하였습니다.')

            elif menu == 2:  # 회원가입
                id = input('>> id : ')
                password = input('>> password : ')
                name = input('>> name : ')

                member = Member(id, password, name)

                if self.ms.join(member):
                    print('회원가입이 완료되었습니다.')
                else:
                    print('회원가입에 실패하였습니다.')

            else:
                print('없는 메뉴입니다.')

        self.say_goodbye()

    def start_admin_menu(self):
        print('---------- 관리자 메뉴 ----------')

        while True:
            menu = self.select_menu(MemberManager.ADMIN_MENU)

            if menu == 0:
                self.current_user = None
                print('로그아웃 되었습니다.')
                break

            elif menu == 1:  # 회원목록
                self.list_all_member()

            elif menu == 2:  # 회원정보조회
                self.search_member()

            elif menu == 3:  # 회원정보수정
                self.update_member_by_admin()

            elif menu == 4:  # 회원탈퇴
                self.delete_member_by_admin()

            else:
                print('없는 메뉴입니다.')

    def start_member_menu(self):
        print('---------- 회원 메뉴 ----------')

        while True:
            menu = self.select_menu(MemberManager.MEMBER_MENU)

            if menu == 0:
                self.current_user = None
                print('로그아웃 되었습니다.')
                break

            elif menu == 1:  # 내정보조회
                self.show_my_info()

            elif menu == 2:  # 내정보수정
                self.update_my_info()

            elif menu == 3:  # 회원탈퇴
                self.withdraw_member()
                break

            else:
                print('없는 메뉴입니다.')

    # ========================
    # 관리자 기능
    def list_all_member(self):
        if self.current_user != MemberManager.ADMIN_ID:
            print('사용 권한이 없습니다.')
            return

        member_list = self.ms.list_members()

        normal_members = [
            member for member in member_list
            if member.get_id() != MemberManager.ADMIN_ID
        ]

        if len(normal_members) == 0:
            print('가입한 회원이 없습니다.')
        else:
            print('---------- 회원 목록 ----------')
            for member in normal_members:
                print(member)

    def search_member(self):
        if self.current_user != MemberManager.ADMIN_ID:
            print('사용 권한이 없습니다.')
            return

        id = input('조회할 회원 id : ')

        if id == MemberManager.ADMIN_ID:
            print('관리자 계정은 조회 대상에서 제외합니다.')
            return

        member = self.ms.get_member_info(id)

        if member:
            print('---------- 회원 정보 ----------')
            print(member)
        else:
            print('해당 회원이 없습니다.')

    def update_member_by_admin(self):
        if self.current_user != MemberManager.ADMIN_ID:
            print('사용 권한이 없습니다.')
            return

        id = input('수정할 회원 id : ')

        if id == MemberManager.ADMIN_ID:
            print('관리자 계정은 수정할 수 없습니다.')
            return

        member = self.ms.get_member_info(id)

        if member is None:
            print('해당 회원이 없습니다.')
            return

        print('현재 회원 정보')
        print(member)

        new_password = input('새 비밀번호 입력, 변경하지 않으려면 Enter : ')
        new_name = input('새 이름 입력, 변경하지 않으려면 Enter : ')

        if self.ms.update_member(id, new_password, new_name):
            print('회원정보가 수정되었습니다.')
        else:
            print('회원정보 수정에 실패하였습니다.')

    def delete_member_by_admin(self):
        if self.current_user != MemberManager.ADMIN_ID:
            print('사용 권한이 없습니다.')
            return

        id = input('탈퇴시킬 회원 id : ')

        if id == MemberManager.ADMIN_ID:
            print('관리자 계정은 삭제할 수 없습니다.')
            return

        member = self.ms.get_member_info(id)

        if member is None:
            print('해당 회원이 없습니다.')
            return

        print('삭제 대상 회원')
        print(member)

        answer = input('정말 삭제하시겠습니까? y/n : ')

        if answer.lower() == 'y':
            if self.ms.delete_member(id):
                print('회원탈퇴가 완료되었습니다.')
            else:
                print('회원탈퇴에 실패하였습니다.')
        else:
            print('회원탈퇴를 취소했습니다.')

    # ========================
    # 일반 회원 기능
    def show_my_info(self):
        member = self.ms.get_member_info(self.current_user)

        if member:
            print('---------- 내 정보 ----------')
            print(member)
        else:
            print('회원 정보를 찾을 수 없습니다.')

    def update_my_info(self):
        member = self.ms.get_member_info(self.current_user)

        if member is None:
            print('회원 정보를 찾을 수 없습니다.')
            return

        print('현재 내 정보')
        print(member)

        new_password = input('새 비밀번호 입력, 변경하지 않으려면 Enter : ')
        new_name = input('새 이름 입력, 변경하지 않으려면 Enter : ')

        if self.ms.update_member(self.current_user, new_password, new_name):
            print('내 정보가 수정되었습니다.')
        else:
            print('내 정보 수정에 실패하였습니다.')

    def withdraw_member(self):
        if self.current_user == MemberManager.ADMIN_ID:
            print('관리자 계정은 탈퇴할 수 없습니다.')
            return

        answer = input('정말 탈퇴하시겠습니까? y/n : ')

        if answer.lower() == 'y':
            if self.ms.delete_member(self.current_user):
                print('회원탈퇴가 완료되었습니다.')
                self.current_user = None
            else:
                print('회원탈퇴에 실패하였습니다.')
        else:
            print('회원탈퇴를 취소했습니다.')

    # ========================
    # 화면 출력 관련 기능
    def show_welcome(self):
        print('=' * 50)
        title = 'Member Manager'
        print(f'{title:^50}')
        print('=' * 50)

    def say_goodbye(self):
        print('프로그램을 종료합니다.')

    def print_menu(self, menu_list):
        print('-' * 40)

        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}')

        print(f'0. {menu_list[0]}')

    def select_menu(self, menu_list):
        self.print_menu(menu_list)

        try:
            menu = int(input('메뉴 선택 : '))
            return menu
        except ValueError:
            return -1


if __name__ == '__main__':
    manager = MemberManager()
    manager.main()