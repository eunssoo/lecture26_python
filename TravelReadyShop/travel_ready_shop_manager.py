# travel_ready_shop_manager.py

class TravelReadyShopManager:
    """
    TravelReadyShop의 전체 메뉴 흐름을 담당하는 Manager 클래스

    역할:
    - 메뉴 출력
    - 사용자 입력
    - Service 메서드 호출
    - 결과 출력
    """

    def __init__(self, member_service, product_service, recommend_service,
                 checklist_service, cart_service, order_service):
        self.member_service = member_service
        self.product_service = product_service
        self.recommend_service = recommend_service
        self.checklist_service = checklist_service
        self.cart_service = cart_service
        self.order_service = order_service

    def input_int(self, message):
        try:
            return int(input(message))
        except ValueError:
            print("숫자로 입력하세요.")
            return None

    def get_current_member_id(self):
        if self.member_service.current_user is None:
            return None

        return self.member_service.current_user.member_id

    def start(self):
        while True:
            print()
            print("====================================")
            print("        TravelReadyShop")
            print("====================================")
            print("1. 상품 목록 조회")
            print("2. 상품 검색")
            print("3. 로그인")
            print("4. 회원가입")
            print("5. 관리자 로그인")
            print("0. 종료")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.list_products_menu()
            elif menu == "2":
                self.search_products_menu()
            elif menu == "3":
                self.login_menu()
            elif menu == "4":
                self.join_menu()
            elif menu == "5":
                self.admin_login_menu()
            elif menu == "0":
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 메뉴입니다.")

    def join_menu(self):
        print()
        print("========== 회원가입 ==========")

        member_id = input("아이디: ")
        password = input("비밀번호: ")
        name = input("이름: ")
        phone = input("전화번호: ")

        result = self.member_service.join(member_id, password, name, phone)

        if result:
            print("회원가입이 완료되었습니다.")
        else:
            print("회원가입에 실패했습니다. 입력값 또는 중복 아이디를 확인하세요.")

    def login_menu(self):
        print()
        print("========== 로그인 ==========")

        member_id = input("아이디: ")
        password = input("비밀번호: ")

        result = self.member_service.login(member_id, password)

        if result:
            print(f"{self.member_service.current_user.name}님 로그인되었습니다.")
            self.member_menu()
        else:
            print("아이디 또는 비밀번호가 일치하지 않습니다.")

    def admin_login_menu(self):
        print()
        print("========== 관리자 로그인 ==========")

        admin_id = input("관리자 아이디: ")
        admin_pw = input("관리자 비밀번호: ")

        if admin_id == "admin" and admin_pw == "1234":
            print("관리자 로그인 성공")
            self.admin_menu()
        else:
            print("관리자 아이디 또는 비밀번호가 일치하지 않습니다.")

    def list_products_menu(self):
        print()
        print("========== 상품 목록 ==========")

        product_list = self.product_service.list_products()

        if len(product_list) == 0:
            print("등록된 상품이 없습니다.")
            return

        for product in product_list:
            print(product)

    def search_products_menu(self):
        print()
        print("========== 상품 검색 ==========")

        keyword = input("검색어 입력: ")
        result = self.product_service.search_products(keyword)

        if len(result) == 0:
            print("검색 결과가 없습니다.")
            return

        for product in result:
            print(product)

    def product_detail_menu(self):
        print()
        print("========== 상품 상세 조회 ==========")

        product_id = self.input_int("상품번호 입력: ")

        if product_id is None:
            return

        product = self.product_service.get_product_detail(product_id)

        if product is None:
            print("존재하지 않는 상품입니다.")
        else:
            print(product.detail_info())

    def member_menu(self):
        while True:
            if self.member_service.current_user is None:
                break

            print()
            print("====================================")
            print("              회원 메뉴")
            print("====================================")
            print("1. 상품 목록 조회")
            print("2. 상품 검색")
            print("3. 상품 상세 조회")
            print("4. 여행 준비물 추천")
            print("5. 내 체크리스트 조회")
            print("6. 장바구니 보기")
            print("7. 주문하기")
            print("8. 내 주문/배송 조회")
            print("9. 내 정보 관리")
            print("10. 로그아웃")
            print("0. 종료")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.list_products_menu()
            elif menu == "2":
                self.search_products_menu()
            elif menu == "3":
                self.product_detail_menu()
            elif menu == "4":
                self.recommend_menu()
            elif menu == "5":
                self.checklist_menu()
            elif menu == "6":
                self.cart_menu()
            elif menu == "7":
                self.order_create_menu()
            elif menu == "8":
                self.my_order_menu()
            elif menu == "9":
                self.my_info_menu()

                if self.member_service.current_user is None:
                    break
            elif menu == "10":
                self.member_service.logout()
                self.recommend_service.last_travel_plan = None
                self.recommend_service.last_recommend_items = []
                print("로그아웃되었습니다.")
                break
            elif menu == "0":
                print("프로그램을 종료합니다.")
                exit()
            else:
                print("잘못된 메뉴입니다.")

    def recommend_menu(self):
        while True:
            print()
            print("====================================")
            print("          여행 준비물 추천 메뉴")
            print("====================================")
            print("1. 여행 조건 입력")
            print("2. 추천 결과 확인")
            print("3. 추천 상품 조회")
            print("4. 추천 결과 체크리스트 저장")
            print("5. 추천 상품 장바구니 담기")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.create_travel_plan_menu()
            elif menu == "2":
                self.show_recommend_items_menu()
            elif menu == "3":
                self.show_recommend_products_menu()
            elif menu == "4":
                self.save_recommend_checklist_menu()
            elif menu == "5":
                self.add_recommend_product_to_cart_menu()
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def create_travel_plan_menu(self):
        print()
        print("========== 여행 조건 입력 ==========")
        print("입력 예시")
        print("- 여행구분: 국내 / 해외")
        print("- 계절: 봄 / 여름 / 가을 / 겨울")
        print("- 목적: 관광 / 휴양 / 출장 / 액티비티 / 가족여행")

        travel_type = input("여행구분 입력: ")
        destination = input("여행지 입력: ")
        season = input("계절 입력: ")
        period = self.input_int("여행 기간 입력(일): ")

        if period is None or period < 1:
            print("여행 기간은 1일 이상 입력해야 합니다.")
            return

        purpose = input("여행 목적 입력: ")

        try:
            travel_plan = self.recommend_service.create_travel_plan(
                travel_type,
                destination,
                season,
                period,
                purpose
            )
        except ValueError as error:
            print(error)
            return

        recommend_items = self.recommend_service.recommend_items(travel_plan)

        print()
        print("여행 조건이 저장되었습니다.")
        print(travel_plan)

        print()
        print("추천 준비물:")
        if len(recommend_items) == 0:
            print("조건에 맞는 추천 준비물이 없습니다.")
        else:
            for item in recommend_items:
                print(f"- {item}")

    def show_recommend_items_menu(self):
        print()
        print("========== 추천 결과 확인 ==========")

        recommend_items = self.recommend_service.last_recommend_items

        if len(recommend_items) == 0:
            print("추천 결과가 없습니다. 먼저 여행 조건을 입력하세요.")
            return

        for index, item in enumerate(recommend_items, start=1):
            print(f"{index}. {item}")

    def show_recommend_products_menu(self):
        print()
        print("========== 추천 상품 조회 ==========")

        recommend_items = self.recommend_service.last_recommend_items

        if len(recommend_items) == 0:
            print("추천 결과가 없습니다. 먼저 여행 조건을 입력하세요.")
            return

        product_list = self.recommend_service.get_recommend_products(
            recommend_items,
            self.product_service
        )

        if len(product_list) == 0:
            print("추천 준비물과 관련된 등록 상품이 없습니다.")
            return

        for product in product_list:
            print(product)

    def save_recommend_checklist_menu(self):
        print()
        print("========== 추천 결과 체크리스트 저장 ==========")

        member_id = self.get_current_member_id()
        travel_plan = self.recommend_service.last_travel_plan
        recommend_items = self.recommend_service.last_recommend_items

        if travel_plan is None or len(recommend_items) == 0:
            print("저장할 추천 결과가 없습니다. 먼저 여행 조건을 입력하세요.")
            return

        checklist = self.checklist_service.save_checklist(
            member_id,
            travel_plan,
            recommend_items
        )

        if checklist is None:
            print("체크리스트 저장에 실패했습니다.")
        else:
            print("체크리스트가 저장되었습니다.")
            print(checklist)

    def add_recommend_product_to_cart_menu(self):
        print()
        print("========== 추천 상품 장바구니 담기 ==========")

        member_id = self.get_current_member_id()
        recommend_items = self.recommend_service.last_recommend_items

        if len(recommend_items) == 0:
            print("추천 결과가 없습니다. 먼저 여행 조건을 입력하세요.")
            return

        product_list = self.recommend_service.get_recommend_products(
            recommend_items,
            self.product_service
        )

        if len(product_list) == 0:
            print("추천 상품이 없습니다.")
            return

        for product in product_list:
            print(product)

        product_id = self.input_int("장바구니에 담을 상품번호 입력: ")

        if product_id is None:
            return

        product = self.product_service.get_product_detail(product_id)

        if product is None:
            print("존재하지 않는 상품입니다.")
            return

        if product not in product_list:
            print("추천 상품 목록에 있는 상품만 담을 수 있습니다.")
            return

        quantity = self.input_int("수량 입력: ")

        if quantity is None:
            return

        result = self.cart_service.add_to_cart(member_id, product, quantity)

        if result:
            print("장바구니에 상품을 담았습니다.")
        else:
            print("장바구니 담기에 실패했습니다. 재고 또는 수량을 확인하세요.")

    def checklist_menu(self):
        while True:
            print()
            print("====================================")
            print("          체크리스트 메뉴")
            print("====================================")
            print("1. 내 체크리스트 조회")
            print("2. 체크리스트 상세 조회")
            print("3. 체크리스트 완료 처리")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.list_my_checklists_menu()
            elif menu == "2":
                self.checklist_detail_menu()
            elif menu == "3":
                self.checklist_check_item_menu()
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def list_my_checklists_menu(self):
        print()
        print("========== 내 체크리스트 조회 ==========")

        member_id = self.get_current_member_id()
        checklist_list = self.checklist_service.get_my_checklists(member_id)

        if len(checklist_list) == 0:
            print("저장된 체크리스트가 없습니다.")
            return

        for checklist in checklist_list:
            print(f"체크리스트 번호: {checklist.checklist_id}, 제목: {checklist.title}")

    def checklist_detail_menu(self):
        print()
        print("========== 체크리스트 상세 조회 ==========")

        member_id = self.get_current_member_id()
        checklist_id = self.input_int("체크리스트 번호 입력: ")

        if checklist_id is None:
            return

        checklist = self.checklist_service.get_checklist_detail(checklist_id, member_id)

        if checklist is None:
            print("존재하지 않거나 본인의 체크리스트가 아닙니다.")
            return

        print(checklist)

    def checklist_check_item_menu(self):
        print()
        print("========== 체크리스트 완료 처리 ==========")

        member_id = self.get_current_member_id()
        checklist_id = self.input_int("체크리스트 번호 입력: ")

        if checklist_id is None:
            return

        checklist = self.checklist_service.get_checklist_detail(checklist_id, member_id)

        if checklist is None:
            print("존재하지 않거나 본인의 체크리스트가 아닙니다.")
            return

        print(checklist)

        item_no = self.input_int("완료 처리할 항목 번호 입력: ")

        if item_no is None:
            return

        result = self.checklist_service.check_item(checklist_id, item_no, member_id)

        if result:
            print("체크리스트 항목을 완료 처리했습니다.")
        else:
            print("완료 처리에 실패했습니다.")

    def cart_menu(self):
        while True:
            print()
            print("====================================")
            print("            장바구니 메뉴")
            print("====================================")
            print("1. 장바구니 보기")
            print("2. 상품 직접 담기")
            print("3. 장바구니 상품 삭제")
            print("4. 장바구니 비우기")
            print("5. 주문하기")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.show_cart_menu()
            elif menu == "2":
                self.add_product_to_cart_menu()
            elif menu == "3":
                self.delete_cart_item_menu()
            elif menu == "4":
                self.clear_cart_menu()
            elif menu == "5":
                self.order_create_menu()
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def show_cart_menu(self):
        print()
        print("========== 장바구니 보기 ==========")

        member_id = self.get_current_member_id()
        cart = self.cart_service.get_cart(member_id)

        print(cart)

    def add_product_to_cart_menu(self):
        print()
        print("========== 상품 장바구니 담기 ==========")

        member_id = self.get_current_member_id()
        self.list_products_menu()

        product_id = self.input_int("장바구니에 담을 상품번호 입력: ")

        if product_id is None:
            return

        product = self.product_service.get_product_detail(product_id)

        if product is None:
            print("존재하지 않는 상품입니다.")
            return

        quantity = self.input_int("수량 입력: ")

        if quantity is None:
            return

        result = self.cart_service.add_to_cart(member_id, product, quantity)

        if result:
            print("장바구니에 상품을 담았습니다.")
        else:
            print("장바구니 담기에 실패했습니다. 재고 또는 수량을 확인하세요.")

    def delete_cart_item_menu(self):
        print()
        print("========== 장바구니 상품 삭제 ==========")

        member_id = self.get_current_member_id()
        cart = self.cart_service.get_cart(member_id)

        if len(cart.item_list) == 0:
            print("장바구니가 비어 있습니다.")
            return

        print(cart)

        product_id = self.input_int("삭제할 상품번호 입력: ")

        if product_id is None:
            return

        result = self.cart_service.delete_cart_item(member_id, product_id)

        if result:
            print("장바구니에서 상품을 삭제했습니다.")
        else:
            print("장바구니에 해당 상품이 없습니다.")

    def clear_cart_menu(self):
        print()
        print("========== 장바구니 비우기 ==========")

        member_id = self.get_current_member_id()
        cart = self.cart_service.get_cart(member_id)

        if len(cart.item_list) == 0:
            print("장바구니가 이미 비어 있습니다.")
            return

        confirm = input("정말 장바구니를 비우시겠습니까? (y/n): ")

        if confirm.lower() != "y":
            print("장바구니 비우기를 취소했습니다.")
            return

        self.cart_service.clear_cart(member_id)
        print("장바구니를 비웠습니다.")

    def order_create_menu(self):
        print()
        print("========== 주문하기 ==========")

        member_id = self.get_current_member_id()
        cart = self.cart_service.get_cart(member_id)

        if len(cart.item_list) == 0:
            print("장바구니가 비어 있어 주문할 수 없습니다.")
            return

        print("[주문 상품 확인]")
        print(cart)

        receiver_name = input("수령인 이름: ")
        receiver_phone = input("수령인 연락처: ")
        address = input("배송지: ")

        confirm = input("주문하시겠습니까? (y/n): ")

        if confirm.lower() != "y":
            print("주문을 취소했습니다.")
            return

        order = self.order_service.create_order(
            member_id,
            cart,
            receiver_name,
            receiver_phone,
            address
        )

        if order is None:
            print("주문에 실패했습니다. 입력값, 장바구니 또는 재고를 확인하세요.")
        else:
            print("주문이 완료되었습니다.")
            print(order)

    def my_order_menu(self):
        while True:
            print()
            print("====================================")
            print("          내 주문/배송 메뉴")
            print("====================================")
            print("1. 내 주문 목록 조회")
            print("2. 주문 상세 보기")
            print("3. 배송 조회")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.list_my_orders_menu()
            elif menu == "2":
                self.my_order_detail_menu()
            elif menu == "3":
                self.my_delivery_status_menu()
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def list_my_orders_menu(self):
        print()
        print("========== 내 주문 목록 조회 ==========")

        member_id = self.get_current_member_id()
        order_list = self.order_service.list_my_orders(member_id)

        if len(order_list) == 0:
            print("주문 내역이 없습니다.")
            return

        for order in order_list:
            print(
                f"주문번호: {order.order_id}, "
                f"총 금액: {order.total_price}원, "
                f"주문상태: {order.order_status}, "
                f"배송상태: {order.delivery_status}"
            )

    def my_order_detail_menu(self):
        print()
        print("========== 주문 상세 보기 ==========")

        order_id = self.input_int("주문번호 입력: ")

        if order_id is None:
            return

        order = self.order_service.get_order_detail(order_id)

        if order is None:
            print("존재하지 않는 주문입니다.")
            return

        if order.member_id != self.get_current_member_id():
            print("본인의 주문만 조회할 수 있습니다.")
            return

        print(order)

    def my_delivery_status_menu(self):
        print()
        print("========== 배송 조회 ==========")

        order_id = self.input_int("주문번호 입력: ")

        if order_id is None:
            return

        order = self.order_service.get_order_detail(order_id)

        if order is None:
            print("존재하지 않는 주문입니다.")
            return

        if order.member_id != self.get_current_member_id():
            print("본인의 주문만 조회할 수 있습니다.")
            return

        print(f"배송상태: {order.delivery_status}")

    def my_info_menu(self):
        while True:
            print()
            print("====================================")
            print("            내 정보 메뉴")
            print("====================================")
            print("1. 내 정보 조회")
            print("2. 내 정보 수정")
            print("3. 회원 탈퇴")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.show_my_info_menu()
            elif menu == "2":
                self.update_my_info_menu()
            elif menu == "3":
                self.delete_my_account_menu()

                if self.member_service.current_user is None:
                    break
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def show_my_info_menu(self):
        print()
        print("========== 내 정보 조회 ==========")

        member = self.member_service.get_my_info()

        if member is None:
            print("로그인 정보가 없습니다.")
        else:
            print(member)

    def update_my_info_menu(self):
        print()
        print("========== 내 정보 수정 ==========")

        password = input("새 비밀번호: ")
        name = input("새 이름: ")
        phone = input("새 전화번호: ")

        result = self.member_service.update_my_info(password, name, phone)

        if result:
            print("회원 정보가 수정되었습니다.")
        else:
            print("회원 정보 수정에 실패했습니다. 입력값을 확인하세요.")

    def delete_my_account_menu(self):
        print()
        print("========== 회원 탈퇴 ==========")

        confirm = input("정말 탈퇴하시겠습니까? (y/n): ")

        if confirm.lower() != "y":
            print("회원 탈퇴를 취소했습니다.")
            return

        result = self.member_service.delete_my_account()

        if result:
            print("회원 탈퇴가 완료되었습니다.")
        else:
            print("회원 탈퇴에 실패했습니다.")

    def admin_menu(self):
        while True:
            print()
            print("====================================")
            print("             관리자 메뉴")
            print("====================================")
            print("1. 상품 관리")
            print("2. 회원 관리")
            print("3. 추천 규칙 관리")
            print("4. 주문/배송 관리")
            print("5. 로그아웃")
            print("0. 종료")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.admin_product_menu()
            elif menu == "2":
                self.admin_member_menu()
            elif menu == "3":
                self.admin_recommend_rule_menu()
            elif menu == "4":
                self.admin_order_menu()
            elif menu == "5":
                print("관리자 로그아웃되었습니다.")
                break
            elif menu == "0":
                print("프로그램을 종료합니다.")
                exit()
            else:
                print("잘못된 메뉴입니다.")

    def admin_product_menu(self):
        while True:
            print()
            print("====================================")
            print("            상품 관리 메뉴")
            print("====================================")
            print("1. 상품 등록")
            print("2. 상품 목록 관리")
            print("3. 상품 상세 관리")
            print("4. 상품 정보 수정")
            print("5. 상품 삭제")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.add_product_menu()
            elif menu == "2":
                self.list_products_menu()
            elif menu == "3":
                self.product_detail_menu()
            elif menu == "4":
                self.update_product_menu()
            elif menu == "5":
                self.delete_product_menu()
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def add_product_menu(self):
        print()
        print("========== 상품 등록 ==========")

        name = input("상품명: ")
        category = input("카테고리: ")
        price = self.input_int("가격: ")

        if price is None:
            return

        stock = self.input_int("재고 수량: ")

        if stock is None:
            return

        description = input("상품 설명: ")

        product = self.product_service.add_product(
            name,
            category,
            price,
            stock,
            description
        )

        if product is None:
            print("상품 등록에 실패했습니다. 입력값을 확인하세요.")
            return

        print("상품이 등록되었습니다.")
        print(product)

    def update_product_menu(self):
        print()
        print("========== 상품 정보 수정 ==========")

        self.list_products_menu()

        product_id = self.input_int("수정할 상품번호 입력: ")

        if product_id is None:
            return

        product = self.product_service.get_product_detail(product_id)

        if product is None:
            print("존재하지 않는 상품입니다.")
            return

        name = input("새 상품명: ")
        category = input("새 카테고리: ")
        price = self.input_int("새 가격: ")

        if price is None:
            return

        stock = self.input_int("새 재고 수량: ")

        if stock is None:
            return

        description = input("새 상품 설명: ")

        result = self.product_service.update_product(
            product_id,
            name,
            category,
            price,
            stock,
            description
        )

        if result:
            print("상품 정보가 수정되었습니다.")
        else:
            print("상품 정보 수정에 실패했습니다. 입력값을 확인하세요.")

    def delete_product_menu(self):
        print()
        print("========== 상품 삭제 ==========")

        self.list_products_menu()

        product_id = self.input_int("삭제할 상품번호 입력: ")

        if product_id is None:
            return

        confirm = input("정말 삭제하시겠습니까? (y/n): ")

        if confirm.lower() != "y":
            print("상품 삭제를 취소했습니다.")
            return

        result = self.product_service.delete_product(product_id)

        if result:
            print("상품이 삭제되었습니다.")
        else:
            print("상품 삭제에 실패했습니다.")

    def admin_member_menu(self):
        while True:
            print()
            print("====================================")
            print("            회원 관리 메뉴")
            print("====================================")
            print("1. 회원 목록 조회")
            print("2. 회원 상세 조회")
            print("3. 회원 삭제")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.admin_list_members_menu()
            elif menu == "2":
                self.admin_member_detail_menu()
            elif menu == "3":
                self.admin_delete_member_menu()
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def admin_list_members_menu(self):
        print()
        print("========== 회원 목록 조회 ==========")

        member_list = self.member_service.list_members()

        if len(member_list) == 0:
            print("등록된 회원이 없습니다.")
            return

        for member in member_list:
            print(member)

    def admin_member_detail_menu(self):
        print()
        print("========== 회원 상세 조회 ==========")

        member_id = input("회원 아이디 입력: ")
        member = self.member_service.get_member_detail(member_id)

        if member is None:
            print("존재하지 않는 회원입니다.")
        else:
            print(member)

    def admin_delete_member_menu(self):
        print()
        print("========== 회원 삭제 ==========")

        member_id = input("삭제할 회원 아이디 입력: ")

        confirm = input("정말 삭제하시겠습니까? (y/n): ")

        if confirm.lower() != "y":
            print("회원 삭제를 취소했습니다.")
            return

        result = self.member_service.delete_member(member_id)

        if result:
            print("회원이 삭제되었습니다.")
        else:
            print("회원 삭제에 실패했습니다.")

    def admin_recommend_rule_menu(self):
        while True:
            print()
            print("====================================")
            print("          추천 규칙 관리 메뉴")
            print("====================================")
            print("1. 추천 규칙 목록 조회")
            print("2. 추천 규칙 추가")
            print("3. 추천 규칙 수정")
            print("4. 추천 규칙 삭제")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.list_recommend_rules_menu()
            elif menu == "2":
                self.add_recommend_rule_menu()
            elif menu == "3":
                self.update_recommend_rule_menu()
            elif menu == "4":
                self.delete_recommend_rule_menu()
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def list_recommend_rules_menu(self):
        print()
        print("========== 추천 규칙 목록 조회 ==========")

        rule_list = self.recommend_service.list_rules()

        if len(rule_list) == 0:
            print("등록된 추천 규칙이 없습니다.")
            return

        for rule in rule_list:
            print(rule)

    def add_recommend_rule_menu(self):
        print()
        print("========== 추천 규칙 추가 ==========")
        print("조건분류 예시: 여행구분, 계절, 기간, 목적")
        print("추천항목은 쉼표로 구분해서 입력하세요.")
        print("예: 선크림, 선글라스, 모자")

        condition_type = input("조건분류: ")
        condition_value = input("조건값: ")
        recommend_items = input("추천항목: ")

        rule = self.recommend_service.add_rule(
            condition_type,
            condition_value,
            recommend_items
        )

        print("추천 규칙이 추가되었습니다.")
        print(rule)

    def update_recommend_rule_menu(self):
        print()
        print("========== 추천 규칙 수정 ==========")

        self.list_recommend_rules_menu()

        rule_id = self.input_int("수정할 규칙번호 입력: ")

        if rule_id is None:
            return

        condition_type = input("새 조건분류: ")
        condition_value = input("새 조건값: ")
        recommend_items = input("새 추천항목: ")

        result = self.recommend_service.update_rule(
            rule_id,
            condition_type,
            condition_value,
            recommend_items
        )

        if result:
            print("추천 규칙이 수정되었습니다.")
        else:
            print("추천 규칙 수정에 실패했습니다.")

    def delete_recommend_rule_menu(self):
        print()
        print("========== 추천 규칙 삭제 ==========")

        self.list_recommend_rules_menu()

        rule_id = self.input_int("삭제할 규칙번호 입력: ")

        if rule_id is None:
            return

        confirm = input("정말 삭제하시겠습니까? (y/n): ")

        if confirm.lower() != "y":
            print("추천 규칙 삭제를 취소했습니다.")
            return

        result = self.recommend_service.delete_rule(rule_id)

        if result:
            print("추천 규칙이 삭제되었습니다.")
        else:
            print("추천 규칙 삭제에 실패했습니다.")

    def admin_order_menu(self):
        while True:
            print()
            print("====================================")
            print("          주문/배송 관리 메뉴")
            print("====================================")
            print("1. 전체 주문 목록 조회")
            print("2. 주문 상세 조회")
            print("3. 주문 상태 변경")
            print("4. 배송 상태 변경")
            print("0. 돌아가기")
            print("====================================")

            menu = input("메뉴 선택: ")

            if menu == "1":
                self.admin_list_all_orders_menu()
            elif menu == "2":
                self.admin_order_detail_menu()
            elif menu == "3":
                self.admin_update_order_status_menu()
            elif menu == "4":
                self.admin_update_delivery_status_menu()
            elif menu == "0":
                break
            else:
                print("잘못된 메뉴입니다.")

    def admin_list_all_orders_menu(self):
        print()
        print("========== 전체 주문 목록 조회 ==========")

        order_list = self.order_service.list_all_orders()

        if len(order_list) == 0:
            print("주문 내역이 없습니다.")
            return

        for order in order_list:
            print(
                f"주문번호: {order.order_id}, "
                f"회원아이디: {order.member_id}, "
                f"총 금액: {order.total_price}원, "
                f"주문상태: {order.order_status}, "
                f"배송상태: {order.delivery_status}"
            )

    def admin_order_detail_menu(self):
        print()
        print("========== 주문 상세 조회 ==========")

        order_id = self.input_int("주문번호 입력: ")

        if order_id is None:
            return

        order = self.order_service.get_order_detail(order_id)

        if order is None:
            print("존재하지 않는 주문입니다.")
        else:
            print(order)

    def admin_update_order_status_menu(self):
        print()
        print("========== 주문 상태 변경 ==========")

        order_id = self.input_int("주문번호 입력: ")

        if order_id is None:
            return

        print("주문 상태 예시: 주문완료, 주문취소")
        status = input("변경할 주문 상태 입력: ")

        result = self.order_service.update_order_status(
            order_id,
            status,
            self.product_service
        )

        if result:
            print("주문 상태가 변경되었습니다.")
        else:
            print("주문 상태 변경에 실패했습니다. 주문번호 또는 상태값을 확인하세요.")

    def admin_update_delivery_status_menu(self):
        print()
        print("========== 배송 상태 변경 ==========")

        order_id = self.input_int("주문번호 입력: ")

        if order_id is None:
            return

        print("배송 상태 예시: 배송준비, 배송중, 배송완료")
        status = input("변경할 배송 상태 입력: ")

        result = self.order_service.update_delivery_status(order_id, status)

        if result:
            print("배송 상태가 변경되었습니다.")
        else:
            print("배송 상태 변경에 실패했습니다. 주문번호 또는 상태값을 확인하세요.")