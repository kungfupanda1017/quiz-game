# ====================
# 퀴즈 게임 진입점 (main.py)
# ====================
# 미션 반영 수정사항
#  1) 메뉴 선택을 숫자 검증으로 처리 (빈 입력/비숫자/범위 밖 재입력)
#  2) Ctrl+C(KeyboardInterrupt) / 입력종료(EOFError) 발생 시
#     안내 출력 + 데이터 저장 후 안전 종료 (비정상 종료 방지)
#  3) 메뉴에 각 항목 설명 추가 (사용자 안내 보강)

from game import QuizGame


def main():
    game = QuizGame()  # 시작 시 state.json 자동 로드 (없으면 기본 데이터)

    print("\n💡 도움말: 메뉴 번호를 입력하세요. 퀴즈 정답은 1~4 번호로 입력합니다.")
    print("   (게임 중간에 Ctrl+C 를 눌러도 기록이 안전하게 저장됩니다)")

    try:
        while True:
            print("\n" + "=" * 40)
            print("        🎮 퀴즈 게임 메뉴")
            print("=" * 40)
            print("  1. 퀴즈 풀기     - 등록된 문제를 순서대로 출제")
            print("  2. 퀴즈 추가     - 문제/선택지 4개/정답 번호 등록")
            print("  3. 퀴즈 목록 보기 - 등록된 문제와 정답 확인")
            print("  4. 점수 확인     - 최고 기록(정답 수·등급) 확인")
            print("  5. 저장          - 현재 데이터를 state.json 에 저장")
            print("  6. 불러오기      - state.json 의 데이터 다시 읽기")
            print("  0. 종료")
            print("=" * 40)

            choice = input("메뉴 선택 (0-6) → ").strip()

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
                game.save_quiz()  # 종료 전 자동 저장
                print("\n👋 게임을 종료합니다. 수고하셨습니다!")
                break
            else:
                print("⚠️ 잘못된 입력입니다. 0-6 사이의 숫자를 입력하세요.")

    # ── 비정상 종료 방지: 안내 출력 + 저장 후 안전 종료 ──
    except KeyboardInterrupt:
        game.save_quiz()
        print("\n\n👋 Ctrl+C 감지: 데이터를 저장하고 안전하게 종료합니다.")

    except EOFError:
        game.save_quiz()
        print("\n\n👋 입력 스트림 종료 감지: 데이터를 저장하고 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
