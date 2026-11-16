from game import QuizGame   

def show_menu():
    print("=" * 35)
    print("        📝 퀴즈 게임")
    print("=" * 35)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록 보기")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 35)

def main():
    game = QuizGame()
    game.load_quiz()          # ← 프로그램 시작 시 자동 불러오기

    while True:
        show_menu()
        choice = input("선택하세요: ").strip()

        if choice == "1":
            game.play()

        elif choice == "2":
            game.add_quiz()
            game.save_quiz()  # ← 퀴즈 추가 후 자동 저장

        elif choice == "3":
            game.show_quiz_list()

        elif choice == "4":
            game.show_score()
     
        elif choice == "5":
            game.save_quiz()  # ← 종료 전 자동 저장
            print("\n퀴즈를 저장하고 종료합니다. 👋")
            break

        else:
            print("❌ 1~5 중에서 선택하세요!")

if __name__ == "__main__":
    main()