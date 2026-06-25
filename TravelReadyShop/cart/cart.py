# cart/cart.py

class Cart:
    """
    회원별 장바구니 정보를 저장하는 클래스
    """

    def __init__(self, member_id):
        self.member_id = member_id
        self.item_list = []

    def add_item(self, product, quantity):
        if quantity <= 0:
            return False

        for item in self.item_list:
            if item["product"].product_id == product.product_id:
                item["quantity"] += quantity
                return True

        self.item_list.append({
            "product": product,
            "quantity": quantity
        })

        return True

    def delete_item(self, product_id):
        for item in self.item_list:
            if item["product"].product_id == product_id:
                self.item_list.remove(item)
                return True

        return False

    def clear(self):
        self.item_list.clear()

    def get_total_price(self):
        total = 0

        for item in self.item_list:
            product = item["product"]
            quantity = item["quantity"]
            total += product.price * quantity

        return total

    def __str__(self):
        if len(self.item_list) == 0:
            return "장바구니가 비어 있습니다."

        result = "[장바구니]\n"

        for index, item in enumerate(self.item_list, start=1):
            product = item["product"]
            quantity = item["quantity"]
            price = product.price * quantity

            result += (
                f"{index}. {product.name} / "
                f"수량: {quantity}개 / "
                f"금액: {price}원\n"
            )

        result += f"총 금액: {self.get_total_price()}원"

        return result