import random


class Solver_8_queens:
    cross_prob = 0.0
    mut_prob = 0.0
    pop_size = 0
    population = []
    best_solution = 0
    current_solution = 0

    def __init__(self, pop_size=100, cross_prob=0.6, mut_prob=0.4):
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.pop_size = pop_size
        self.get_initial_population()

    def solve(self, min_fitness=6.7, max_epochs=600):
        self.crossingover()
        self.mutation()
        epoch_num = 0
        for i in range(max_epochs):
            self.selection()
            if self.fitness(self.current_solution) > self.fitness(self.best_solution):
                self.best_solution = self.current_solution
                epoch_num = i + 1
            if self.fitness(self.current_solution) >= min_fitness:
                break
            else:
                self.crossingover()
                self.mutation()
        best_fit = self.fitness(self.best_solution)
        temp = str(self.decode(self.best_solution))
        visualization = ''
        for i in range(len(temp)):
            for j in range(len(temp)):
                if int(temp[i]) == j + 1:
                    visualization += 'Q'
                else:
                    visualization += '+'
            visualization += '\n'
        return best_fit, epoch_num, visualization

    def encode(self, individual):
        string = str(individual)
        chromosome = '0b'
        for elem in string:
            temp = bin(int(elem))[2:].zfill(4)
            chromosome += temp
        return int(chromosome, 2)

    def decode(self, chromosome):
        code = bin(chromosome)[2:].zfill(32)
        phenotype = ''
        temp = []
        count = 0
        for i in range(0, len(code), 4):
            temp.append('0b' + code[count * 4 : i + 4])
            phenotype += str(int(temp[count], 2))
            count += 1
        return int(phenotype)

    def crossingover(self):
        for i in range(len(self.population)):
            if random.random() <= self.cross_prob:
                index = random.randint(1, len(self.population) - 1)
                first_parent = self.population[i]
                second_parent = self.population[index]
                separate_point = random.randint(1, second_parent.bit_length() - 1)
                a_start = first_parent >> separate_point << separate_point
                b_start = second_parent >> separate_point << separate_point
                a_end = first_parent & (pow(2, separate_point) - 1)
                b_end = second_parent & (pow(2, separate_point) - 1)
                first_child = a_start + b_end
                second_child = b_start + a_end
                self.population[i] = first_child
                self.population[index] = second_child

    def mutation(self):
        for i in range(len(self.population)):
            if random.random() <= self.mut_prob:
                phenotype = self.population[i]
                genotype = bin(phenotype)
                gen = phenotype.bit_length() - random.randint(0, phenotype.bit_length() - 1)
                if genotype[gen + 1] == '0':
                    genotype = genotype[:gen + 1] + '1' + genotype[gen + 2:]
                else:
                    genotype = genotype[:gen + 1] + '0' + genotype[gen + 2:]
                phenotype = int(genotype, 2)
                self.population[i] = phenotype

    def fitness(self, genotype):
        fit_func = 0.0
        temp = []
        individual = self.decode(genotype)
        s = str(individual)
        for i in range(len(s)):
            temp.append(int(s[i]))
        for i in range(len(temp) - 1):
            for j in range(i + 1, len(temp)):
                diff1 = abs(temp[i] - temp[j])
                diff2 = abs(i - j)
                if diff1 != 0 and i != j:
                    fit_func += 0.12
                else:
                    fit_func -= fit_func * 0.3
                if diff1 != diff2:
                    fit_func += 0.12
                else:
                    fit_func -= fit_func * 0.3
        if len(temp) != 8:
            fit_func -= fit_func * 0.3
        for i in range(len(temp)):
            if temp[i] == 0 or temp[i] == 9:
                fit_func -= fit_func * 0.2
        return fit_func

    def selection(self):
        fit_func = []
        fit_sum = 0
        roulette_sectors = []
        max_fit = 0
        selected_population = []
        for i in range(len(self.population)):
            fit = self.fitness(self.population[i])
            if fit >= max_fit:
                max_fit = fit
                self.current_solution = self.population[i]
            fit_sum += fit
            fit_func.append(fit)
        fit_func[0] /= fit_sum
        roulette_sectors.append(fit_func[0])
        for i in range(1, len(self.population)):
            fit_func[i] /= fit_sum
            roulette_sectors.append(roulette_sectors[i - 1] + fit_func[i])
        for i in range(len(self.population)):
            rand = random.random()
            for k in range(len(self.population)):
                if rand <= roulette_sectors[k]:
                    selected_population.append(self.population[k])
                    break
        self.population = selected_population

    def get_initial_population(self):
        for i in range(self.pop_size):
            phenotype = []
            individual = ''
            for k in range(1, 9):
                phenotype.append(k)
            random.shuffle(phenotype)
            for k in range(len(phenotype)):
                individual += str(phenotype[k])
            self.population.append(self.encode(int(individual)))

