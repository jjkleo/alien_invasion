import sys
import time

import pygame
from bullet import Bullet
from alien import Alien


def fire_bullet(ai_settings,screen,ship,bullets):
	#创建一颗子弹，加入到bullets中
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	"""响应按键"""
	if event.key==pygame.K_RIGHT:
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key==pygame.K_q:
		sys.exit()
	
def check_keyup_events(event,ship):
	"""响应松开"""
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False

def check_events(ai_settings,screen,ship,bullets):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type ==pygame.QUIT:
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)


def update_bullets(ai_settings,screen,ship,aliens,bullets):
	#更新子弹位置
	bullets.update()
	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)
		
def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
	"""响应子弹和外星人的碰撞"""
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
	#没外星人时再创建一批
	if len(aliens)==0:
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)

def get_number_aliens_x(ai_settings,alien_width):
	"""计算每行可容纳多少外星人"""
	available_space_x=ai_settings.screen_width - 2*alien_width
	number_aliens_x=int(available_space_x / (2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
	"""计算屏幕能容纳多少外星人"""
	available_space_y=ai_settings.screen_height-(3*alien_height)-ship_height
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
	"""创建外星人群"""
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	#创建一行外星人
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
	"""外星人到达边缘采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings,aliens):
	"""将整群外星人下移并改变方向"""
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *=-1
	
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	#响应外星人和飞船之间的碰撞
	if stats.ships_left>0:
		stats.ships_left-=1
		aliens.empty()
		bullets.empty()
		#创建一批新的外星人
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		#暂停
		time.sleep(0.5)
	else :
		stats.game_active=False
	
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
	"""检查是否有外星人到达屏幕底部"""
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >=screen_rect.bottom:
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
			break

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
	check_fleet_edges(ai_settings,aliens)
	aliens.update()	
	#检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
	#检查是否有外星人到达屏幕底部
	check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
		
def update_screen(ai_settings,screen,ship,aliens,bullets):
	"""更新屏幕上的图像，并切换到新屏幕"""
	
	#每次循环时重绘屏幕	
	screen.fill(ai_settings.bg_color)
	#绘制子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	#绘制飞船
	ship.blitme()
	#绘制外星人群
	aliens.draw(screen)
	
	# 让最近绘制的屏幕可见
	pygame.display.flip()
