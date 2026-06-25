# member/member.py

class Member:
    """
    회원 정보를 저장하는 클래스
    """

    def __init__(self, member_id, password, name, phone):
        self.member_id = member_id
        self.password = password
        self.name = name
        self.phone = phone

    def __str__(self):
        return (
            f"아이디: {self.member_id}, "
            f"이름: {self.name}, "
            f"전화번호: {self.phone}"
        )