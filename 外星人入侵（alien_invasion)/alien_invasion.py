import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源及行为"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen=pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # 播放背景音乐
        pygame.mixer.init()
        # 音效变量
        self.bullet_sound=None
        self.explosion_sound=None
        self.ship_explosion_sound=None
        self.load_sounds()
        # 创建飞船并初始化游戏统计信息
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.bg_color = (230, 230, 230)
        self.game_active = False
        self.play_button = Button(self, "Play")
        # 在 __init__ 方法中加载背景音乐
        try:
            pygame.mixer.music.load("sounds/bassline背景音乐_耳聆网_[声音ID：10136].wav")
            pygame.mixer.music.play(-1)  # -1 表示循环播放
        except pygame.error as e:
            print(f"无法加载背景音乐: {e}")

    def load_sounds(self):
        """加载游戏音效"""
        try:
            # 加载音效文件（使用你实际的文件名）
            self.bullet_sound = pygame.mixer.Sound("sounds/激光音效_耳聆网_[声音ID：10231].wav")
            self.explosion_sound = pygame.mixer.Sound("sounds/爆炸_耳聆网_[声音ID：37764].wav")
            self.ship_explosion_sound = pygame.mixer.Sound("sounds/爆炸_耳聆网_[声音ID：37764].wav")  # 使用相同爆炸音效
        except pygame.error as e:
            # 如果无法加载音效文件，则保持为None（无音效）
            print(f"无法加载音效文件: {e}")
            pass


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            # 侦听键盘和鼠标事件
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         sys.exit()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                # self.bullets.update()
                # for bullet in self.bullets.copy():
                #     if bullet.rect.bottom <= 0:
                #         self.bullets.remove(bullet)
                # print(len(self.bullets))
                self._update_aliens()
            self._update_screen()
            # self.screen.fill(self.settings.bg_color)
            # self.ship.blitme()
            # # 每次循环时都重绘屏幕
            # pygame.display.flip()
            self.clock.tick(60)

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人，并计算一行可容纳多少个外星人
        # 外星人间距为外星人宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height
            # new_alien = Alien(self)current_x
            # self
            # new_alien.x=current_x
            # new_alien.rect.x=.aliens.add(new_alien)
            # self._creat_alien(current_x)
            # current_x+=2*alien_width
        # self.aliens.add(alien)
        # 创建第一行外星人

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_events(self):
        """响应案件和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                # if event.key == pygame.K_RIGHT:
                #     self.ship.moving_right = True
                # elif event.key == pygame.K_LEFT:
                #     self.ship.moving_left = True
                if event.key == pygame.K_q:
                    self.stats.save_high_score()
                    sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                # if event.key == pygame.K_RIGHT:
                #     self.ship.moving_right = False
                # elif event.key == pygame.K_LEFT:
                #     self.ship.moving_left = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)



    def _start_game(self):
        """开始新游戏的核心逻辑"""
        # 重置游戏统计信息
        self.stats.reset_stats()
        self.game_active = True

        # 清空余下的外星人和子弹
        self.bullets.empty()
        self.aliens.empty()

        # 创建一群新的外星人并让飞船居中
        self._create_fleet()
        self.ship.center_ship()

        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)


    def _check_play_button(self,mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            self._start_game()
            self.stats.reset_stats()
            self.sb.prep_images()
            # self.sb.prep_score()
            # self.sb.prep_level()
            # self.sb.prep_ships()
            # self.game_active=True
            # self.aliens.empty()
            # self.bullets.empty()
            # self._create_fleet()
            # self.ship.center_ship()
            # pygame.mouse.set_visible(False)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_pos=pygame.mouse.get_pos()
            self._check_play_button(mouse_pos)
        elif event.key == pygame.K_p:
            if not self.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            if self.bullet_sound:
                self.bullet_sound.play()

    def _update_bullets(self):
        """更新子弹的位置，并删除已消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        # 检查是否有子弹击中了外星人
        self._check_bullet_alien_collisions()
        # collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        # if not self.aliens:
        #     # 删除现有的所有外星人，并创建一个新的外星舰队
        #     self.bullets.empty()
        #     self._create_fleet()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        if not self.aliens:
            self.start_new_level()
            # 删除现有的所有外星人，并创建一个新的外星舰队
            # self.bullets.empty()
            # self._create_fleet()
            # self.settings.increase_speed()
            # self.stats.level += 1
            # self.sb.prep_level()
        if collisions:
            # self.stats.score += self.settings.alien_points
            # self.sb.prep_score()
            #播放音效
            if self.explosion_sound:
                self.explosion_sound.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


    def start_new_level(self):
        """开始下一关"""
        # 删除现有的所有外星人，并创建一个新的外星舰队
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()
    def _update_aliens(self):
        """更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检查外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
        #播放音效
        if self.ship_explosion_sound:
            self.ship_explosion_sound.play()
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将ships_left减1
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            self.stats.save_high_score()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        # screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break
if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
