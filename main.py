import pygame
import random
from pygame import mixer

pygame.init()
#screen width * height
screen = pygame.display.set_mode ((800,600))
spacebg = pygame.image.load('space background.png')
shopbg = pygame.image.load('shop.png')
menubg = pygame.image.load('menu.png')
clusterpng = pygame.image.load('shell.png')
missilepng = pygame.image.load('rocket.png')
bulletpng = pygame.image.load('bullet.png')
explode = pygame.image.load('explosion.png')

#title
pygame.display.set_caption('Space Invaders')
#icon
icon = pygame.image.load ('UFO.png')
pygame.display.set_icon(icon)

#player
playerimg = pygame.image.load('spaceship.png') 



enemyX = []
enemyY =  []
enemyXchange = []
enemyYchange = []
enemyvel = []
enemyimg = []
enemynum = 6 
enemyadd = 0

menu = True
game = False
shop = False

multishot = False
cluster = False
missile = False
shopmultishot = 'locked'
shopcluster = 'locked'
shopmissile = 'locked'

#bullet
bullet = bulletpng


for i in range(enemynum):
	enemyimg.append(pygame.image.load('enemy.png')) 
	enemyX.append(random.randint(0,700))
	enemyY.append(random.randint(10,150))
	enemyXchange.append(3)
	enemyYchange.append(40)
	enemyvel.append(random.randint(1,4))

playerX = 370
playerY = 480
xchange = 0
ychange = 0


bullets = 1 
bullready = 0
bulletY = []
bulletX = []
bulletYchange = []
bulletstate = []
clusterexplosion = []
count = []
explosionX = []
explosionY = []

missilestate = []
targetX = []
targetY = []
for i in range(bullets):
	bulletY.append(480)
	bulletX.append(0)
	bulletYchange.append(.3)
	bulletstate.append('ready') 
	clusterexplosion.append(False)
	count.append(0)
	explosionX.append(0)
	explosionY.append(0)
	missilestate.append('ready')
	targetX.append(0)
	targetY.append(0)


score = 0
font = pygame.font.Font('freesansbold.ttf',64)
scoreX = 10
scoreY = 536 

gc = True
game_over_font = pygame.font.Font('freesansbold.ttf',108)

shopfont = pygame.font.Font('freesansbold.ttf',32)
itemfont = pygame.font.Font('freesansbold.ttf',16)
shoplock = shopfont.render('LOCKED',True,(255,255,255))


money = 1000
def update_bullets():
	global bullet
	if cluster:
		bullet = clusterpng
	elif missile:
		bullet = missilepng
	else:
		bullet = bulletpng
	global bullets
	global bullready
	if multishot:
		bullets = 3
		bullready = 0
	elif missile:
		bullets = 2
		bullready = 0
	else:
		bullets = 1
		bullready = 0
	global bulletY
	global bulletX
	global bulletYchange
	global bulletstate
	global missilestate
	global targetX
	global targetY

	bulletY = []
	bulletX = [] 
	bulletYchange = []
	bulletstate = []

	clusterexplosion = []
	count = []
	explosionX = []
	explosionY = []

	missilestate = []
	targetX = []
	targetY = []
	for i in range(bullets):
		bulletY.append(480)
		bulletX.append(0)
		if cluster:
			bulletYchange.append(.23)
		elif missile:
			bulletYchange.append(.45)
		else:
			bulletYchange.append(.3)
		bulletstate.append('ready') 
		clusterexplosion.append(False)
		count.append(0)
		explosionX.append(0)
		explosionY.append(0)
		missilestate.append('ready')
		targetX.append(0)
		targetY.append(0)
def add_enemy():
	global enemynum
	global enemyimg
	global enemyX
	global enemyY
	global enemyXchange
	global enemyYchange
	global enemyvel
	global score
	global enemyadd
	enemyadd += 1
	oldscore = score
	for i in range(5):
		score += 1
		if score == oldscore + 2:
			enemynum += 1
			enemyimg.append(pygame.image.load('enemy.png')) 
			enemyX.append(random.randint(0,700))
			enemyY.append(random.randint(10,150))
			enemyXchange.append(3)
			enemyYchange.append(40)
			enemyvel.append(random.randint(2,4))
def remove_enemy():
	global enemynum
	global enemyimg
	global enemyX
	global enemyY
	global enemyXchange
	global enemyYchange
	global enemyvel
	global score
	global enemyadd

	for i in range(enemyadd):
		enemynum -= 1
		enemyadd -= 1
		enemyimg.pop() 
		enemyX.pop()
		enemyY.pop()
		enemyXchange.pop()
		enemyYchange.pop()
		enemyvel.pop()			
