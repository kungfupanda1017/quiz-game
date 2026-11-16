from game import QuizGame

def main():
    game = QuizGame()

    while True:
        print("\n" + "=" * 40)
        print("        🎮 퀴즈 게임 메뉴")
        print("=" * 40)
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록 보기")
        print("  4. 점수 확인")
        print("  5. 퀴즈 저장")
        print("  6. 퀴즈 불러오기")
        print("  0. 종료")
        print("=" * 40)

        choice = input("메뉴 선택 → ").strip()

        if choice == "1":
            game.play()
        elif choice == "2":
            game.add_quiz()
        elif choice == "3":
            game.show_quiz_list()
        elif choice == "4":
            game.show_score()
        elif choice == "5":
            game.save_quiz()
        elif choice == "6":
            game.load_quiz()
        elif choice == "0":
            print("\n👋 게임을 종료합니다. 수고하셨습니다!")
            break
        else:
            print("\n⚠️ 올바른 메뉴 번호를 입력하세요.")

if __name__ == "__main__":
    main()