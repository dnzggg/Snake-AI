import math

from Neural_network import NeuralNetwork
import numpy as np
import snake
import random


class Genetic:
    def __init__(self, population, generation):
        self.generation = generation
        self.population = population
        self.mutation_rate = 0.05

        self.neural = dict
        self.neural_networks = []

        self.create_population()

    def create_population(self) -> None:
        for x in range(self.population):
            self.neural_networks.append(NeuralNetwork(np.array([[1, 1, 1, 1]]), np.array([1])))
        self.fitness()

    def fitness(self) -> None:
        self.generation += 1
        # 1 point when it gets closer to food -1.5 point when it moves away 10 points when eats food
        for neural in self.neural_networks:
            env = snake.Environment(self.generation)

            while env.cont:
                env.screen.fill((0, 0, 0))
                env.draw()
                env.look_for_input()

                env.look_for_collision(neural)
                env.point_system(neural)

                inputs = self.calculate_input(env)
                neural.setInput(np.array(inputs))
                neural.feed_forward()
                output = neural.output
                env.neural_input(output)
                print(output)
                # print(neural.score)

                env.clock.tick(20)
                snake.pygame.display.flip()

        self.selection()

    def selection(self) -> None:
        # based on fitness function
        n = parents = self.neural_networks

        best = max(n, key=lambda item: item.score)
        for x in range(5):
            n.remove(best)
            parents.append(best)

        best2 = max(n, key=lambda item: item.score)
        for x in range(3):
            parents.append(best2)

        self.neural_networks = []
        for x in range(self.population):
            parent1, parent2 = random.sample(parents, 2)
            self.neural_networks.append(self.crossover(parent1, parent2))

        self.fitness()

    def crossover(self, p1, p2) -> NeuralNetwork:
        # from selected parents make child
        size = p1.w1.shape
        child = NeuralNetwork(np.array([[1, 1, 1, 1]]), np.array([1]))

        for x in range(size[0]):
            for y in range(size[1]):
                if not self.mutate():
                    if random.randint(0, 1) == 0:
                        child.w1[x][y] = p1.w1[x][y]
                    else:
                        child.w1[x][y] = p2.w1[x][y]

        size = p1.w2.shape
        for x in range(size[0]):
            for y in range(size[1]):
                if not self.mutate():
                    if random.randint(0, 1) == 0:
                        child.w2[x][y] = p1.w2[x][y]
                    else:
                        child.w2[x][y] = p2.w2[x][y]
        return child

    def mutate(self):
        # mutate the child with the mutation rate
        if random.random() < self.mutation_rate:
            return True
        else:
            return False

    @staticmethod
    def calculate_input(env):
        right_input = 0
        left_input = 0
        front_input = 0

        if env.move == 'up':
            if env.food_pos[1] == env.position_of_snake()[1]:
                if env.food_pos[0] > env.position_of_snake()[0]:
                    right_input = 1
                elif env.food_pos[0] < env.position_of_snake()[0]:
                    left_input = 1
            elif env.food_pos[0] == env.position_of_snake()[0]:
                if env.food_pos[1] < env.position_of_snake()[1]:
                    front_input = 1
        elif env.move == 'down':
            if env.food_pos[1] == env.position_of_snake()[1]:
                if env.food_pos[0] > env.position_of_snake()[0]:
                    left_input = 1
                elif env.food_pos[0] < env.position_of_snake()[0]:
                    right_input = 1
            elif env.food_pos[0] == env.position_of_snake()[0]:
                if env.food_pos[1] > env.position_of_snake()[1]:
                    front_input = 1
        elif env.move == 'right':
            if env.food_pos[0] == env.position_of_snake()[0]:
                if env.food_pos[1] > env.position_of_snake()[1]:
                    right_input = 1
                elif env.food_pos[1] < env.position_of_snake()[1]:
                    left_input = 1
            elif env.food_pos[1] == env.position_of_snake()[1]:
                if env.food_pos[0] > env.position_of_snake()[0]:
                    front_input = 1
        elif env.move == 'left':
            if env.food_pos[0] == env.position_of_snake()[0]:
                if env.food_pos[1] > env.position_of_snake()[1]:
                    left_input = 1
                elif env.food_pos[1] < env.position_of_snake()[1]:
                    right_input = 1
            elif env.food_pos[1] == env.position_of_snake()[1]:
                if env.food_pos[0] < env.position_of_snake()[0]:
                    front_input = 1

        angle_input = math.atan2(env.food_pos[1] - env.position_of_snake()[1],
                                 env.food_pos[0] - env.position_of_snake()[0])
        angle_input = math.degrees(angle_input)
        angle_input /= 180

        return [right_input, left_input, front_input, angle_input]


gen = Genetic(30, 0)
