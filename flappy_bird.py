import pygame
import random
import time

pygame.init()

#GAME CONSTANTS
display_width = 800
display_height = 600
gap_width = 50
gap_height = 120
gameDisplay = pygame.display.set_mode((display_width, display_height))
grey =(153, 155, 158)
white = (255, 255, 255)
green = (2, 112, 11)
dgreen =(7, 56, 1)
blue = (2, 4, 96)
yellow = (232, 132, 11)
black = (0, 0, 0)
bird_width = 40
bird_height = 40
birdX = 100
highscore = 0
clock=pygame.time.Clock()

#GAME DIFFICULTY SETTINGS
jump_vel = 15
g = 1
speedX = 5
timer =40

#LOADING THE IMAGES
bg_image = pygame.image.load("background.png")
bg_image = pygame.transform.scale(bg_image, (display_width, display_height))
bird = pygame.image.load("bird.png")
bird = pygame.transform.scale(bird, (bird_width, bird_height))

#GRID FOR ADJUSTING THE DIMENSION PARAMETERS
def draw_grid():
	for i in range(0, display_height, 100):
		pygame.draw.line(gameDisplay, grey, (0,i), (display_width,i))
	for i in range(0, display_width, 100):
		pygame.draw.line(gameDisplay, grey, (i,0), (i,display_height))

def display_score(score):
	global highscore
	if score>highscore:
		highscore = score
	font = pygame.font.SysFont(None, 35)
	text1 = font.render("Score: "+ str(score), True, blue)
	text2= font.render("High Score: "+ str(highscore), True, blue)
	gameDisplay.blit(text1, (0,0))
	gameDisplay.blit(text2, (display_width-200,0))

def draw_bird(birdY):
	gameDisplay.blit(bird,(birdX, birdY))

def game_over():
	font = pygame.font.SysFont(None, 110)
	text = font.render("Game over! ", True, blue)
	textRect = text.get_rect()
	textRect.center = (display_width*0.5, display_height*0.5)
	gameDisplay.blit(text, textRect)
	pygame.display.update()
	time.sleep(2)
	game_loop()

def game_loop():
	gameExit=False
	init_y = (display_height)//2
	birdY = (display_height)//2
	imageX = 0
	score = 0
	t = 0
	v = 0
	x = 300
	ypos =[]
	time.sleep(2)
	for i in range(3):
		ypos.append(random.randrange(100, display_height-200))
		
	while not gameExit:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_SPACE:
					v=-jump_vel
					init_y = birdY
					t= 0

		birdY = init_y + v*t + g*t*t
		gameDisplay.blit(bg_image,(imageX,0))
		gameDisplay.blit(bg_image,(imageX+display_width,0))
		draw_grid()
		xpos = x
		i = 0
		while xpos<display_width:
			pygame.draw.rect(gameDisplay, green, [xpos, 0, gap_width, ypos[i]])
			pygame.draw.rect(gameDisplay, dgreen, [xpos-4, ypos[i]-20, gap_width+8, 20])
			pygame.draw.rect(gameDisplay, green, [xpos, ypos[i]+gap_height, gap_width, display_height-ypos[i]-gap_height])
			pygame.draw.rect(gameDisplay, dgreen, [xpos-4, ypos[i]+gap_height, gap_width+8, 20])
			xpos+=300
			i+=1
		draw_bird(birdY)
		display_score(score)
		t+=1
		x-=speedX
		imageX-=speedX
		if imageX == -display_width:
			imageX+= display_width
		if x==-gap_width:
			x=x+300
			del ypos[0]
			ypos.append(random.randrange(100, display_height-200))

		pygame.display.update()
		clock.tick(timer)
		if birdY>display_height or birdY+bird_height<0:
			game_over()

		if (birdY<=ypos[0] or birdY+bird_height>=ypos[0]+gap_height) and (x<birdX+gap_width//2<x+gap_width):
			game_over()

		if (birdY+bird_height//2<=ypos[0] or birdY+bird_height//2>=ypos[0]+gap_height) and (x==birdX+bird_width-2):
			game_over()

		if (x+gap_width==birdX):
			score+=1
		

game_loop()
pygame.quit()
quit()