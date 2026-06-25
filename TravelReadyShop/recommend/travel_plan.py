# recommend/travel_plan.py

class TravelPlan:
    """
    회원이 입력한 여행 조건을 저장하는 클래스
    """

    def __init__(self, travel_type, destination, season, period, purpose):
        if period < 1:
            raise ValueError("여행 기간은 1일 이상이어야 합니다.")

        self.travel_type = travel_type
        self.destination = destination
        self.season = season
        self.period = period
        self.purpose = purpose
        self.period_type = self.set_period_type()

    def set_period_type(self):
        if self.period <= 2:
            return "단기"
        elif self.period <= 6:
            return "중기"
        else:
            return "장기"

    def __str__(self):
        return (
            f"여행구분: {self.travel_type}, "
            f"여행지: {self.destination}, "
            f"계절: {self.season}, "
            f"기간: {self.period}일({self.period_type}), "
            f"목적: {self.purpose}"
        )