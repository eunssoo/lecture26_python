#========================
# 데이터 모델 정의 : Member
class Member:
    def __init__(self, id, password, name):
        self.__id = id
        self.__password = password
        self.__name = name

    def get_id(self):
        return self.__id

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def set_password(self, password):
        self.__password = password

    def set_name(self, name):
        self.__name = name

    def __str__(self):
        return f'ID: {self.__id}, 이름: {self.__name}, 비밀번호: {self.__password}'


#================
# 회원 관리 서비스 로직 (Controller) : MemberService
class MemberService:
    def __init__(self, memberDao):
        self.__dao = memberDao

    def join(self, member):
        # 이미 있는 아이디인지 확인
        if self.__dao.is_exist(member.get_id()):
            return False

        self.__dao.insert_member(member)
        return True

    def login(self, id, password):
        member = self.__dao.get_member_info(id)

        if member:
            if password == member.get_password():
                return id

        return None

    def list_members(self):
        return self.__dao.get_all_members()

    def get_member_info(self, id):
        return self.__dao.get_member_info(id)

    def update_member(self, id, new_password, new_name):
        member = self.__dao.get_member_info(id)

        if member is None:
            return False

        if new_password != '':
            member.set_password(new_password)

        if new_name != '':
            member.set_name(new_name)

        return True

    def delete_member(self, id):
        return self.__dao.delete_member(id)


#================
# 회원 데이터 접근 (CRUD) : MemberDAO
class MemberDAO:
    def __init__(self):
        self.__memberDB = {}

    def insert_member(self, member):
        self.__memberDB[member.get_id()] = member

    def is_exist(self, id):
        return id in self.__memberDB

    def get_member_info(self, id):
        if self.is_exist(id):
            return self.__memberDB[id]
        else:
            return None

    def get_all_members(self):
        return list(self.__memberDB.values())

    def delete_member(self, id):
        if self.is_exist(id):
            del self.__memberDB[id]
            return True
        else:
            return False