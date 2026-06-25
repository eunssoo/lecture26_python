# cart/cart_service.py

from cart.cart import Cart


class CartService:
    def __init__(self):
        self.cart_list = []

    def get_or_create_cart(self, member_id):
        for cart in self.cart_list:
            if cart.member_id == member_id:
                return cart

        new_cart = Cart(member_id)
        self.cart_list.append(new_cart)

        return new_cart

    def add_to_cart(self, member_id, product, quantity):
        if product is None:
            return False

        if quantity <= 0:
            return False

        cart = self.get_or_create_cart(member_id)

        current_quantity = 0

        for item in cart.item_list:
            if item["product"].product_id == product.product_id:
                current_quantity = item["quantity"]

        if product.stock < current_quantity + quantity:
            return False

        return cart.add_item(product, quantity)

    def get_cart(self, member_id):
        return self.get_or_create_cart(member_id)

    def delete_cart_item(self, member_id, product_id):
        cart = self.get_or_create_cart(member_id)
        return cart.delete_item(product_id)

    def clear_cart(self, member_id):
        cart = self.get_or_create_cart(member_id)
        cart.clear()

        return True