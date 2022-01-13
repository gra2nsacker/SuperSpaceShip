from random import random
import pygame
from pygame.sprite import Sprite


class Player:
    def __init__(self, width, height, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def move(self, x, y):
        self.pos_x += x
        self.pos_y += y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_position(self):
        return self.pos_x, self.pos_y


class Board:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen

    def render(self):
        for i in range(200):
            self.screen.fill(pygame.Color('white'),
                        (random() * self.width,
                         random() * self.height, 1, 1))



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