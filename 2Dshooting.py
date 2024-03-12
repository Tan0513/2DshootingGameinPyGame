import pygame
import random
import os


FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


WIDTH = 500
HEIGHT = 600


# 游戲初始化 & 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("面有楠色")
clock = pygame.time.Clock()


# 載入圖片
background_img = pygame.image.load(os.path.join("Game", "source", "img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("Game", "source", "img", "player(new).png")).convert()
player_L_img = pygame.image.load(os.path.join("Game", "source", "img", "player(left).png")).convert()
player_L_img.set_colorkey(GREEN)
player_R_img = pygame.image.load(os.path.join("Game", "source", "img", "player(right).png")).convert()
player_R_img.set_colorkey(GREEN)
player_mini_img = pygame.transform.scale(player_img, (25, 25))
player_mini_img.set_colorkey(GREEN)
pygame.display.set_icon(player_mini_img)
bullet_img = pygame.image.load(os.path.join("Game", "source", "img", "bullet.png")).convert()
start_img = pygame.image.load(os.path.join("Game", "source", "img", "start_btn.png")).convert()
exit_img = pygame.image.load(os.path.join("Game", "source", "img", "exit_btn.png")).convert()
back_img = pygame.image.load(os.path.join("Game", "source", "img", "back_btn.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("Game", "source", "img", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("Game", "source", "img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("Game", "source", "img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs = {}
power_imgs['heal'] = pygame.image.load(os.path.join("Game", "source", "img", "heal.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("Game", "source", "img", "gun.png")).convert()


# 載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("Game", "source", "sound", "shoot.wav"))
shoot_sound.set_volume(0.1)
gun_sound = pygame.mixer.Sound(os.path.join("Game", "source", "sound", "pow1.wav"))
gun_sound.set_volume(0.1)
heal_sound = pygame.mixer.Sound(os.path.join("Game", "source", "sound", "pow0.wav"))
heal_sound.set_volume(0.1)
die_sound = pygame.mixer.Sound(os.path.join("Game", "source", "sound", "rumble.ogg"))
die_sound.set_volume(0.1)
exel_sounds = [
    pygame.mixer.Sound(os.path.join("Game", "source", "sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("Game", "source", "sound", "expl1.wav"))
]
exel_sounds[0].set_volume(0.1)
exel_sounds[1].set_volume(0.1)
pygame.mixer.music.load(os.path.join("Game", "source", "sound", "background.ogg"))
pygame.mixer.music.set_volume(0.2)






# 玩家屬性
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img #生成玩家飛船
        # self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(GREEN) #去背
        self.rect = self.image.get_rect()
        self.radius = 20 #生成飛船判定大小
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.speedy = 6
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0


    def update(self):
        now = pygame.time.get_ticks()
        #更新火力等級
        if self.gun > 1 and now - self.gun_time > 5000: #5秒
            self.gun -= 1
            self.gun_time = now


        #更新復活無敵時間
        if self.hidden and now - self.hide_time > 1000: #1秒
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10


        #獲得鍵盤輸入
        key_pressed = pygame.key.get_pressed()
        if key_pressed != 1:
            self.image = player_img
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
            self.image = player_R_img
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
            self.image = player_L_img
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedy - 1


        #防止飛船飛出畫面
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT and self.hidden is False:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0 and self.hidden is False:
            self.rect.top = 0


    #火力等級
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun == 2:
                bullet1 = Bullet(self.rect.left + 10, self.rect.centery)
                bullet2 = Bullet(self.rect.right - 10, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            elif self.gun >= 3:
                bullet1 = Bullet(self.rect.left + 8, self.rect.centery)
                bullet2 = Bullet(self.rect.right - 8, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()


    #復活無敵
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)


    #火力升級
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


# 石頭屬性
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)


    #石頭旋轉
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.rot_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #召回超出畫面的石頭
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)


# 子彈屬性
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.speedx = random.randrange(-3, 3)  


    #刪除超出畫面的子彈
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# 爆炸屬性
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):#刪除最後的爆炸圖片
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


# 升級屬性
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['heal', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3


    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


# 按鈕屬性
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False


    def draw(self, surface):
        action = False
        # 獲得滑鼠位置
        pos = pygame.mouse.get_pos()


        # 滑鼠覆蓋 & 按下滑鼠
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        # 載入按鈕
        surface.blit(self.image, (self.rect.x, self.rect.y))


        return action


# 創建按鈕
start_button = Button(WIDTH / 2, 400, start_img, 0.7)
exit_button = Button(WIDTH / 2, 500, exit_img, 0.7)
back_button = Button(WIDTH / 2, 400, back_img, 0.15)


# 載入字體
font_name = os.path.join("Game", "source", "font.ttf")


# 生成字體
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


# 生成石頭
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)


# 生成血量條
def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


# 生成生命條
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 28 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# 生成初始畫面
def draw_init():
    screen.blit(background_img,(0,0))
    start_button.draw(screen)
    exit_button.draw(screen)
    draw_text(screen, '太空生存戰', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, '← →移動飛船 空白鍵發射子彈~', 22, WIDTH / 2, HEIGHT / 2)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT or exit_button.draw(screen):
                pygame.quit()
                return True
            elif start_button.draw(screen):
                waiting = False
                return False


# 生成結束畫面
def draw_end():
    screen.blit(background_img,(0,0))
    draw_text(screen, '游戲結束~', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, '分數:' + str(score), 22, WIDTH / 2, HEIGHT / 2)
    back_button.draw(screen) #載入按鈕
    pygame.display.update()
    ending = True
    while ending:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif back_button.draw(screen):
                ending = False
                return False






# 無限播放BGM
pygame.mixer.music.play(-1)


# 游戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        show_end = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0




    clock.tick(FPS)
    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    # 更新游戲
    all_sprites.update()
    # 判定石頭 子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(exel_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.93: #掉寶率
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()


    # 判定飛船 石頭相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()


    # 判定飛船 寶物相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'heal':
            player.health += 20
            if player.health > 100:
                player.health = 100
            heal_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()


    if player.lives == 0 and not(death_expl.alive()):
        show_end = True


    # 畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update()


    if show_end:
        close = draw_end()
        if close:
            break
        show_init = True


pygame.quit()

