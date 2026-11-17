# ====================
# QuizGame 클래스 (게임 전체 관리)
# ====================
# 미션 반영 수정사항
#  1) 데이터 저장을 state.json 1개 파일로 통합 (quizzes + best_score, UTF-8)
#  2) 프로그램 시작 시 state.json 자동 로드, 파일 없으면 기본 데이터 사용
#  3) 파일 손상 시 안내 후 백업 보존 + 기본 데이터로 복구, PermissionError 등 처리
#  4) play() 정답 입력: 숫자 1~4 범위 검증, 빈 입력/비숫자 재입력 처리
#  5) add_quiz: 선택지 4개 + 정답 번호 입력받고, 추가 즉시 자동 저장
#  6) 모든 저장 시 .bak 백업 파일 생성 후 기록 (복구용)

import json
import os
import shutil
from datetime import datetime

from quiz import Quiz, DEFAULT_QUIZZES

STATE_FILE = "state.json"


class QuizGame:
    def __init__(self):
        self.quizzes = []           # Quiz 객체 목록
        self.best_score = 0         # 최고 정답 수
        self.best_total = 0         # 최고 기록 당 총 문제 수
        self.score = 0              # 이번 판 맞힌 수
        self._load_state()          # 시작 시 자동 로드

    # ─────────────────────────────────────────
    # 내부 유틸: Quiz 목록 ↔ dict 목록 변환
    # ─────────────────────────────────────────
    def _quizzes_to_dicts(self):
        return [q.to_dict() for q in self.quizzes]

    def _dicts_to_quizzes(self, raw_list):
        quizzes = []
        for item in raw_list:
            if isinstance(item, dict) and item.get("question"):
                quizzes.append(Quiz.from_dict(item))
        return quizzes

    # ─────────────────────────────────────────
    # state.json 불러오기 (손상/권한 오류 대응 포함)
    # ─────────────────────────────────────────
    def _load_state(self):
        # 1) state.json 이 없고 구버전 quizzes.json 만 있으면 자동 이전(마이그레이션)
        if not os.path.exists(STATE_FILE) and os.path.exists("quizzes.json"):
            try:
                with open("quizzes.json", "r", encoding="utf-8") as f:
                    old_quizzes = json.load(f)
                self.quizzes = self._dicts_to_quizzes(old_quizzes)
                self._save_state()
                print(f"\n📂 구버전 quizzes.json 의 퀴즈 {len(self.quizzes)}개를 "
                      f"state.json 으로 자동 이전했습니다.")
                return
            except (json.JSONDecodeError, OSError):
                pass  # 이전 실패 시 기본 데이터 경로로 진행

        # 2) 파일이 없으면 기본 퀴즈 데이터 사용 (미션 요구)
        if not os.path.exists(STATE_FILE):
            self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
            print("\n📂 저장 파일이 없어 기본 퀴즈 데이터로 시작합니다. (퀴즈 5개)")
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = self._dicts_to_quizzes(data.get("quizzes", []))
            best = data.get("best_score", {})
            if isinstance(best, dict):
                self.best_score = best.get("score", 0)
                self.best_total = best.get("total", 0)
            else:  # 단순 숫자로 저장된 구버전 호환
                self.best_score = best
            print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")

        # 3) 파일이 손상된 경우: 백업 보존 후 기본 데이터로 복구
        except json.JSONDecodeError:
            backup = STATE_FILE + ".broken"
            try:
                shutil.copy(STATE_FILE, backup)
                print(f"\n⚠️ {STATE_FILE} 파일이 손상되어 기본 데이터로 복구합니다.")
                print(f"   (손상된 파일은 {backup} 로 보존했습니다)")
            except OSError:
                print(f"\n⚠️ {STATE_FILE} 파일이 손상되어 기본 데이터로 복구합니다.")
            self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
            self.best_score = 0
            self.best_total = 0
            self._save_state()  # 정상 파일로 즉시 재기록

        # 4) 읽기 권한 등 OS 오류
        except (PermissionError, OSError) as e:
            print(f"\n⚠️ {STATE_FILE} 읽기 오류({e.errno}): 기본 데이터로 시작합니다.")
            self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]

    # ─────────────────────────────────────────
    # state.json 저장 (백업 생성 후 기록)
    # ─────────────────────────────────────────
    def _save_state(self):
        data = {
            "quizzes": self._quizzes_to_dicts(),
            "best_score": {
                "score": self.best_score,
                "total": self.best_total,
            },
        }
        # 쓰기 전 기존 파일 백업 (손상 복구용)
        if os.path.exists(STATE_FILE):
            try:
                shutil.copy(STATE_FILE, STATE_FILE + ".bak")
            except OSError:
                pass  # 백업 실패는 저장 자체를 막지 않음
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except (PermissionError, OSError) as e:
            print(f"\n❌ 저장 실패({e.errno if hasattr(e, 'errno') else e}): "
                  f"파일 권한이나 디스크 상태를 확인하세요.")
            return False

    # ─────────────────────────────────────────
    # 공통: 정수 입력 검증 (범위 검사 포함)
    # ─────────────────────────────────────────
    def _input_number(self, prompt, min_value, max_value):
        """빈 입력/비숫자/범위 밖 입력을 모두 검사해 유효한 정수만 반환한다."""
        while True:
            raw = input(prompt).strip()          # 앞뒤 공백 제거
            if raw == "":                        # 빈 입력(그냥 Enter)
                print("⚠️ 빈 입력입니다. 숫자를 입력하세요.")
                continue
            try:
                number = int(raw)
            except ValueError:                   # 숫자 변환 실패 (예: abc)
                print(f"⚠️ 숫자만 입력하세요. ({min_value}-{max_value})")
                continue
            if number < min_value or number > max_value:  # 범위 밖
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue
            return number

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
        print(f"       🎮 퀴즈 게임 시작! (총 {total}문제)")
        print("=" * 40)

        for i, quiz in enumerate(self.quizzes, 1):
            quiz.display(index=i, total=total)
            choice = self._input_number("정답 입력 (1-4) → ", 1, len(quiz.choices))

            if quiz.is_correct(choice):
                print("✅ 정답입니다!")
                self.score += 1
            else:
                print(f"❌ 오답! 정답은 '{quiz.answer_text()}' 입니다.")

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

        # ── 최고점수 갱신 + 자동 저장 ──
        if self.score > self.best_score:
            self.best_score = self.score
            self.best_total = total
            print("\n🏆 새로운 최고점수 달성!")
            print(f"   {self.score}/{total} ({grade}등급)")
        self._save_state()  # 플레이 결과는 항상 자동 저장

    # ─────────────────────────────────────────
    # 퀴즈 추가 (선택지 4개 + 정답 번호 + 자동 저장)
    # ─────────────────────────────────────────
    def add_quiz(self):
        print("\n" + "=" * 40)
        print("        ➕ 퀴즈 추가")
        print("=" * 40)

        question = input("문제를 입력하세요 → ").strip()
        if not question:
            print("❌ 문제를 입력해야 합니다. 추가가 취소되었습니다.")
            return

        choices = []
        for n in range(1, 5):
            choice = input(f"선택지 {n} → ").strip()
            if not choice:
                print("❌ 선택지를 모두 입력해야 합니다. 추가가 취소되었습니다.")
                return
            choices.append(choice)

        answer = self._input_number("정답 번호 (1-4) → ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        print(f"✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)")

        # 추가 즉시 자동 저장 (프로그램이 강제 종료돼도 데이터 유지)
        if self._save_state():
            print("💾 state.json 에 자동 저장되었습니다.")

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
            print(f"  {i}. Q: {quiz.question}")
            for n, choice in enumerate(quiz.choices, 1):
                mark = "⭕" if n == quiz.answer else "  "
                print(f"     {n}. {choice} {mark}")
        print(f"\n  총 {len(self.quizzes)}개의 퀴즈")

    # ─────────────────────────────────────────
    # 점수 확인
    # ─────────────────────────────────────────
    def show_score(self):
        print("\n" + "=" * 40)
        print("        🏆 점수 확인")
        print("=" * 40)

        if self.best_score == 0:
            print("  아직 최고 기록이 없습니다. 퀴즈를 풀어보세요!")
        else:
            rate = (self.best_score / self.best_total) * 100 if self.best_total else 0
            print("  [ 🥇 최고 기록 ]")
            print(f"  맞힌 수 : {self.best_score} / {self.best_total}")
            print(f"  정답률  : {rate:.1f}%")
            print(f"  등급    : {self._get_grade(rate)}등급")
        print("=" * 40)

    # ─────────────────────────────────────────
    # 수동 저장 / 불러오기 (메뉴용)
    # ─────────────────────────────────────────
    def save_quiz(self):
        if self._save_state():
            print(f"\n✅ 퀴즈 {len(self.quizzes)}개와 최고점수가 저장되었습니다. (state.json)")

    def load_quiz(self):
        self._load_state()
