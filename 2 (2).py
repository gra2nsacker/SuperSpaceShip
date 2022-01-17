import os
import random
import sys

import pygame


FIRES_ARRAY = []
ENEMIES_ARRAY = []
SIZE = 1000, 1000
cnt = 0


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Board:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen

    def render(self):
        for i in range(50):
            self.screen.fill(pygame.Color('white'),
                        (random.random() * self.width,
                         random.random() * self.height, 2, 2))


class Fire(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("fire.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def move(self):
        self.rect.y -= 2

    def set_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("spaceship.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = SIZE[0] // 2
        self.rect.y = SIZE[1] // 2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("enemy_spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def move(self):
        self.rect.y += 1

    def set_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y


def shoot(sprite, coord_x, coord_y):
    fire = Fire(sprite)
    fire.set_coords(coord_x, coord_y)
    FIRES_ARRAY.append(fire)


def spawn_enemy(board, enemy_sprites):
    enemy = Enemy(enemy_sprites)
    enemy.rect.x = random.randint(0, board.width)
    enemy.rect.y = 0
    ENEMIES_ARRAY.append(enemy)


def game_over():
    sys.exit()


def tick(hero):
    global ENEMIES_ARRAY
    TMP_ARRAY = []
    shipes_colides = pygame.sprite.Group([ship for ship in ENEMIES_ARRAY])
    for i in FIRES_ARRAY:
        i.move()
    for ship in ENEMIES_ARRAY:
        ship.move()
        if len(pygame.sprite.spritecollide(hero, shipes_colides, False)):
            game_over()
    for fire in FIRES_ARRAY:
        tmp = pygame.sprite.spritecollide(fire, shipes_colides, False)
        if len(tmp):
            for delitable in tmp:
                for k in range(len(ENEMIES_ARRAY)):
                    if ENEMIES_ARRAY[k] == delitable:
                        ENEMIES_ARRAY[k].kill()
                        ENEMIES_ARRAY.pop(k)
                        fire.kill()
                        FIRES_ARRAY.remove(fire)
                        # Андрон, вот здесь счет + 1
                        break


def main():
    size = SIZE
    stars_screen = pygame.display.set_mode(size)
    space_screen = pygame.display.set_mode(size)
    fire_screen = pygame.display.set_mode(size)
    score_screen = pygame.display.set_mode(size)


    board = Board(size[0], size[1], stars_screen)
    all_sprites = pygame.sprite.Group()
    hero = Hero(all_sprites)
    dist = 1

    enemy_sprites = pygame.sprite.Group()

    fire_sprites = pygame.sprite.Group()

    k = 0
    running = True
    while running:
        k += 1
        if k % 900 == 0:
            spawn_enemy(board, enemy_sprites)
        tick(hero)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            hero.rect.top += dist
        elif keys[pygame.K_UP]:
            hero.rect.top -= dist
        if keys[pygame.K_RIGHT]:
            hero.rect.left += dist
        elif keys[pygame.K_LEFT]:
            hero.rect.left -= dist
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(fire_sprites, hero.rect.left + 10, hero.rect.top - 20)
            if hero.rect.top < 600:
                hero.rect.top = 600
            if hero.rect.left < 0:
                hero.rect.left = 0
            if hero.rect.right > 1000:
                hero.rect.right = 1000
            if hero.rect.bottom > 1000:
                hero.rect.bottom = 1000
        if k >= 10000:
            k = 0

        stars_screen.fill((0, 0, 20))
        board.render()

        all_sprites.draw(space_screen)
        enemy_sprites.draw(space_screen)
        fire_sprites.draw(fire_screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
