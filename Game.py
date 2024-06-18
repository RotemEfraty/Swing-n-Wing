import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (100, 100, 100)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Swing n' Wing")

main_dir = os.path.dirname(__file__)
image_dir = os.path.join(main_dir, 'images')
sound_dir = os.path.join(main_dir, 'sounds')

# Load assets
background_image = pygame.image.load(os.path.join(image_dir,'background_image.png'))
start_button_image = pygame.image.load(os.path.join(image_dir,'start_button.png'))
quit_button_image = pygame.image.load(os.path.join(image_dir,'quit_button.png'))
retry_button_image = pygame.image.load(os.path.join(image_dir,'retry_button.png'))
player_image_idle = pygame.image.load(os.path.join(image_dir,'player.png'))
player_image_flying = pygame.image.load(os.path.join(image_dir,'player_wings.png'))
platform_image = pygame.image.load(os.path.join(image_dir,'platform_image.png'))
background_music = os.path.join(sound_dir,'background_music.mp3')
jump_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'jump.mp3'))
swing_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'swing.mp3'))
hurt_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'hurt.mp3'))
victory_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'victory.mp3'))
wind_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'wind.mp3'))
heart_image = pygame.image.load(os.path.join(image_dir,'heart.png'))
heart_image_grey = pygame.image.load(os.path.join(image_dir,'heart_grey.png'))
slime_image = pygame.image.load(os.path.join(image_dir,'slime.png'))
monster_image = pygame.image.load(os.path.join(image_dir,'monster.png'))
final_boss_image = pygame.image.load(os.path.join(image_dir,'final_boss.png'))
win_image = pygame.image.load(os.path.join(image_dir,'win.png'))
wings_image = pygame.image.load(os.path.join(image_dir,'wings.png'))

# Resize buttons
swing_sound.set_volume(99.9)
hurt_sound.set_volume(99.9)  
start_button_image = pygame.transform.scale(start_button_image, (440, 250))
quit_button_image = pygame.transform.scale(quit_button_image, (380, 170))
retry_button_image = pygame.transform.scale(retry_button_image, (440, 250))
player_image_idle = pygame.transform.scale(player_image_idle, (75, 75))
player_image_flying = pygame.transform.scale(player_image_flying, (120, 75))
heart_image = pygame.transform.scale(heart_image, (45, 45))
heart_image_grey = pygame.transform.scale(heart_image_grey, (45, 45))
monster_image = pygame.transform.scale(monster_image, (75, 75))
slime_image = pygame.transform.scale(slime_image, (55, 55))
final_boss_image = pygame.transform.scale(final_boss_image, (55, 55))
win_image = pygame.transform.scale(win_image, (440, 250))
wings_image = pygame.transform.scale(wings_image, (75, 65))

# Button class
class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Health class
class Health:
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health

    def lose_health(self, amount=1):
        self.current_health = max(0, self.current_health - amount)

    def gain_health(self, amount=1):
        self.current_health = min(self.max_health, self.current_health + amount)

