import random
import numpy as np

POPULATION_SIZE = 20

batch_courses = {1: {4, 8}, 2: {4, 3, 6, 5}, 3: {2, 1, 3}, 4: {7, 2, 5}}
course_faculty = {1: {1}, 2: {1}, 3: {2}, 4: {3}, 5: {4}, 6: {3}, 7: {4}, 8: {2}}
course_duration = {1: 10, 2: 8, 3: 4, 4: 8, 5: 8, 6: 4, 7: 10, 8: 8}
allSlots = {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [], 'Sat': []}
batch_deprecatedSlots = {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [], 'Sat': []}
day = [1, 2, 3, 4, 5]
time = [10, 11, 13, 14, 15, 16]
room = [101, 102, 201, 202]


class Gene:
    def __init__(self, batch, course, faculty, day, time):
        self.batch = batch
        self.course = course
        self.faculty = faculty
        self.day = day
        self.time = time
        #self.room = room

    def __repr__(self):
        return " - ".join([str(self.batch), str(self.course), str(self.faculty), str(self.day), str(self.time)])


class Timetable:

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def create_genome(cls):
        global batch_courses, course_faculty, course_duration, day
        temp_timetable = []
        for batch in batch_courses:
            for course in batch_courses[batch]:
                for j in range(course_duration[course]):
                    gene = Gene(batch, course, course_faculty[course], random.choice(day), random.choice(time))
                    temp_timetable.append(gene)
        # print(temp_timetable)
        return temp_timetable

    def mutated_gene(self):
        global day, time
        return random.choice(day), random.choice(time)

    def crossover(self, parent2):
        child_chromosome = []

        for gene1, gene2 in zip(self.chromosome, parent2.chromosome):
            crossover_prob = random.random()
            if crossover_prob < 0.495:
                child_chromosome.append(gene1)

            elif crossover_prob < 0.99:
                child_chromosome.append(gene2)

            # Mutation
            else:
                m_gene = self.mutated_gene()
                child_chromosome.append(Gene(gene1.batch, gene1.course, gene1.faculty, m_gene[0], m_gene[1]))

        return Timetable(child_chromosome)

    def cal_fitness(self):
        global day, time
        fitness = 0
        mat = np.zeros(shape=(len(day), len(time)), dtype='object')
        for gene in self.chromosome:
            d = day.index(gene.day)
            t = time.index(gene.time)
            if mat[d, t] == 0:
                mat[d, t] = [set(), set()]
                mat[d, t][0].add(gene.batch)
                mat[d, t][1].update(gene.faculty)
            else:
                # Batch Check
                if gene.batch in mat[d, t][0]:
                    fitness += 1
                else:
                    mat[d, t][0].add(gene.batch)

                # Faculty Check
                if not (gene.faculty.isdisjoint(mat[d, t][1])):
                    temp_set = gene.faculty.difference(mat[d, t][1])
                    fitness += (len(gene.faculty) - len(temp_set))
                    mat[d, t][1].update(temp_set)
                else:
                    mat[d, t][1].update(gene.faculty)
                # if i[5] in mat[d, t][2]:
                #     fitness += 1
                # else:
                #     mat[d, t][2].append(i[5])
        return fitness

