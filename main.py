from random import random
import pygame
import os
import sys
from pygame.sprite import Sprite


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("spaceship2.jpg")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
size = width, height = 500, 500


class Bomb(pygame.sprite.Sprite):
    image = load_image("spaceship2.png")
    image_boom = load_image("spaceship2.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = random.randrange(height)

    def update(self, *args):
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   random.randrange(3) - 1)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


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


def main():
    size = 500, 500
    space_screen = pygame.display.set_mode(size)
    # space_screen = pygame.display.set_mode(size)

    '''создание персонажа'''
    player = Player(10, 10, size[0] // 2, 10)
    pygame.draw.circle(space_screen, (255, 0, 0), player.get_position(), 10)

    board = Board(500, 500, space_screen)
    running = True
    board.render()
    k_timer = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        k_timer += 1
        player.move(0, 10)
        board.render()
        space_screen.fill((0, 0, 0))
        # if k_timer % 5000 == 0:
        #     board.render()

        pygame.display.flip()


if __name__ == '__main__':
    main()