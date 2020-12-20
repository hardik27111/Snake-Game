import random
import pygame
import time
import os

pygame.mixer.init()


pygame.init()

width=600
heigth=600
screen = pygame.display.set_mode((width,heigth))

# colors
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
drake_green=(40,250,40)
black=(0,0,0)
orange=(255,69,0)
# tiles stcuture in game
di = 20
sq = width // di
def tiles():
    colors=[green,drake_green]
    for r in range (di):
        for c in range (di):
            color = colors[((r+c)%2)]
            pygame.draw.rect(screen,color,[c*sq,r*sq,sq,sq])


# Game spefici variable

clock = pygame.time.Clock()

# text funtion
font=pygame.font.SysFont(None,35)
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

def message(text,color):
    text_go = font.render(text,True,color)
    textRect = text_go.get_rect()
    textRect.center = (width//2,heigth//2)
    screen.blit(text_go,textRect)
# snake funtion
def plot_snake(screen, color, snk_list, snake_size,border):
    for x,y in snk_list:
        pygame.draw.circle(screen, color, [x, y], snake_size,2)






sound1 = pygame.mixer.Sound('bite.wav')

def gameloop():
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play()
    exit_game=False
    game_over = False
    snake_x = 75
    snake_y = 75
    velocity_x = 0
    velocity_y = 0
    food_size = 8
    num = 15
    food = [num * i for i in range(1, 39) if (i % 2 != 0)]
    fod_y = [num * i for i in range(5, 39) if (i % 2 != 0)]
    food_x = random.choice(food)
    food_y = random.choice(fod_y)
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")
    with open("highscore.txt","r") as f:
        hiscore=f.read()
    score = 0
    init_velocity = 5
    snake_size = 9
    fps = 30
    life=3
    snk_list = []
    snk_length = 1
    # game loop
    while not exit_game:

            if game_over:
                with open("highscore.txt","w") as f:
                    f.write(str(hiscore))
                screen.fill(white)
                message('Game over! Press Enter to continue', red)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            gameloop()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game=True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            velocity_x = init_velocity
                            velocity_y = 0

                        if event.key == pygame.K_LEFT:
                            velocity_x = - init_velocity
                            velocity_y = 0

                        if event.key == pygame.K_UP:
                            velocity_y = - init_velocity
                            velocity_x = 0

                        if event.key == pygame.K_DOWN:
                            velocity_y = init_velocity
                            velocity_x = 0

                snake_x = snake_x + velocity_x
                snake_y = snake_y + velocity_y



                if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                    score += 10
                    food_x = random.choice(food)
                    food_y = random.choice(fod_y)
                    sound1.play()
                    snk_length += 3
                    if score>int(hiscore):
                        hiscore=score

                tiles()
                pygame.draw.line(screen,black,[0,30],[600,30],3)
                pygame.draw.circle(screen, red, [food_x, food_y],food_size)
                pygame.draw.circle(screen,black,[food_x,food_y],food_size+1,1)
                pygame.draw.rect(screen,white,[0,0,600,30])
                text_screen(" Score: " + str(score) + '   Life :'+str(life) + '    Hiscore :'+str(hiscore), red, 3, 3)


                head = []
                head.append(snake_x)
                head.append(snake_y)
                snk_list.append(head)

                if len(snk_list) > snk_length:
                    del snk_list[0]

                if head in snk_list[:-1]:
                    life-=1
                    time.sleep(1)
                    if life==0:
                        game_over=True
                        pygame.mixer.music.load('over.mp3')
                        pygame.mixer.music.play()
                if snake_x<0 or snake_x>width or snake_y<35 or snake_y>heigth:
                    life-=1
                    time.sleep(1)
                    plot_snake(screen, colo, snk_list, snake_size, 2)
                    if life == 0:
                        game_over = True
                        pygame.mixer.music.load('over.mp3')
                        pygame.mixer.music.play()


                col=[(255,240,0),(204,102,153),(255,51,0),(204,0,255),(153,0,255)]
                colo=random.choice(col)
                pygame.draw.circle(screen, black, [snake_x, snake_y], snake_size)

                plot_snake(screen,colo , snk_list, snake_size,2)
                pygame.display.update()
                clock.tick(fps)

            pygame.display.update()

    pygame.quit()
    quit()

def welcome():
    pygame.mixer.music.load('welcome.mp3')
    pygame.mixer.music.play()
    while True:
        screen.fill(white)
        image = pygame.image.load('sn.jpeg')
        image=pygame.transform.scale(image,(600,600))
        screen.blit(image, (0, 0))

        text_screen('Welcome to the snake world',green, 150, 500)
        text_screen(' Press SPACEBAR forplay the game',green,100,550)
        for event in pygame.event.get():


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()
        pygame.display.update()
    pygame.quit()
    quit()


welcome()