from member.member import Member
from member.member_dao import MemberDAO


class MemberService:
    def __init__(self, member_dao: MemberDAO):
        self.__member_dao = member_dao
        self.__current_user = None

    # 회원가입
    def join_member(self, user_id, password, name, phone, address):
        try:
            if self.__member_dao.is_member_exist(user_id):
                return False

            member_no = self.__member_dao.get_next_member_no()

            member = Member(
                member_no,
                user_id,
                password,
                name,
                phone,
                address,
                Member.ROLE_MEMBER,
            )

            result = self.__member_dao.insert_member(member)
            return result is not False

        except (TypeError, ValueError):
            return False

    # 로그인
    def login(self, user_id, password):
        member = self.__member_dao.select_member_by_id(user_id)

        if member is None:
            return False

        if member.get_password() != password:
            return False

        self.__current_user = member
        return True

    # 로그아웃
    def logout(self):
        self.__current_user = None

    # 로그인 여부
    def is_login(self):
        return self.__current_user is not None

    # 관리자 여부
    def is_admin(self):
        return (
            self.__current_user is not None
            and self.__current_user.is_admin()
        )

    # 현재 로그인 회원 조회
    def get_current_user(self):
        return self.__current_user

    # 전체 회원 조회: 관리자 전용
    def get_all_members(self):
        if not self.is_admin():
            return []

        return self.__member_dao.select_all_members()

    # 아이디로 회원 조회: 본인 또는 관리자만 가능
    def get_member_info(self, user_id):
        if not self.is_login():
            return None

        if (
            not self.is_admin()
            and not self.__is_current_user(user_id)
        ):
            return None

        return self.__member_dao.select_member_by_id(user_id)

    # 회원번호로 회원 조회: 관리자 전용
    def get_member_info_by_no(self, member_no):
        if not self.is_admin():
            return None

        return self.__member_dao.select_member_by_no(member_no)

    # 회원정보 수정: 현재 로그인한 본인만 가능
    def modify_member_info(self, user_id, phone, address):
        if not self.__is_current_user(user_id):
            return False

        member = self.__member_dao.select_member_by_id(user_id)

        if member is None:
            return False

        updated_member = self.__create_updated_member(
            member=member,
            phone=phone,
            address=address,
        )

        return self.__save_updated_member(
            user_id,
            updated_member,
        )

    # 비밀번호 변경: 현재 로그인한 본인만 가능
    def change_password(
        self,
        user_id,
        old_password,
        new_password,
    ):
        if not self.__is_current_user(user_id):
            return False

        member = self.__member_dao.select_member_by_id(user_id)

        if member is None:
            return False

        if member.get_password() != old_password:
            return False

        updated_member = self.__create_updated_member(
            member=member,
            password=new_password,
        )

        return self.__save_updated_member(
            user_id,
            updated_member,
        )

    # 전화번호 변경: 현재 로그인한 본인만 가능
    def change_phone(self, user_id, phone):
        if not self.__is_current_user(user_id):
            return False

        member = self.__member_dao.select_member_by_id(user_id)

        if member is None:
            return False

        updated_member = self.__create_updated_member(
            member=member,
            phone=phone,
        )

        return self.__save_updated_member(
            user_id,
            updated_member,
        )

    # 주소 변경: 현재 로그인한 본인만 가능
    def change_address(self, user_id, address):
        if not self.__is_current_user(user_id):
            return False

        member = self.__member_dao.select_member_by_id(user_id)

        if member is None:
            return False

        updated_member = self.__create_updated_member(
            member=member,
            address=address,
        )

        return self.__save_updated_member(
            user_id,
            updated_member,
        )

    # 회원탈퇴: 현재 로그인한 본인만 가능
    def remove_member(self, user_id, password):
        if not self.__is_current_user(user_id):
            return False

        member = self.__member_dao.select_member_by_id(user_id)

        if member is None or member.is_admin():
            return False

        if member.get_password() != password:
            return False

        result = self.__member_dao.delete_member(user_id)

        if result:
            self.logout()

        return result

    # 관리자에 의한 회원 삭제
    def remove_member_by_admin(self, user_id):
        if not self.is_admin():
            return False

        member = self.__member_dao.select_member_by_id(user_id)

        if member is None or member.is_admin():
            return False

        return self.__member_dao.delete_member(user_id)

    # 전달받은 아이디가 현재 로그인 회원인지 확인
    def __is_current_user(self, user_id):
        return (
            self.__current_user is not None
            and self.__current_user.get_user_id() == user_id
        )

    # 기존 정보를 보존하면서 수정된 회원 객체 생성
    def __create_updated_member(
        self,
        member,
        password=None,
        phone=None,
        address=None,
    ):
        try:
            return Member(
                member.get_member_no(),
                member.get_user_id(),
                (
                    password
                    if password is not None
                    else member.get_password()
                ),
                member.get_name(),
                (
                    phone
                    if phone is not None
                    else member.get_phone()
                ),
                (
                    address
                    if address is not None
                    else member.get_address()
                ),
                member.get_role(),
            )
        except (TypeError, ValueError):
            return None

    # 수정 객체 저장 및 현재 로그인 정보 갱신
    def __save_updated_member(
        self,
        user_id,
        updated_member,
    ):
        if updated_member is None:
            return False

        try:
            result = self.__member_dao.update_member(
                user_id,
                updated_member,
            )
        except (TypeError, ValueError):
            return False

        if result and self.__is_current_user(user_id):
            self.__current_user = updated_member

        return result