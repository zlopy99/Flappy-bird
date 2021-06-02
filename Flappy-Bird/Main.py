import pygame, sys, random

def draw_floor():       # X, Y
    screen.blit(floor, (floor_x, 704))
                        # X + veličina X-a...trebalo bi 600, ali ne poklapa se sa floorom
    screen.blit(floor, (floor_x + 578, 704))

def create_pipe():
    random_pipe = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(670, random_pipe - 290))
    bottom_pipe = pipe_surface.get_rect(midtop = (670, random_pipe))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    pom = 0
    for pipe in pipes:
        pipe.centerx -= 3.5
        if (pipe.centerx < bird_rect.centerx and pipe.centerx > 95) or (pipe.centerx < bird_rect1.centerx and pipe.centerx > 95):
            pom = 1
            score_sound.play()
    return pipes, pom

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            screen.blit(pipe_surface, pipe)
        else:                          # Zaokrenuti sliku u: X ili Y smjeru
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 704:
        death_sound.play()
        return False

    return True

def check_collision1(pipes):
    for pipe in pipes:
        if bird_rect1.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect1.top <= -50 or bird_rect1.bottom >= 704:
        death_sound.play()
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotate(bird, -bird_movment * 2.5)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def bird_animation1():
    new_bird = bird_frames1[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def day_night():
    Day_surface = game_font.render('Day', True, (255, 255, 0))
    Day_rect = Day_surface.get_rect(center=(200, 260))
    screen.blit(Day_surface, Day_rect)

    Night_surface = game_font.render('Night', True, (0, 0, 0))
    Night_rect = Night_surface.get_rect(center=(400, 260))
    screen.blit(Night_surface, Night_rect)

def score_dispaly(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render('Score: '+str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (300, 80))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(300, 80))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render('High Score: ' + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(300, 680))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 1, buffer = 212)
pygame.init()                  # width height
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('FlappyBird_Python-master/04B_19.TTF', 40)

# Game Varijable
gravity = 0.25
bird_movment = 0
game_active = False
score = 0
high_score = 0
time_of_day = True

# Background display 1                                                               Converta file prepoznatljiv pythonu radi lakšeg korištenja i brzine
bg_surface = pygame.image.load('FlappyBird_Python-master/assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
# Background display 2
bg_surface1 = pygame.image.load('FlappyBird_Python-master/assets/background-night.png').convert()
bg_surface1 = pygame.transform.scale2x(bg_surface1)

# Floor
floor = pygame.image.load('FlappyBird_Python-master/assets/base.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x = 0

# Bird 1
bird_downflap = pygame.transform.scale2x(pygame.image.load('FlappyBird_Python-master/assets/bluebird-downflap.png').convert())
bird_midflap = pygame.transform.scale2x(pygame.image.load('FlappyBird_Python-master/assets/bluebird-midflap.png').convert())
bird_upflap = pygame.transform.scale2x(pygame.image.load('FlappyBird_Python-master/assets/bluebird-upflap.png').convert())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 400))
bird_flap = pygame.USEREVENT + 1 # Već imamo jedan USEREVENT, tako ako bi stvarali drugi samo + 1
pygame.time.set_timer(bird_flap, 200)
# Bird 2
bird_downflap1 = pygame.transform.scale2x(pygame.image.load('FlappyBird_Python-master/assets/redbird-downflap.png').convert())
bird_midflap1 = pygame.transform.scale2x(pygame.image.load('FlappyBird_Python-master/assets/redbird-midflap.png').convert())
bird_upflap1 = pygame.transform.scale2x(pygame.image.load('FlappyBird_Python-master/assets/redbird-upflap.png').convert())
bird_frames1 = [bird_downflap1, bird_midflap1, bird_upflap1]
bird_surface1 = bird_frames1[bird_index]
bird_rect1 = bird_surface1.get_rect(center = (100, 400))

# Pipe
pipe_surface = pygame.image.load('FlappyBird_Python-master/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
spawn_pipe = pygame.USEREVENT     # Milisekunde
pygame.time.set_timer(spawn_pipe, 1300)
pipe_height = [350, 450, 550]

# Game Over
game_over_surface = pygame.image.load('FlappyBird_Python-master/assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (300, 380))

# Sounds
flap_sound = pygame.mixer.Sound('FlappyBird_Python-master/sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('FlappyBird_Python-master/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('FlappyBird_Python-master/sound/sfx_point.wav')

while True:
    # All ervents
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movment = 0
                bird_movment -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 400)
                bird_rect1.center = (100, 400)
                bird_movment = -5
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            if time_of_day:
                bird_surface, bird_rect = bird_animation()
            else:
                bird_surface1, bird_rect1 = bird_animation1()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            if pygame.mouse.get_pressed()[0]:
                if pygame.mouse.get_pos()[0] >= 159 and pygame.mouse.get_pos()[0] <= 237 and pygame.mouse.get_pos()[1] >= 237 and pygame.mouse.get_pos()[1] <= 286:
                    time_of_day = True
                elif pygame.mouse.get_pos()[0] >= 345 and pygame.mouse.get_pos()[0] <= 453 and pygame.mouse.get_pos()[1] >= 233 and pygame.mouse.get_pos()[1] <= 286:
                    time_of_day = False

    # Background           width height
    if time_of_day:
        screen.blit(bg_surface, (0,0))
    else:
        screen.blit(bg_surface1, (0, 0))

    if game_active:

        # Bird
        bird_movment += gravity
        if time_of_day:
            rotated_bird = rotate_bird(bird_surface1)
            bird_rect1.centery += bird_movment
            screen.blit(rotated_bird, bird_rect1)

            # Colide 1
            game_active = check_collision1(pipe_list)
        else:
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movment
            screen.blit(rotated_bird, bird_rect)

            # Colide 2
            game_active = check_collision(pipe_list)

        # Pipes
        pipe_list, pom = move_pipes(pipe_list)
        score += pom
        draw_pipes(pipe_list)

        # Score
        score_dispaly('main_game')
    else:
        high_score = update_score(score, high_score)
        score_dispaly('game_over')

        # Game Over
        screen.blit(game_over_surface, game_over_rect)

        # Day - Night
        day_night()

    # Floor
    floor_x -= 1
    draw_floor()
    if floor_x <= -578:
        floor_x = 0

    # Constant update of screen
    pygame.display.update()

    # frame limit
    clock.tick(120) # frames(up to 120, cant go anny higher, but it can go lower)