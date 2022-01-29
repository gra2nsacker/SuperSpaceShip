import os
import random
import sys
import pygame
pygame.font.init()


FIRES_ARRAY = []
SKIN = 'WHITE'
ENEMIES_ARRAY = []
SIZE = 1000, 1000
CNT = 0
LIFES = 3
TYPE_OF_LEVEL = [(0, 0, 20), (40, 10, 30)]
COLOR_INDEX = 0


def load_image(name, per_pixel_alpha=False, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if per_pixel_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    return image


class Board:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen

    def render(self):
        self.screen.fill('yellow')
        for i in range(50):
            self.screen.fill(pygame.Color('black'),
                        (random.random() * self.width,
                         random.random() * self.height, 4, 4))


class BoardShop:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen


class Fire(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("trubochka.png", True)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def move(self):
        self.rect.y -= 4

    def set_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("dgj.png", True)
        self.rect = self.image.get_rect()
        self.rect.x = SIZE[0] // 2
        self.rect.y = SIZE[1] // 2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("enemy_spaceship.png", True)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def move(self):
        self.rect.x += 2

    def set_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y


def shoot(sprite, coord_x, coord_y):
    fire = Fire(sprite)
    fire.set_coords(coord_x, coord_y)
    FIRES_ARRAY.append(fire)


def spawn_enemy(board, enemy_sprites):
    enemy = Enemy(enemy_sprites)
    enemy.rect.y = random.randint(100, board.width // 2)
    enemy.rect.x = 0
    ENEMIES_ARRAY.append(enemy)


def game_over():
    print(CNT)
    sys.exit()


def tick(hero, to_menu_screen, stars_screen):
    global ENEMIES_ARRAY, CNT
    shipes_colides = pygame.sprite.Group([ship for ship in ENEMIES_ARRAY])
    for i in FIRES_ARRAY:
        i.move()
    for ship in ENEMIES_ARRAY:
        ship.move()
        if len(pygame.sprite.spritecollide(hero, shipes_colides, False)):
            start_screen(to_menu_screen)
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
                        CNT += 1
                        level_color()
                        break


def level_color():
    global COLOR_INDEX
    if CNT > 8:
        COLOR_INDEX = 1


def score(screen):
    f1 = pygame.font.Font(None, 50)
    text1 = f1.render(f'SCORE: {CNT}', True,
                      (255, 255, 255))
    screen.blit(text1, (800, 100))


def start_screen(screen):
    all_sprites = pygame.sprite.Group()
    hero = Hero(all_sprites)
    screen2 = pygame.Surface(SIZE)
    cnt = 1
    cnt2 = 1
    hero.rect.y = SIZE[0] // 6
    fon = pygame.transform.scale(load_image('fon.jpg'), SIZE)
    screen.blit(fon, (0, 0))

    while True:
        hero.rect.x += cnt
        hero.rect.y += cnt2
        for event in pygame.event.get():
            screen2 = pygame.Surface(screen.get_size())
            if event.type == pygame.QUIT:
                game_over()
            elif 107 <= pygame.mouse.get_pos()[0] <= 230 and 810 <= pygame.mouse.get_pos()[
                1] <= 900 and event.type == pygame.MOUSEBUTTONDOWN:
                main(1)
            elif 420 <= pygame.mouse.get_pos()[0] <= 580 and 810 <= pygame.mouse.get_pos()[
                1] <= 900 and event.type == pygame.MOUSEBUTTONDOWN:
                main(2)
            elif 765 <= pygame.mouse.get_pos()[0] <= 930 and 810 <= pygame.mouse.get_pos()[
                1] <= 900 and event.type == pygame.MOUSEBUTTONDOWN:
                main(3)
        pygame.display.flip()
        if hero.rect.x >= 850:
            cnt = -1
        if hero.rect.y >= 620:
            cnt2 = -1
        if hero.rect.x <= 50:
            cnt = 1
        if hero.rect.y <= 50:
            cnt2 = 1
        screen2.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()


def main(n):
    size = SIZE
    menu_screen = pygame.display.set_mode(size)
    if n == 1:
        stars_screen = pygame.display.set_mode(size)
        space_screen = pygame.display.set_mode(size)
        fire_screen = pygame.display.set_mode(size)

        board = Board(size[0], size[1], stars_screen)
        all_sprites = pygame.sprite.Group()
        hero = Hero(all_sprites)
        dist = 2

        enemy_sprites = pygame.sprite.Group()

        fire_sprites = pygame.sprite.Group()
        sc = pygame.display.set_mode(SIZE)
        k = 0
        running = True
        while running:
            if LIFES == 0:
                game_over()
            k += 1
            if k % 300 == 0:
                spawn_enemy(board, enemy_sprites)
            tick(hero, menu_screen, stars_screen)
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
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shoot(fire_sprites, hero.rect.left + hero.rect.width // 2 - 20, hero.rect.top + hero.rect.height // 2 - 20)
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

            stars_screen.fill(TYPE_OF_LEVEL[COLOR_INDEX])
            board.render()
            score(sc)

            all_sprites.draw(space_screen)
            enemy_sprites.draw(space_screen)
            fire_sprites.draw(fire_screen)
            pygame.display.flip()

        pygame.quit()
    elif n == 2:
        stars_screen = pygame.display.set_mode(size)
        fon = pygame.transform.scale(load_image('store-fon.jpg'), SIZE)
        stars_screen.blit(fon, (0, 0))

        board = BoardShop(size[0], size[1], stars_screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print(2)
                if 696 <= pygame.mouse.get_pos()[0] <= 965 and 858 <= pygame.mouse.get_pos()[
                    1] <= 974 and event.type == pygame.MOUSEBUTTONDOWN:
                    start_screen(menu_screen)
            pygame.display.flip()
        pygame.quit()
    elif n == 3:
        stars_screen = pygame.display.set_mode(size)
        fon = pygame.transform.scale(load_image('fon.jpg'), SIZE)
        stars_screen.blit(fon, (0, 0))
        board = BoardShop(size[0], size[1], stars_screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print(2)
                if 696 <= pygame.mouse.get_pos()[0] <= 965 and 858 <= pygame.mouse.get_pos()[
                    1] <= 974 and event.type == pygame.MOUSEBUTTONDOWN:
                    start_screen(menu_screen)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    menu_screen = pygame.display.set_mode(SIZE)
    start_screen(menu_screen)
