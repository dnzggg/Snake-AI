import json
import random
import snake


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


gen = Genetic(15)
