# member/member.py 파일에 있는 Member 클래스를 가져온다.
# 회원가입할 때 Member 객체를 생성해야 하므로 필요하다.
from member.member import Member

# member/member_dao.py 파일에 있는 MemberDAO 클래스를 가져온다.
# MemberService가 사용할 회원 저장소 역할이다.
from member.member_dao import MemberDAO

# member/member_service.py 파일에 있는 MemberService 클래스를 가져온다.
# 로그인, 회원가입, 회원조회, 회원탈퇴 같은 기능을 처리한다.
from member.member_service import MemberService


# 회원관리 프로그램의 메뉴와 사용자 입력을 담당하는 클래스
class MemberManager:
    # 시작 메뉴
    # 리스트의 0번은 항상 종료/로그아웃/돌아가기 역할로 사용한다.
    start_menu = ['종료', '로그인', '회원가입']

    # 관리자 로그인 후 메뉴
    admin_menu = ['로그아웃', '회원목록', '회원정보조회', '회원탈퇴']

    # 일반 회원 로그인 후 메뉴
    member_menu = ['로그아웃', '내정보조회', '내정보수정', '회원탈퇴']

    # 생성자
    def __init__(self):
        # MemberService 객체 생성
        # MemberService는 MemberDAO가 필요하므로 MemberDAO 객체를 넣어준다.
        # 이것을 의존성 주입이라고 볼 수 있다.
        self.ms = MemberService(MemberDAO())

    # 프로그램의 시작 함수
    def main(self):
        self.show_welcome()

        while True:
            # 시작 메뉴 출력 후 사용자 선택 입력
            menu = self.select_menu(MemberManager.start_menu)

            if menu == 0:
                # 0번: 종료
                break

            elif menu == 1:
                # 1번: 로그인
                self.menu_login()

            elif menu == 2:
                # 2번: 회원가입
                self.menu_join()

            else:
                print('없는 메뉴입니다.')

        self.say_goodbye()

    # 로그인 메뉴
    def menu_login(self):
        id = input('>> id : ')
        password = input('>> password : ')

        # MemberService의 login()을 호출해서 로그인 처리
        if self.ms.login(id, password):
            # 로그인한 사용자가 관리자라면 관리자 메뉴로 이동
            if self.ms.current_user == MemberService.ADMIN_ID:
                self.start_admin_menu()

            # 일반 회원이면 회원 메뉴로 이동
            else:
                self.start_member_menu()

        else:
            print('로그인에 실패하였습니다.')

    # 회원가입 메뉴
    def menu_join(self):
        id = input('>> id : ')
        password = input('>> password : ')
        name = input('>> name : ')

        # 입력받은 정보로 Member 객체 생성
        member = Member(id, password, name)

        # MemberService의 join()을 호출해서 회원가입 처리
        if self.ms.join(member):
            print('회원가입이 완료되었습니다.')
        else:
            print('회원가입에 실패하였습니다.')

    # 관리자 메뉴 실행
    def start_admin_menu(self):
        print('---------- 관리자 메뉴 ----------')

        while True:
            menu = self.select_menu(MemberManager.admin_menu)

            if menu == 0:
                # 0번: 로그아웃
                self.menu_logout()
                break

            elif menu == 1:
                # 회원목록
                self.menu_member_list()

            elif menu == 2:
                # 회원정보조회
                self.menu_member_info()

            elif menu == 3:
                # 회원탈퇴, 즉 관리자에 의한 회원 강퇴
                self.menu_member_remove()

            else:
                print('없는 메뉴입니다.')

    # 관리자 전용 회원목록 출력
    def menu_member_list(self):
        # 관리자만 회원목록을 볼 수 있게 권한 확인
        if self.ms.current_user != MemberService.ADMIN_ID:
            print('사용 권한이 없습니다.')
            return

        member_list = self.ms.list_members()

        # 관리자 계정을 제외한 일반 회원만 따로 모은다.
        normal_members = []

        for member in member_list:
            if member.get_id() != MemberService.ADMIN_ID:
                normal_members.append(member)

        if len(normal_members) == 0:
            print('가입한 회원이 없습니다.')
        else:
            for member in normal_members:
                print(member)

    # 관리자 전용 회원정보조회 메뉴
    def menu_member_info(self):
        id = input('>> 조회할 id : ')
        self.view_member_info(id)

    # 관리자 전용 회원탈퇴, 회원강퇴 메뉴
    def menu_member_remove(self):
        id = input('>> 탈퇴 처리할 id : ')

        if self.ms.remove_member(id):
            print('탈퇴 처리되었습니다.')
        else:
            print('회원 탈퇴 처리에 실패하였습니다.')

    # 로그아웃
    def menu_logout(self):
        self.ms.logout()
        print('로그아웃되었습니다.')

    # 일반 회원 메뉴 실행
    def start_member_menu(self):
        print('---------- 회원 메뉴 ----------')

        while True:
            menu = self.select_menu(MemberManager.member_menu)

            if menu == 0:
                # 0번: 로그아웃
                self.menu_logout()
                break

            elif menu == 1:
                # 내정보조회
                self.menu_view_my_info()

            elif menu == 2:
                # 내정보수정, 현재는 비밀번호 수정
                self.menu_update_my_info()

            elif menu == 3:
                # 회원탈퇴
                # 탈퇴 성공 시 current_user가 None이 되므로 메뉴를 빠져나간다.
                if self.menu_remove_member():
                    break

            else:
                print('없는 메뉴입니다.')

    # 내 정보 조회
    def menu_view_my_info(self):
        self.view_member_info(self.ms.current_user)

    # 회원 정보 조회 공통 함수
    # 관리자도 사용하고, 일반 회원도 사용한다.
    def view_member_info(self, id):
        member = self.ms.view_member_info(id)

        if member:
            print(member)
        else:
            print('없는 id입니다.')

    # 내 정보 수정
    # 현재는 비밀번호 수정만 처리한다.
    def menu_update_my_info(self):
        print('---- 비밀번호 변경 ----')

        org_password = input('기존 패스워드 : ')
        new_password = input('새 패스워드 : ')

        if self.ms.update_member_password(self.ms.current_user, org_password, new_password):
            print('비밀번호를 수정하였습니다.')
        else:
            print('비밀번호 수정에 실패하였습니다.')

    # 일반 회원 탈퇴
    def menu_remove_member(self):
        print('---- 회원 탈퇴 ----')

        password = input('비밀번호 확인 : ')

        # 현재 로그인한 회원 정보 조회
        member = self.ms.view_member_info(self.ms.current_user)

        # 회원 정보가 없으면 실패
        if not member:
            print('회원 정보를 찾을 수 없습니다.')
            return False

        # 비밀번호가 틀리면 탈퇴 실패
        if member.get_password() != password:
            print('비밀번호가 일치하지 않습니다.')
            return False

        # 비밀번호가 맞으면 탈퇴 처리
        if self.ms.remove_member(self.ms.current_user):
            print('회원탈퇴가 완료되었습니다.')
            return True

        print('회원탈퇴에 실패하였습니다.')
        return False

    # 시작 문구 출력
    def show_welcome(self):
        print('=' * 50)
        title = 'Sungsoo Member Manager'
        print(f'{title:^50}')
        print('=' * 50)

    # 종료 문구 출력
    def say_goodbye(self):
        print('Sungsoo Member Manager를 사용해주셔서 감사합니다.')
        print('안녕히 가세요')

    # 메뉴 출력
    def print_menu(self, menu_list):
        print('-' * 40)

        # 1번부터 마지막 메뉴까지 출력
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}')

        # 0번 메뉴는 마지막에 출력
        print(f'0. {menu_list[0]}')
        print('-' * 40)

    # 메뉴 선택 입력
    def select_menu(self, menu_list):
        self.print_menu(menu_list)

        try:
            menu = int(input('메뉴 선택 : '))
            return menu

        except ValueError:
            # 숫자가 아닌 값을 입력하면 -1 반환
            return -1


# 이 파일을 직접 실행했을 때만 실행된다.
if __name__ == '__main__':
    app = MemberManager()
    app.main()