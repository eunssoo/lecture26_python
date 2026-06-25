# recommend/recommend_service.py

from recommend.travel_plan import TravelPlan
from recommend.recommend_rule import RecommendRule


class RecommendService:
    """
    여행 조건 기반 추천 기능을 처리하는 Service 클래스

    담당 기능:
    - 여행 조건 입력
    - 추천 결과 생성
    - 추천 상품 조회
    - 추천 규칙 목록 조회
    - 추천 규칙 추가
    - 추천 규칙 수정
    - 추천 규칙 삭제
    """

    def __init__(self):
        self.recommend_rule_list = []
        self.next_rule_id = 1

        # 마지막으로 입력한 여행 조건과 추천 결과 저장
        self.last_travel_plan = None
        self.last_recommend_items = []

        # 기본 추천 규칙 등록
        self.init_rules()

    def init_rules(self):
        """
        프로그램 실행 시 기본 추천 규칙을 등록한다.
        """

        # 국내 / 해외 기준
        self.add_rule(
            "여행구분",
            "국내",
            ["신분증", "숙소 예약 확인", "교통 예약 확인", "보조배터리", "상비약"]
        )

        self.add_rule(
            "여행구분",
            "해외",
            ["여권", "비자 확인", "여행자 보험", "멀티 어댑터", "보조배터리"]
        )

        # 계절 기준
        self.add_rule(
            "계절",
            "봄",
            ["얇은 겉옷", "마스크", "선크림", "알레르기 약", "물티슈"]
        )

        self.add_rule(
            "계절",
            "여름",
            ["선크림", "선글라스", "모자", "휴대용 선풍기", "쿨링 티슈", "방수팩"]
        )

        self.add_rule(
            "계절",
            "가을",
            ["가벼운 겉옷", "보습제", "선크림", "편한 운동화", "휴대용 우산"]
        )

        self.add_rule(
            "계절",
            "겨울",
            ["목도리", "장갑", "핫팩", "보온병", "립밤", "보습 크림"]
        )

        # 여행 기간 기준
        self.add_rule(
            "기간",
            "단기",
            ["미니 파우치", "보조배터리", "간단한 세면도구", "여벌 속옷"]
        )

        self.add_rule(
            "기간",
            "중기",
            ["여벌 옷", "세면도구 세트", "여행용 파우치", "빨래 봉투", "보조가방"]
        )

        self.add_rule(
            "기간",
            "장기",
            ["압축팩", "세탁망", "휴대용 세제", "대용량 파우치", "예비 충전기"]
        )

        # 여행 목적 기준
        self.add_rule(
            "목적",
            "관광",
            ["편한 운동화", "작은 크로스백", "보조배터리", "셀카봉", "휴대용 물병"]
        )

        self.add_rule(
            "목적",
            "휴양",
            ["수영복", "방수팩", "슬리퍼", "비치타월", "선크림", "선글라스"]
        )

        self.add_rule(
            "목적",
            "출장",
            ["노트북 충전기", "노트북 파우치", "서류 파일", "정장 관리용품", "멀티 어댑터"]
        )

        self.add_rule(
            "목적",
            "액티비티",
            ["방수팩", "스포츠 타월", "여분 양말", "활동용 가방", "밴드", "소독약"]
        )

        self.add_rule(
            "목적",
            "가족여행",
            ["대용량 물티슈", "가족 상비약", "간식", "보조가방", "휴대용 담요"]
        )

    def create_travel_plan(self, travel_type, destination, season, period, purpose):
        """
        여행 조건을 TravelPlan 객체로 생성한다.
        """
        travel_plan = TravelPlan(
            travel_type,
            destination,
            season,
            period,
            purpose
        )

        self.last_travel_plan = travel_plan

        return travel_plan

    def recommend_items(self, travel_plan):
        """
        여행 조건에 맞는 추천 준비물 목록을 생성한다.

        추천 기준:
        - 여행구분: 국내 / 해외
        - 계절: 봄 / 여름 / 가을 / 겨울
        - 기간: 단기 / 중기 / 장기
        - 목적: 관광 / 휴양 / 출장 / 액티비티 / 가족여행
        """
        result = []

        for rule in self.recommend_rule_list:
            is_match = False

            if rule.condition_type == "여행구분" and rule.condition_value == travel_plan.travel_type:
                is_match = True

            elif rule.condition_type == "계절" and rule.condition_value == travel_plan.season:
                is_match = True

            elif rule.condition_type == "기간" and rule.condition_value == travel_plan.period_type:
                is_match = True

            elif rule.condition_type == "목적" and rule.condition_value == travel_plan.purpose:
                is_match = True

            if is_match:
                for item in rule.recommend_items:
                    if item not in result:
                        result.append(item)

        self.last_recommend_items = result

        return result

    def get_recommend_products(self, recommend_items, product_service):
        """
        추천 준비물과 관련된 상품 목록을 조회한다.

        ProductService의 상품 목록에서
        상품명, 카테고리, 설명에 추천 항목이 포함되어 있으면 추천 상품으로 판단한다.
        """
        result = []

        product_list = product_service.list_products()

        for recommend_item in recommend_items:
            for product in product_list:
                if (
                    recommend_item in product.name
                    or recommend_item in product.category
                    or recommend_item in product.description
                    or product.name in recommend_item
                ):
                    if product not in result:
                        result.append(product)

        return result

    def list_rules(self):
        """
        추천 규칙 목록을 반환한다.
        """
        return self.recommend_rule_list

    def get_rule(self, rule_id):
        """
        추천 규칙 번호로 추천 규칙을 조회한다.
        """
        for rule in self.recommend_rule_list:
            if rule.rule_id == rule_id:
                return rule

        return None

    def add_rule(self, condition_type, condition_value, recommend_items):
        """
        추천 규칙 추가

        recommend_items는 리스트 또는 문자열로 받을 수 있다.
        문자열인 경우 쉼표를 기준으로 나누어 리스트로 변환한다.
        """
        item_list = self.change_to_item_list(recommend_items)

        new_rule = RecommendRule(
            self.next_rule_id,
            condition_type,
            condition_value,
            item_list
        )

        self.recommend_rule_list.append(new_rule)
        self.next_rule_id += 1

        return new_rule

    def update_rule(self, rule_id, condition_type, condition_value, recommend_items):
        """
        추천 규칙 수정
        """
        rule = self.get_rule(rule_id)

        if rule is None:
            return False

        rule.condition_type = condition_type
        rule.condition_value = condition_value
        rule.recommend_items = self.change_to_item_list(recommend_items)

        return True

    def delete_rule(self, rule_id):
        """
        추천 규칙 삭제
        """
        rule = self.get_rule(rule_id)

        if rule is None:
            return False

        self.recommend_rule_list.remove(rule)

        return True

    def change_to_item_list(self, recommend_items):
        """
        추천 항목을 리스트 형태로 변환한다.

        예:
        "선크림, 선글라스, 모자"
        → ["선크림", "선글라스", "모자"]
        """
        if isinstance(recommend_items, list):
            return recommend_items

        item_list = []

        split_items = recommend_items.split(",")

        for item in split_items:
            item = item.strip()

            if item != "":
                item_list.append(item)

        return item_list