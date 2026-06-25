# checklist/checklist.py

class Checklist:
    """
    회원별 여행 준비 체크리스트를 저장하는 클래스
    """

    def __init__(self, checklist_id, member_id, title, item_list):
        self.checklist_id = checklist_id
        self.member_id = member_id
        self.title = title
        self.item_list = []

        for item in item_list:
            self.item_list.append({
                "item_name": item,
                "is_checked": False
            })

    def check_item(self, item_no):
        index = item_no - 1

        if index < 0 or index >= len(self.item_list):
            return False

        self.item_list[index]["is_checked"] = True
        return True

    def __str__(self):
        result = f"[체크리스트 번호: {self.checklist_id}] {self.title}\n"

        for index, item in enumerate(self.item_list, start=1):
            if item["is_checked"]:
                status = "완료"
            else:
                status = "미완료"

            result += f"{index}. {item['item_name']} - {status}\n"

        return result