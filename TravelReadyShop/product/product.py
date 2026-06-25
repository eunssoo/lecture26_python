# product/product.py

class Product:
    """
    여행용품 상품 정보를 저장하는 클래스
    """

    def __init__(self, product_id, name, category, price, stock, description):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description

    def __str__(self):
        return (
            f"상품번호: {self.product_id}, "
            f"상품명: {self.name}, "
            f"카테고리: {self.category}, "
            f"가격: {self.price}원, "
            f"재고: {self.stock}개"
        )

    def detail_info(self):
        return (
            f"상품번호: {self.product_id}\n"
            f"상품명: {self.name}\n"
            f"카테고리: {self.category}\n"
            f"가격: {self.price}원\n"
            f"재고: {self.stock}개\n"
            f"상품 설명: {self.description}"
        )