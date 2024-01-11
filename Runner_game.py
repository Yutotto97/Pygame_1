import pygame
from sys import exit
from random import randint,random
import numpy as np

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]        
        self.rect = self.image.get_rect(midbottom =(80,300))
        self.gravity = 0
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >=300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
    
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index=0
            self.image = self.player_walk[int(self.player_index)]
    
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    
class Victor(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        victor_1 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/Victor_1.png').convert_alpha()
        victor_2 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/Victor_2.png').convert_alpha()
        self.victor_head = [victor_1,victor_2]
        self.victor_index = 0

        self.image = self.victor_head[self.victor_index] 
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(midbottom =(1100,250))
        self.dt = 0
    
    def animation_state(self):
        self.victor_index += random()*0.04
        if int(self.victor_index) >= len(self.victor_head):
            self.victor_index=0
        self.image = self.victor_head[int(self.victor_index)]
        if 1.-self.victor_index < 0.1 and 1.-self.victor_index > -0.1:
            obstacle_group.add(Obstacle(self.rect.x,self.rect.y))
            self.victor_index += 0.2
        # print(int(self.victor_index))
        # print(self.victor_index)
        self.image = pygame.transform.scale2x(self.image)
        
    def displace_y(self):
        self.rect.y += int(3*np.sin(self.dt/20))
        # print(self.rect.y)
        # print(int(3*np.sin(np.pi*pygame.time.get_ticks()/1000)))
        # print(pygame.time.get_ticks())
        
    def update(self):
        if self.rect.x >= 600:
            self.rect.x -= 2
            self.victor_index = 0
        else:
            self.displace_y()
            self.dt +=1
        self.animation_state()
        
class Obstacle(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        super().__init__()
        if int(random()*1.1):
            fire_1 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/fire1.png').convert_alpha()
            fire_2 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/fire2.png').convert_alpha()
            fire_3 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/fire3.png').convert_alpha()
            self.frames = []
            self.hurtful = 1
            for frame in [fire_1,fire_2,fire_3]:
                self.frames.append(pygame.transform.rotate(frame,-90))
            # y_pos = randint(290,300)
                
        else:
            self.hurtful = 0
            self.gravity = -5
            snail_walk_1 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/snail1.png').convert_alpha()
            snail_walk_2 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/snail2.png').convert_alpha()
            self.frames = [snail_walk_1,snail_walk_2]
            # y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topright = (x+10,y+60))
    
    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        
        self.image = self.frames[int(self.animation_index)]        
     
    def moving(self):
        if self.hurtful == 0:
            self.gravity += 1
            self.rect.y += self.gravity
            if self.rect.bottom >=300:
                self.rect.bottom = 300
            self.rect.x -= 6
        else:
            self.rect.x -= 6
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
        
    def update(self):
        self.animation_state()
        self.moving()
        self.destroy()
        
    
def display_score():
    current_time = (pygame.time.get_ticks() - start_time)//364
    score_surf = test_font.render(str(current_time),False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time
    
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 6
            
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else:
        return []
    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True
   
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        victor.empty()
        victor.add(Victor())
        return False
    else:
        return True
    
def player_animation():
    global player_surf, player_index
   
    if player_rect.bottom < 300:
        player_surf = player_jump
    
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index=0
        player_surf = player_walk[int(player_index)]
        
# def snail_animation():
#     global snail_surf, snail_index
    
#     snail_index += 0.1
#     if snail_index >= len(snail_walk):
#         snail_index=0
#     snail_surf = snail_walk[int(snail_index)]
        
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)


player = pygame.sprite.GroupSingle()
player.add(Player())

victor = pygame.sprite.GroupSingle()
victor.add(Victor())

obstacle_group = pygame.sprite.Group()

game_active = False
start_time = 0
score = 0
sky_surface = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/Sky.png').convert()
ground_surface = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/ground.png').convert()

game_name = test_font.render('Your PhD life',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,60))

snail_walk_1 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/snail1.png').convert_alpha()
snail_walk_2 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/snail2.png').convert_alpha()
snail_walk = [snail_walk_1,snail_walk_2]
snail_index = 0
snail_surf = snail_walk[snail_index]
snail_rect = snail_surf.get_rect(bottomright= (600,300))

fly_surf = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/fire1.png').convert_alpha()


obstacle_rect_list = []


player_walk_1 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_surf = player_walk[player_index]

player_jump = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/jump.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom =(80,300))
player_gravity = 0

player_stand = pygame.image.load('/Users/Yuto/Documents/Personal_Files/Game project/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand_scaled.get_rect(center = (400,200))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit() 
            exit()
        
        if game_active:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >=300:
                    player_gravity = -20
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800
                start_time = pygame.time.get_ticks()
         
        
        # if event.type == obstacle_timer and game_active:
        #     obstacle_group.add(Obstacle())
            # if randint(0,2):
            #     obstacle_rect_list.append(snail_surf.get_rect
            #                           (bottomright = (randint(1000,1200),300)))
            # else:
            #     obstacle_rect_list.append(fly_surf.get_rect
            #                           (bottomright = (randint(900,1200),200)))
        # if event.type == snail_animation_timer and game_active:
        #     if snail_index == 0:
        #         snail_index = 1
        #     else:
        #         snail_index = 0
        #     snail_surf = snail_walk[snail_index]                
    
    if game_active:
        
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # screen.blit(text_surface,(300,150))
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surf,score_rect)
        score = display_score()
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surf,snail_rect)
    
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()
        # # snail_animation()
        # screen.blit(player_surf,player_rect)
        
        player.draw(screen)
        player.update()
        
        victor.draw(screen)
        victor.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collision_sprite()
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        # # if snail_rect.colliderect(player_rect):
        # #     game_active = False
        # game_active = collisions(player_rect,obstacle_rect_list)
        
    else:
        screen.fill((94,129,162))    
        screen.blit(player_stand_scaled,player_stand_rect)
        score_message = test_font.render(f'You lasted : {score} days', 
                                         False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
    pygame.display.update()
    clock.tick(60)
