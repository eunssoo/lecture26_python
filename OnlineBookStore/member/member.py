class Member:
    ROLE_MEMBER = "member"
    ROLE_ADMIN = "admin"

    VALID_ROLES = {
        ROLE_MEMBER,
        ROLE_ADMIN,
    }

    def __init__(
        self,
        member_no: int,
        user_id: str,
        password: str,
        name: str,
        phone: str,
        address: str,
        role: str = ROLE_MEMBER,
    ):
        self.__member_no = self.__validate_member_no(member_no)
        self.__user_id = self.__validate_text(user_id, "아이디")
        self.__password = self.__validate_text(password, "비밀번호")
        self.__name = self.__validate_text(name, "이름")
        self.__phone = self.__validate_text(phone, "전화번호")
        self.__address = self.__validate_text(address, "주소")
        self.__role = self.__validate_role(role)

    def get_member_no(self):
        return self.__member_no

    def get_user_id(self):
        return self.__user_id

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_address(self):
        return self.__address

    def get_role(self):
        return self.__role

    def set_password(self, password):
        self.__password = self.__validate_text(
            password,
            "비밀번호",
        )

    def set_phone(self, phone):
        self.__phone = self.__validate_text(
            phone,
            "전화번호",
        )

    def set_address(self, address):
        self.__address = self.__validate_text(
            address,
            "주소",
        )

    def is_admin(self):
        return self.__role == self.ROLE_ADMIN

    @staticmethod
    def __validate_member_no(member_no):
        if isinstance(member_no, bool) or not isinstance(member_no, int):
            raise TypeError("회원번호는 정수여야 합니다.")

        # 관리자 번호 0을 허용한다.
        if member_no < 0:
            raise ValueError("회원번호는 0 이상이어야 합니다.")

        return member_no

    @classmethod
    def __validate_role(cls, role):
        if role not in cls.VALID_ROLES:
            raise ValueError(f"유효하지 않은 권한입니다: {role}")

        return role

    @staticmethod
    def __validate_text(value, field_name):
        if not isinstance(value, str):
            raise TypeError(f"{field_name}은 문자열이어야 합니다.")

        value = value.strip()

        if not value:
            raise ValueError(f"{field_name}은 비어 있을 수 없습니다.")

        return value

    def __str__(self):
        return (
            f"회원번호: {self.__member_no}, "
            f"아이디: {self.__user_id}, "
            f"이름: {self.__name}, "
            f"전화번호: {self.__phone}, "
            f"주소: {self.__address}, "
            f"권한: {self.__role}"
        )