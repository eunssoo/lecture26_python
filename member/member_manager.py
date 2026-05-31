from member import Member
from member_dao import MemberDAO
from member_service import MemberService

class MemberManager:
    start_menu = ['종료', '로그인', '회원가입']
    admin_menu = ['로그아웃', '회원목록', '회원정보조회', '회원탈퇴']
    member_menu = ['로그아웃', '내정보조회', '내정보수정', '회원탈퇴']

    def __init__(self):
        self.ms = MemberService(MemberDAO()) # DB에 대한 의존성 주입

    def main(self):
        self.show_welcome()
        # 테스트용
        # self.ms.join(Member('hyejeong', '1234', '이혜정'))
        # self.ms.join(Member('curi', '1234', '큐리'))
        while True:
            menu = self.select_menu(MemberManager.start_menu)
            if menu == 0: break
            elif menu == 1: # 로그인
                self.menu_login()
            elif menu == 2: # 회원가입
                self.menu_join()
            else:
                print('없는 메뉴입니다.')
        self.say_goodbye()

    def menu_login(self):
        id = input('>> id : ')
        password = input('>> password : ')
        
        if self.ms.login(id, password):
            if self.ms.current_user == MemberService.ADMIN_ID:
                self.start_admin_menu()
            else:
                self.start_member_menu()
        else:
            print('로그인에 실패하였습니다.')

    def menu_join(self):
        id = input('>> id : ')
        password = input('>> password : ')
        name = input('>> name : ')
        member = Member(id, password, name)
        if self.ms.join(member):
            print('회원가입이 완료되었습니다.')
        else:
            print('회원가입에 실패하였습니다.')
        
    def start_admin_menu(self):
        print('---------- 관리자 메뉴 ----------')
        while True:
            menu = self.select_menu(MemberManager.admin_menu)
            if menu == 0: break
            elif menu == 1: # 회원목록
                self.menu_member_list()
            elif menu == 2: # 회원정보조회
                self.menu_member_info()
            elif menu == 3: # 회원강퇴
                self.menu_member_remove()
            elif menu == 4: # 로그아웃
                self.menu_logout()
                break
            else:
                print('없는 메뉴입니다.')

    def menu_member_list(self):
        print(self.ms.current_user)
        if self.ms.current_user != MemberService.ADMIN_ID:
            print('사용 권한이 없습니다.')
            return
        
        member_list = self.ms.list_members()
        if len(member_list) <= 1:
            print('가입한 회원이 없습니다.')
        else:
            for member in member_list[1:]:
                print(member)

    def menu_member_info(self):
        id = input(">> id : ")
        self.view_member_info(id)

    def menu_member_remove(self):
        id = input(">> id : ")
        if self.ms.remove_member(id):
            print('탈퇴 처리되었습니다.')
        else:
            print('회원 탈퇴 처리에 실패하였습니다.')

    def menu_logout(self):
        self.ms.logout()

    def start_member_menu(self):
        print('---------- 회원 메뉴 ----------')
        while True:
            menu = self.select_menu(MemberManager.member_menu)
            if menu == 0: break
            elif menu == 1:
                self.menu_view_my_info()
            elif menu == 2:
                self.menu_update_my_info()
            elif menu == 3:
                self.menu_remove_member()
            elif menu == 4:
                self.menu_logout()

    def menu_view_my_info(self):
        self.view_member_info(self.ms.current_user)

    def view_member_info(self, id):
        member = self.ms.view_member_info(id)
        if member: print(member)
        else:
            print('없는 id입니다.')

    def menu_update_my_info(self):
        print('---- 비밀번호 변경 ----')
        org_password = input('기존 패스워드 : ')
        new_password = input('새 패스워트 : ')
        if self.ms.update_member_password(self.ms.current_user, org_password, new_password):
            print('비밀번호를 수정하였습니다.')
        else:
            print('비밀번호 수정에 실패하였습니다.')

    def menu_remove_member(self):
        pass

    def show_welcome(self):
        print('=' * 50)
        title = 'Hyejeong Member Manager'
        print(f'{title:^50}')
        print('=' * 50)

    def say_goodbye(self):
        print('Hyejeong Member Manager를 사용해주셔서 감사합니다.')
        print('안녕히 가세요')

    def print_menu(self, menu_list):
        print('-' * 40)
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}')
        print(f'0. {menu_list[0]}')
        print('-' * 40)

    def select_menu(self, menu_list):
        self.print_menu(menu_list)
        try:
            menu = int(input('메뉴 선택 : '))
            return menu
        except ValueError:
            return -1

if __name__ == '__main__':
    app = MemberManager()
    app.main()