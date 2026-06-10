# order/order_service.py

from datetime import datetime

from order.order import Order, OrderItem, DeliveryInfo


class OrderService:
    def __init__(
        self,
        order_dao,
        order_item_dao,
        delivery_dao,
        cart_service,
        book_service,
    ):
        self.__order_dao = order_dao
        self.__order_item_dao = order_item_dao
        self.__delivery_dao = delivery_dao
        self.__cart_service = cart_service
        self.__book_service = book_service

    # 주문 생성
    def create_order(
        self,
        member_id,
        receiver_name,
        receiver_phone,
        delivery_address,
    ):
        if not self.__is_valid_member_id(member_id):
            return None

        if self.__cart_service.is_cart_empty(member_id):
            return None

        if not self.__cart_service.validate_cart_stock(member_id):
            return None

        cart_items = self.__cart_service.get_cart_items(member_id)
        total_price = self.__cart_service.get_total_price(member_id)

        if not cart_items or total_price is None:
            return None

        order_no = self.__order_dao.get_next_order_no()
        order_date = datetime.now()

        try:
            order = Order(
                order_no,
                member_id,
                order_date,
                total_price,
                Order.STATUS_ORDER_COMPLETE,
            )

            delivery_info = DeliveryInfo(
                order_no,
                receiver_name,
                receiver_phone,
                delivery_address,
                DeliveryInfo.STATUS_PREPARING,
            )

            order_items = []

            for cart_item in cart_items:
                book_no = cart_item.get_book_no()
                quantity = cart_item.get_quantity()
                book = self.__book_service.get_book_info(book_no)

                if book is None:
                    return None

                order_items.append(
                    OrderItem(
                        order_no,
                        book_no,
                        quantity,
                        book.get_price(),
                    )
                )
        except (TypeError, ValueError):
            return None

        if not self.__order_dao.insert_order(order):
            return None

        saved_items = False
        saved_delivery = False
        decreased_stocks = []

        try:
            for order_item in order_items:
                if not self.__order_item_dao.insert_order_item(
                    order_item
                ):
                    raise RuntimeError("주문 항목 저장 실패")

            saved_items = True

            if not self.__delivery_dao.insert_delivery_info(
                delivery_info
            ):
                raise RuntimeError("배송 정보 저장 실패")

            saved_delivery = True

            # 저장 직후 재고를 다시 확인한다.
            for order_item in order_items:
                if not self.__book_service.check_stock(
                    order_item.get_book_no(),
                    order_item.get_quantity(),
                ):
                    raise RuntimeError("재고 부족")

            for order_item in order_items:
                book_no = order_item.get_book_no()
                quantity = order_item.get_quantity()

                if not self.__book_service.decrease_stock(
                    book_no,
                    quantity,
                ):
                    raise RuntimeError("재고 감소 실패")

                decreased_stocks.append((book_no, quantity))

            if not self.__cart_service.clear_cart(member_id):
                raise RuntimeError("장바구니 비우기 실패")

            return order_no

        except (RuntimeError, TypeError, ValueError):
            # 이미 감소한 재고를 복구한다.
            for book_no, quantity in reversed(decreased_stocks):
                self.__book_service.increase_stock(
                    book_no,
                    quantity,
                )

            if saved_delivery:
                self.__delivery_dao.delete_delivery_info(order_no)

            if saved_items:
                self.__order_item_dao.delete_order_items(order_no)
            else:
                # 일부 항목만 저장됐을 수도 있으므로 항상 정리한다.
                self.__order_item_dao.delete_order_items(order_no)

            self.__order_dao.delete_order(order_no)
            return None

    # 전체 주문 조회
    def get_all_orders(self):
        return self.__order_dao.select_all_orders()

    # 주문번호로 주문 조회
    def get_order_info(self, order_no):
        if not self.__is_valid_order_no(order_no):
            return None

        return self.__order_dao.select_order_by_no(order_no)

    # 회원별 주문 목록 조회
    def get_orders_by_member_id(self, member_id):
        if not self.__is_valid_member_id(member_id):
            return []

        return self.__order_dao.select_orders_by_member_id(member_id)

    # 본인의 주문 조회
    def get_my_order_info(self, member_id, order_no):
        if not self.__is_valid_member_id(member_id):
            return None

        order = self.get_order_info(order_no)

        if order is None:
            return None

        if order.get_member_id() != member_id:
            return None

        return order

    # 주문 항목 조회
    def get_order_items(self, order_no):
        if not self.__is_valid_order_no(order_no):
            return []

        return self.__order_item_dao.select_order_items_by_order_no(
            order_no
        )

    # 배송 정보 조회
    def get_delivery_info(self, order_no):
        if not self.__is_valid_order_no(order_no):
            return None

        return self.__delivery_dao.select_delivery_info_by_order_no(
            order_no
        )

    # 주문 상세 조회
    def get_order_detail(self, order_no):
        order = self.get_order_info(order_no)

        if order is None:
            return None

        order_items = self.get_order_items(order_no)
        delivery_info = self.get_delivery_info(order_no)
        item_details = []

        for order_item in order_items:
            book = self.__book_service.get_book_info(
                order_item.get_book_no()
            )

            if book is None:
                title = "삭제된 도서"
                author = "-"
                publisher = "-"
            else:
                title = book.get_title()
                author = book.get_author()
                publisher = book.get_publisher()

            item_details.append({
                "book_no": order_item.get_book_no(),
                "title": title,
                "author": author,
                "publisher": publisher,
                "order_price": order_item.get_order_price(),
                "quantity": order_item.get_quantity(),
                "subtotal": order_item.get_subtotal(),
            })

        return {
            "order": order,
            "order_items": item_details,
            "delivery_info": delivery_info,
        }

    # 본인의 주문 상세 조회
    def get_my_order_detail(self, member_id, order_no):
        if self.get_my_order_info(member_id, order_no) is None:
            return None

        return self.get_order_detail(order_no)

    # 주문 상태 변경
    def change_order_status(self, order_no, new_status):
        order = self.get_order_info(order_no)

        if order is None:
            return False

        if new_status == Order.STATUS_CANCELED:
            return self.cancel_order(order_no)

        status_mapping = {
            Order.STATUS_PREPARING:
                DeliveryInfo.STATUS_PREPARING,
            Order.STATUS_SHIPPING:
                DeliveryInfo.STATUS_SHIPPING,
            Order.STATUS_DELIVERED:
                DeliveryInfo.STATUS_DELIVERED,
        }

        delivery_status = status_mapping.get(new_status)

        if delivery_status is None:
            return False

        return self.change_delivery_status(
            order_no,
            delivery_status,
        )

    # 배송 상태 변경
    def change_delivery_status(
        self,
        order_no,
        new_delivery_status,
    ):
        order = self.get_order_info(order_no)
        delivery_info = self.get_delivery_info(order_no)

        if order is None or delivery_info is None:
            return False

        if order.get_order_status() == Order.STATUS_CANCELED:
            return False

        current_delivery_status = (
            delivery_info.get_delivery_status()
        )

        if not self.__is_valid_delivery_transition(
            order.get_order_status(),
            current_delivery_status,
            new_delivery_status,
        ):
            return False

        order_status_mapping = {
            DeliveryInfo.STATUS_PREPARING:
                Order.STATUS_PREPARING,
            DeliveryInfo.STATUS_SHIPPING:
                Order.STATUS_SHIPPING,
            DeliveryInfo.STATUS_DELIVERED:
                Order.STATUS_DELIVERED,
        }

        new_order_status = order_status_mapping.get(
            new_delivery_status
        )

        if new_order_status is None:
            return False

        # 배송 상태를 먼저 변경한다.
        if current_delivery_status != new_delivery_status:
            if not self.__delivery_dao.update_delivery_status(
                order_no,
                new_delivery_status,
            ):
                return False

        # 주문 상태 변경 실패 시 배송 상태를 원래대로 복구한다.
        if not self.__order_dao.update_order_status(
            order_no,
            new_order_status,
        ):
            if current_delivery_status != new_delivery_status:
                self.__delivery_dao.update_delivery_status(
                    order_no,
                    current_delivery_status,
                )

            return False

        return True

    # 주문 취소
    def cancel_order(self, order_no):
        order = self.get_order_info(order_no)

        if order is None:
            return False

        cancelable_statuses = {
            Order.STATUS_ORDER_COMPLETE,
            Order.STATUS_PREPARING,
        }

        if order.get_order_status() not in cancelable_statuses:
            return False

        order_items = self.get_order_items(order_no)
        restored_stocks = []

        # 주문 당시 감소한 재고를 복구한다.
        for order_item in order_items:
            book_no = order_item.get_book_no()
            quantity = order_item.get_quantity()

            if not self.__book_service.increase_stock(
                book_no,
                quantity,
            ):
                # 복구 도중 실패하면 앞서 증가시킨 재고를 다시 감소시킨다.
                for restored_book_no, restored_quantity in reversed(
                    restored_stocks
                ):
                    self.__book_service.decrease_stock(
                        restored_book_no,
                        restored_quantity,
                    )

                return False

            restored_stocks.append((book_no, quantity))

        if not self.__order_dao.update_order_status(
            order_no,
            Order.STATUS_CANCELED,
        ):
            for book_no, quantity in reversed(restored_stocks):
                self.__book_service.decrease_stock(
                    book_no,
                    quantity,
                )

            return False

        return True

    # 배송 상태 전환 가능 여부 확인
    @staticmethod
    def __is_valid_delivery_transition(
        order_status,
        current_status,
        new_status,
    ):
        # 주문완료 상태에서 배송준비중으로 전환하는 경우
        if (
            order_status == Order.STATUS_ORDER_COMPLETE
            and current_status == DeliveryInfo.STATUS_PREPARING
            and new_status == DeliveryInfo.STATUS_PREPARING
        ):
            return True

        allowed_transitions = {
            DeliveryInfo.STATUS_PREPARING: {
                DeliveryInfo.STATUS_SHIPPING,
            },
            DeliveryInfo.STATUS_SHIPPING: {
                DeliveryInfo.STATUS_DELIVERED,
            },
            DeliveryInfo.STATUS_DELIVERED: set(),
        }

        return new_status in allowed_transitions.get(
            current_status,
            set(),
        )

    @staticmethod
    def __is_valid_member_id(member_id):
        return (
            isinstance(member_id, str)
            and bool(member_id.strip())
        )

    @staticmethod
    def __is_valid_order_no(order_no):
        return (
            isinstance(order_no, int)
            and not isinstance(order_no, bool)
            and order_no > 0
        )