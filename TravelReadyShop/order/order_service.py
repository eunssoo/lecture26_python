# order/order_service.py

from order.order import Order


class OrderService:
    def __init__(self):
        self.order_list = []
        self.next_order_id = 1

    def create_order(self, member_id, cart, receiver_name, receiver_phone, address):
        if cart is None:
            return None

        if len(cart.item_list) == 0:
            return None

        if receiver_name == "" or receiver_phone == "" or address == "":
            return None

        for item in cart.item_list:
            product = item["product"]
            quantity = item["quantity"]

            if product.stock < quantity:
                return None

        total_price = cart.get_total_price()

        new_order = Order(
            self.next_order_id,
            member_id,
            cart.item_list,
            total_price,
            receiver_name,
            receiver_phone,
            address
        )

        for item in cart.item_list:
            product = item["product"]
            quantity = item["quantity"]
            product.stock -= quantity

        self.order_list.append(new_order)
        self.next_order_id += 1

        cart.clear()

        return new_order

    def list_my_orders(self, member_id):
        result = []

        for order in self.order_list:
            if order.member_id == member_id:
                result.append(order)

        return result

    def get_order_detail(self, order_id):
        for order in self.order_list:
            if order.order_id == order_id:
                return order

        return None

    def get_delivery_status(self, order_id):
        order = self.get_order_detail(order_id)

        if order is None:
            return None

        return order.delivery_status

    def list_all_orders(self):
        return self.order_list

    def update_order_status(self, order_id, status, product_service=None):
        order = self.get_order_detail(order_id)

        if order is None:
            return False

        before_status = order.order_status
        result = order.update_order_status(status)

        if result is False:
            return False

        if status == "주문취소" and before_status != "주문취소":
            self.restore_stock(order, product_service)

        return True

    def restore_stock(self, order, product_service):
        if product_service is None:
            return False

        for item in order.order_items:
            product = product_service.get_product_detail(item["product_id"])

            if product is not None:
                product.stock += item["quantity"]

        return True

    def update_delivery_status(self, order_id, status):
        order = self.get_order_detail(order_id)

        if order is None:
            return False

        return order.update_delivery_status(status)