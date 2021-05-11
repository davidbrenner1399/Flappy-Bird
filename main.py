import pygame, sys, random


HEIGHT = 800
WIDTH = 500 
FPS = 120 
WHITE = (255,255,255) 

#Have 2 floors, this allows for continous motion 
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,702))
    screen.blit(floor_surface,(floor_x_pos + WIDTH,702))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))

    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 350))
    return bottom_pipe,top_pipe


def move_pipes(pipes):
    #will take our list of pipes
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_surface,pipe)
        else:                                               #X   #Y
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
    

#testing for collision

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >= 650:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement *3,1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,WHITE)
        score_rect = score_surface.get_rect(center = (WIDTH/2,30))
        screen.blit(score_surface,score_rect)
    
    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}',True,WHITE)
        score_rect = score_surface.get_rect(center = (WIDTH/2,130))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,WHITE)
        high_score_rect = high_score_surface.get_rect(center = (WIDTH/2,600))
        screen.blit(high_score_surface,high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100,size = 16, channels = 1, buffer = 1024 )
pygame.init()

#display surface
screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()

game_font = pygame.font.Font('04B_19.TTF',40)


# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

#making background

bg_surface = pygame.image.load('assets/background-day.png').convert()

#scaling image to fit display
#bg_surface = pygame.transform.scale(bg_surface,(WIDTH,HEIGHT))
bg_surface = pygame.transform.scale2x(bg_surface)


#making the floor

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)

#getting floor to move

floor_x_pos = 0


#making our birds

#need to switch between different birds

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())

#list of bird positions

bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1

pygame.time.set_timer(BIRDFLAP,200)


#bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)

#putting rectangle around bird
#bird_rect = bird_surface.get_rect(center = (100,HEIGHT//2))


#making the pipes
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,450,600]


game_over_suface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_suface.get_rect(center = (WIDTH/2, HEIGHT/2 - 125))


#SOUNDS

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')

death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

#since our point system is based around .01 this will allow us to match up nicely 
score_sound_countdown = 100

#game loop
while True:
    #event loop
    for event in pygame.event.get():
       if event.type == pygame.QUIT :
           pygame.quit()
           sys.exit()

       if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:

                #make bird movement negative to work
                # against gravity, have to set movement to zero though
                #or we will run into problems
                bird_movement = 0
                bird_movement -= 12 
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0
            

                 
       if event.type == SPAWNPIPE:
           #extending list by a tuple
           pipe_list.extend(create_pipe())
        
       if event.type == BIRDFLAP:
           if bird_index < 2:
               bird_index += 1

           else:
               bird_index = 0

           bird_surface,bird_rect = bird_animation()
            

        

    #displaying background using blit
    screen.blit(bg_surface,(0,0))

    if game_active:

        # BIRD
        bird_movement += gravity

        #rotation for bird
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)

        game_active = check_collision(pipe_list)


        # PIPES
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game') 
        score_sound_countdown -= 1  #will decrease appropriately compared to score
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100 
    else:
        screen.blit(game_over_suface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    # FLOOR
    floor_x_pos -= 1
    draw_floor()

    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(FPS) #setting frame rate
