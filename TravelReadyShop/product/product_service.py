# product/product_service.py

from product.product import Product


class ProductService:
    def __init__(self):
        self.product_list = []
        self.next_product_id = 1
        self.init_products()

    def init_products(self):
        self.add_product("선크림", "여름용품", 12000, 30, "여름 여행과 야외 활동에 필요한 자외선 차단제")
        self.add_product("휴대용 선풍기", "여름용품", 18000, 20, "더운 날씨에 사용할 수 있는 충전식 휴대용 선풍기")
        self.add_product("멀티 어댑터", "해외여행용품", 25000, 15, "해외여행 시 여러 국가의 콘센트에 사용할 수 있는 어댑터")
        self.add_product("여행용 파우치", "수납용품", 9000, 40, "옷, 세면도구, 소품을 정리할 수 있는 여행용 파우치")
        self.add_product("보조배터리", "전자기기", 30000, 25, "휴대폰과 전자기기를 충전할 수 있는 보조배터리")
        self.add_product("핫팩", "겨울용품", 3000, 50, "겨울 여행 시 체온 유지를 위한 휴대용 핫팩")
        self.add_product("방수팩", "휴양용품", 8000, 35, "물놀이와 휴양지 여행에서 스마트폰을 보호하는 방수팩")
        self.add_product("노트북 파우치", "출장용품", 22000, 10, "출장 시 노트북을 안전하게 보관할 수 있는 파우치")

    def list_products(self):
        return self.product_list

    def search_products(self, keyword):
        if keyword is None:
            return []

        keyword = keyword.strip()

        if keyword == "":
            return []

        result = []

        for product in self.product_list:
            if keyword in product.name or keyword in product.category:
                result.append(product)

        return result

    def get_product_detail(self, product_id):
        for product in self.product_list:
            if product.product_id == product_id:
                return product

        return None

    def add_product(self, name, category, price, stock, description):
        if name == "" or category == "" or description == "":
            return None

        if price < 0 or stock < 0:
            return None

        new_product = Product(
            self.next_product_id,
            name,
            category,
            price,
            stock,
            description
        )

        self.product_list.append(new_product)
        self.next_product_id += 1

        return new_product

    def update_product(self, product_id, name, category, price, stock, description):
        product = self.get_product_detail(product_id)

        if product is None:
            return False

        if name == "" or category == "" or description == "":
            return False

        if price < 0 or stock < 0:
            return False

        product.name = name
        product.category = category
        product.price = price
        product.stock = stock
        product.description = description

        return True

    def delete_product(self, product_id):
        product = self.get_product_detail(product_id)

        if product is None:
            return False

        self.product_list.remove(product)

        return True