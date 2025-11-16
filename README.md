# alien-invasion-game
一个使用Python和Pygame开发的2D射击游戏
# 外星人入侵 (Alien Invasion)

一个使用Python和Pygame开发的经典2D射击游戏。

## 项目描述

玩家控制一艘位于屏幕底部的飞船，通过左右移动和发射子弹来击落从屏幕上方不断出现的外星人舰队。游戏包含多关卡、分数统计、生命值系统和最高分记录功能。

## 技术栈

*   **语言**: Python
*   **图形库**: Pygame
*   **架构**: 面向对象编程 (OOP)，模块化设计

## 游戏特性

*   🚀 飞船移动与射击
*   👾 外星人群组运动与边缘检测
*   💥 精确的碰撞检测系统
*   🎯 随关卡提升的动态难度
*   📊 实时记分牌与最高分持久化存储
*   🎵 背景音乐与游戏音效

## 如何运行

1.  确保已安装Python (建议3.6+版本)。
2.  安装必需的Pygame库：
    ```bash
    pip install pygame
    ```
3.  克隆本项目到本地：
    ```bash
    git clone https://github.com/【你的GitHub用户名】/alien-invasion-game.git
    ```
4.  进入项目目录，运行主程序：
    ```bash
    cd alien-invasion-game
    python alien_invasion.py
    ```

## 项目结构

- `alien_invasion.py` - 游戏主程序
- `settings.py` - 游戏设置
- `ship.py` - 飞船类
- `bullet.py` - 子弹类
- `alien.py` - 外星人类
- `game_stats.py` - 游戏统计
- `scoreboard.py` - 记分牌
- `button.py` - 按钮类
- `images/` - 图片资源
- `sounds/` - 音效资源

---
> 此项目是我的个人作品，用于展示Python编程与游戏开发能力。
