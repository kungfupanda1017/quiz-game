# =====================
# 퀴즈 데이터
# =====================
quiz_data = [
    {
        "question": "조선을 건국한 사람은 누구인가요?",
        "options": ["이성계", "세종대왕", "정도전", "이순신"],
        "answer": "이성계"
    },
    {
        "question": "한글을 만든 조선의 왕은 누구인가요?",
        "options": ["태조", "세종대왕", "연산군", "정조"],
        "answer": "세종대왕"
    },
    {
        "question": "이집트 문명의 대표적인 건축물은 무엇인가요?",
        "options": ["콜로세움", "만리장성", "피라미드", "파르테논"],
        "answer": "피라미드"
    },
    {
        "question": "제2차 세계대전을 일으킨 독일의 지도자는 누구인가요?",
        "options": ["히틀러", "무솔리니", "스탈린", "처칠"],
        "answer": "히틀러"
    },
    {
        "question": "삼국시대에 속하지 않는 나라는?",
        "options": ["고구려", "백제", "신라", "가야"],
        "answer": "가야"
    }
]

# =====================
# Quiz 클래스 (문제 하나)
# =====================
class Quiz:
    def __init__(self, question, options, answer):
        self.question = question   # 문제
        self.options = options     # 보기 4개 (리스트)
        self.answer = answer       # 정답

# =====================
# QuizGame 클래스 (게임 전체)
# =====================
class QuizGame:
    def __init__(self):
        self.quizzes = []   # Quiz 객체들을 담는 리스트
        self.score = 0      # 점수

    def load_data(self):
        """quiz_data를 Quiz 객체로 변환해서 저장"""
        for item in quiz_data:
            quiz = Quiz(item["question"], item["options"], item["answer"])
            self.quizzes.append(quiz)

# =====================
# 실행 테스트
# =====================
if __name__ == "__main__":
    game = QuizGame()
    game.load_data()
    print(f"퀴즈 {len(game.quizzes)}개 로드 완료!")
    print(f"첫 번째 문제: {game.quizzes[0].question}")
    