def reset():

	for i in range(enemynum):
		enemyimg[i] = pygame.image.load('enemy.png')
		enemyX[i] = random.randint(0,700)
		enemyY[i] = random.randint(10,150)
		enemyXchange[i] = 3
		enemyYchange[i] = 40
		enemyvel[i] = random.randint(1,4) 
reset()
def game_over():
	gsound = mixer.Sound('game over.wav')
	global gc
	remove_enemy()
	if gc:
		gsound.play()
	gc = False
	over = game_over_font.render('GAME OVER',True,(255,255,255))
	screen.blit(over,(75,250))
	show_score(400,400)
	pygame.display.update()
def show_score(x,y):
	scr = font.render(str(score),True,(200,200,255))
	screen.blit(scr,(x,y))

def player(x,y):
	screen.blit(playerimg,(x,y))

def Enemy(x,y,i):
	screen.blit(enemyimg[i], (x,y))
def explosion(x,y):
	screen.blit(explode,(x,y))
def fire_bullet(x,y,_):
	screen.blit(bullet,(x,y))
def isCollision(ex,ey,bx,by,am):
	distance = ((((ex - bx)**2)+(ey-by)**2)**0.5)
	if distance < am:
		return True
	else:
		return False
def button(cords,x1,y1,x2,y2):
	if  cords[0]>= x1 and cords[0] <=x2 and cords[1]>y1 and cords[1]<=y2:
		return True
	else:
		return False
def shop_buttons(pos):
	global multishot
	global cluster
	global missile
	global shopmissile
	global shopmultishot
	global shopcluster
	global money

	if button(pos,50,490,170,550): # for the cluster bomb
		if shopcluster is 'locked' and money >= 150:
			shopcluster = 'unlocked'
			money -= 150
		if cluster:
			cluster = False
		elif shopcluster is 'unlocked':
			cluster = True
			missile = False
			multishot = False

	if button(pos,295,490,450,550): # for the seeking missile
		if shopmissile is 'locked' and money >= 100:
			shopmissile = 'unlocked'
			money -= 100
		if missile:
			missile = False
		elif shopmissile is 'unlocked':
			missile = True	
			cluster = False
			multishot = False

	if button(pos,530,490,700,550): #for multishot
		if shopmultishot is 'locked' and money >= 50: 
			shopmultishot = 'unlocked'
			money -= 50

		if multishot:
			multishot = False
		elif shopmultishot is 'unlocked':
			multishot = True
			cluster = False
			missile = False



