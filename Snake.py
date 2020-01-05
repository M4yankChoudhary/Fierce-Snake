import pygame
import random
import os

pygame.init()

#sound
pygame.mixer.init()

# define colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0,0,0)
screen_width = 1024
screen_height = 720

#creating window
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Fierce Snake") #game title
pygame.display.update() # Update portions of the screen for software displays

#images
background_image = pygame.image.load("background_image.jpg")   #background image
background_image = pygame.transform.scale(background_image,(screen_width,screen_height)).convert_alpha()

start_image = pygame.image.load("start.jpg") #welcome screen
start_image = pygame.transform.scale(start_image,(screen_width,screen_height)).convert_alpha()

game_over_img = pygame.image.load("gameover.jpg") #gameover image
game_over_img = pygame.transform.scale(game_over_img,(screen_width,screen_height)).convert_alpha()


#for fps
clock = pygame.time.Clock()

#font for score etc
font = pygame.font.SysFont(None, 32)

#defining methods
def score_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y,snake_size,snake_size])

#welcome method for welcome screen

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(black)
        gameWindow.blit(start_image,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('backgroundmusic.ogg')
                    pygame.mixer.music.play(-1)
                    gameLoop()

        pygame.display.update()
        clock.tick(60)

#Game loop
def gameLoop():
    # %%%%%%%%%%%%%%%%%%%%%% Game specific variables %%%%%%%%%%%%%%%%%%%%%%
    exit_game = False
    game_over = False
    snake_x = 40
    snake_y = 50
    velocity_x = 0
    velocity_y = 0
    velocity_for_correction = 0
    init_velocity = 5
    fps = 60
    snake_size = 30
    
    #score
    score = 0
    
    # for increasing snakes height
    snake_list = []
    snake_length = 1
    
    # for creating food for our snake
    food_x = random.randint(0, screen_width / 2)
    food_y = random.randint(0, screen_height / 2)

    #check if highscore.txt exists
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")

    # opening file
    with open("highscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(black)
            gameWindow.blit(game_over_img, (0,0))
            score_screen(str(score), white, 210, 662)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                         welcome()

        else :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = velocity_for_correction

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = velocity_for_correction

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = velocity_for_correction

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = velocity_for_correction

                    #%%%%%%%%%%%%%%%Cheat codes%%%%%%%%%%%%%%%%
                    
                    if event.key == pygame.K_k:
                         score += 5
                         
                    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<25 and abs(snake_y - food_y)<25:#abs() gives absolute values
                score += 10
                food_x = random.randint(0, screen_width / 2)  # for putting food at random location 
                food_y = random.randint(0, screen_height / 2)
                snake_length += 5
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('Beep.ogg'))

                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(black)   #colors window white
            gameWindow.blit(background_image, (0, 0) )   #set background image
            pygame.draw.rect(gameWindow, white, [food_x, food_y, snake_size, snake_size]) #food
            score_screen("Score :" + str(score), white, 5, 5)
            score_screen("High Score :" + str(hiscore), white, 800, 5) 


            head = [] #snake's head
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]
            

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.ogg')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y <0 or snake_y > screen_height: 
                game_over = True
                pygame.mixer.music.load('gameover.ogg')
                pygame.mixer.music.play()

            plot_snake(gameWindow, red, snake_list, snake_size)
            
        pygame.display.update()
        clock.tick(fps) #frame per seconds

    pygame.quit()
    quit()

#call game loop
welcome() #Welcome Screen
