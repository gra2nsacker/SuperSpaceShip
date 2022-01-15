import os
import random
import pygame


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
                         random.random() * self.height, 1, 1))


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("spaceship_hero.png")
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 800


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100


def Fire(screen, left, top):
    pygame.draw.rect(screen, "YELLOW", (left, top, 10, 200))


def main():
    size = 1000, 1000
    space_screen = pygame.display.set_mode(size)
    board = Board(1000, 1000, space_screen)

    all_sprites = pygame.sprite.Group()
    hero = Hero(all_sprites)
    dist = 10

    enemy_sprites = pygame.sprite.Group()
    enemy = Enemy(enemy_sprites)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                hero.rect.top += dist
            elif key[pygame.K_UP]:
                hero.rect.top -= dist
            if key[pygame.K_RIGHT]:
                hero.rect.left += dist
            elif key[pygame.K_LEFT]:
                hero.rect.left -= dist
            if key[pygame.K_SPACE]:
                Fire(space_screen,  hero.rect.left, hero.rect.top)
            if hero.rect.top < 600:
                hero.rect.top = 600
            if hero.rect.left < 0:
                hero.rect.left = 0
            if hero.rect.right > 1000:
                hero.rect.right = 1000
            if hero.rect.bottom > 1000:
                hero.rect.bottom = 1000
        space_screen.fill((0, 0, 20))
        board.render()
        all_sprites.draw(space_screen)
        enemy_sprites.draw(space_screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
