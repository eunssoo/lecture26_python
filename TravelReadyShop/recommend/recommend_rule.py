# recommend/recommend_rule.py

class RecommendRule:
    """
    여행 조건에 따른 추천 규칙을 저장하는 클래스
    """

    def __init__(self, rule_id, condition_type, condition_value, recommend_items):
        self.rule_id = rule_id
        self.condition_type = condition_type
        self.condition_value = condition_value
        self.recommend_items = recommend_items

    def __str__(self):
        items = ", ".join(self.recommend_items)

        return (
            f"규칙번호: {self.rule_id}, "
            f"조건분류: {self.condition_type}, "
            f"조건값: {self.condition_value}, "
            f"추천항목: {items}"
        )