# Weapon class
class Weapon:
    def __init__(self):
        self.swinging = False

    def swing(self):
        swing_sound.play()
        self.swinging = True

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.type = enemy_type
        self.health = Health(3)
        self.weapon = Weapon()
        self.on_ground = False
        self.velocity = pygame.math.Vector2(0, 0)
        self.jump_cooldown = 0
        self.attack_cooldown = 0
        self.first_collision = True

        if self.type == 'slime':
            self.image = slime_image
            self.jump_cooldown = 120
            self.attack_cooldown = 0
        elif self.type == 'monster':
            self.image = monster_image
            self.attack_cooldown = 120
        elif self.type == 'final_boss':
            self.health = Health(9)
            self.image = final_boss_image
            self.jump_cooldown = 120
            self.attack_cooldown = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, player, platforms):
        self.on_ground = False

        if self.type == 'slime':
            self.jump_cooldown -= 1
            self.attack_cooldown -=1
            if self.jump_cooldown <= 0:
                self.velocity.y = -15
                self.jump_cooldown = 60

        elif self.type == 'monster':
            self.attack_cooldown -= 1

        elif self.type == 'final_boss':
            self.attack_cooldown -= 1
            self.jump_cooldown -= 1
            if self.jump_cooldown <= 0:
                self.velocity.y = -10
                self.jump_cooldown = 60

            if player.rect.x > self.rect.x:
                self.velocity.x = 2
            else:
                self.velocity.x = -2

        self.velocity.y += 0.5
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.colliderect(player.rect) and self.attack_cooldown <= 0:
            if self.first_collision and self.type == 'monster':
                self.attack_cooldown = 30
                self.first_collision = False
            elif self.type == 'final_boss':
                self.attack_cooldown = 60
                if random.randint(1, 4) == 1:
                    player.rect.x -= 40
                    player.health.lose_health()
                    hurt_sound.play()
                    self.weapon.swinging = False
            else: 
                player.rect.x -= 40
                player.health.lose_health()
                hurt_sound.play()
                self.weapon.swinging = False
                self.attack_cooldown = 90

        self.check_collision(platforms)

    def check_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.collision_rect):
                if self.velocity.y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top + 22
                    self.velocity.y = 0
                    self.on_ground = True

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image_idle
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.health = Health(3)
        self.weapon = Weapon()
        self.attack_cooldown = 0
        self.ATTACK_COOLDOWN_TIME = 30

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0

        if self.on_ground and keys[pygame.K_SPACE]:
            self.velocity.y = -10
            jump_sound.play()

        if keys[pygame.K_z] and self.attack_cooldown == 0:
            self.weapon.swing()
            self.attack_cooldown = self.ATTACK_COOLDOWN_TIME

        self.attack_cooldown = max(0, self.attack_cooldown - 1)

        self.velocity.y += 0.5
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        self.on_ground = False

        if self.health.current_health <= 0:
            game_over()

    def check_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.collision_rect):
                if self.velocity.y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top + 28
                    self.velocity.y = 0
                    self.on_ground = True

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(platform_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        collision_margin = 70
        self.collision_rect = pygame.Rect(self.rect.x + collision_margin, self.rect.y, self.rect.width - 2 * collision_margin, self.rect.height)

# Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Main menu function
def main_menu():
    start_button = Button(start_button_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    quit_button = Button(quit_button_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    menu_running = True

    while menu_running:
        screen.blit(background_image, (-50, -50))
        start_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    game_loop()
                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Game over function
def game_over():
    wind_sound.stop()
    retry_button = Button(retry_button_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    quit_button = Button(quit_button_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    game_over_running = True

    while game_over_running:
        screen.blit(background_image, (-50, -50))
        retry_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.is_clicked(event.pos):
                    game_loop()
                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Pause menu function
def pause_menu():
    resume_button = Button(start_button_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    quit_button = Button(quit_button_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    pause_running = True

    while pause_running:
        screen.blit(background_image, (-50, -50))
        resume_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.is_clicked(event.pos):
                    return
                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Victory menu function
def victory_menu():
    quit_button = Button(quit_button_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    win_image = pygame.image.load(os.path.join(image_dir, 'win.png'))
    win_image_rect = win_image.get_rect()
    win_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    victory_running = True

    while victory_running:
        screen.blit(background_image, (-50, -50))
        screen.blit(win_image, win_image_rect)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Game loop function
def game_loop():
    player = Player(100, 100)
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    platform_width = 180
    platform_height = 100

    platforms.add(
        Platform(100, 500, platform_width, platform_height),
        Platform(200, 500, platform_width, platform_height),
        Platform(400, 400, platform_width, platform_height),
        Platform(500, 400, platform_width, platform_height),
        Platform(600, 400, platform_width, platform_height),
        Platform(800, 300, platform_width, platform_height),
        Platform(900, 300, platform_width, platform_height),
        Platform(900, 500, platform_width, platform_height),
        Platform(1200, 200, platform_width, platform_height),
        Platform(1300, 200, platform_width, platform_height),
        Platform(1400, 200, platform_width, platform_height),
        Platform(1200, 400, platform_width, platform_height),
        Platform(1400, 500, platform_width, platform_height),
        Platform(1600, 400, platform_width, platform_height),
        Platform(1900, 400, platform_width, platform_height),
        Platform(2100, 300, platform_width, platform_height),
        Platform(2200, 300, platform_width, platform_height),
        Platform(2400, 200, platform_width, platform_height),
        Platform(2700, 400, platform_width, platform_height),
        Platform(2800, 400, platform_width, platform_height),
        Platform(2900, 400, platform_width, platform_height),
        Platform(3100, 300, platform_width, platform_height),
        Platform(3200, 300, platform_width, platform_height),
        Platform(3400, 200, platform_width, platform_height),
        Platform(3600, 100, platform_width, platform_height),
        Platform(4000, 500, platform_width, platform_height),
        Platform(4300, 500, platform_width, platform_height),
        Platform(4600, 500, platform_width, platform_height),
        Platform(4900, 500, platform_width, platform_height),
        Platform(5100, 400, platform_width, platform_height),
        Platform(5200, 400, platform_width, platform_height),
        Platform(5400, 300, platform_width, platform_height),
        Platform(5500, 300, platform_width, platform_height),
        Platform(5700, 400, platform_width, platform_height),
        Platform(5800, 400, platform_width, platform_height),
        Platform(5900, 400, platform_width, platform_height),
        Platform(6100, 300, platform_width, platform_height),
        Platform(6300, 200, platform_width, platform_height),
        Platform(6500, 100, platform_width, platform_height),
        Platform(6600, 100, platform_width, platform_height),
        Platform(6500, 300, platform_width, platform_height),
        Platform(6600, 300, platform_width, platform_height),
        Platform(6800, 500, platform_width, platform_height),
        Platform(6900, 500, platform_width, platform_height),
        Platform(7000, 500, platform_width, platform_height),
        Platform(6900, 200, platform_width, platform_height),
        Platform(7100, 500, platform_width, platform_height),
        Platform(7100, 400, platform_width, platform_height),
        Platform(7200, 500, platform_width, platform_height),
        Platform(7300, 300, platform_width, platform_height),
        Platform(7300, 500, platform_width, platform_height),
        Platform(7400, 500, platform_width, platform_height),
        Platform(7500, 500, platform_width, platform_height),
        Platform(7500, 400, platform_width, platform_height),
        Platform(7600, 500, platform_width, platform_height),
        Platform(7700, 500, platform_width, platform_height),
        Platform(7800, 500, platform_width, platform_height),
    )
    
    enemies.add(
        Enemy(7300, 300, 'final_boss'),
        Enemy(250, 500, 'monster'),
        Enemy(460, 400, 'slime'),
        Enemy(660, 400, 'slime'),
        Enemy(950, 300, 'monster'),
        Enemy(1250, 200, 'monster'),
        Enemy(1450, 200, 'monster'),
        Enemy(1460, 500, 'slime'),
        Enemy(2250, 300, 'monster'),
        Enemy(2760, 400, 'slime'),
        Enemy(2960, 400, 'slime'),
        Enemy(3250, 300, 'monster'),
        Enemy(3660, 100, 'slime'),
        Enemy(4360, 500, 'slime'),
        Enemy(4960, 500, 'slime'),
        Enemy(5250, 400, 'monster'),
        Enemy(5550, 300, 'monster'),
        Enemy(5760, 400, 'slime'),
        Enemy(5850, 400, 'monster'),
        Enemy(5960, 400, 'slime'),
        Enemy(6360, 200, 'slime'),
        Enemy(6600, 100, 'slime'),
        Enemy(6550, 300, 'monster'),
        Enemy(6650, 300, 'monster'),
        Enemy(7150, 400, 'monster'),
        Enemy(7360, 300, 'slime'),
        Enemy(7550, 400, 'monster'),
    )

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(*platforms)
    all_sprites.add(*enemies)

    wings = pygame.sprite.Sprite()
    wings.image = wings_image
    wings.rect = wings.image.get_rect()
    wings.rect.topleft = (950, 480)
    all_sprites.add(wings)
    
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    camera = Camera(8000, SCREEN_HEIGHT)

    game_running = True
    flying = False
    flying_timer = 0

    while game_running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

        if player.rect.colliderect(wings.rect):
            flying = True
            flying_timer = 1200
            wings.kill()
            wind_sound.play()

        if flying:
            flying_timer -= 1
            if flying_timer <= 0:
                flying = False
                player.image = player_image_idle
            else:
                player.image = player_image_flying
                if keys[pygame.K_SPACE]:
                    player.velocity.y = -5
                else:
                    player.velocity.y += 0.5


        player.update(keys)
        player.check_collision(platforms)

        for enemy in enemies:
            enemy.update(player, platforms)
            if player.weapon.swinging and player.rect.colliderect(enemy.rect):
                enemy.health.lose_health()
                player.weapon.swinging = False
                if enemy.type == 'final_boss' or enemy.type == 'monster':
                    enemy.rect.x += 65
                if enemy.health.current_health == 0 and enemy.type == 'final_boss':
                    enemy.kill()
                    victory_sound.play()
                    pygame.mixer.music.stop()
                    victory_menu()
                elif enemy.health.current_health == 0:
                    enemy.kill()
                

            if isinstance(enemy, Enemy) and enemy.type == 'final_boss' and enemy.rect.top > SCREEN_HEIGHT:
                enemy.rect.x = 7300
                enemy.rect.y = 300
                enemy.velocity = pygame.math.Vector2(0, 0)

        camera.update(player)

        if player.rect.top > SCREEN_HEIGHT:
            game_running = False
            game_over()

        screen.blit(background_image, (-500, -100))
        for entity in all_sprites:
            screen.blit(entity.image, camera.apply(entity))
        
        for i in range(player.health.max_health):
            if i < player.health.current_health:
                screen.blit(heart_image, (10 + i * 40, 10))
            else:
                screen.blit(heart_image_grey, (10 + i * 40, 10))
        
        pygame.display.update()
        pygame.time.Clock().tick(60)

main_menu()