import pygame
import random
import time
from AI import AI
import json

pygame.init()

# GAME CONSTANTS
display_width = 800
display_height = 600
gap_width = 50
gap_height = 120
grey =(153, 155, 158)
white = (255, 255, 255)
red = (155, 16, 1)
dgreen =(7,70, 1)
green = (7, 85, 1)
black = (0, 0, 0)
yellow = (232, 132, 11)
bird_width = 40
bird_height = 40
birdX = 100
ai = AI()

#LOADING HIGHSCORE AND NUMBER OF ITERATIONS FROM JSON FILE
try:
	f = open('bot_scores.json', 'r')
	scores = json.load(f)
	highscore = scores['highscore']
	iterations = scores['iterations']
	f.close()
except IOError:
	pass

clock=pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))

# GAME DIFFICULTY SETTINGS
jump_vel = 12
g = 1
speedX = 5
fps = 100

# LOADING THE IMAGES
bg_image = pygame.image.load("background.png")
bg_image = pygame.transform.scale(bg_image, (display_width, display_height))
bird = pygame.image.load("bird.png")
bird = pygame.transform.scale(bird, (bird_width, bird_height))

# FUNCTION FOR DISPLAYING TEXT
def display_text(font_size, text_string, color, text_center):
	font = pygame.font.SysFont(None, font_size)
	text = font.render(text_string, True, color)
	textRect = text.get_rect()
	textRect.center = text_center
	gameDisplay.blit(text, textRect)

# GRID FOR ADJUSTING THE DIMENSION PARAMETERS
def draw_grid(freq):
	for i in range(0, display_height, freq):
		pygame.draw.line(gameDisplay, grey, (0,i), (display_width,i))
	for i in range(0, display_width, freq):
		pygame.draw.line(gameDisplay, grey, (i,0), (i,display_height))

# FUNCTION FOR DISPLAYING CURRENT SCORE AND HIGHSCORE
def display_score(score):
	global highscore
	if score>highscore:
		highscore = score
	display_text(35, "Score: "+str(score), black, (60,20))
	display_text(35, "AI Mode ", black, (60,45))
	display_text(35, "High Score: "+str(highscore), black, (display_width-120,20))
	display_text(35, "Iterations: "+str(iterations), black, (display_width-120,45))
	
# FUNCTION FOR DRAWING THE BACKGROUND
def draw_bg(imageX):
	gameDisplay.blit(bg_image,(imageX,0))
	gameDisplay.blit(bg_image,(imageX+display_width,0))

# FUNCTION FOR DRAWING THE BIRD
def draw_bird(birdY):
	gameDisplay.blit(bird,(birdX, birdY))

# FUNCTION FOR DRAWING THE PIPES
def draw_pipe(xpos, ypos):
	i = 0
	while xpos<display_width:
		pygame.draw.rect(gameDisplay, green, [xpos, 0, gap_width, ypos[i]])
		pygame.draw.rect(gameDisplay, dgreen, [xpos-4, ypos[i]-20, gap_width+8, 20])
		pygame.draw.rect(gameDisplay, green, [xpos, ypos[i]+gap_height, gap_width, display_height-ypos[i]-gap_height])
		pygame.draw.rect(gameDisplay, dgreen, [xpos-4, ypos[i]+gap_height, gap_width+8, 20])
		xpos+=300
		i+=1

# FUNCTION TO BE EXECUTED WHEN GAME IS OVER
def game_over(score):
	global iterations, highscore
	iterations += 1
	scores['iterations'] = iterations
	scores['highscore'] = highscore
	scores['scores'].append(score)
	f = open("bot_scores.json", "w")
	json.dump(scores, f)
	f.close()

	# GAME OVER
	display_text(110, "Game over!", black, (display_width*0.5, display_height*0.4))
	# FINAL SCORE
	display_text(50, "Score: "+str(score), black, (display_width*0.5, display_height*0.5))
	# PRESS ENTER FOR NEW GAME
	time.sleep(0.5)
	if iterations > 6000:
		pygame.quit()
		quit()
	game_loop()

# GAME LOOP
def game_loop():

	global ai
	init_y = (display_height * 0.4) # Initial height; updates to current height every time a jump is made
	birdY = (display_height * 0.4) # Current height of the bird
	imageX = 0
	score = 0
	t = 0
	u = 0 # Initial velocity; updates every time a jump is made
	birdV = 0 # Current velocity of the bird
	x = 300 # X coordinate of the leftmost pipe
	ypos =[]
	pipeX = 300
	# Y COORDINATE OF TOP LEFT CORNER OF THE NEXT 3 GAPS; WILL BE UPDATED WHEN ANY PIPE GOES OUT OF SIGHT
	for i in range(3):
		ypos.append(random.randrange(80, display_height-200))
	time.sleep(0.5)
	pipeY = ypos[0]
		
	while True:
		#EQUATION OF MOTION OF THE BIRD
		birdV = u + g*t
		birdY = init_y + u*t + g*t*t

		#BOT DECIDES WHETHER TO JUMP OR DO NOTHING 
		jump = ai.act(pipeX-birdX, pipeY-birdY, birdV)
		if jump:
			u =-jump_vel
			init_y = birdY
			t = 0

		#DRAW THE BACKGROUND, BIRD AND PIPES 
		draw_bg(imageX)
		#draw_grid(10)
		draw_pipe(x,ypos)
		draw_bird(birdY)
		display_score(score)
		pygame.display.update()
		clock.tick(fps)

		# UPDATING THE GAME VARIABLES
		t += 1
		x -= speedX
		imageX -= speedX
		if imageX == -display_width:
			imageX+= display_width 

		if x+gap_width<=birdX:
			pipeX = x+300
			pipeY = ypos[1]
		else:
			pipeX = x 
			pipeY = ypos[0]

		# WHETN LEFTMOST PIPE GOES OUT OF DISPLAY, DELETE ITS RANDOMLY GENERATED Y COORDINATE AND ADD A NEW Y COORDINATE FOR THE NEXT PIPE
		if x == -gap_width:
			x = x+300
			del ypos[0]
			ypos.append(random.randrange(100, display_height-200))

		
		# CONDITIONS FOR GAME OVER; BIRD HITTING THE PIPE OR GOING BELOW DISPLAY  
		if birdY>=display_height:
			ai.update_q()
			game_over(score)

		if (birdY+5<=ypos[0] or birdY+bird_height>=ypos[0]+gap_height) and (x<birdX+gap_width//2<x+gap_width):
			ai.update_q()
			game_over(score)

		if (birdY+bird_height//2<=ypos[0] or birdY+bird_height//2>=ypos[0]+gap_height) and (x==birdX+bird_width-2):
			ai.update_q()
			game_over(score)

		# UPDATING SCORE EVERY TIME A PIPE IS CROSSED 
		if (x+gap_width==birdX):
			score+=1
		

# GAME INTRO
def start_game():
	
	imageX = 0
	while True:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_RETURN:
					game_loop()

		draw_bg(imageX)
		imageX-=2
		if imageX == -display_width:
			imageX+= display_width
		display_text(110, "FLAPPY BIRDS", red, (display_width*0.5, display_height*0.3))
		display_text(40, "AI MODE", red, (display_width*0.5, display_height*0.39))
		display_text(50, "* Press the Spacebar to keep the bird flying", black, (display_width*0.5, display_height*0.5))
		display_text(50, "* You score one point for avoiding one pipe!", black, (display_width*0.5, display_height*0.6))
		display_text(50, "Press ENTER to continue", red, (display_width*0.5, display_height*0.8))
		pygame.display.update()


start_game()
pygame.quit()
quit()