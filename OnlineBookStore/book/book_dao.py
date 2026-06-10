from book.book import Book


class BookDAO:
    def __init__(self):
        self.__book_list = []
        self.__next_book_no = 1
        self.__init_books()

    def __init_books(self):
        books = [
            Book(
                self.get_next_book_no(),
                "점프 투 파이썬",
                "박응용",
                "이지스퍼블리싱",
                22000,
                10,
            ),
            Book(
                self.get_next_book_no(),
                "혼자 공부하는 파이썬",
                "윤인성",
                "한빛미디어",
                26000,
                8,
            ),
            Book(
                self.get_next_book_no(),
                "Do it! 자바스크립트",
                "고경희",
                "이지스퍼블리싱",
                24000,
                5,
            ),
            Book(
                self.get_next_book_no(),
                "데이터베이스 개론",
                "김연희",
                "한빛아카데미",
                29000,
                7,
            ),
        ]

        for book in books:
            self.insert_book(book)

    def insert_book(self, book):
        if not isinstance(book, Book):
            raise TypeError("Book 객체만 등록할 수 있습니다.")

        if self.is_book_exist(book.get_book_no()):
            return False

        self.__book_list.append(book)
        return True

    def select_all_books(self):
        return self.__book_list.copy()

    def select_book_by_no(self, book_no):
        for book in self.__book_list:
            if book.get_book_no() == book_no:
                return book

        return None

    def search_books(self, keyword):
        if not isinstance(keyword, str):
            raise TypeError("검색어는 문자열이어야 합니다.")

        keyword = keyword.strip().casefold()

        if not keyword:
            return []

        result = []

        for book in self.__book_list:
            searchable_values = (
                book.get_title(),
                book.get_author(),
                book.get_publisher(),
            )

            if any(
                keyword in value.casefold()
                for value in searchable_values
            ):
                result.append(book)

        return result

    def update_book(self, book_no, book):
        if not isinstance(book, Book):
            raise TypeError("Book 객체만 수정할 수 있습니다.")

        # 기존 도서의 고유번호가 변경되는 것을 방지한다.
        if book.get_book_no() != book_no:
            return False

        for index, current_book in enumerate(self.__book_list):
            if current_book.get_book_no() == book_no:
                self.__book_list[index] = book
                return True

        return False

    def delete_book(self, book_no):
        for index, book in enumerate(self.__book_list):
            if book.get_book_no() == book_no:
                del self.__book_list[index]
                return True

        return False

    def is_book_exist(self, book_no):
        return self.select_book_by_no(book_no) is not None

    def get_next_book_no(self):
        book_no = self.__next_book_no
        self.__next_book_no += 1
        return book_no