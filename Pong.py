#Simple PONG game clone
import pygame
import sys
import os
import random

#All variables setting

grey = (208, 208, 208)
white = (253, 253, 253)
black = (0, 0, 0)

player1_movement = 0
player2_movement = 0
playerPC_movement = 4
begin_pong_speedx = 6
begin_pong_speedy = 6
intermission = True
x = 0

def player1_move():

    """It does not allow the player to go outside the app window"""

    global player_movement
    
    player_1.y = player_1.y + player1_movement
    
    if player_1.top <= 0:
        player_1.top = 0
    if player_1.bottom >= 800:
        player_1.bottom = 800

def player2_move():

    """It does not allow the player to go outside the app window"""

    global player_movement
    
    player_2.y = player_2.y + player2_movement
    
    if player_2.top <= 0:
        player_2.top = 0
    if player_2.bottom >= 800:
        player_2.bottom = 800

def player2_PC():

    """It does not allow the AI player to go outside the window;
       sets the AI player's behaviors"""

    global player_2
    global player_movement

    if player_2.top <= 0:
        player_2.top = 0
    if player_2.bottom >= 800:
        player_2.bottom = 800
    
    if player_2.top <= pong.y:
        player_2.y = player_2.y + playerPC_movement
    if player_2.bottom > pong.y:
        player_2.y = player_2.y - playerPC_movement

def ping_pong_roll():

    """Creates a ping pong move across the table"""
    
    global begin_pong_speedx
    global begin_pong_speedy
    global player1_points
    global player2_points
    global intermission
    global x

    pong.x = pong.x + begin_pong_speedx
    pong.y = pong.y + begin_pong_speedy
    
    if pong.left <= 0: #It does not allow the ping pong to go outside the window
        player2_points = player2_points + 1 #Count points
        x = 1
        pygame.mixer.Sound.play(score_sound)
        intermission = pygame.time.get_ticks()
    if pong.right >= 1064: #This also do the same as previous
        player1_points = player1_points + 1
        x = 2
        pygame.mixer.Sound.play(score_sound)
        intermission = pygame.time.get_ticks()
        
    if pong.top <= 0 or pong.bottom >= 800: #The same but without points
        begin_pong_speedy = begin_pong_speedy * (-1)
        pygame.mixer.Sound.play(wall_sound)
        
    if pong.colliderect(player_1) and begin_pong_speedx < 0: #Checks collisions
        begin_pong_speedx = begin_pong_speedx * (-1)
        pygame.mixer.Sound.play(racket_sound)
    if pong.colliderect(player_2) and begin_pong_speedx > 0:
                                                        #Also checks collisions
        begin_pong_speedx = begin_pong_speedx * (-1)
        pygame.mixer.Sound.play(racket_sound)

def re_start_game(part):

    """Restart the game or start a new one"""
    
    global begin_pong_speedx
    global begin_pong_speedy
    global time_break
    global intermission
    global x
    
    pong.center = (532, 400)
    intermission_checker = pygame.time.get_ticks()

    if part == 1:
        pass
    else:
        if intermission_checker - intermission < 1000: #Intermission
            begin_pong_speedx = 0
            begin_pong_speedy = 0
        else:
            if x == 1:
                begin_pong_speedx = 6
                begin_pong_speedy = 6 * random.choice((1,-1))
                intermission = None
            else:
                begin_pong_speedx = -6
                begin_pong_speedy = 6 * random.choice((1,-1))
                intermission = None

def actual_game(mode):

    """Actual game with keys on keyboards"""

    re_start_game(1)

    global player1_movement
    global player2_movement
    global player1_points
    global player2_points

    player1_points = 0
    player2_points = 0

    while True: #workings keys on keyboard and closing app
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1_movement = player1_movement - 4
                if event.key == pygame.K_s:
                    player1_movement = player1_movement + 4
                if event.key == pygame.K_ESCAPE:
                    if mode == 1: #Updating hihscores
                        highscore = open("Highscore_p1.txt", "rb+")
                        highscore_r = highscore.readlines()
                        if eval((highscore_r[0])) < player1_points:
                            pre_highscore = open("+-+.txt", "w")
                            pre_highscore.write("%s\n%d" % (player1_points,
                                                            player2_points))
                            pre_highscore.close()
                            highscore.close()
                            os.remove("Highscore_p1.txt")
                            os.rename("+-+.txt", "Highscore_p1.txt")
                    elif mode == 2: #Also updating hihscores
                        highscore = open("Highscore_p2.txt", "rb+")
                        highscore_r = highscore.readlines()
                        if player1_points > player2_points:
                            i = 0
                            record_score = player1_points
                        else:
                            i = 1
                            record_score = player2_points
                        if eval((highscore_r[i])) < record_score:
                            pre_highscore = open("+-+.txt", "w")
                            pre_highscore.write("%s\n%d" % (player1_points,
                                                            player2_points))
                            pre_highscore.close()
                            highscore.close()
                            os.remove("Highscore_p2.txt")
                            os.rename("+-+.txt", "Highscore_p2.txt")
                        
                    menu()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player1_movement = player1_movement + 4
                if event.key == pygame.K_s:
                    player1_movement = player1_movement - 4
                    
            if mode == 2:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player2_movement = player2_movement - 4
                    if event.key == pygame.K_DOWN:
                        player2_movement = player2_movement + 4
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player2_movement = player2_movement + 4
                    if event.key == pygame.K_DOWN:
                        player2_movement = player2_movement - 4

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        whole_game(mode)

