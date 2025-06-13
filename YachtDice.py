import random
import sys

class YachtDiceGame:
    def __init__(self):
        self.players = []
        self.num_players = 0
        self.current_player = 0
        self.round = 1
        self.max_rounds = 12
        self.dice = [0, 0, 0, 0, 0]
        self.held = [False, False, False, False, False]
        self.roll_count = 0
        self.max_rolls = 3
        self.score_categories = [
            "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Choice", "Four of a Kind", "Full House", "Small Straight", 
            "Large Straight", "Yacht"
        ]
        self.score_options = {}

    def setup_game(self):
        print("=== 요트 다이스 게임 ===")
        while True:
            try:
                self.num_players = int(input("플레이어 수를 입력하세요 (2-4): "))
                if 2 <= self.num_players <= 4:
                    break
                else:
                    print("2에서 4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("유효한 숫자를 입력하세요.")

        for i in range(self.num_players):
            name = input(f"플레이어 {i+1}의 이름을 입력하세요: ")
            self.players.append({
                "name": name,
                "scores": {category: None for category in self.score_categories},
                "total": 0
            })

    def roll_dice(self):
        print("\n주사위를 굴립니다...")
        for i in range(5):
            if not self.held[i]:
                self.dice[i] = random.randint(1, 6)
        self.roll_count += 1
        self.display_dice()

    def display_dice(self):
        print("\n현재 주사위 상태:")
        for i, value in enumerate(self.dice):
            hold_status = " (고정)" if self.held[i] else ""
            print(f"{i+1}번 주사위: {value}{hold_status}")
        print(f"({self.roll_count}/{self.max_rolls} 회 굴림)")

    def toggle_hold(self):
        while True:
            try:
                choice = input("\n고정할 주사위 번호를 입력하세요 (1-5, 0=종료): ")
                if choice == '0':
                    break
                dice_num = int(choice) - 1
                if 0 <= dice_num <= 4:
                    self.held[dice_num] = not self.held[dice_num]
                    self.display_dice()
                else:
                    print("1에서 5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("유효한 숫자를 입력하세요.")

    def calculate_score_options(self):
        self.score_options = {}
        counts = [self.dice.count(i) for i in range(1, 7)]  # 1-6 counts
        
        # 상단 부분 (1-6)
        for i in range(6):
            category = self.score_categories[i]
            if self.players[self.current_player]["scores"][category] is None:
                self.score_options[category] = counts[i] * (i+1)
        
        # 하단 부분
        # Choice (주사위 합계)
        if self.players[self.current_player]["scores"]["Choice"] is None:
            self.score_options["Choice"] = sum(self.dice)
        
        # Four of a Kind (4개 같은 숫자)
        if self.players[self.current_player]["scores"]["Four of a Kind"] is None:
            if any(count >= 4 for count in counts):
                self.score_options["Four of a Kind"] = sum(self.dice)
            else:
                self.score_options["Four of a Kind"] = 0
        
        # Full House (3+2)
        if self.players[self.current_player]["scores"]["Full House"] is None:
            has_three = any(count == 3 for count in counts)
            has_two = any(count == 2 for count in counts)
            if has_three and has_two:
                self.score_options["Full House"] = sum(self.dice)
            else:
                self.score_options["Full House"] = 0
        
        # Small Straight (4연속 숫자)
        if self.players[self.current_player]["scores"]["Small Straight"] is None:
            unique_sorted = sorted(list(set(self.dice)))
            consecutive = 1
            max_consecutive = 1
            for i in range(1, len(unique_sorted)):
                if unique_sorted[i] == unique_sorted[i-1] + 1:
                    consecutive += 1
                    max_consecutive = max(max_consecutive, consecutive)
                else:
                    consecutive = 1
            if max_consecutive >= 4:
                self.score_options["Small Straight"] = 15
            else:
                self.score_options["Small Straight"] = 0
        
        # Large Straight (5연속 숫자)
        if self.players[self.current_player]["scores"]["Large Straight"] is None:
            if sorted(self.dice) in [[1,2,3,4,5], [2,3,4,5,6]]:
                self.score_options["Large Straight"] = 30
            else:
                self.score_options["Large Straight"] = 0
        
        # Yacht (5개 같은 숫자)
        if self.players[self.current_player]["scores"]["Yacht"] is None:
            if any(count == 5 for count in counts):
                self.score_options["Yacht"] = 50
            else:
                self.score_options["Yacht"] = 0

    def display_score_options(self):
        print("\n점수 기록 가능한 항목:")
        for i, (category, score) in enumerate(self.score_options.items()):
            print(f"{i+1}. {category}: {score}점")
        print("0. 돌아가기")

    def record_score(self):
        while True:
            try:
                choice = int(input("기록할 항목 번호를 선택하세요: "))
                if choice == 0:
                    return False
                elif 1 <= choice <= len(self.score_options):
                    selected_category = list(self.score_options.keys())[choice-1]
                    score = self.score_options[selected_category]
                    
                    # 점수 기록
                    self.players[self.current_player]["scores"][selected_category] = score
                    self.players[self.current_player]["total"] += score
                    
                    print(f"{selected_category}에 {score}점을 기록했습니다!")
                    return True
                else:
                    print("유효한 번호를 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def display_scores(self):
        print("\n=== 현재 점수 현황 ===")
        for i, player in enumerate(self.players):
            print(f"\n{player['name']}의 점수:")
            for category, score in player["scores"].items():
                score_display = score if score is not None else "미기록"
                print(f"{category}: {score_display}")
            print(f"총점: {player['total']}")

    def player_turn(self):
        player = self.players[self.current_player]
        print(f"\n=== {self.round}라운드 - {player['name']}의 차례 ===")
        
        # 초기화
        self.dice = [0, 0, 0, 0, 0]
        self.held = [False, False, False, False, False]
        self.roll_count = 0
        
        # 첫 번째 굴림
        input("\n엔터를 눌러 주사위를 굴리세요...")
        self.roll_dice()
        
        # 추가 굴림 및 고정 선택
        while self.roll_count < self.max_rolls:
            action = input("\n무엇을 하시겠습니까? (1=굴리기, 2=주사위 고정/해제, 3=점수 기록): ")
            
            if action == '1':
                self.roll_dice()
            elif action == '2':
                self.toggle_hold()
            elif action == '3':
                break
            else:
                print("잘못된 입력입니다.")
        
        # 점수 계산 및 기록
        self.calculate_score_options()
        while True:
            self.display_score_options()
            if self.record_score():
                break
        
        self.display_scores()

    def next_turn(self):
        self.current_player = (self.current_player + 1) % self.num_players
        if self.current_player == 0:
            self.round += 1

    def play_game(self):
        self.setup_game()
        
        while self.round <= self.max_rounds:
            self.player_turn()
            self.next_turn()
        
        # 게임 종료 및 최종 결과
        print("\n=== 게임 종료! 최종 결과 ===")
        self.display_scores()
        
        # 승자 결정
        winner = max(self.players, key=lambda x: x["total"])
        print(f"\n축하합니다! {winner['name']}님이 {winner['total']}점으로 승리하셨습니다!")
        print("플레이 해주셔서 감사합니다.")

if __name__ == "__main__":
    game = YachtDiceGame()
    game.play_game()