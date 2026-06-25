# member/member_service.py

from member.member import Member


class MemberService:
    def __init__(self):
        self.member_list = []
        self.current_user = None

    def join(self, member_id, password, name, phone):
        if member_id == "" or password == "" or name == "" or phone == "":
            return False

        for member in self.member_list:
            if member.member_id == member_id:
                return False

        new_member = Member(member_id, password, name, phone)
        self.member_list.append(new_member)

        return True

    def login(self, member_id, password):
        for member in self.member_list:
            if member.member_id == member_id and member.password == password:
                self.current_user = member
                return True

        return False

    def logout(self):
        self.current_user = None

    def is_login(self):
        return self.current_user is not None

    def get_my_info(self):
        return self.current_user

    def update_my_info(self, password, name, phone):
        if self.current_user is None:
            return False

        if password == "" or name == "" or phone == "":
            return False

        self.current_user.password = password
        self.current_user.name = name
        self.current_user.phone = phone

        return True

    def delete_my_account(self):
        if self.current_user is None:
            return False

        self.member_list.remove(self.current_user)
        self.current_user = None

        return True

    def list_members(self):
        return self.member_list

    def get_member_detail(self, member_id):
        for member in self.member_list:
            if member.member_id == member_id:
                return member

        return None

    def delete_member(self, member_id):
        target_member = self.get_member_detail(member_id)

        if target_member is None:
            return False

        self.member_list.remove(target_member)

        if self.current_user == target_member:
            self.current_user = None

        return True