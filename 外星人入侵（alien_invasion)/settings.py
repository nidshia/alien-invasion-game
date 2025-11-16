class Settings:
    """存储游戏设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        self.ship_speed = 4
        self.ship_limit = 3
        self.alien_speed = 1
        self.fleet_drop_speed = 10
        #以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        #  fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        # 子弹设置
        self.bullet_speed = 5
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (50, 50, 50)
        self.bullets_allowed = 5

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1
        # fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """提高游戏速度"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)