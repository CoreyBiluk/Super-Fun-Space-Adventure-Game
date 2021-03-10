#############################
# SUPER FUN SPACE ADVENTURE #
#############################
# Art: kenney.nl
# Music / SFX: Corey Biluk

#TODO LIST
# make ship icons for lives bigger
# add a Boss
# 1up Powerups
# add enemy ships that have different patterns and shoot
# More than 2 gun power levels with spread gun

import pygame
import random
from os import path
# Set asset folders
img_dir = path.join(path.dirname(__file__), "img")
audio_dir = path.join(path.dirname(__file__), "audio")

# Game Window Variables
WIDTH = 480
HEIGHT = 600
FPS = 60

# Set length of gun powerup here
POWERUP_TIME = 5000

# Define Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Fun Space Adventure Game!")
clock = pygame.time.Clock()

# Load Audio
music = pygame.mixer.music.load(path.join(audio_dir, "music_SP.ogg"))
shoot_sound = pygame.mixer.Sound(path.join(audio_dir, "sfx_laser2.ogg"))
pygame.mixer.Sound.set_volume(shoot_sound, 0.4)
shoot_sound2 = pygame.mixer.Sound(path.join(audio_dir, "sfx_laser1.ogg"))
pygame.mixer.Sound.set_volume(shoot_sound2, 0.4)
shield_powerup_sound = pygame.mixer.Sound(path.join(audio_dir, "sfx_shieldUp.ogg"))
pygame.mixer.Sound.set_volume(shield_powerup_sound, 0.8)
gun_powerup_sound = pygame.mixer.Sound(path.join(audio_dir, "sfx_twoTone.ogg"))
pygame.mixer.Sound.set_volume(gun_powerup_sound, 0.8)
player_die_sound = pygame.mixer.Sound(path.join(audio_dir, "rumble2.wav"))
explosion_sounds = []
for snd in ['Explosion1.wav', 'Explosion2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(path.join(audio_dir, snd)))

# Load Images
background_img = pygame.image.load(path.join(img_dir, "BG.png")).convert()
background_rect = background_img.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_green.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
laser_img = pygame.image.load(path.join(img_dir, "laserGreen11.png")).convert()
meteor_images = []
meteor_list = ["meteorBrown_big1.png","meteorBrown_big2.png","meteorBrown_med1.png","meteorBrown_med2.png",
               "meteorBrown_small1.png","meteorBrown_small2.png","meteorBrown_tiny1.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
explosion_animation['player'] = []
for i in range(9):
    filename = "regularExplosion{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animation['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animation['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_animation['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'powerupGreen_shield.png')).convert() 
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'powerupRed_bolt.png')).convert() 

# Functions
font_name = pygame.font.match_font('Comic Sans')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_WIDTH = 15
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_WIDTH)
    fill_rect = pygame.Rect(x, y, fill, BAR_WIDTH)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)
    
def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)
        
def show_go_screen():
    screen.blit(background_img, background_rect)
    draw_text(screen, "SUPER FUN", 64, WIDTH /2, 50)
    draw_text(screen, "SPACE ADVENTURE", 64, WIDTH /2, 150)
    draw_text(screen, "GAME!!!", 64, WIDTH /2, 250)
    draw_text(screen, "Left: a     Right: d     Shoot: [space]", 32, WIDTH /2, 350)
    draw_text(screen, "Press any key to begin...", 32, WIDTH /2, 450)
    draw_text(screen, "Art: Kenney.nl", 28, WIDTH / 2, 500)
    draw_text(screen, "Sound / Music: Corey", 28, WIDTH / 2, 550)
    pygame.display.flip()
    waiting = True
    while waiting:
        #clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
            
        
# Create a player class for sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.bottom = HEIGHT - 10
        self.rect.centerx = WIDTH / 2
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        #timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()
        # unhide if hidden 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.bottom = HEIGHT - 10
            self.rect.centerx = WIDTH / 2
            
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -10
        if keystate[pygame.K_d]:
            self.speedx = 10   
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def Powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()
    
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound2.play()
    def hide(self):
        # hide the player between death and spawn
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        # move sprite offscreen
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

# Create a Mob class for sprite
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rot_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)    
               
# Create a bullet class for sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (10 , 40))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = - 10

    def update(self):
        self.rect.y += self.speedy
        # kill it if moves off screen
        if self.rect.bottom < 0:
            self.kill()

# Create a power-up class for sprite
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill it if moves off screen
        if self.rect.top > HEIGHT:
            self.kill()

# Create a explosion class for sprite
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Start Music (Music commented out till music is composed)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1) #(-1 for endless loop)

# Game Loop
run = True
game_over = True

while run:
    if game_over:
        show_go_screen()
        game_over = False
        # create sprite groups 
        all_sprites = pygame.sprite.Group() 
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        # player spawn
        player = Player()
        all_sprites.add(player)
        # mobs spawn
        for i in range(16):
            new_mob()
        # set score
        score = 0
    # keep loop running at right speed
    clock.tick(FPS)
    
    # Process input (events)
    for event in pygame.event.get():
        # check for window close
        if event.type == pygame.QUIT:
            run = False
            
    # Update
    all_sprites.update()
    
    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 70 - hit.radius
        pygame.mixer.Sound.set_volume(explosion_sounds[0], 0.2)
        pygame.mixer.Sound.set_volume(explosion_sounds[1], 0.2)
        random.choice(explosion_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        # spawn powerups
        if random.random() > 0.95:
            powerup = Pow(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)
        new_mob()
    
    # check to see if player hits a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            shield_powerup_sound.play()
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            gun_powerup_sound.play()
            player.Powerup()
    
    # check to see if a mob hit the character
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_mob()
        if player.shield <= 0:
            player_die_sound.play()
            pygame.mixer.Sound.set_volume(player_die_sound, 0.5)
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # if player died and explosion has finished
    if player.lives == 0 and not death_explosion.alive():
        game_over = True
    
    # Draw / Render
    screen.fill(BLACK)
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {str(score)}", 30, (WIDTH / 2) - 12, 10)
    draw_text(screen, "Shield", 26, 40, 5)
    draw_shield_bar(screen, 15, 25, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()
    
pygame.quit()
 



