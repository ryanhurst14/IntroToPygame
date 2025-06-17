import pygame
from sys import exit 
from random import randint

def display_score():
    current_time = int((pygame.time.get_ticks()/1000)) - start_time
    score_surface = test_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacles):
    if obstacles:
        for obstacle in obstacles:
            obstacle.x -= 5
            
            if obstacle.bottom == 300:
                screen.blit(snail_surface, obstacle)
            else:
                screen.blit(fly_surf, obstacle)

        
        obstacle_list = [obstacle for obstacle in obstacles if obstacle.x > -100]
        return obstacle_list
    return []
    

def collisions(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return False
            
    return True

pygame.init() #Init Pygame
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Ryan's Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

game_active = False 
start_time = 0
score = 0

sky_surface = pygame.image.load("graphics/Sky.png")
ground_surface = pygame.image.load("graphics/ground.png")

# score_surface= test_font.render("My game", False, (64,64,64))
# score_rect = score_surface.get_rect(center = (400, 50))

#obstacles

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha() #convert_alpha() makes it run faster
fly_surf = pygame.image.load("graphics/fly/fly1.png").convert_alpha()

obstacle_rect_list = []


player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))

player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

player_gravity = 0

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render("Press space to run", False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 340))


#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

#EVENT LOOP
while True:
    #Draw and update everything
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100), 210)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 300)))
            



        
        
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        # screen.blit(score_surface, score_rect)
        score = display_score()

        # #SNAIL
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        #PLAYER
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)


        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        

        #collision
        game_active = collisions(player_rect, obstacle_rect_list)
    else:
        obstacle_rect_list.clear()
        screen.fill((94, 129, 162))
        screen.blit(player_stand,player_stand_rect)
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        score_message = test_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(60) #60 FPS