running = True
while running:

	while shop:

		screen.fill((0,0,0))
		screen.blit(shopbg,(0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				shop = False
			if event.type == pygame.MOUSEBUTTONDOWN: 
				pos = pygame.mouse.get_pos()
				if button(pos,570,85,735,158):
					menu = True
					shop = False
				shop_buttons(pos)
		if cluster:
			screen.blit(clusterpng,(75,450))
		if missile:
			screen.blit(missilepng,(350,450))
		if multishot:
			screen.blit(bulletpng,(610,450))
		if shopmultishot is 'locked':
			multishotprice = itemfont.render('(50)',True,(255,255,255))
			screen.blit(shoplock,(580,550))
			screen.blit(multishotprice,(630,580))
		if shopmissile is 'locked':
			missileprice = itemfont.render('(100)',True,(255,255,255))
			screen.blit(shoplock,(310,550))
			screen.blit(missileprice,(360,580))
		if shopcluster is 'locked':
			clusterprice = itemfont.render('(150)',True,(255,255,255))
			screen.blit(shoplock,(50,550))
			screen.blit(clusterprice,(100,580))
		update_bullets( )
		amount = font.render('$' + str(money),True,(255,255,255))
		screen.blit(amount,(10,10))
		pygame.display.update()

	while game:
		gc = True
		screen.blit(spacebg,(0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				game = False

			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					xchange = -3
				if event.key == pygame.K_RIGHT: 
					xchange = 3
				if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
					if bullready < bullets and bulletstate[bullready] is 'ready': 
						bullready += 1
						bsound = mixer.Sound('pew.wav')
						bsound.play()
						
						if bulletstate[bullready - 1] is 'ready':
							bulletX[bullready - 1] = playerX
							fire_bullet(bulletX[bullready - 1],bulletY[bullready - 1],bullready)
							bulletstate[bullready - 1] = 'fire'


			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					xchange = 0
				
		if playerX < 1:
			playerX = 1
		if playerX >=736:
			playerX = 736

		for i in range(enemynum):
			#game over
			if enemyY[i] >= 450:
				for j in range(enemynum):
					enemyY[j] = 2000
				
				game_over()
				pygame.time.delay(4000)
				menu = True
				game = False
				money += score
				score = 0
				reset()
				break

			if  enemyX[i] <=0:
				enemyXchange[i] = enemyvel[i]
				enemyY[i] += enemyYchange[i]
			if enemyX[i] >= 736:
				enemyXchange[i] = -enemyvel[i]
				enemyY[i] += enemyYchange[i]

			#collision
			for k in range(bullets):
				
				if not cluster:
					if not missile:
						collision = isCollision(enemyX[i],enemyY[i],bulletX[k],bulletY[k],27)
					if missile:
						collision = isCollision(enemyX[i],enemyY[i],bulletX[k],bulletY[k],35)
					if collision:
						boom = mixer.Sound('boom.wav')
						boom.play()
						bulletY[k] = 480
						bulletstate[k] = 'ready'
						if missile:
							missilestate[k] = 'ready'
						bullready -= 1
						score += 1
						enemyX[i] = random.randint(0,700)
						enemyY[i] = random.randint(10,150)
				if cluster:
					collision = isCollision(enemyX[i],enemyY[i],bulletX[k],bulletY[k],50)
					if collision and bulletY[k] < 460:
						explosionX[k] = bulletX[k]
						explosionY[k] = bulletY[k]
						boom = mixer.Sound('boom.wav')
						boom.play()
						bulletY[k] = 480
						bulletstate[k] = 'ready'
						bullready -= 1
						score += 1
						enemyX[i] = random.randint(0,700)
						enemyY[i] = random.randint(10,150)
						clusterexplosion[k] = True


					if clusterexplosion[k] is True:
						count[k] += 1
						if count[k] > 1000:
							count[k] = 0
							clusterexplosion[k] = False
						explosion(explosionX[k],explosionY[k])
						if isCollision(enemyX[i],enemyY[i],explosionX[k],explosionY[k],50) and count[k] < 900:
							boom = mixer.Sound('boom.wav')
							boom.play()
							enemyX[i] = random.randint(0,700)
							enemyY[i] = random.randint(10,150)	
							score += 1	

				if bulletstate[k] is 'fire':
					if missile:
						if isCollision(enemyX[i],enemyY[i],bulletX[k],bulletY[k], 200) and missilestate[k] is 'ready':
							intersection = (((((enemyY[k]-bulletY[k])**2)**0.5)/bulletYchange[k])*enemyXchange[i]) + (((enemyX[k]-bulletX[k])**2)**0.5)
							if targetX[k] > enemyX[i]:
								intersection = -intersection
							targetX[k] = enemyX[i] + intersection
							targetY[k] = enemyY[i]
							missilestate[k] = 'locked'
						if missilestate[k] is 'locked':
							if targetX[k] > bulletX[k]:
								bulletX[k] += bulletYchange[k]
							if targetX[k] < bulletX[k]:
								bulletX[k] -= bulletYchange[k]
						bulletY[k] -=  bulletYchange[k] 
						bulletstate[k] = 'fire' 
						fire_bullet(bulletX[k],bulletY[k],k)
						if targetY < bulletY :
							missilestate[k] = 'ready'
					else:
						fire_bullet(bulletX[k],bulletY[k],k)
						bulletstate[k] = 'fire'
						bulletY[k] -=  bulletYchange[k] 
				if bulletY[k]<= 0:
					bulletY[k] = 490
					bulletstate[k] = 'ready'
					bullready -= 1
					missilestate[k] = 'ready'

					
			enemyX[i] += enemyXchange[i]	
			Enemy(enemyX[i],enemyY[i],i)

		if score%30 == 0 and score > 0 :
			add_enemy()
		playerX += xchange	 
		player(playerX,playerY)
		show_score(scoreX,scoreY)
		pygame.display.update()

	while menu:
		screen.fill((0,0,0))
		screen.blit(menubg,(0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				menu = False
			if event.type == pygame.MOUSEBUTTONDOWN: 
				pos = pygame.mouse.get_pos()
				if button(pos,270,285,475,375):
					game = True
					menu = False
					break
				if button(pos,260,410,500,475):
					shop = True
					menu = False
					break
		pygame.display.update()

	
	 