def main():
    generation = 1
    terminate = False

    population = []
    # t = [(1, 1, 1, 2, 9, 101), (1, 1, 1, 3, 8, 201), (1, 1, 1, 2, 9, 202), (1, 1, 1, 5, 15, 202), (1, 1, 1, 4, 11, 101), (1, 1, 1, 1, 8, 201), (1, 1, 1, 1, 14, 202), (1, 1, 1, 2, 15, 101), (1, 1, 1, 1, 9, 101), (1, 1, 1, 3, 15, 102), (1, 2, 1, 4, 9, 102), (1, 2, 1, 5, 10, 202), (1, 2, 1, 4, 10, 102), (1, 2, 1, 5, 10, 201), (1, 2, 1, 4, 9, 202), (1, 2, 1, 4, 11, 102), (1, 2, 1, 3, 10, 101), (1, 2, 1, 1, 15, 201), (1, 3, 2, 5, 13, 202), (1, 3, 2, 2, 9, 101), (1, 3, 2, 1, 14, 201), (1, 3, 2, 3, 9, 101), (2, 3, 2, 5, 16, 101), (2, 3, 2, 2, 13, 202), (2, 3, 2, 2, 13, 202), (2, 3, 2, 5, 10, 201), (2, 4, 3, 3, 8, 101), (2, 4, 3, 5, 9, 102), (2, 4, 3, 3, 14, 102), (2, 4, 3, 2, 10, 202), (2, 4, 3, 4, 16, 201), (2, 4, 3, 5, 8, 102), (2, 4, 3, 1, 9, 102), (2, 4, 3, 1, 16, 102), (2, 5, 4, 3, 8, 202), (2, 5, 4, 2, 11, 202), (2, 5, 4, 1, 13, 101), (2, 5, 4, 4, 10, 102), (2, 5, 4, 2, 10, 101), (2, 5, 4, 4, 10, 201), (2, 5, 4, 1, 15, 202), (2, 5, 4, 1, 13, 101), (2, 6, 3, 2, 8, 101), (2, 6, 3, 2, 14, 102), (2, 6, 3, 2, 14, 202), (2, 6, 3, 3, 10, 101), (3, 2, 1, 5, 15, 102), (3, 2, 1, 4, 14, 101), (3, 2, 1, 2, 15, 201), (3, 2, 1, 4, 15, 102), (3, 2, 1, 5, 14, 201), (3, 2, 1, 1, 11, 201), (3, 2, 1, 2, 16, 101), (3, 2, 1, 5, 13, 101), (3, 5, 4, 4, 13, 102), (3, 5, 4, 3, 9, 102), (3, 5, 4, 1, 16, 102), (3, 5, 4, 3, 14, 201), (3, 5, 4, 5, 11, 202), (3, 5, 4, 1, 16, 201), (3, 5, 4, 5, 15, 101), (3, 5, 4, 3, 11, 201), (3, 7, 4, 5, 14, 102), (3, 7, 4, 4, 10, 202), (3, 7, 4, 4, 8, 102), (3, 7, 4, 1, 13, 202), (3, 7, 4, 1, 11, 201), (3, 7, 4, 2, 10, 202), (3, 7, 4, 4, 15, 101), (3, 7, 4, 2, 10, 101), (3, 7, 4, 5, 16, 201), (3, 7, 4, 2, 10, 101), (4, 4, 3, 3, 14, 101), (4, 4, 3, 5, 9, 201), (4, 4, 3, 1, 8, 202), (4, 4, 3, 5, 8, 201), (4, 4, 3, 2, 16, 201), (4, 4, 3, 3, 15, 201), (4, 4, 3, 3, 16, 101), (4, 4, 3, 5, 9, 102), (4, 8, 2, 2, 14, 202), (4, 8, 2, 5, 15, 101), (4, 8, 2, 1, 11, 102), (4, 8, 2, 4, 16, 102), (4, 8, 2, 3, 10, 202), (4, 8, 2, 1, 11, 102), (4, 8, 2, 4, 14, 102), (4, 8, 2, 5, 9, 102)]
    # tt = []
    # for _ in t:
    #     gene = Gene(_[0],_[1],{_[2]},_[3],_[4])
    #     tt.append(gene)
    # print(Timetable(tt).fitness)
    # print(temp)

    for _ in range(POPULATION_SIZE):
        gnome = Timetable.create_genome()
        #print(Timetable(gnome).fitness)
        population.append(Timetable(gnome))
    # print(population)

    while not terminate:

        # Sorting The Population with Increasing Order of Fitness
        population = sorted(population, key=lambda x: x.fitness)

        # Termination
        if population[0].fitness <= 0:
            terminate = True

        new_generation = []

        promotion_marker = int((20 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:promotion_marker])

        balance_filler = int((80 * POPULATION_SIZE) / 100)
        for _ in range(balance_filler):
            parent1 = random.choice(population[:10])
            parent2 = random.choice(population[:10])
            child = parent1.crossover(parent2)
            new_generation.append(child)

        population = new_generation

        generation += 1
        # generations.append(generation)
        # fitness_rec.append(population[0].fitness)
        # if generation > 1 :
        # 	break
        print("generation : ", generation)
        print("fitness : ", population[0].fitness)
    for _ in population[0].chromosome:
        print(_)


if __name__ == '__main__':
    main()
