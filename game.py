from quiz import Quiz, quiz_data

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score   = 0

    def load_data(self):
        self.quizzes = []
        for item in quiz_data:
            quiz = Quiz(item["question"], item["options"], item["answer"])
            self.quizzes.append(quiz)

    def play(self):
        self.load_data()
        self.score = 0

        print("\n📝 퀴즈를 시작합니다!")
        print("─" * 35)

        for i, quiz in enumerate(self.quizzes):
            print(f"\n[{i+1}/{len(self.quizzes)}] {quiz.question}")

            for j, option in enumerate(quiz.options):
                print(f"  {j+1}. {option}")

            answer = input("\n정답을 입력하세요: ").strip()

            # ✅ 번호 → 텍스트 변환
            if answer.isdigit():
                idx = int(answer) - 1
                if 0 <= idx < len(quiz.options):
                    selected = quiz.options[idx]
                else:
                    print("❌ 올바른 번호를 입력하세요!")
                    continue
            else:
                selected = answer

            # 채점
            if selected == quiz.answer:
                print("✅ 정답입니다!")
                self.score += 1
            else:
                print(f"❌ 오답! 정답은 '{quiz.answer}' 입니다.")

            print("─" * 35)

        print(f"\n🏆 최종 점수: {self.score}/{len(self.quizzes)}")

        if self.score == len(self.quizzes):
            print("🎉 완벽합니다! 모두 맞혔어요!")
        elif self.score >= len(self.quizzes) // 2:
            print("👍 잘 하셨어요! 조금만 더 공부해봐요!")
        else:
            print("💪 아쉽네요! 다시 도전해보세요!")