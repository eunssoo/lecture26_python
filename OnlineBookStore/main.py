from member.member_dao import MemberDAO
from book.book_dao import BookDAO
from cart.cart_dao import CartDAO, CartItemDAO
from order.order_dao import OrderDAO, OrderItemDAO, DeliveryDAO

from member.member_service import MemberService
from book.book_service import BookService
from cart.cart_service import CartService
from order.order_service import OrderService

from online_book_store import OnlineBookStore


def main():
    # DAO 객체 생성
    member_dao = MemberDAO()
    book_dao = BookDAO()
    cart_dao = CartDAO()
    cart_item_dao = CartItemDAO()
    order_dao = OrderDAO()
    order_item_dao = OrderItemDAO()
    delivery_dao = DeliveryDAO()

    # Service 객체 생성
    member_service = MemberService(member_dao)
    book_service = BookService(book_dao)

    cart_service = CartService(
        cart_dao,
        cart_item_dao,
        book_service,
    )

    order_service = OrderService(
        order_dao,
        order_item_dao,
        delivery_dao,
        cart_service,
        book_service,
    )

    # 콘솔 애플리케이션 생성 및 실행
    app = OnlineBookStore(
        member_service,
        book_service,
        cart_service,
        order_service,
    )

    app.run()


if __name__ == "__main__":
    main()