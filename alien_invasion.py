import sys

import pygame
import game_functions as gf

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats



def run_game():
	
	# 初始化游戏
	pygame.init()
	ai_settings=Settings()
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	#创建统计信息实例
	stats=GameStats(ai_settings)
	
	#创飞船、子弹和外星人的编组
	ship=Ship(ai_settings,screen)
	bullets=Group()
	aliens=Group()
	
	#创建外星人群
	gf.create_fleet(ai_settings,screen,ship,aliens)
	
	#设置背景色
	bg_color=(230,230,230)
	
	# 开始游戏主循环
	while True:
		gf.check_events(ai_settings,screen,ship,bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
			gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
			
		gf.update_screen(ai_settings,screen,ship,aliens,bullets)

run_game()
