from book.book import Book
from book.book_dao import BookDAO


class BookService:
    def __init__(self, book_dao: BookDAO):
        self.__book_dao = book_dao

    # 도서 등록
    def add_book(self, title, author, publisher, price, stock):
        try:
            book_no = self.__book_dao.get_next_book_no()

            book = Book(
                book_no,
                title,
                author,
                publisher,
                price,
                stock,
            )
        except (TypeError, ValueError):
            return False

        result = self.__book_dao.insert_book(book)

        # 반환값이 없는 기존 DAO도 지원한다.
        return result is not False

    # 전체 도서 조회
    def get_all_books(self):
        return self.__book_dao.select_all_books()

    # 도서번호로 상세 조회
    def get_book_info(self, book_no):
        if not self.__is_valid_book_no(book_no):
            return None

        return self.__book_dao.select_book_by_no(book_no)

    # 제목, 저자, 출판사 통합 검색
    def search_books(self, keyword):
        if not isinstance(keyword, str):
            return []

        keyword = keyword.strip()

        if not keyword:
            return []

        return self.__book_dao.search_books(keyword)

    # 도서 정보 수정
    def modify_book_info(
        self,
        book_no,
        title,
        author,
        publisher,
        price,
        stock,
    ):
        if not self.__is_valid_book_no(book_no):
            return False

        if not self.__book_dao.is_book_exist(book_no):
            return False

        try:
            updated_book = Book(
                book_no,
                title,
                author,
                publisher,
                price,
                stock,
            )
        except (TypeError, ValueError):
            return False

        return self.__book_dao.update_book(
            book_no,
            updated_book,
        )

    # 도서 삭제
    def remove_book(self, book_no):
        if not self.__is_valid_book_no(book_no):
            return False

        if not self.__book_dao.is_book_exist(book_no):
            return False

        return self.__book_dao.delete_book(book_no)

    # 도서 존재 여부 확인
    def is_book_exist(self, book_no):
        if not self.__is_valid_book_no(book_no):
            return False

        return self.__book_dao.is_book_exist(book_no)

    # 재고 확인
    def check_stock(self, book_no, quantity):
        if not self.__is_valid_book_no(book_no):
            return False

        if not self.__is_valid_quantity(quantity):
            return False

        book = self.__book_dao.select_book_by_no(book_no)

        if book is None:
            return False

        return book.get_stock() >= quantity

    # 재고 감소
    def decrease_stock(self, book_no, quantity):
        if not self.__is_valid_book_no(book_no):
            return False

        if not self.__is_valid_quantity(quantity):
            return False

        book = self.__book_dao.select_book_by_no(book_no)

        if book is None:
            return False

        if book.get_stock() < quantity:
            return False

        new_stock = book.get_stock() - quantity

        return self.__update_stock(book, new_stock)

    # 재고 증가
    def increase_stock(self, book_no, quantity):
        if not self.__is_valid_book_no(book_no):
            return False

        if not self.__is_valid_quantity(quantity):
            return False

        book = self.__book_dao.select_book_by_no(book_no)

        if book is None:
            return False

        new_stock = book.get_stock() + quantity

        return self.__update_stock(book, new_stock)

    # 재고만 변경한 새로운 Book 객체를 생성하여 저장
    def __update_stock(self, book, new_stock):
        try:
            updated_book = Book(
                book.get_book_no(),
                book.get_title(),
                book.get_author(),
                book.get_publisher(),
                book.get_price(),
                new_stock,
            )
        except (TypeError, ValueError):
            return False

        return self.__book_dao.update_book(
            book.get_book_no(),
            updated_book,
        )

    # 유효한 도서번호인지 확인
    def __is_valid_book_no(self, book_no):
        return (
            isinstance(book_no, int)
            and not isinstance(book_no, bool)
            and book_no > 0
        )

    # 유효한 수량인지 확인
    def __is_valid_quantity(self, quantity):
        return (
            isinstance(quantity, int)
            and not isinstance(quantity, bool)
            and quantity > 0
        )