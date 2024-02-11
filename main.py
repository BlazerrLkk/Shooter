import time

import pygame.display
from pygame import *
from random import randint

missed = 0
shooted = 0

image_bg = 'galaxy.png'
image_player = 'rocket.png'
image_enemy = 'ufo.png'
image_bullet = 'bullet.png'

window_width = 700
window_height = 500
window = pygame.display.set_mode((window_width, window_height))


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x <= window_width - 100:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x >= 20:
            self.rect.x -= self.speed
        if keys[K_w] and self.rect.y >= window_height - 200:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y <= window_height - 110:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(image_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y >= window_height:
            self.rect.x = randint(50, window_width - 80)
            self.rect.y = 0
            missed += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
bullets = sprite.Group()

monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(image_enemy, randint(50, window_width - 80), 0, 60, 60, randint(1, 5))
    monsters.add(monster)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)
text_win = font2.render('YOU WIN!', True, (255, 255, 255) )
text_lose = font2.render('YOU LOSE', True, (180, 0, 0) )

max_shooted = 5
max_missed = 5


player = Player(image_player, window_width / 2, window_height - 115, 130, 120, 10)

bg = transform.scale(image.load(image_bg), (window_width, window_height))

run = True
finish = False
FPS = 30
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if bullets.__len__() < 3:
                    player.fire()
                    fire_sound.play()

    if not finish:
        window.blit(bg, (0, 0))
        player.reset()
        text_missed = font1.render('Пропущено: ' + str(missed), 1, (255, 255, 255))
        text_shooted = font1.render('Збито: ' + str(shooted), 1, (255, 255, 255))
        window.blit(text_missed, (520, 20))
        window.blit(text_shooted, (10, 20))
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        monsters.update()
        player.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
                shooted += 1
                monster = Enemy(image_enemy, randint(50, window_width - 80), 0, 60, 60, randint(1, 5))
                monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or missed >= max_missed:
            finish = True
            window.blit(text_lose, (200, 200))
        if shooted >= max_shooted:
            finish = True
            window.blit(text_win, (200, 200))
        display.update()
    clock.tick(FPS)
