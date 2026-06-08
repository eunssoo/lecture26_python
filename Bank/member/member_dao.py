# member/member.py 파일에 있는 Member 클래스를 가져온다.
# MemberDAO는 Member 객체를 저장하고 관리해야 하므로 필요하다.
from member.member import Member


# ====================
# 회원 데이터 접근 클래스
# DAO = Data Access Object
# 역할: 회원 데이터를 저장, 조회, 수정, 삭제한다.
class MemberDAO:
    def __init__(self):
        # 회원 정보를 저장할 딕셔너리
        # key   : 회원 id
        # value : Member 객체
        #
        # 예:
        # {
        #     'sungsoo': Member('sungsoo', '1234', '은성수'),
        #     'curi': Member('curi', '1234', '큐리')
        # }
        self.__memberDB = {}

    # 회원 추가
    def insert_member(self, member):
        # 추가하려는 회원의 id가 이미 존재하면 저장 실패
        if self.is_exist(member.get_id()):
            return False

        # id를 key로, Member 객체를 value로 저장
        self.__memberDB[member.get_id()] = member
        return True

    # 회원 id 존재 여부 확인
    def is_exist(self, id):
        # id가 딕셔너리 key 안에 있으면 True
        if id in self.__memberDB.keys():
            return True

        # 없으면 False
        return False

    # 회원 id로 회원 정보 조회
    def get_member_info(self, id):
        # 해당 id가 존재하면 Member 객체 반환
        if self.is_exist(id):
            return self.__memberDB[id]

        # 없으면 None 반환
        return None

    # 전체 회원 목록 조회
    def get_all_members(self):
        # 딕셔너리에 저장된 모든 Member 객체를 리스트로 변환해서 반환한다.
        # 회원이 하나도 없으면 빈 리스트 []가 반환된다.
        return list(self.__memberDB.values())

    # 회원 정보 수정
    def update_member_info(self, id, member):
        # 수정하려는 id가 존재하면
        if self.is_exist(id):
            # 해당 id 위치에 새로운 Member 객체를 덮어쓴다.
            self.__memberDB[id] = member
            return True

        # id가 없으면 수정 실패
        return False

    # 회원 삭제
    def remove_member(self, id):
        # 삭제하려는 id가 존재하면
        if self.is_exist(id):
            # 딕셔너리에서 해당 회원 삭제
            self.__memberDB.pop(id)
            return True

        # id가 없으면 삭제 실패
        return False


# 이 파일을 직접 실행했을 때만 아래 테스트 코드가 실행된다.
# 다른 파일에서 import할 때는 실행되지 않는다.
if __name__ == '__main__':
    # MemberDAO 객체 생성
    dao = MemberDAO()

    # 아직 회원이 없으므로 False 출력
    print(dao.is_exist('sungsoo'))

    # 회원 2명 추가
    member = Member('sungsoo', '1234', '은성수')
    dao.insert_member(member)

    member = Member('curi', '1234', '큐리')
    dao.insert_member(member)

    # 특정 회원 정보 조회
    print('--- 특정 회원 조회 ---')
    print(dao.get_member_info('sungsoo'))
    print(dao.get_member_info('curi'))

    # 전체 회원 목록 조회
    print('--- 전체 회원 목록 ---')
    members = dao.get_all_members()
    for member in members:
        print(member)

    # 회원 비밀번호 수정
    print('--- 회원 정보 수정 ---')
    member = dao.get_member_info('sungsoo')

    if member:
        member.set_password('1111')
        dao.update_member_info('sungsoo', member)

    members = dao.get_all_members()
    for member in members:
        print(member)

    # 회원 삭제
    print('--- 회원 삭제 후 목록 ---')
    dao.remove_member('sungsoo')

    members = dao.get_all_members()
    for member in members:
        print(member)