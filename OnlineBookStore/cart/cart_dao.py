from cart.cart import Cart, CartItem


class CartDAO:
    def __init__(self):
        self.__cart_list = []

    # 장바구니 등록
    def insert_cart(self, cart):
        if not isinstance(cart, Cart):
            raise TypeError("Cart 객체만 등록할 수 있습니다.")

        if self.is_cart_exist(cart.get_member_id()):
            return False

        self.__cart_list.append(cart)
        return True

    # 회원 아이디로 장바구니 조회
    def select_cart_by_member_id(self, member_id):
        for cart in self.__cart_list:
            if cart.get_member_id() == member_id:
                return cart

        return None

    # 장바구니 삭제
    def delete_cart(self, member_id):
        for index, cart in enumerate(self.__cart_list):
            if cart.get_member_id() == member_id:
                del self.__cart_list[index]
                return True

        return False

    # 장바구니 존재 여부 확인
    def is_cart_exist(self, member_id):
        return self.select_cart_by_member_id(member_id) is not None


class CartItemDAO:
    def __init__(self):
        self.__cart_item_list = []

    # 장바구니 항목 등록
    def insert_cart_item(self, cart_item):
        if not isinstance(cart_item, CartItem):
            raise TypeError("CartItem 객체만 등록할 수 있습니다.")

        member_id = cart_item.get_member_id()
        book_no = cart_item.get_book_no()

        if self.is_cart_item_exist(member_id, book_no):
            return False

        self.__cart_item_list.append(cart_item)
        return True

    # 특정 회원의 전체 장바구니 항목 조회
    def select_cart_items_by_member_id(self, member_id):
        return [
            cart_item
            for cart_item in self.__cart_item_list
            if cart_item.get_member_id() == member_id
        ]

    # 특정 장바구니 항목 조회
    def select_cart_item(self, member_id, book_no):
        for cart_item in self.__cart_item_list:
            if (
                cart_item.get_member_id() == member_id
                and cart_item.get_book_no() == book_no
            ):
                return cart_item

        return None

    # 장바구니 항목 수량 수정
    def update_cart_item(self, member_id, book_no, quantity):
        for index, cart_item in enumerate(self.__cart_item_list):
            if (
                cart_item.get_member_id() == member_id
                and cart_item.get_book_no() == book_no
            ):
                try:
                    updated_item = CartItem(
                        member_id,
                        book_no,
                        quantity,
                    )
                except (TypeError, ValueError):
                    return False

                self.__cart_item_list[index] = updated_item
                return True

        return False

    # 특정 장바구니 항목 삭제
    def delete_cart_item(self, member_id, book_no):
        for index, cart_item in enumerate(self.__cart_item_list):
            if (
                cart_item.get_member_id() == member_id
                and cart_item.get_book_no() == book_no
            ):
                del self.__cart_item_list[index]
                return True

        return False

    # 특정 회원의 장바구니 항목 전체 삭제
    def delete_all_cart_items(self, member_id):
        self.__cart_item_list = [
            cart_item
            for cart_item in self.__cart_item_list
            if cart_item.get_member_id() != member_id
        ]

        # 이미 비어 있는 장바구니도 정상적으로 비워진 상태로 본다.
        return True

    # 특정 장바구니 항목 존재 여부 확인
    def is_cart_item_exist(self, member_id, book_no):
        return self.select_cart_item(member_id, book_no) is not None