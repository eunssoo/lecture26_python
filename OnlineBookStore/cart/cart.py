class Cart:
    def __init__(self, member_id):
        self.__member_id = self.__validate_member_id(member_id)

    def get_member_id(self):
        return self.__member_id

    @staticmethod
    def __validate_member_id(member_id):
        if not isinstance(member_id, str):
            raise TypeError("회원 아이디는 문자열이어야 합니다.")

        member_id = member_id.strip()

        if not member_id:
            raise ValueError("회원 아이디는 비어 있을 수 없습니다.")

        return member_id

    def __str__(self):
        return f"회원 아이디: {self.__member_id}의 장바구니"


class CartItem:
    def __init__(self, member_id, book_no, quantity):
        self.__member_id = self.__validate_member_id(member_id)
        self.__book_no = self.__validate_book_no(book_no)
        self.__quantity = self.__validate_quantity(quantity)

    def get_member_id(self):
        return self.__member_id

    def get_book_no(self):
        return self.__book_no

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = self.__validate_quantity(quantity)

    def increase_quantity(self, quantity):
        quantity = self.__validate_quantity(quantity)
        self.__quantity += quantity

    def decrease_quantity(self, quantity):
        quantity = self.__validate_quantity(quantity)

        if quantity >= self.__quantity:
            return False

        self.__quantity -= quantity
        return True

    @staticmethod
    def __validate_member_id(member_id):
        if not isinstance(member_id, str):
            raise TypeError("회원 아이디는 문자열이어야 합니다.")

        member_id = member_id.strip()

        if not member_id:
            raise ValueError("회원 아이디는 비어 있을 수 없습니다.")

        return member_id

    @staticmethod
    def __validate_book_no(book_no):
        if isinstance(book_no, bool) or not isinstance(book_no, int):
            raise TypeError("도서번호는 정수여야 합니다.")

        if book_no <= 0:
            raise ValueError("도서번호는 1 이상이어야 합니다.")

        return book_no

    @staticmethod
    def __validate_quantity(quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("수량은 정수여야 합니다.")

        if quantity <= 0:
            raise ValueError("수량은 1 이상이어야 합니다.")

        return quantity

    def __str__(self):
        return (
            f"회원 아이디: {self.__member_id}, "
            f"도서번호: {self.__book_no}, "
            f"수량: {self.__quantity}권"
        )