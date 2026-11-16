import json
from datetime import datetime

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.high_score = self._load_high_score()  # 파일에서 불러오기

    # ─────────────────────────────────────────
    # 최고점수 파일 불러오기
    # ─────────────────────────────────────────
    def _load_high_score(self):
        try:
            with open("high_score.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "score": 0,
                "total": 0,
                "rate": 0.0,
                "grade": "-",
                "date": "-"
            }

    # ─────────────────────────────────────────
    # 최고점수 파일 저장
    # ─────────────────────────────────────────
    def _save_high_score(self):
        with open("high_score.json", "w", encoding="utf-8") as f:
            json.dump(self.high_score, f, ensure_ascii=False, indent=4)

    # ─────────────────────────────────────────
    # 등급 계산
    # ─────────────────────────────────────────
    def _get_grade(self, rate):
        if rate == 100:
            return "S"
        elif rate >= 80:
            return "A"
        elif rate >= 60:
            return "B"
        else:
            return "C"

    # ─────────────────────────────────────────
    # 퀴즈 풀기
    # ─────────────────────────────────────────
    def play(self):
        if not self.quizzes:
            print("\n❌ 퀴즈가 없습니다. 먼저 퀴즈를 추가하거나 불러오세요.")
            return

        self.score = 0
        total = len(self.quizzes)

        print("\n" + "=" * 40)
        print("       🎮 퀴즈 게임 시작!")
        print("=" * 40)

        for i, quiz in enumerate(self.quizzes, 1):
            print(f"\n[{i}/{total}] {quiz['question']}")
            answer = input("정답 입력 → ").strip()

            if answer == quiz["answer"]:
                print("✅ 정답입니다!")
                self.score += 1
            else:
                print(f"❌ 오답! 정답은 '{quiz['answer']}' 입니다.")

        # ── 결과 계산 ──
        rate = (self.score / total) * 100
        grade = self._get_grade(rate)

        print("\n" + "=" * 40)
        print("           📊 최종 결과")
        print("=" * 40)
        print(f"  총 문제 수 : {total}문제")
        print(f"  맞힌 문제  : {self.score}문제")
        print(f"  정답률     : {rate:.1f}%")
        print(f"  등급       : {grade}등급")
        print("=" * 40)

        # ── 최고점수 갱신 ──
        if rate > self.high_score["rate"]:
            self.high_score = {
                "score": self.score,
                "total": total,
                "rate": rate,
                "grade": grade,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self._save_high_score()  # 파일에 저장
            print("\n🏆 새로운 최고점수 달성!")
            print(f"   정답률 {rate:.1f}% ({grade}등급)")
        else:
            print(f"\n🏆 현재 최고점수 : {self.high_score['rate']:.1f}%")
            print(f"   ({self.high_score['date']} 기록)")

    # ─────────────────────────────────────────
    # 퀴즈 추가
    # ─────────────────────────────────────────
    def add_quiz(self):
        print("\n" + "=" * 40)
        print("        ➕ 퀴즈 추가")
        print("=" * 40)

        question = input("문제를 입력하세요 → ").strip()
        answer = input("정답을 입력하세요 → ").strip()

        if not question or not answer:
            print("❌ 문제와 정답을 모두 입력해야 합니다.")
            return

        self.quizzes.append({
            "question": question,
            "answer": answer
        })
        print(f"✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)")

    # ─────────────────────────────────────────
    # 퀴즈 목록 보기
    # ─────────────────────────────────────────
    def show_quiz_list(self):
        print("\n" + "=" * 40)
        print("        📋 퀴즈 목록")
        print("=" * 40)

        if not self.quizzes:
            print("  등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes, 1):
            print(f"  {i}. Q: {quiz['question']}")
            print(f"     A: {quiz['answer']}")
        print(f"\n  총 {len(self.quizzes)}개의 퀴즈")

    # ─────────────────────────────────────────
    # 점수 확인
    # ─────────────────────────────────────────
    def show_score(self):
        print("\n" + "=" * 40)
        print("        🏆 점수 확인")
        print("=" * 40)

        # 현재 점수
        if self.score == 0 and len(self.quizzes) == 0:
            print("  아직 플레이 기록이 없습니다.")
        else:
            total = len(self.quizzes)
            if total > 0 and self.score > 0:
                rate = (self.score / total) * 100
                grade = self._get_grade(rate)
                print("  [ 이번 플레이 ]")
                print(f"  맞힌 문제  : {self.score} / {total}")
                print(f"  정답률     : {rate:.1f}%")
                print(f"  등급       : {grade}등급")
            else:
                print("  아직 플레이 기록이 없습니다.")

        # 최고점수
        print("\n  [ 🥇 최고 기록 ]")
        if self.high_score["date"] == "-":
            print("  아직 최고 기록이 없습니다.")
        else:
            print(f"  정답률  : {self.high_score['rate']:.1f}%")
            print(f"  맞힌 수 : {self.high_score['score']} / {self.high_score['total']}")
            print(f"  등급    : {self.high_score['grade']}등급")
            print(f"  날짜    : {self.high_score['date']}")
        print("=" * 40)

    # ─────────────────────────────────────────
    # 퀴즈 저장
    # ─────────────────────────────────────────
    def save_quiz(self):
        with open("quizzes.json", "w", encoding="utf-8") as f:
            json.dump(self.quizzes, f, ensure_ascii=False, indent=4)
        print(f"\n✅ {len(self.quizzes)}개의 퀴즈가 저장되었습니다. (quizzes.json)")

    # ─────────────────────────────────────────
    # 퀴즈 불러오기
    # ─────────────────────────────────────────
    def load_quiz(self):
        try:
            with open("quizzes.json", "r", encoding="utf-8") as f:
                self.quizzes = json.load(f)
            print(f"\n✅ {len(self.quizzes)}개의 퀴즈를 불러왔습니다.")
        except FileNotFoundError:
            print("\n❌ 저장된 퀴즈 파일이 없습니다. (quizzes.json)")