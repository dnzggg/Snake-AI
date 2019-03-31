import math
import os
import random
import sys

import pygame

os.environ = [100, 10]


class Environment:
    def __init__(self, title):
        pygame.init()
        self.w, self.h = (1280, 720)
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.HWSURFACE)
        pygame.display.set_caption("Generation: " + str(title))
        self.clock = pygame.time.Clock()
        self.snake_pos = [[400, 400]]
        self.snake_length = 1
        self.previous_distance = 0
        self.cont = True
        self.food_pos = [random.randint(1, self.w / 20 - 1) * 20, random.randint(1, self.h / 20 - 1) * 20]
        self.move = "right"
        self.draw()

    def look_for_input(self):
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_F4 and alt_pressed:
                    sys.exit()
                self.game_input(event)
        self.update()

    def game_input(self, event):
        if (event.key == pygame.K_w) or (event.key == pygame.K_UP) and self.move != "down":
            self.move = "up"
        elif (event.key == pygame.K_a) or (event.key == pygame.K_LEFT) and self.move != "right":
            self.move = "left"
        elif (event.key == pygame.K_s) or (event.key == pygame.K_DOWN) and self.move != "up":
            self.move = "down"
        elif (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT) and self.move != "left":
            self.move = "right"

    def neural_input(self, output):
        if output < 0.8:
            move = "left"
        elif output < 0.9:
            move = "straight"
        else:
            move = "right"

        if self.move == "right":
            if move == "left":
                self.move = "up"
            elif move == "right":
                self.move = "down"
        elif self.move == "left":
            if move == "left":
                self.move = "down"
            elif move == "right":
                self.move = "up"
        elif self.move == "up":
            if move == "left":
                self.move = "left"
            elif move == "right":
                self.move = "right"
        elif self.move == "down":
            if move == "left":
                self.move = "left"
            elif move == "right":
                self.move = "right"

    def update(self):
        snake = self.snake_pos[0]
        if self.move == "right":
            self.snake_pos.insert(0, [snake[0] + 20, snake[1]])
        elif self.move == "left":
            self.snake_pos.insert(0, [snake[0] - 20, snake[1]])
        elif self.move == "up":
            self.snake_pos.insert(0, [snake[0], snake[1] - 20])
        elif self.move == "down":
            self.snake_pos.insert(0, [snake[0], snake[1] + 20])

        self.snake_pos = self.snake_pos[:self.snake_length]

    def draw(self):
        pos = self.snake_pos[0]
        if self.move == "up":
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0], pos[1] + 10, 20, 10))
            pygame.draw.circle(self.screen, (0, 255, 0), (pos[0] + 10, pos[1] + 10), 10)

        elif self.move == "down":
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 20, 10))
            pygame.draw.circle(self.screen, (0, 255, 0), (pos[0] + 10, pos[1] + 10), 10)

        elif self.move == "right":
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 20))
            pygame.draw.circle(self.screen, (0, 255, 0), (pos[0] + 10, pos[1] + 10), 10)

        elif self.move == "left":
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0] + 10, pos[1], 10, 20))
            pygame.draw.circle(self.screen, (0, 255, 0), (pos[0] + 10, pos[1] + 10), 10)

        for pos in self.snake_pos[1:]:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 20, 20))

        pygame.draw.ellipse(self.screen, (255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], 20, 20))

    def look_for_collision(self, neural):
        snake_pos = self.snake_pos[0]
        if snake_pos == self.food_pos:
            self.snake_length += 1
            self.food_pos = [random.randint(1, self.w / 20 - 1) * 20, random.randint(1, self.h / 20 - 1) * 20]
            neural.score += 10
        if snake_pos[0] < 0:
            self.cont = False
        elif snake_pos[0] > self.w:
            self.cont = False
        elif snake_pos[1] < 0:
            self.cont = False
        elif snake_pos[1] > self.h:
            self.cont = False
        """
        doesnt hit itself
        for index, pos in enumerate(self.snake_pos[1:]):
            if pos == snake_pos:
                self.cont = False
        """

    def position_of_snake(self):
        return self.snake_pos[-1]

    def length(self, x, y):
        return math.sqrt(x ** 2 + y ** 2)

    def distance_to(self):
        return self.length(self.snake_pos[-1][0] - self.food_pos[0], self.snake_pos[-1][1] - self.food_pos[1])

    def point_system(self, neural):
        if self.previous_distance > self.distance_to():
            neural.score += 1
        else:
            neural.score -= 1.5
        self.previous_distance = self.distance_to()


# repeats game
# env = Environment()
#
# while env.cont:
#     env.screen.fill((0, 0, 0))
#     env.draw()
#     env.look_for_input()
#     env.look_for_collision()
#     env.clock.tick(20)
#     pygame.display.flip()
