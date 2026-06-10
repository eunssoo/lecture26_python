from member.member import Member

class MemberDAO:
    def __init__(self):
        self.__member_list = []
        self.__next_member_no = 1
        self.__init_admin()

    def __init_admin(self):
        admin = Member(
            0,
            "admin",
            "1234",
            "관리자",
            "010-0000-0000",
            "관리자 주소",
            Member.ROLE_ADMIN,
        )
        self.__member_list.append(admin)

    def insert_member(self, member):
        if not isinstance(member, Member):
            raise TypeError("Member 객체만 등록할 수 있습니다.")

        if self.is_member_exist(member.get_user_id()):
            return False

        if self.select_member_by_no(member.get_member_no()) is not None:
            return False

        self.__member_list.append(member)
        return True

    def select_all_members(self):
        return self.__member_list.copy()

    def select_member_by_id(self, user_id):
        return next(
            (
                member
                for member in self.__member_list
                if member.get_user_id() == user_id
            ),
            None,
        )

    def select_member_by_no(self, member_no):
        return next(
            (
                member
                for member in self.__member_list
                if member.get_member_no() == member_no
            ),
            None,
        )

    def update_member(self, user_id, member):
        if not isinstance(member, Member):
            raise TypeError("Member 객체만 수정할 수 있습니다.")

        for index, current_member in enumerate(self.__member_list):
            if current_member.get_user_id() != user_id:
                continue

            if current_member.get_member_no() != member.get_member_no():
                return False

            if member.get_user_id() != user_id:
                return False

            self.__member_list[index] = member
            return True

        return False

    def delete_member(self, user_id):
        for index, member in enumerate(self.__member_list):
            if member.get_user_id() != user_id:
                continue

            if member.is_admin():
                return False

            del self.__member_list[index]
            return True

        return False

    def is_member_exist(self, user_id):
        return self.select_member_by_id(user_id) is not None

    def get_next_member_no(self):
        member_no = self.__next_member_no
        self.__next_member_no += 1
        return member_no