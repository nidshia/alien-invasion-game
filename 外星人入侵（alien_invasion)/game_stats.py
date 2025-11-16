import json

class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        # self.game_active = False
        self.high_score = self.load_high_score()
        self.level = 1
    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def load_high_score(self):
        """读取最高分"""
        try:
            with open('high_score.json', 'r') as f_obj:
                high_score = json.load(f_obj)
        except FileNotFoundError:
            high_score = 0
        return high_score

    def save_high_score(self):
        """将最高分保存到文件中"""
        filename = 'high_score.json'
        try:
            with open(filename, 'w') as f:
                json.dump(self.high_score, f)
        except:
            print("无法保存最高分到文件")