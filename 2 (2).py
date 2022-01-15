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


class Hero():
    def __init__(self):
        all_sprites = pygame.sprite.Group()
        hero_image = load_image("spaceship2.jpg")
        hero = pygame.sprite.Sprite(all_sprites)
        hero.image = hero_image
        hero.rect = hero.image.get_rect()


def main():
    size = 1000, 1000
    space_screen = pygame.display.set_mode(size)
    board = Board(1000, 1000, space_screen)


    dist = 10

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
        space_screen.fill((0, 0, 20))
        board.render()
        all_sprites.draw(space_screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
