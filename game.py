import json
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

            if answer.isdigit():
                idx = int(answer) - 1
                if 0 <= idx < len(quiz.options):
                    selected = quiz.options[idx]
                else:
                    print("❌ 올바른 번호를 입력하세요!")
                    continue
            else:
                selected = answer

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

    def add_quiz(self):
        print("\n📝 퀴즈 추가")
        print("─" * 35)

        question = input("문제를 입력하세요: ").strip()
        if not question:
            print("❌ 문제를 입력해야 합니다!")
            return

        options = []
        for i in range(4):
            option = input(f"선택지 {i+1}번 입력: ").strip()
            if not option:
                print("❌ 선택지를 입력해야 합니다!")
                return
            options.append(option)

        print("\n선택지 목록:")
        for i, opt in enumerate(options):
            print(f"  {i+1}. {opt}")

        answer_num = input("\n정답 번호를 입력하세요 (1~4): ").strip()

        if not answer_num.isdigit() or not (1 <= int(answer_num) <= 4):
            print("❌ 1~4 사이의 번호를 입력해야 합니다!")
            return

        answer = options[int(answer_num) - 1]

        quiz_data.append({
            "question": question,
            "options": options,
            "answer": answer
        })

        print(f"\n✅ 퀴즈가 추가되었습니다!")
        print(f"   문제: {question}")
        print(f"   정답: {answer}")
        print("─" * 35)

    def show_quiz_list(self):
        print("\n📋 퀴즈 목록")
        print("─" * 35)

        if not quiz_data:
            print("❌ 등록된 퀴즈가 없습니다!")
            return

        for i, item in enumerate(quiz_data):
            print(f"\n[{i+1}] {item['question']}")
            for j, opt in enumerate(item['options']):
                print(f"  {j+1}. {opt}")
            print(f"  ✅ 정답: {item['answer']}")
            print("─" * 35)

        print(f"\n총 {len(quiz_data)}개의 퀴즈가 있습니다!")

    def save_quiz(self):
        with open("quizzes.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=4)
        print("\n✅ 퀴즈가 저장되었습니다! (quizzes.json)")

    def show_score(self):
        print("\n🏆 점수 확인")
        print("─" * 35)

        # 퀴즈를 한 번도 안 풀었을 때
        if self.score == 0 and len(self.quizzes) == 0:
            print("❌ 아직 퀴즈를 풀지 않았어요!")
            print("   먼저 퀴즈를 풀어보세요! 💪")
            print("─" * 35)
            return

        total = len(self.quizzes)   # 총 문제 수
        score = self.score          # 맞힌 개수

        # 정답률 계산
        rate = (score / total) * 100

        # 등급 계산
        if rate == 100:
            grade = "S 🌟"
        elif rate >= 80:
            grade = "A 😊"
        elif rate >= 60:
            grade = "B 👍"
        else:
            grade = "C 💪"

        # 출력
        print(f"  📊 점수    : {score} / {total}")
        print(f"  📈 정답률  : {rate:.1f}%")
        print(f"  🎖️  등급    : {grade}")
        print("─" * 35)

    def load_quiz(self):
        try:
            with open("quizzes.json", "r", encoding="utf-8") as f:
                loaded = json.load(f)
            quiz_data.clear()
            quiz_data.extend(loaded)
            print(f"\n✅ {len(quiz_data)}개의 퀴즈를 불러왔습니다!")
        except FileNotFoundError:
            print("\n❌ 저장된 파일이 없습니다!")