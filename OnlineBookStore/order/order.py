from datetime import date, datetime


class Order:
    STATUS_ORDER_COMPLETE = "주문완료"
    STATUS_PREPARING = "배송준비중"
    STATUS_SHIPPING = "배송중"
    STATUS_DELIVERED = "배송완료"
    STATUS_CANCELED = "주문취소"

    VALID_STATUSES = {
        STATUS_ORDER_COMPLETE,
        STATUS_PREPARING,
        STATUS_SHIPPING,
        STATUS_DELIVERED,
        STATUS_CANCELED,
    }

    def __init__(
        self,
        order_no,
        member_id,
        order_date,
        total_price,
        order_status=STATUS_ORDER_COMPLETE,
    ):
        self.__order_no = self.__validate_positive_integer(
            order_no,
            "주문번호",
        )
        self.__member_id = self.__validate_text(
            member_id,
            "회원 아이디",
        )
        self.__order_date = self.__validate_order_date(order_date)
        self.__total_price = self.__validate_price(
            total_price,
            "총 주문금액",
        )
        self.__order_status = self.__validate_status(order_status)

    def get_order_no(self):
        return self.__order_no

    def get_member_id(self):
        return self.__member_id

    def get_order_date(self):
        return self.__order_date

    def get_total_price(self):
        return self.__total_price

    def get_order_status(self):
        return self.__order_status

    # 주문 상태만 변경할 수 있다.
    # 실제 상태 전환 가능 여부는 OrderService에서 검사한다.
    def set_order_status(self, order_status):
        self.__order_status = self.__validate_status(order_status)

    @classmethod
    def __validate_status(cls, order_status):
        if order_status not in cls.VALID_STATUSES:
            raise ValueError(
                f"유효하지 않은 주문 상태입니다: {order_status}"
            )

        return order_status

    @staticmethod
    def __validate_order_date(order_date):
        if isinstance(order_date, (date, datetime)):
            return order_date

        if isinstance(order_date, str) and order_date.strip():
            return order_date.strip()

        raise ValueError(
            "주문일자는 날짜 객체 또는 비어 있지 않은 문자열이어야 합니다."
        )

    @staticmethod
    def __validate_positive_integer(value, field_name):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{field_name}는 정수여야 합니다.")

        if value <= 0:
            raise ValueError(f"{field_name}는 1 이상이어야 합니다.")

        return value

    @staticmethod
    def __validate_price(value, field_name):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{field_name}은 정수여야 합니다.")

        if value < 0:
            raise ValueError(f"{field_name}은 0원 이상이어야 합니다.")

        return value

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
            f"주문번호: {self.__order_no}, "
            f"회원 아이디: {self.__member_id}, "
            f"주문일자: {self.__order_date}, "
            f"총 금액: {self.__total_price:,}원, "
            f"주문상태: {self.__order_status}"
        )


class OrderItem:
    def __init__(
        self,
        order_no,
        book_no,
        quantity,
        order_price,
    ):
        self.__order_no = self.__validate_positive_integer(
            order_no,
            "주문번호",
        )
        self.__book_no = self.__validate_positive_integer(
            book_no,
            "도서번호",
        )
        self.__quantity = self.__validate_positive_integer(
            quantity,
            "주문 수량",
        )
        self.__order_price = self.__validate_price(order_price)

    def get_order_no(self):
        return self.__order_no

    def get_book_no(self):
        return self.__book_no

    def get_quantity(self):
        return self.__quantity

    def get_order_price(self):
        return self.__order_price

    def get_subtotal(self):
        return self.__order_price * self.__quantity

    @staticmethod
    def __validate_positive_integer(value, field_name):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{field_name}는 정수여야 합니다.")

        if value <= 0:
            raise ValueError(f"{field_name}는 1 이상이어야 합니다.")

        return value

    @staticmethod
    def __validate_price(order_price):
        if (
            isinstance(order_price, bool)
            or not isinstance(order_price, int)
        ):
            raise TypeError("주문 가격은 정수여야 합니다.")

        if order_price < 0:
            raise ValueError("주문 가격은 0원 이상이어야 합니다.")

        return order_price

    def __str__(self):
        return (
            f"주문번호: {self.__order_no}, "
            f"도서번호: {self.__book_no}, "
            f"수량: {self.__quantity}권, "
            f"주문가격: {self.__order_price:,}원, "
            f"소계: {self.get_subtotal():,}원"
        )


class DeliveryInfo:
    STATUS_PREPARING = "배송준비중"
    STATUS_SHIPPING = "배송중"
    STATUS_DELIVERED = "배송완료"

    VALID_STATUSES = {
        STATUS_PREPARING,
        STATUS_SHIPPING,
        STATUS_DELIVERED,
    }

    def __init__(
        self,
        order_no,
        receiver_name,
        receiver_phone,
        delivery_address,
        delivery_status=STATUS_PREPARING,
    ):
        self.__order_no = self.__validate_order_no(order_no)
        self.__receiver_name = self.__validate_text(
            receiver_name,
            "수령인 이름",
        )
        self.__receiver_phone = self.__validate_text(
            receiver_phone,
            "수령인 전화번호",
        )
        self.__delivery_address = self.__validate_text(
            delivery_address,
            "배송 주소",
        )
        self.__delivery_status = self.__validate_status(
            delivery_status
        )

    def get_order_no(self):
        return self.__order_no

    def get_receiver_name(self):
        return self.__receiver_name

    def get_receiver_phone(self):
        return self.__receiver_phone

    def get_delivery_address(self):
        return self.__delivery_address

    def get_delivery_status(self):
        return self.__delivery_status

    def set_receiver_name(self, receiver_name):
        self.__receiver_name = self.__validate_text(
            receiver_name,
            "수령인 이름",
        )

    def set_receiver_phone(self, receiver_phone):
        self.__receiver_phone = self.__validate_text(
            receiver_phone,
            "수령인 전화번호",
        )

    def set_delivery_address(self, delivery_address):
        self.__delivery_address = self.__validate_text(
            delivery_address,
            "배송 주소",
        )

    # 실제 상태 전환 가능 여부는 OrderService에서 검사한다.
    def set_delivery_status(self, delivery_status):
        self.__delivery_status = self.__validate_status(
            delivery_status
        )

    @staticmethod
    def __validate_order_no(order_no):
        if isinstance(order_no, bool) or not isinstance(order_no, int):
            raise TypeError("주문번호는 정수여야 합니다.")

        if order_no <= 0:
            raise ValueError("주문번호는 1 이상이어야 합니다.")

        return order_no

    @classmethod
    def __validate_status(cls, delivery_status):
        if delivery_status not in cls.VALID_STATUSES:
            raise ValueError(
                f"유효하지 않은 배송 상태입니다: {delivery_status}"
            )

        return delivery_status

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
            f"주문번호: {self.__order_no}, "
            f"수령인: {self.__receiver_name}, "
            f"전화번호: {self.__receiver_phone}, "
            f"배송주소: {self.__delivery_address}, "
            f"배송상태: {self.__delivery_status}"
        )