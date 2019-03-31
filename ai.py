import json
import random
import snake
import math


class Genetic:
    def __init__(self, population):
        self.generation = 0
        self.population = population
        self.mutation_rate = 0.05

        self.neural = dict
        self.parents = []

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
            population = self.neural[str(i)]

            input_layer_to_hidden_layer = population['inputLayerToHiddenLayer']
            hidden_layer_to_output = population['hiddenLayerToOutput']

            for hidden in range(5):
                # hidden_layer_to_output[str(hidden)] = random.random()
                for inputs in range(4):
                    # input_layer_to_hidden_layer[str(inputs)][str(hidden)] = random.random()
                    pass

    def fitness(self):
        # 1 point when it gets closer to food -1.5 point when it moves away 10 points when eats food
        for i in range(self.population):

            env = snake.Environment()

            while env.cont:
                env.screen.fill((0, 0, 0))
                env.draw()
                env.look_for_input()
                env.look_for_collision()
                env.clock.tick(20)
                snake.pygame.display.flip()

    def selection(self):
        # based on fitness function
        pass

    def crossover(self):
        # from selected parents make child
        pass

    def mutation(self):
        # mutate the child with the mutation rate
        pass


class NeuralNetwork:
    def __init__(self, person):
        self.person = person
        self.neural = self.file_to_dict()[str(person)]

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

        hidden1 = input1 * input_layer_to_hidden_layer["0"]["0"] + input2 * input_layer_to_hidden_layer["1"]
        ["0"] + input3 * input_layer_to_hidden_layer["2"]["0"] + input4 * input_layer_to_hidden_layer["3"]["0"]

        hidden2 = input1 * input_layer_to_hidden_layer["0"]["1"] + input2 * input_layer_to_hidden_layer["1"]
        ["1"] + input3 * input_layer_to_hidden_layer["2"]["1"] + input4 * input_layer_to_hidden_layer["3"]["1"]

        hidden3 = input1 * input_layer_to_hidden_layer["0"]["2"] + input2 * input_layer_to_hidden_layer["1"]
        ["2"] + input3 * input_layer_to_hidden_layer["2"]["2"] + input4 * input_layer_to_hidden_layer["3"]["2"]

        hidden4 = input1 * input_layer_to_hidden_layer["0"]["3"] + input2 * input_layer_to_hidden_layer["1"]
        ["3"] + input3 * input_layer_to_hidden_layer["2"]["3"] + input4 * input_layer_to_hidden_layer["3"]["3"]

        hidden5 = input1 * input_layer_to_hidden_layer["0"]["4"] + input2 * input_layer_to_hidden_layer["1"]
        ["4"] + input3 * input_layer_to_hidden_layer["2"]["4"] + input4 * input_layer_to_hidden_layer["3"]["4"]

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


gen = Genetic(15)