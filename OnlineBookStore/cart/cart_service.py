from cart.cart import Cart, CartItem
from cart.cart_dao import CartDAO, CartItemDAO
from book.book_service import BookService


class CartService:
    def __init__(
        self,
        cart_dao: CartDAO,
        cart_item_dao: CartItemDAO,
        book_service: BookService,
    ):
        self.__cart_dao = cart_dao
        self.__cart_item_dao = cart_item_dao
        self.__book_service = book_service

    # 장바구니 생성
    def create_cart(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return False

        if self.__cart_dao.is_cart_exist(member_id):
            return False

        try:
            cart = Cart(member_id)
        except (TypeError, ValueError):
            return False

        return self.__cart_dao.insert_cart(cart)

    # 장바구니에 도서 추가
    def add_book_to_cart(self, member_id, book_no, quantity):
        if not self.__is_valid_member_id(member_id):
            return False

        if not self.__is_valid_book_no(book_no):
            return False

        if not self.__is_valid_quantity(quantity):
            return False

        book = self.__book_service.get_book_info(book_no)

        if book is None:
            return False

        if not self.__cart_dao.is_cart_exist(member_id):
            if not self.create_cart(member_id):
                return False

        cart_item = self.__cart_item_dao.select_cart_item(
            member_id,
            book_no,
        )

        if cart_item is not None:
            new_quantity = cart_item.get_quantity() + quantity

            if not self.__book_service.check_stock(
                book_no,
                new_quantity,
            ):
                return False

            return self.__cart_item_dao.update_cart_item(
                member_id,
                book_no,
                new_quantity,
            )

        if not self.__book_service.check_stock(book_no, quantity):
            return False

        try:
            new_cart_item = CartItem(
                member_id,
                book_no,
                quantity,
            )
        except (TypeError, ValueError):
            return False

        return self.__cart_item_dao.insert_cart_item(
            new_cart_item
        )

    # 장바구니 조회
    def get_cart(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return None

        return self.__cart_dao.select_cart_by_member_id(
            member_id
        )

    # 장바구니 항목 조회
    def get_cart_items(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return []

        return self.__cart_item_dao.select_cart_items_by_member_id(
            member_id
        )

    # 장바구니 상세 정보 조회
    def get_cart_detail(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return []

        cart_items = self.get_cart_items(member_id)
        result = []

        for cart_item in cart_items:
            book_no = cart_item.get_book_no()
            quantity = cart_item.get_quantity()
            book = self.__book_service.get_book_info(book_no)

            if book is None:
                result.append({
                    "book_no": book_no,
                    "title": "삭제된 도서",
                    "author": None,
                    "publisher": None,
                    "price": 0,
                    "quantity": quantity,
                    "subtotal": 0,
                    "available": False,
                })
                continue

            price = book.get_price()

            result.append({
                "book_no": book.get_book_no(),
                "title": book.get_title(),
                "author": book.get_author(),
                "publisher": book.get_publisher(),
                "price": price,
                "quantity": quantity,
                "subtotal": price * quantity,
                "available": True,
            })

        return result

    # 장바구니 항목 수량 변경
    def change_quantity(self, member_id, book_no, quantity):
        if not self.__is_valid_member_id(member_id):
            return False

        if not self.__is_valid_book_no(book_no):
            return False

        if not self.__is_valid_quantity(quantity):
            return False

        if not self.__cart_item_dao.is_cart_item_exist(
            member_id,
            book_no,
        ):
            return False

        if not self.__book_service.check_stock(
            book_no,
            quantity,
        ):
            return False

        return self.__cart_item_dao.update_cart_item(
            member_id,
            book_no,
            quantity,
        )

    # 장바구니에서 도서 제거
    def remove_book_from_cart(self, member_id, book_no):
        if not self.__is_valid_member_id(member_id):
            return False

        if not self.__is_valid_book_no(book_no):
            return False

        if not self.__cart_item_dao.is_cart_item_exist(
            member_id,
            book_no,
        ):
            return False

        return self.__cart_item_dao.delete_cart_item(
            member_id,
            book_no,
        )

    # 장바구니 항목 비우기
    def clear_cart(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return False

        return self.__cart_item_dao.delete_all_cart_items(
            member_id
        )

    # 회원의 장바구니 전체 삭제
    # 회원 탈퇴 또는 관리자의 회원 삭제 시 사용한다.
    def delete_cart(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return False

        # 장바구니 항목을 먼저 모두 삭제한다.
        self.__cart_item_dao.delete_all_cart_items(member_id)

        # 장바구니가 없어도 삭제 완료 상태로 본다.
        if not self.__cart_dao.is_cart_exist(member_id):
            return True

        return self.__cart_dao.delete_cart(member_id)

    # 장바구니 총액 계산
    def get_total_price(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return None

        cart_items = self.get_cart_items(member_id)
        total_price = 0

        for cart_item in cart_items:
            book = self.__book_service.get_book_info(
                cart_item.get_book_no()
            )

            # 삭제된 도서가 있으면 총액을 계산하지 않는다.
            if book is None:
                return None

            total_price += (
                book.get_price()
                * cart_item.get_quantity()
            )

        return total_price

    # 장바구니가 비어 있는지 확인
    def is_cart_empty(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return True

        return len(self.get_cart_items(member_id)) == 0

    # 장바구니의 모든 도서 재고 확인
    def validate_cart_stock(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return False

        cart_items = self.get_cart_items(member_id)

        if not cart_items:
            return False

        for cart_item in cart_items:
            if not self.__book_service.check_stock(
                cart_item.get_book_no(),
                cart_item.get_quantity(),
            ):
                return False

        return True

    @staticmethod
    def __is_valid_member_id(member_id):
        return (
            isinstance(member_id, str)
            and bool(member_id.strip())
        )

    @staticmethod
    def __is_valid_book_no(book_no):
        return (
            isinstance(book_no, int)
            and not isinstance(book_no, bool)
            and book_no > 0
        )

    @staticmethod
    def __is_valid_quantity(quantity):
        return (
            isinstance(quantity, int)
            and not isinstance(quantity, bool)
            and quantity > 0
        )