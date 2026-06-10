class Book:
    def __init__(
        self,
        book_no,
        title,
        author,
        publisher,
        price,
        stock,
    ):
        self.__validate_book_no(book_no)

        self.__book_no = book_no
        self.set_title(title)
        self.set_author(author)
        self.set_publisher(publisher)
        self.set_price(price)
        self.set_stock(stock)

    def get_book_no(self):
        return self.__book_no

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_publisher(self):
        return self.__publisher

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def set_title(self, title):
        self.__title = self.__validate_text(title, "도서 제목")

    def set_author(self, author):
        self.__author = self.__validate_text(author, "저자")

    def set_publisher(self, publisher):
        self.__publisher = self.__validate_text(publisher, "출판사")

    def set_price(self, price):
        if isinstance(price, bool) or not isinstance(price, int):
            raise TypeError("가격은 정수여야 합니다.")

        if price < 0:
            raise ValueError("가격은 0원 이상이어야 합니다.")

        self.__price = price

    def set_stock(self, stock):
        if isinstance(stock, bool) or not isinstance(stock, int):
            raise TypeError("재고는 정수여야 합니다.")

        if stock < 0:
            raise ValueError("재고는 0권 이상이어야 합니다.")

        self.__stock = stock

    def __validate_book_no(self, book_no):
        if isinstance(book_no, bool) or not isinstance(book_no, int):
            raise TypeError("도서번호는 정수여야 합니다.")

        if book_no <= 0:
            raise ValueError("도서번호는 1 이상이어야 합니다.")

    def __validate_text(self, value, field_name):
        if not isinstance(value, str):
            raise TypeError(f"{field_name}은 문자열이어야 합니다.")

        value = value.strip()

        if not value:
            raise ValueError(f"{field_name}은 비어 있을 수 없습니다.")

        return value

    def __str__(self):
        return (
            f"도서번호: {self.__book_no}, "
            f"제목: {self.__title}, "
            f"저자: {self.__author}, "
            f"출판사: {self.__publisher}, "
            f"가격: {self.__price:,}원, "
            f"재고: {self.__stock}권"
        )