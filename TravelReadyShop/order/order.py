# order/order.py

class Order:
    """
    주문 정보와 배송 정보를 저장하는 클래스
    """

    ORDER_STATUS_LIST = ["주문완료", "주문취소"]
    DELIVERY_STATUS_LIST = ["배송준비", "배송중", "배송완료"]

    def __init__(self, order_id, member_id, order_items, total_price,
                 receiver_name, receiver_phone, address):
        self.order_id = order_id
        self.member_id = member_id
        self.order_items = []

        # 주문 당시의 상품 정보를 따로 저장한다.
        for item in order_items:
            product = item["product"]

            self.order_items.append({
                "product_id": product.product_id,
                "product_name": product.name,
                "price": product.price,
                "quantity": item["quantity"]
            })

        self.total_price = total_price
        self.receiver_name = receiver_name
        self.receiver_phone = receiver_phone
        self.address = address
        self.order_status = "주문완료"
        self.delivery_status = "배송준비"

    def update_order_status(self, status):
        if status not in self.ORDER_STATUS_LIST:
            return False

        self.order_status = status
        return True

    def update_delivery_status(self, status):
        if status not in self.DELIVERY_STATUS_LIST:
            return False

        self.delivery_status = status
        return True

    def __str__(self):
        result = (
            f"[주문번호: {self.order_id}]\n"
            f"회원아이디: {self.member_id}\n"
            f"주문상태: {self.order_status}\n"
            f"배송상태: {self.delivery_status}\n"
            f"수령인: {self.receiver_name}\n"
            f"연락처: {self.receiver_phone}\n"
            f"배송지: {self.address}\n"
            f"주문상품:\n"
        )

        for index, item in enumerate(self.order_items, start=1):
            price = item["price"] * item["quantity"]

            result += (
                f"{index}. {item['product_name']} / "
                f"수량: {item['quantity']}개 / "
                f"금액: {price}원\n"
            )

        result += f"총 주문 금액: {self.total_price}원"

        return result