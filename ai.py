import json
import random
import snake
import math


# a

class Genetic:
    def __init__(self, population, generation):
        self.generation = generation
        self.population = population
        self.mutation_rate = 0.05

        self.neural = dict
        self.neurals = []

        self.create_population()

    @staticmethod
    def file_to_dict():
        neural_file = open("neurals.json")
        return json.loads(neural_file.read())

    @staticmethod
    def dict_to_file(dictionary):
        with open("neurals.json", "w") as f:
            json.dump(dictionary, f, indent=4)

    def create_population(self):
        self.neural = self.file_to_dict()

        for i in range(self.population):
            self.neurals.append(NeuralNetwork(i))

            # running for the first time
            # population = self.neural[str(i)]
            # input_layer_to_hidden_layer = population['inputLayerToHiddenLayer']
            # hidden_layer_to_output = population['hiddenLayerToOutput']
            #
            # for hidden in range(5):
            #     # hidden_layer_to_output[str(hidden)] = random.random()
            #     for inputs in range(4):
            #         # input_layer_to_hidden_layer[str(inputs)][str(hidden)] = random.random()
            #         pass

        self.fitness()

    def fitness(self):
        # 1 point when it gets closer to food -1.5 point when it moves away 10 points when eats food
        for neural in self.neurals:

            env = snake.Environment(self.generation)

            while env.cont:
                env.screen.fill((0, 0, 0))
                env.draw()
                env.look_for_input()

                env.look_for_collision(neural)
                env.point_system(neural)

                inputs = self.calculate_input(env)
                output = neural.calculate_output(inputs)
                env.neural_input(output)

                env.clock.tick(20)
                snake.pygame.display.flip()

        self.selection()

    def selection(self):
        # based on fitness function
        neural = self.neural
        n = parents = self.neurals

        for i in range(2):
            best = max(n, key=lambda item: item.score)
            parents.append(best)
            parents.append(best)
            parents.append(best)
            parents.append(best)
            n.remove(best)
        for i in range(4):
            best = max(n, key=lambda item: item.score)
            parents.append(best)
            parents.append(best)
            n.remove(best)

        for i in range(self.population):
            parent1, parent2 = random.sample(parents, 2)
            self.crossover(i, neural, parent1, parent2)

        self.neural = neural
        self.dict_to_file(self.neural)

    def crossover(self, i, neural, p1, p2):
        # from selected parents make child
        parent1_neural = self.neural[str(p1.person)]
        parent2_neural = self.neural[str(p2.person)]
        child = neural[str(i)]

        p1_input_layer_to_hidden_layer = parent1_neural['inputLayerToHiddenLayer']
        p1_hidden_layer_to_output = parent1_neural['hiddenLayerToOutput']

        p2_input_layer_to_hidden_layer = parent2_neural['inputLayerToHiddenLayer']
        p2_hidden_layer_to_output = parent2_neural['hiddenLayerToOutput']

        c_input_layer_to_hidden_layer = child['inputLayerToHiddenLayer']
        c_hidden_layer_to_output = child['hiddenLayerToOutput']

        for hidden in range(5):
            if not self.mutate():
                if random.randint(0, 1) == 0:
                    c_hidden_layer_to_output[str(hidden)] = p1_hidden_layer_to_output[str(hidden)]
                else:
                    c_hidden_layer_to_output[str(hidden)] = p2_hidden_layer_to_output[str(hidden)]
            else:
                c_hidden_layer_to_output[str(hidden)] = random.random()
            for inputs in range(4):
                if not self.mutate():
                    if random.randint(0, 1) == 0:
                        c_input_layer_to_hidden_layer[str(inputs)][str(hidden)] = \
                            p1_input_layer_to_hidden_layer[str(inputs)][str(hidden)]
                    else:
                        c_input_layer_to_hidden_layer[str(inputs)][str(hidden)] = \
                            p2_input_layer_to_hidden_layer[str(inputs)][str(hidden)]
                else:
                    c_input_layer_to_hidden_layer[str(inputs)][str(hidden)] = random.random()

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


class NeuralNetwork:
    def __init__(self, person):
        self.person = person
        self.neural = self.file_to_dict()[str(person)]
        self.score = 0

    @staticmethod
    def file_to_dict():
        neural_file = open("neurals.json")
        return json.loads(neural_file.read())

    @staticmethod
    def dict_to_file(dictionary):
        with open("neurals.json", "w") as f:
            json.dump(dictionary, f, indent=4)

    @staticmethod
    def sigmoid(value):
        new_value = 1 / (1 + math.e ** -value)
        return new_value

    def calculate_output(self, inputs):
        input1 = inputs[0]
        input2 = inputs[1]
        input3 = inputs[2]
        input4 = inputs[3]

        input_layer_to_hidden_layer = self.neural['inputLayerToHiddenLayer']

        hidden1 = input1 * input_layer_to_hidden_layer["0"]["0"] + input2 * input_layer_to_hidden_layer["1"][
            "0"] + input3 * input_layer_to_hidden_layer["2"]["0"] + input4 * input_layer_to_hidden_layer["3"]["0"]

        hidden2 = input1 * input_layer_to_hidden_layer["0"]["1"] + input2 * input_layer_to_hidden_layer["1"][
            "1"] + input3 * input_layer_to_hidden_layer["2"]["1"] + input4 * input_layer_to_hidden_layer["3"]["1"]

        hidden3 = input1 * input_layer_to_hidden_layer["0"]["2"] + input2 * input_layer_to_hidden_layer["1"][
            "2"] + input3 * input_layer_to_hidden_layer["2"]["2"] + input4 * input_layer_to_hidden_layer["3"]["2"]

        hidden4 = input1 * input_layer_to_hidden_layer["0"]["3"] + input2 * input_layer_to_hidden_layer["1"][
            "3"] + input3 * input_layer_to_hidden_layer["2"]["3"] + input4 * input_layer_to_hidden_layer["3"]["3"]

        hidden5 = input1 * input_layer_to_hidden_layer["0"]["4"] + input2 * input_layer_to_hidden_layer["1"][
            "4"] + input3 * input_layer_to_hidden_layer["2"]["4"] + input4 * input_layer_to_hidden_layer["3"]["4"]

        sigmoid_hidden1 = self.sigmoid(hidden1)
        sigmoid_hidden2 = self.sigmoid(hidden2)
        sigmoid_hidden3 = self.sigmoid(hidden3)
        sigmoid_hidden4 = self.sigmoid(hidden4)
        sigmoid_hidden5 = self.sigmoid(hidden5)

        hidden_layer_to_output = self.neural['hiddenLayerToOutput']

        sum_of_output = sigmoid_hidden1 * hidden_layer_to_output["0"] + sigmoid_hidden2 * hidden_layer_to_output[
            "1"] + sigmoid_hidden3 * hidden_layer_to_output["2"] + sigmoid_hidden4 * hidden_layer_to_output[
                            "3"] + sigmoid_hidden5 * hidden_layer_to_output["4"]

        output = self.sigmoid(sum_of_output)

        return output


for i in range(1000):
    print("Generation: " + str(i))
    gen = Genetic(15, i)
