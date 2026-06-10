from order.order import Order, OrderItem, DeliveryInfo


class OrderDAO:
    def __init__(self):
        self.__order_list = []
        self.__next_order_no = 1

    # 주문 등록
    def insert_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("Order 객체만 등록할 수 있습니다.")

        if self.select_order_by_no(order.get_order_no()) is not None:
            return False

        self.__order_list.append(order)
        return True

    # 전체 주문 조회
    def select_all_orders(self):
        return self.__order_list.copy()

    # 주문번호로 주문 조회
    def select_order_by_no(self, order_no):
        for order in self.__order_list:
            if order.get_order_no() == order_no:
                return order

        return None

    # 회원 아이디로 주문 목록 조회
    def select_orders_by_member_id(self, member_id):
        return [
            order
            for order in self.__order_list
            if order.get_member_id() == member_id
        ]

    # 주문 상태 변경
    def update_order_status(self, order_no, order_status):
        for index, order in enumerate(self.__order_list):
            if order.get_order_no() != order_no:
                continue

            try:
                updated_order = Order(
                    order.get_order_no(),
                    order.get_member_id(),
                    order.get_order_date(),
                    order.get_total_price(),
                    order_status,
                )
            except (TypeError, ValueError):
                return False

            self.__order_list[index] = updated_order
            return True

        return False

    # 주문 존재 여부 확인
    def is_order_exist(self, order_no):
        return self.select_order_by_no(order_no) is not None
    
    # 주문 생성 실패 시 저장된 미완성 주문 복구
    # 일반 주문 삭제 기능으로 사용하지 않는다.
    def delete_order(self, order_no):
        for index, order in enumerate(self.__order_list):
            if order.get_order_no() == order_no:
                del self.__order_list[index]
                return True

        return False
    
    # 다음 주문번호 발급
    def get_next_order_no(self):
        order_no = self.__next_order_no
        self.__next_order_no += 1
        return order_no


class OrderItemDAO:
    def __init__(self):
        self.__order_item_list = []

    # 주문 항목 등록
    def insert_order_item(self, order_item):
        if not isinstance(order_item, OrderItem):
            raise TypeError("OrderItem 객체만 등록할 수 있습니다.")

        if self.is_order_item_exist(
            order_item.get_order_no(),
            order_item.get_book_no(),
        ):
            return False

        self.__order_item_list.append(order_item)
        return True

    # 주문번호로 주문 항목 목록 조회
    def select_order_items_by_order_no(self, order_no):
        return [
            order_item
            for order_item in self.__order_item_list
            if order_item.get_order_no() == order_no
        ]

    # 주문번호와 도서번호로 주문 항목 조회
    def select_order_item(self, order_no, book_no):
        for order_item in self.__order_item_list:
            if (
                order_item.get_order_no() == order_no
                and order_item.get_book_no() == book_no
            ):
                return order_item

        return None

    # 주문 항목 존재 여부 확인
    def is_order_item_exist(self, order_no, book_no):
        return self.select_order_item(order_no, book_no) is not None

    # 특정 주문의 주문 항목 전체 삭제
    def delete_order_items(self, order_no):
        self.__order_item_list = [
            order_item
            for order_item in self.__order_item_list
            if order_item.get_order_no() != order_no
        ]

        # 이미 항목이 없어도 삭제된 상태이므로 성공으로 처리한다.
        return True


class DeliveryDAO:
    def __init__(self):
        self.__delivery_list = []

    # 배송 정보 등록
    def insert_delivery_info(self, delivery_info):
        if not isinstance(delivery_info, DeliveryInfo):
            raise TypeError(
                "DeliveryInfo 객체만 등록할 수 있습니다."
            )

        order_no = delivery_info.get_order_no()

        if self.select_delivery_info_by_order_no(order_no) is not None:
            return False

        self.__delivery_list.append(delivery_info)
        return True

    # 주문번호로 배송 정보 조회
    def select_delivery_info_by_order_no(self, order_no):
        for delivery_info in self.__delivery_list:
            if delivery_info.get_order_no() == order_no:
                return delivery_info

        return None

    # 배송 상태 변경
    def update_delivery_status(self, order_no, delivery_status):
        for index, delivery_info in enumerate(
            self.__delivery_list
        ):
            if delivery_info.get_order_no() != order_no:
                continue

            try:
                updated_delivery_info = DeliveryInfo(
                    delivery_info.get_order_no(),
                    delivery_info.get_receiver_name(),
                    delivery_info.get_receiver_phone(),
                    delivery_info.get_delivery_address(),
                    delivery_status,
                )
            except (TypeError, ValueError):
                return False

            self.__delivery_list[index] = updated_delivery_info
            return True

        return False

    # 배송 정보 수정
    def update_delivery_info(
        self,
        order_no,
        receiver_name,
        receiver_phone,
        delivery_address,
    ):
        for index, delivery_info in enumerate(
            self.__delivery_list
        ):
            if delivery_info.get_order_no() != order_no:
                continue

            try:
                updated_delivery_info = DeliveryInfo(
                    order_no,
                    receiver_name,
                    receiver_phone,
                    delivery_address,
                    delivery_info.get_delivery_status(),
                )
            except (TypeError, ValueError):
                return False

            self.__delivery_list[index] = updated_delivery_info
            return True

        return False

    # 배송 정보 존재 여부 확인
    def is_delivery_info_exist(self, order_no):
        return (
            self.select_delivery_info_by_order_no(order_no)
            is not None
        )

    # 배송 정보 삭제
    # 주문 생성 도중 실패했을 때 복구하기 위해 사용한다.
    def delete_delivery_info(self, order_no):
        for index, delivery_info in enumerate(
            self.__delivery_list
        ):
            if delivery_info.get_order_no() == order_no:
                del self.__delivery_list[index]
                return True

        return False