def whole_game(players):

    """Actual game without keys on keyboards"""
    
    ping_pong_roll()
    player1_move()
    
    if players == 1: #Game mode
        player2_PC()
    else:
        player2_move()

    screen.fill(pygame.Color("black"))
    pygame.draw.rect(screen, grey, player_1)
    pygame.draw.rect(screen, grey, player_2)
    pygame.draw.rect(screen, grey, pong)
    
    for i in range (0, 160): #Dotted line
        if i % 5 == 0: 
            pygame.draw.line(screen, grey, (532, i * 5), (532, i * 5 + 10), 5)
    
    player1_score = point_font.render("%s" % player1_points, True, grey)
    screen.blit(player1_score, (370, 50))
    player2_score = point_font.render("%s" % player2_points, True, grey)
    screen.blit(player2_score, (644, 50))

    if intermission:
        re_start_game(2)

    pygame.display.flip()
    clock.tick(75)

def how_to_play():

    """Screen with instruction how to play PONG"""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                
        backgroundh = os.path.join("Images", "How_to_play.jpg")
        screen.blit(pygame.image.load(backgroundh), (0,0))

        pygame.display.flip()
        clock.tick(75)

def about_creator():

    """Screen with something about me"""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                
        backgroundh = os.path.join("Images", "About.jpg")
        screen.blit(pygame.image.load(backgroundh), (0,0))

        pygame.display.flip()
        clock.tick(75)

def highscores():

    """Screen with Highscores"""

    menu_font = pygame.font.Font("Blippo Bold.ttf", 46)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                
        backgroundh = os.path.join("Images", "Highscore_bg.jpg")
                                                    #loading highscores
        screen.blit(pygame.image.load(backgroundh), (0,0))

        highscore1 = open("Highscore_p1.txt", "rb+")
        highscore2 = open("Highscore_p2.txt", "rb+")
        highscore1_r = highscore1.readlines()
        highscore2_r = highscore2.readlines()
        
        hs1 = menu_font.render("%s - %d" % (eval(highscore1_r[0]),
                                            eval(highscore1_r[1])), True, white)
        screen.blit(hs1, (750, 420))
        hs2 = menu_font.render("%s - %d" % (eval(highscore2_r[0]),
                                            eval(highscore2_r[1])), True, white)
        screen.blit(hs2, (750, 540))
        
        highscore1.close()
        highscore2.close()

        pygame.display.flip()
        clock.tick(75)

def button(x, y, width, height, text):

    """Every working button on the screen"""

    menu_font = pygame.font.Font("Blippo Bold.ttf", 46)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, white, (x - 10, y - 10, height + 20, width + 20))
    
    btn_text = menu_font.render(text, True, black)
    text_rect = btn_text.get_rect()
    text_rect.center = (x + 153, y + 50)
    screen.blit(btn_text, text_rect)
    
    if x + height > mouse[0] > x and y + width > mouse[1] > y:
        pygame.draw.rect(screen, (180, 180, 180), (x, y, height, width))
        if click[0] == 1:
            if text == "vs. AI":
                actual_game(1)
            elif text == "Exit" and text != "Back":
                pygame.quit()
                sys.exit()
            elif text == "vs. Player":
                actual_game(2)
            elif text == "Game Rules":
                how_to_play()
            elif text == "About Creator":
                about_creator()
            elif text == "Highscores":
                highscores()
    else:
        pygame.draw.rect(screen, grey, (x, y, height, width))

    btn_text = menu_font.render(text, True, black)
    text_rect = btn_text.get_rect()
    text_rect.center = (x + 147, y + 50)
    screen.blit(btn_text, text_rect)


def menu():

    """Whole main menu"""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        background = os.path.join("Images", "Background.jpg")
        screen.blit(pygame.image.load(background), (0,0))

        button(90, 360, 100, 300, "vs. AI")
        button(90, 500, 100, 300, "Game Rules")
        button(90, 640, 100, 300, "About Creator")
        button(674, 360, 100, 300, "vs. Player")
        button(674, 500, 100, 300, "Highscores")
        button(674, 640, 100, 300, "Exit")
        pygame.display.flip()
        clock.tick(75)

pygame.init() #Initialising game
clock = pygame.time.Clock()

player_1 = pygame.Rect(20, 325, 13, 110)
player_2 = pygame.Rect(1031, 325, 13, 110)
pong = pygame.Rect(525, 379, 14, 14)

screen = pygame.display.set_mode((1064, 800))
pygame.display.set_caption("Pong 49th anniversary")
point_font = pygame.font.Font("pong-score.ttf", 128)

racket_sound = pygame.mixer.Sound(os.path.join("Sounds", "bounce_racket.mp3"))
wall_sound = pygame.mixer.Sound(os.path.join("Sounds", "bounce_wall.mp3"))
score_sound = pygame.mixer.Sound(os.path.join("Sounds", "score.mp3"))

menu()
