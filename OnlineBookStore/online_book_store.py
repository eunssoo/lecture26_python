from order.order import DeliveryInfo


class OnlineBookStore:
    def __init__(
        self,
        member_service,
        book_service,
        cart_service,
        order_service,
    ):
        self.__member_service = member_service
        self.__book_service = book_service
        self.__cart_service = cart_service
        self.__order_service = order_service

    def input_int(self, message):
        while True:
            try:
                return int(input(message))
            except ValueError:
                print("숫자로 입력해주세요.")

    def run(self):
        self.start_menu()

    def start_menu(self):
        while True:
            print("\n========== OnlineBookStore ==========")
            print("1. 도서 목록")
            print("2. 도서 검색")
            print("3. 로그인")
            print("4. 회원가입")
            print("0. 종료")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.show_book_list()
            elif menu == 2:
                self.search_books()
            elif menu == 3:
                self.login()
            elif menu == 4:
                self.join_member()
            elif menu == 0:
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 메뉴입니다.")

    def join_member(self):
        print("\n========== 회원가입 ==========")

        user_id = input("아이디: ").strip()
        password = input("비밀번호: ")
        name = input("이름: ").strip()
        phone = input("전화번호: ").strip()
        address = input("주소: ").strip()

        result = self.__member_service.join_member(
            user_id,
            password,
            name,
            phone,
            address,
        )

        if not result:
            print("회원가입에 실패했습니다.")
            return

        if not self.__cart_service.create_cart(user_id):
            print("회원가입은 완료됐지만 장바구니 생성에 실패했습니다.")
            return

        print("회원가입이 완료되었습니다.")

    def login(self):
        print("\n========== 로그인 ==========")

        user_id = input("아이디: ").strip()
        password = input("비밀번호: ")

        if not self.__member_service.login(user_id, password):
            print("로그인에 실패했습니다.")
            return

        print("로그인되었습니다.")

        if self.__member_service.is_admin():
            self.admin_menu()
        else:
            self.member_menu()

    # ================================
    # 관리자 기능
    # ================================

    def admin_menu(self):
        while (
            self.__member_service.is_login()
            and self.__member_service.is_admin()
        ):
            print("\n========== 관리자 메뉴 ==========")
            print("1. 도서 관리")
            print("2. 회원 관리")
            print("3. 주문/배송 관리")
            print("0. 로그아웃")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.book_manage_menu()
            elif menu == 2:
                self.member_manage_menu()
            elif menu == 3:
                self.order_delivery_manage_menu()
            elif menu == 0:
                self.__member_service.logout()
                print("로그아웃되었습니다.")
            else:
                print("잘못된 메뉴입니다.")

    def book_manage_menu(self):
        if not self.__require_admin():
            return

        while True:
            print("\n========== 도서 관리 ==========")
            print("1. 도서 등록")
            print("2. 도서 목록 조회")
            print("3. 도서 상세 조회")
            print("4. 도서 정보 수정")
            print("5. 도서 삭제")
            print("0. 돌아가기")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.add_book()
            elif menu == 2:
                self.show_book_list()
            elif menu == 3:
                self.show_book_detail()
            elif menu == 4:
                self.modify_book()
            elif menu == 5:
                self.remove_book()
            elif menu == 0:
                break
            else:
                print("잘못된 메뉴입니다.")

    def add_book(self):
        if not self.__require_admin():
            return

        print("\n========== 도서 등록 ==========")

        title = input("제목: ").strip()
        author = input("저자: ").strip()
        publisher = input("출판사: ").strip()
        price = self.input_int("가격: ")
        stock = self.input_int("재고: ")

        result = self.__book_service.add_book(
            title,
            author,
            publisher,
            price,
            stock,
        )

        print(
            "도서가 등록되었습니다."
            if result
            else "도서 등록에 실패했습니다."
        )

    def modify_book(self):
        if not self.__require_admin():
            return

        print("\n========== 도서 정보 수정 ==========")

        book_no = self.input_int("수정할 도서번호: ")
        book = self.__book_service.get_book_info(book_no)

        if book is None:
            print("해당 도서를 찾을 수 없습니다.")
            return

        print(book)

        title = input("새 제목: ").strip()
        author = input("새 저자: ").strip()
        publisher = input("새 출판사: ").strip()
        price = self.input_int("새 가격: ")
        stock = self.input_int("새 재고: ")

        result = self.__book_service.modify_book_info(
            book_no,
            title,
            author,
            publisher,
            price,
            stock,
        )

        print(
            "도서 정보가 수정되었습니다."
            if result
            else "도서 정보 수정에 실패했습니다."
        )

    def remove_book(self):
        if not self.__require_admin():
            return

        print("\n========== 도서 삭제 ==========")

        book_no = self.input_int("삭제할 도서번호: ")
        book = self.__book_service.get_book_info(book_no)

        if book is None:
            print("해당 도서를 찾을 수 없습니다.")
            return

        print(book)

        if input("정말 삭제하시겠습니까? (y/n): ").strip().lower() != "y":
            print("도서 삭제를 취소했습니다.")
            return

        result = self.__book_service.remove_book(book_no)

        print(
            "도서가 삭제되었습니다."
            if result
            else "도서 삭제에 실패했습니다."
        )

    def member_manage_menu(self):
        if not self.__require_admin():
            return

        while True:
            print("\n========== 회원 관리 ==========")
            print("1. 회원 목록 조회")
            print("2. 회원 상세 조회")
            print("3. 회원 강제 삭제")
            print("0. 돌아가기")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.show_member_list()
            elif menu == 2:
                self.show_member_detail()
            elif menu == 3:
                self.remove_member_by_admin()
            elif menu == 0:
                break
            else:
                print("잘못된 메뉴입니다.")

    def show_member_list(self):
        if not self.__require_admin():
            return

        members = self.__member_service.get_all_members()

        print("\n========== 회원 목록 ==========")

        if not members:
            print("등록된 회원이 없습니다.")
            return

        for member in members:
            print(member)

    def show_member_detail(self):
        if not self.__require_admin():
            return

        member_no = self.input_int("회원번호: ")
        member = self.__member_service.get_member_info_by_no(member_no)

        if member is None:
            print("해당 회원을 찾을 수 없습니다.")
            return

        print(member)

    def remove_member_by_admin(self):
        if not self.__require_admin():
            return

        user_id = input("삭제할 회원 아이디: ").strip()
        member = self.__member_service.get_member_info(user_id)

        if member is None:
            print("해당 회원을 찾을 수 없습니다.")
            return

        print(member)

        if input("정말 삭제하시겠습니까? (y/n): ").strip().lower() != "y":
            print("회원 삭제를 취소했습니다.")
            return

        result = self.__member_service.remove_member_by_admin(user_id)

        if result:
            self.__cart_service.delete_cart(user_id)
            print("회원이 삭제되었습니다.")
        else:
            print("회원 삭제에 실패했습니다.")

    def order_delivery_manage_menu(self):
        if not self.__require_admin():
            return

        while True:
            print("\n========== 주문/배송 관리 ==========")
            print("1. 전체 주문 목록 조회")
            print("2. 주문 상세 조회")
            print("3. 배송 상태 변경")
            print("0. 돌아가기")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.show_all_orders()
            elif menu == 2:
                self.show_order_detail_by_admin()
            elif menu == 3:
                self.change_delivery_status()
            elif menu == 0:
                break
            else:
                print("잘못된 메뉴입니다.")

    def show_all_orders(self):
        if not self.__require_admin():
            return

        orders = self.__order_service.get_all_orders()

        if not orders:
            print("주문 내역이 없습니다.")
            return

        for order in orders:
            print(order)

    def show_order_detail_by_admin(self):
        if not self.__require_admin():
            return

        order_no = self.input_int("주문번호: ")
        detail = self.__order_service.get_order_detail(order_no)
        self.print_order_detail(detail)

    def change_delivery_status(self):
        if not self.__require_admin():
            return

        order_no = self.input_int("주문번호: ")

        print("1. 배송준비중")
        print("2. 배송중")
        print("3. 배송완료")

        status_menu = self.input_int("변경할 배송 상태: ")

        statuses = {
            1: DeliveryInfo.STATUS_PREPARING,
            2: DeliveryInfo.STATUS_SHIPPING,
            3: DeliveryInfo.STATUS_DELIVERED,
        }

        status = statuses.get(status_menu)

        if status is None:
            print("잘못된 배송 상태입니다.")
            return

        result = self.__order_service.change_delivery_status(
            order_no,
            status,
        )

        if result:
            print("배송 상태가 변경되었습니다.")
        else:
            print(
                "배송 상태 변경에 실패했습니다. "
                "배송준비중 → 배송중 → 배송완료 순서를 확인해주세요."
            )

    # ================================
    # 공통 도서 기능
    # ================================

    def show_book_list(self):
        books = self.__book_service.get_all_books()

        print("\n========== 도서 목록 ==========")

        if not books:
            print("등록된 도서가 없습니다.")
            return

        for book in books:
            print(book)

    def show_book_detail(self):
        book_no = self.input_int("도서번호: ")
        book = self.__book_service.get_book_info(book_no)

        if book is None:
            print("해당 도서를 찾을 수 없습니다.")
            return

        print(book)

    def search_books(self):
        keyword = input("검색어: ").strip()
        books = self.__book_service.search_books(keyword)

        if not books:
            print("검색 결과가 없습니다.")
            return

        for book in books:
            print(book)

    # ================================
    # 일반 회원 기능
    # ================================

    def member_menu(self):
        while (
            self.__member_service.is_login()
            and not self.__member_service.is_admin()
        ):
            print("\n========== 회원 메뉴 ==========")
            print("1. 도서 목록")
            print("2. 도서 검색")
            print("3. 장바구니 도서 담기")
            print("4. 장바구니 관리")
            print("5. 주문하기")
            print("6. 내 주문 관리")
            print("7. 내 정보")
            print("0. 로그아웃")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.show_book_list()
            elif menu == 2:
                self.search_books()
            elif menu == 3:
                self.add_book_to_cart()
            elif menu == 4:
                self.cart_menu()
            elif menu == 5:
                self.order_from_cart()
            elif menu == 6:
                self.my_order_menu()
            elif menu == 7:
                self.my_info_menu()
            elif menu == 0:
                self.__member_service.logout()
                print("로그아웃되었습니다.")
            else:
                print("잘못된 메뉴입니다.")

    def add_book_to_cart(self):
        member_id = self.__get_current_member_id()

        if member_id is None:
            return

        book_no = self.input_int("도서번호: ")
        quantity = self.input_int("수량: ")

        result = self.__cart_service.add_book_to_cart(
            member_id,
            book_no,
            quantity,
        )

        print(
            "장바구니에 도서를 담았습니다."
            if result
            else "장바구니 담기에 실패했습니다."
        )

    def cart_menu(self):
        while self.__member_service.is_login():
            print("\n========== 장바구니 메뉴 ==========")
            print("1. 장바구니 보기")
            print("2. 도서 수량 변경")
            print("3. 도서 삭제")
            print("4. 주문하기")
            print("0. 돌아가기")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.show_cart()
            elif menu == 2:
                self.change_cart_quantity()
            elif menu == 3:
                self.remove_book_from_cart()
            elif menu == 4:
                self.order_from_cart()
            elif menu == 0:
                break
            else:
                print("잘못된 메뉴입니다.")

    def show_cart(self):
        member_id = self.__get_current_member_id()

        if member_id is None:
            return

        details = self.__cart_service.get_cart_detail(member_id)

        print("\n========== 장바구니 ==========")

        if not details:
            print("장바구니가 비어 있습니다.")
            return

        for item in details:
            status = "" if item["available"] else " [구매 불가]"
            print(
                f"도서번호: {item['book_no']}, "
                f"제목: {item['title']}{status}, "
                f"가격: {item['price']:,}원, "
                f"수량: {item['quantity']}권, "
                f"소계: {item['subtotal']:,}원"
            )

        total_price = self.__cart_service.get_total_price(member_id)

        if total_price is None:
            print("삭제된 도서가 있어 총 금액을 계산할 수 없습니다.")
            return

        print(f"총 주문 금액: {total_price:,}원")

    def change_cart_quantity(self):
        member_id = self.__get_current_member_id()

        if member_id is None:
            return

        book_no = self.input_int("도서번호: ")
        quantity = self.input_int("변경할 수량: ")

        result = self.__cart_service.change_quantity(
            member_id,
            book_no,
            quantity,
        )

        print(
            "수량이 변경되었습니다."
            if result
            else "수량 변경에 실패했습니다."
        )

    def remove_book_from_cart(self):
        member_id = self.__get_current_member_id()

        if member_id is None:
            return

        book_no = self.input_int("삭제할 도서번호: ")

        result = self.__cart_service.remove_book_from_cart(
            member_id,
            book_no,
        )

        print(
            "장바구니에서 도서를 삭제했습니다."
            if result
            else "장바구니 도서 삭제에 실패했습니다."
        )

    def order_from_cart(self):
        member_id = self.__get_current_member_id()

        if member_id is None:
            return

        if self.__cart_service.is_cart_empty(member_id):
            print("장바구니가 비어 있어 주문할 수 없습니다.")
            return

        if not self.__cart_service.validate_cart_stock(member_id):
            print("삭제됐거나 재고가 부족한 도서가 있습니다.")
            return

        self.show_cart()

        receiver_name = input("수령인 이름: ").strip()
        receiver_phone = input("수령인 전화번호: ").strip()
        delivery_address = input("배송 주소: ").strip()

        if input("주문을 확정하시겠습니까? (y/n): ").strip().lower() != "y":
            print("주문을 취소했습니다.")
            return

        order_no = self.__order_service.create_order(
            member_id,
            receiver_name,
            receiver_phone,
            delivery_address,
        )

        if order_no is None:
            print("주문에 실패했습니다.")
        else:
            print(f"주문이 완료되었습니다. 주문번호: {order_no}")

    def my_order_menu(self):
        while self.__member_service.is_login():
            print("\n========== 내 주문 관리 ==========")
            print("1. 내 주문 목록")
            print("2. 주문 상세 보기")
            print("3. 주문 취소")
            print("0. 돌아가기")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.show_my_orders()
            elif menu == 2:
                self.show_my_order_detail()
            elif menu == 3:
                self.cancel_my_order()
            elif menu == 0:
                break
            else:
                print("잘못된 메뉴입니다.")

    def show_my_orders(self):
        member_id = self.__get_current_member_id()

        if member_id is None:
            return

        orders = self.__order_service.get_orders_by_member_id(member_id)

        if not orders:
            print("주문 내역이 없습니다.")
            return

        for order in orders:
            print(order)

    def show_my_order_detail(self):
        member_id = self.__get_current_member_id()

        if member_id is None:
            return

        order_no = self.input_int("주문번호: ")
        detail = self.__order_service.get_my_order_detail(
            member_id,
            order_no,
        )

        self.print_order_detail(detail)

    def cancel_my_order(self):
        member_id = self.__get_current_member_id()

        if member_id is None:
            return

        order_no = self.input_int("취소할 주문번호: ")

        if self.__order_service.get_my_order_info(
            member_id,
            order_no,
        ) is None:
            print("본인의 주문만 취소할 수 있습니다.")
            return

        if input("주문을 취소하시겠습니까? (y/n): ").strip().lower() != "y":
            print("주문 취소를 중단했습니다.")
            return

        result = self.__order_service.cancel_order(order_no)

        print(
            "주문이 취소되고 재고가 복구되었습니다."
            if result
            else "주문 취소에 실패했습니다."
        )

    def print_order_detail(self, detail):
        if detail is None:
            print("주문 정보를 찾을 수 없습니다.")
            return

        print("\n========== 주문 기본 정보 ==========")
        print(detail["order"])

        print("\n========== 주문 도서 목록 ==========")
        for item in detail["order_items"]:
            print(
                f"도서번호: {item['book_no']}, "
                f"제목: {item['title']}, "
                f"가격: {item['order_price']:,}원, "
                f"수량: {item['quantity']}권, "
                f"소계: {item['subtotal']:,}원"
            )

        print("\n========== 배송 정보 ==========")
        delivery_info = detail["delivery_info"]
        print(delivery_info if delivery_info else "배송 정보가 없습니다.")

    def my_info_menu(self):
        while self.__member_service.is_login():
            print("\n========== 내 정보 메뉴 ==========")
            print("1. 회원 정보 조회")
            print("2. 비밀번호 변경")
            print("3. 전화번호 변경")
            print("4. 주소 변경")
            print("5. 회원 탈퇴")
            print("0. 돌아가기")

            menu = self.input_int("메뉴 선택: ")

            if menu == 1:
                self.show_my_info()
            elif menu == 2:
                self.change_my_password()
            elif menu == 3:
                self.change_my_phone()
            elif menu == 4:
                self.change_my_address()
            elif menu == 5:
                self.withdraw_member()
                if not self.__member_service.is_login():
                    break
            elif menu == 0:
                break
            else:
                print("잘못된 메뉴입니다.")

    def show_my_info(self):
        current_user = self.__member_service.get_current_user()

        if current_user is None:
            print("로그인이 필요합니다.")
            return

        print(current_user)

    def change_my_password(self):
        user_id = self.__get_current_member_id()

        if user_id is None:
            return

        old_password = input("현재 비밀번호: ")
        new_password = input("새 비밀번호: ")

        result = self.__member_service.change_password(
            user_id,
            old_password,
            new_password,
        )

        print(
            "비밀번호가 변경되었습니다."
            if result
            else "비밀번호 변경에 실패했습니다."
        )

    def change_my_phone(self):
        user_id = self.__get_current_member_id()

        if user_id is None:
            return

        phone = input("새 전화번호: ").strip()
        result = self.__member_service.change_phone(user_id, phone)

        print(
            "전화번호가 변경되었습니다."
            if result
            else "전화번호 변경에 실패했습니다."
        )

    def change_my_address(self):
        user_id = self.__get_current_member_id()

        if user_id is None:
            return

        address = input("새 주소: ").strip()
        result = self.__member_service.change_address(user_id, address)

        print(
            "주소가 변경되었습니다."
            if result
            else "주소 변경에 실패했습니다."
        )

    def withdraw_member(self):
        user_id = self.__get_current_member_id()

        if user_id is None:
            return

        password = input("비밀번호 확인: ")

        if input("정말 탈퇴하시겠습니까? (y/n): ").strip().lower() != "y":
            print("회원 탈퇴를 취소했습니다.")
            return

        result = self.__member_service.remove_member(
            user_id,
            password,
        )

        if result:
            self.__cart_service.delete_cart(user_id)
            print("회원 탈퇴가 완료되었습니다.")
        else:
            print("회원 탈퇴에 실패했습니다.")

    # ================================
    # 내부 확인 메서드
    # ================================

    def __get_current_member_id(self):
        current_user = self.__member_service.get_current_user()

        if current_user is None:
            print("로그인이 필요합니다.")
            return None

        return current_user.get_user_id()

    def __require_admin(self):
        if not self.__member_service.is_admin():
            print("관리자 권한이 필요합니다.")
            return False

        return True