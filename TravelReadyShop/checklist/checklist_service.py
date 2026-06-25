# checklist/checklist_service.py

from checklist.checklist import Checklist


class ChecklistService:
    def __init__(self):
        self.checklist_list = []
        self.next_checklist_id = 1

    def save_checklist(self, member_id, travel_plan, recommend_items):
        if recommend_items is None or len(recommend_items) == 0:
            return None

        title = f"{travel_plan.destination} 여행 준비 체크리스트"

        new_checklist = Checklist(
            self.next_checklist_id,
            member_id,
            title,
            recommend_items
        )

        self.checklist_list.append(new_checklist)
        self.next_checklist_id += 1

        return new_checklist

    def get_my_checklists(self, member_id):
        result = []

        for checklist in self.checklist_list:
            if checklist.member_id == member_id:
                result.append(checklist)

        return result

    def get_checklist_detail(self, checklist_id, member_id=None):
        for checklist in self.checklist_list:
            if checklist.checklist_id == checklist_id:
                if member_id is None or checklist.member_id == member_id:
                    return checklist

        return None

    def check_item(self, checklist_id, item_no, member_id=None):
        checklist = self.get_checklist_detail(checklist_id, member_id)

        if checklist is None:
            return False

        return checklist.check_item(item_no)