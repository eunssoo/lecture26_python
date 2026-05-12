# 회원 한 명의 정보를 저장하는 클래스
class Member:
    # 생성자: 회원 객체를 만들 때 필요한 정보를 받는다.
    def __init__(self, member_no, user_id, password, name, phone, address):
        self.member_no = member_no  # 회원번호
        self.user_id = user_id      # 아이디
        self.password = password    # 비밀번호
        self.name = name            # 이름
        self.phone = phone          # 전화번호
        self.address = address      # 주소

    # print(member)를 했을 때 출력될 문자열을 정한다.
    def __str__(self):
        return f'회원번호: {self.member_no}, 아이디: {self.user_id}, 이름: {self.name}, 전화번호: {self.phone}, 주소: {self.address}'


# 회원 목록을 관리하는 서비스 클래스
class MemberService:
    def __init__(self):
        # Member 객체들을 저장할 리스트
        self.member_list = []

    # 회원가입
    def join(self, member):
        self.member_list.append(member)
        print('회원가입이 완료되었습니다.')

    # 회원목록 출력
    def list_members(self):
        if len(self.member_list) == 0:
            print('등록된 회원이 없습니다.')
            return

        for member in self.member_list:
            print(member)

    # 회원상세정보
    def detail_member(self, user_id):
        for member in self.member_list:
            if member.user_id == user_id:
                print(member)
                return

        print('해당 아이디의 회원이 없습니다.')

    # 회원정보수정
    def update_member(self, user_id, phone, address):
        for member in self.member_list:
            if member.user_id == user_id:
                member.phone = phone
                member.address = address
                print('회원정보가 수정되었습니다.')
                return

        print('해당 아이디의 회원이 없습니다.')

    # 회원탈퇴
    def delete_member(self, user_id):
        for member in self.member_list:
            if member.user_id == user_id:
                self.member_list.remove(member)
                print('회원탈퇴가 완료되었습니다.')
                return

        print('해당 아이디의 회원이 없습니다.')


# 회원 관리 기능을 담당할 객체 생성
service = MemberService()

# 메뉴 반복 실행
while True:
    print('\n===== 회원 관리 프로그램 =====')
    print('1. 회원가입')
    print('2. 회원목록')
    print('3. 회원상세정보')
    print('4. 회원정보수정')
    print('5. 회원탈퇴')
    print('0. 종료')

    menu = input('메뉴 선택: ')

    if menu == '1':
        member_no = input('회원번호: ')
        user_id = input('아이디: ')
        password = input('비밀번호: ')
        name = input('이름: ')
        phone = input('전화번호: ')
        address = input('주소: ')

        member = Member(member_no, user_id, password, name, phone, address)
        service.join(member)

    elif menu == '2':
        service.list_members()

    elif menu == '3':
        user_id = input('조회할 아이디: ')
        service.detail_member(user_id)

    elif menu == '4':
        user_id = input('수정할 아이디: ')
        phone = input('새 전화번호: ')
        address = input('새 주소: ')
        service.update_member(user_id, phone, address)

    elif menu == '5':
        user_id = input('탈퇴할 아이디: ')
        service.delete_member(user_id)

    elif menu == '0':
        print('프로그램을 종료합니다.')
        break

    else:
        print('잘못된 메뉴입니다.')