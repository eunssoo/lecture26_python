# main.py

from member.member_service import MemberService
from product.product_service import ProductService
from recommend.recommend_service import RecommendService
from checklist.checklist_service import ChecklistService
from cart.cart_service import CartService
from order.order_service import OrderService

from travel_ready_shop_manager import TravelReadyShopManager


def main():
    """
    TravelReadyShop 프로그램 실행 함수

    역할:
    1. Service 객체 생성
    2. Manager 객체 생성
    3. 프로그램 시작
    """

    # Service 객체 생성
    member_service = MemberService()
    product_service = ProductService()
    recommend_service = RecommendService()
    checklist_service = ChecklistService()
    cart_service = CartService()
    order_service = OrderService()

    # Manager 객체 생성
    app = TravelReadyShopManager(
        member_service,
        product_service,
        recommend_service,
        checklist_service,
        cart_service,
        order_service
    )

    # 프로그램 실행
    app.start()


if __name__ == "__main__":
    main()