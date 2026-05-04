import random

# 1. 단어 리스트 만들기
word_list = ["MAN", "WOMAN", "BANANA", "TOMATO", "APPEL"]

# 2. 컴퓨터가 단어 랜덤 선택
target_word = random.choice(word_list)

# 3. 기본 설정
blank_char = "_"
limit_error = 7

# 4. 화면에 보여줄 단어 상태 만들기
# 예: MAN -> ___
word_screen = blank_char * len(target_word)

# 5. 오답 횟수
num_error = 0

print("========== Hangman ==========")
print("Computer가 생각한 단어 :", word_screen)
print(f"({len(target_word)}글자)")

while num_error < limit_error:
    # 사용자 알파벳 입력
    user_input = input(">> 알파벳 입력 : ").upper()

    # 입력한 알파벳이 단어에 없으면 오답 횟수 증가
    if target_word.find(user_input) == -1:
        num_error += 1
        print(f"오답 : {num_error}회")
        print(word_screen)

    # 입력한 알파벳이 단어에 있으면 해당 위치 채우기
    else:
        for i in range(len(target_word)):
            if target_word[i] == user_input:
                word_screen = word_screen[:i] + user_input + word_screen[i + 1:]

        print("정답 :", word_screen)

    # 단어를 다 맞히면 사용자 승리
    if word_screen.count(blank_char) == 0:
        print("You win ~~~~ !!!")
        break

# 오답 횟수가 제한에 도달하면 패배
if num_error >= limit_error:
    print("You lose ... :", target_word)