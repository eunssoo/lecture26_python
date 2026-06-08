# member/member_dao.py 파일에 있는 MemberDAO 클래스를 가져온다.
# MemberService는 실제 회원 저장/조회/삭제를 DAO에게 맡긴다.
from member.member_dao import MemberDAO

# member/member.py 파일에 있는 Member 클래스를 가져온다.
# 관리자 계정을 만들거나 회원 객체를 다룰 때 필요하다.
from member.member import Member


# ==================
# 회원 관리 서비스 클래스
# 역할: 회원가입, 로그인, 로그아웃, 회원정보조회, 비밀번호수정, 회원탈퇴 같은 기능을 처리한다.
class MemberService:
    # 관리자 계정 정보
    # 프로그램이 시작될 때 자동으로 생성되는 관리자 계정이다.
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    # 생성자
    # MemberService 객체를 만들 때 MemberDAO 객체를 받아서 저장한다.
    def __init__(self, memberDao):
        # 실제 회원 데이터 저장/조회/삭제는 DAO가 담당한다.
        self.__dao = memberDao

        # 관리자 계정을 기본 회원으로 추가한다.
        self.join(Member(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD, '관리자'))

        # 현재 로그인한 사용자의 id를 저장한다.
        # 로그인하지 않은 상태면 None이다.
        self.current_user = None

    # 회원가입
    def join(self, member):
        # 이미 존재하는 아이디인지 확인한다.
        if self.__dao.is_exist(member.get_id()):
            return False

        # 존재하지 않는 아이디이면 DAO에 저장 요청
        self.__dao.insert_member(member)
        return True

    # 로그인
    def login(self, id, password):
        # 입력한 id로 회원 정보를 조회한다.
        member = self.__dao.get_member_info(id)

        # 회원이 존재하고 비밀번호가 일치하면 로그인 성공
        if member:
            if password == member.get_password():
                self.current_user = id
                return True

        # 회원이 없거나 비밀번호가 틀리면 로그인 실패
        return False

    # 전체 회원 목록 조회
    def list_members(self):
        return self.__dao.get_all_members()

    # 로그아웃
    def logout(self):
        self.current_user = None

    # 특정 회원 정보 조회
    def view_member_info(self, id):
        return self.__dao.get_member_info(id)

    # 회원 정보 전체 수정
    def update_member_info(self, id, member):
        return self.__dao.update_member_info(id, member)

    # 회원 비밀번호 수정
    def update_member_password(self, id, org_password, new_password):
        # 본인만 자기 비밀번호를 바꿀 수 있게 한다.
        if self.current_user != id:
            return False

        # id로 회원 정보 조회
        member = self.__dao.get_member_info(id)

        # 회원이 없으면 실패
        if not member:
            return False

        # 기존 비밀번호가 맞으면 새 비밀번호로 변경
        if member.get_password() == org_password:
            member.set_password(new_password)
            return True

        # 기존 비밀번호가 틀리면 실패
        return False

    # 회원 삭제 / 회원 탈퇴
    def remove_member(self, id):
        # 관리자 계정은 삭제하지 못하게 막는다.
        if id == MemberService.ADMIN_ID:
            return False

        # 본인이 자기 계정을 삭제하거나,
        # 관리자가 다른 회원을 삭제할 수 있다.
        if self.current_user == id or self.current_user == MemberService.ADMIN_ID:
            result = self.__dao.remove_member(id)

            # 본인이 탈퇴한 경우 로그인 상태도 해제한다.
            if result and self.current_user == id:
                self.current_user = None

            return result

        # 권한이 없으면 삭제 실패
        return False


# 이 파일을 직접 실행했을 때만 아래 테스트 코드가 실행된다.
# 다른 파일에서 import할 때는 실행되지 않는다.
if __name__ == '__main__':
    # MemberService 객체 생성
    # MemberService는 MemberDAO를 사용해야 하므로 MemberDAO 객체를 넣어준다.
    ms = MemberService(MemberDAO())

    # 회원 2명 가입
    ms.join(Member('sungsoo', '1234', '성수'))
    ms.join(Member('curi', '1111', '큐리'))

    # 전체 회원 목록 출력
    print('--- 전체 회원 목록 ---')
    members = ms.list_members()
    for member in members:
        print(member)

    # curi 로그인 테스트
    print('--- 로그인 테스트 ---')
    print(ms.login('curi', '1111'))
    print('현재 로그인 사용자:', ms.current_user)

    # 로그아웃 테스트
    print('--- 로그아웃 테스트 ---')
    ms.logout()
    print('현재 로그인 사용자:', ms.current_user)

    # 회원 정보 조회
    print('--- 회원 정보 조회 ---')
    print(ms.view_member_info('curi'))

    # sungsoo 로그인 후 비밀번호 변경 테스트
    print('--- 비밀번호 변경 테스트 ---')
    ms.login('sungsoo', '1234')
    print(ms.update_member_password('sungsoo', '1234', '4321'))
    print(ms.view_member_info('sungsoo'))

    # 관리자 로그인 후 sungsoo 삭제 테스트
    print('--- 관리자 회원 삭제 테스트 ---')
    ms.login(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD)
    print(ms.remove_member('sungsoo'))
    print(ms.view_member_info('sungsoo'))

    # 삭제 후 전체 회원 목록 출력
    print('--- 삭제 후 전체 회원 목록 ---')
    members = ms.list_members()
    for member in members:
        print(member)