# ====================
# Quiz 클래스 (문제 하나) + 기본 퀴즈 데이터
# ====================
# 미션 요구: 속성 question(문제) / choices(선택지 4개) / answer(정답 번호 1~4)
# 정답은 "번호"로 관리해 입력 검증(1~4 범위 검사)과 일관성을 유지한다.


class Quiz:
    """개별 퀴즈(문제 1개)를 표현하는 클래스"""

    def __init__(self, question, choices, answer):
        self.question = question          # 문제 (str)
        self.choices = choices            # 선택지 4개 (list)
        self.answer = answer              # 정답 번호 1~4 (int)

    # ── 저장용 dict 변환 (state.json 스키마와 일치) ──
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    # ── 저장된 dict → Quiz 객체 복원 ──
    # 구버전(quizzes.json: 정답이 문자열, choices 누락 가능) 데이터도 호환 처리
    @classmethod
    def from_dict(cls, data):
        question = data.get("question", "")
        choices = data.get("choices") or data.get("options") or []
        answer = data.get("answer")

        # 구버전: 정답이 문자열로 저장된 경우 → 선택지에서 번호를 찾아 변환
        if isinstance(answer, str) and choices:
            answer = choices.index(answer) + 1 if answer in choices else 1
        if not isinstance(answer, int):
            try:
                answer = int(answer)
            except (TypeError, ValueError):
                answer = 1
        return cls(question, choices, answer)

    # ── 문제 출력 ──
    def display(self, index=None, total=None):
        header = f"[{index}/{total}] " if index and total else ""
        print(f"\n{header}{self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    # ── 정답 확인 ──
    def is_correct(self, choice_number):
        return choice_number == self.answer

    # ── 정답 텍스트 (오답 안내용) ──
    def answer_text(self):
        if 1 <= self.answer <= len(self.choices):
            return self.choices[self.answer - 1]
        return "?"


# ====================
# 기본 퀴즈 데이터 (한국사 + 세계사, 총 5문제)
# ====================
# state.json 이 없는 첫 실행 시 이 데이터로 시작한다. (미션: "파일이 없으면 기본 퀴즈 데이터 사용")
DEFAULT_QUIZZES = [
    {
        "question": "조선을 건국한 사람은 누구인가요?",
        "choices": ["이성계", "세종대왕", "정도전", "이순신"],
        "answer": 1,
    },
    {
        "question": "한글을 만든 조선의 왕은 누구인가요?",
        "choices": ["태조", "세종대왕", "연산군", "정조"],
        "answer": 2,
    },
    {
        "question": "이집트 문명의 대표적인 건축물은 무엇인가요?",
        "choices": ["콜로세움", "만리장성", "피라미드", "파르테논"],
        "answer": 3,
    },
    {
        "question": "제2차 세계대전을 일으킨 독일의 지도자는 누구인가요?",
        "choices": ["히틀러", "무솔리니", "스탈린", "처칠"],
        "answer": 1,
    },
    {
        "question": "삼국시대에 속하지 않는 나라는?",
        "choices": ["고구려", "백제", "신라", "가야"],
        "answer": 4,
    },
]
