# 회원 한 명의 정보를 저장하는 클래스
class Member:
    def __init__(self, member_no, user_id, password, name, phone, address):
        self.member_no = member_no
        self.user_id = user_id
        self.password = password
        self.name = name
        self.phone = phone
        self.address = address

    def __str__(self):
        return f'회원번호: {self.member_no}, 아이디: {self.user_id}, 이름: {self.name}, 전화번호: {self.phone}, 주소: {self.address}'


# 회원 목록을 관리하는 서비스 클래스
class MemberService:
    def __init__(self):
        self.member_list = []

    # 아이디로 회원을 찾는 메서드
    # 회원이 있으면 Member 객체를 반환하고, 없으면 None을 반환한다.
    def find_member(self, user_id):
        for member in self.member_list:
            if member.user_id == user_id:
                return member

        return None

    # 회원가입
    def join(self, member):
        # 이미 같은 아이디가 있으면 회원가입을 진행하면 안 된다.
        # 그래서 직접 ValueError 예외를 발생시킨다.
        if self.find_member(member.user_id) is not None:
            raise ValueError('이미 사용 중인 아이디입니다.')

        self.member_list.append(member)
        print('회원가입이 완료되었습니다.')

    # 회원목록 출력
    def list_members(self):
        # 회원 목록이 비어 있으면 출력할 회원이 없다.
        # 이 상황을 예외로 처리하여 메인 코드의 except에서 메시지를 출력하게 한다.
        if len(self.member_list) == 0:
            raise ValueError('등록된 회원이 없습니다.')

        for member in self.member_list:
            print(member)

    # 회원상세정보
    def detail_member(self, user_id):
        member = self.find_member(user_id)

        # 입력한 아이디에 해당하는 회원이 없으면 예외 발생
        if member is None:
            raise ValueError('해당 아이디의 회원이 없습니다.')

        print(member)

    # 회원정보수정
    def update_member(self, user_id, phone, address):
        member = self.find_member(user_id)

        # 수정하려는 회원이 없으면 수정할 수 없으므로 예외 발생
        if member is None:
            raise ValueError('해당 아이디의 회원이 없습니다.')

        member.phone = phone
        member.address = address
        print('회원정보가 수정되었습니다.')

    # 회원탈퇴
    def delete_member(self, user_id):
        member = self.find_member(user_id)

        # 탈퇴하려는 회원이 없으면 삭제할 수 없으므로 예외 발생
        if member is None:
            raise ValueError('해당 아이디의 회원이 없습니다.')

        self.member_list.remove(member)
        print('회원탈퇴가 완료되었습니다.')


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

    # try 안에는 오류가 발생할 가능성이 있는 코드를 넣는다.
    # 여기서는 잘못된 메뉴, 잘못된 회원번호, 없는 회원 조회 등이 발생할 수 있다.
    try:
        if menu == '1':
            member_no = input('회원번호: ')

            # 회원번호는 숫자로만 입력받고 싶기 때문에 검사한다.
            # isdigit()은 문자열이 숫자로만 구성되어 있으면 True를 반환한다.
            if not member_no.isdigit():
                # 조건에 맞지 않으면 직접 ValueError 예외를 발생시킨다.
                raise ValueError('회원번호는 숫자로 입력해야 합니다.')

            user_id = input('아이디: ')
            password = input('비밀번호: ')
            name = input('이름: ')
            phone = input('전화번호: ')
            address = input('주소: ')

            # 아이디, 비밀번호, 이름은 반드시 필요한 정보라고 가정한다.
            # 하나라도 비어 있으면 회원가입을 진행하지 않고 예외를 발생시킨다.
            if user_id == '' or password == '' or name == '':
                raise ValueError('아이디, 비밀번호, 이름은 반드시 입력해야 합니다.')

            member = Member(member_no, user_id, password, name, phone, address)
            service.join(member)

        elif menu == '2':
            # 회원목록이 비어 있으면 list_members() 안에서 ValueError가 발생한다.
            service.list_members()

        elif menu == '3':
            user_id = input('조회할 아이디: ')

            # 조회할 아이디를 입력하지 않은 경우 예외 발생
            if user_id == '':
                raise ValueError('아이디를 입력해야 합니다.')

            # 해당 아이디의 회원이 없으면 detail_member() 안에서 ValueError가 발생한다.
            service.detail_member(user_id)

        elif menu == '4':
            user_id = input('수정할 아이디: ')
            phone = input('새 전화번호: ')
            address = input('새 주소: ')

            # 수정할 아이디를 입력하지 않은 경우 예외 발생
            if user_id == '':
                raise ValueError('아이디를 입력해야 합니다.')

            # 해당 아이디의 회원이 없으면 update_member() 안에서 ValueError가 발생한다.
            service.update_member(user_id, phone, address)

        elif menu == '5':
            user_id = input('탈퇴할 아이디: ')

            # 탈퇴할 아이디를 입력하지 않은 경우 예외 발생
            if user_id == '':
                raise ValueError('아이디를 입력해야 합니다.')

            # 해당 아이디의 회원이 없으면 delete_member() 안에서 ValueError가 발생한다.
            service.delete_member(user_id)

        elif menu == '0':
            print('프로그램을 종료합니다.')
            break

        else:
            # 1, 2, 3, 4, 5, 0 이외의 메뉴를 입력하면 예외 발생
            raise ValueError('잘못된 메뉴입니다.')

    # try 안에서 ValueError가 발생하면 프로그램이 종료되지 않고 여기로 이동한다.
    # as e는 발생한 오류 메시지를 e라는 변수에 저장한다.
    except ValueError as e:
        print(e)