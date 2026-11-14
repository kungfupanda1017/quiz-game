from quiz import QuizGame

def show_menu():
    print("=============================")
    print("       📝 퀴즈 게임")
    print("=============================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록 보기")
    print("4. 점수 확인")
    print("5. 종료")
    print("=============================")

def main():
    game = QuizGame()  # 퀴즈게임 객체 생성
    
    while True:
        show_menu()
        choice = input("선택하세요: ").strip()
        
        if choice == "1":
            print("퀴즈 풀기 (준비중)")
        elif choice == "2":
            print("퀴즈 추가 (준비중)")
        elif choice == "3":
            print("퀴즈 목록 (준비중)")
        elif choice == "4":
            print("점수 확인 (준비중)")
        elif choice == "5":
            print("게임을 종료합니다. 👋")
            break
        else:
            print("❌ 1~5 중에서 선택하세요!")

if __name__ == "__main__":
    main()