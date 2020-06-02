import random

import numpy as np

from model import *

POPULATION_SIZE = 25

day = [1, 2, 3, 4, 5, 6]
time = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6]
lower_cross_prob = 0.40
higher_cross_prob = 0.95


class Gene:
    def __init__(self, data, gene_day, gene_time):
        self.data = data
        self.time = gene_time
        self.day = gene_day


class Timetable:

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.collisions, self.data_matrix = self.get_data_matrix_collisions()

    @staticmethod
    def create_genome(data):
        global day, time
        temp_timetable = []
        for _ in data:
            d = _.duration
            f = _.frequency
            for j in range(f):
                new_gene = Timetable.get_new_gene(_)
                temp_timetable.append(new_gene)
        return temp_timetable

    @staticmethod
    def get_new_gene(_):
        global day, time
        d = _.duration
        if _.is_pseudo:
            if _.is_jnr:
                gene = Gene(_, random.choice(day), (time[-1] - 1) - d + 1)
            else:
                gene = Gene(_, random.choice(day), (time[-1]) - d + 1)
            return gene
        if _.is_compound:
            if _.is_jnr:  # TODO: Remove Static List And Make it Dynamic
                gene = Gene(_, random.choice(day), random.choice([1, 2, 4, 5]) - 1)
            else:
                gene = Gene(_, random.choice(day), random.choice([1, 2, 4, 5]))
            return gene

        if _.is_lab:
            _.room = set()
            for c in _.course:
                _.room.add(random.choice(c.preferred_rooms))
            if _.is_jnr:
                gene = Gene(_, random.choice(day), random.choice([0, 3]))
            else:
                gene = Gene(_, random.choice(day), random.choice([1, 4]))
            return gene

        if not _.is_lab and not _.is_compound:
            if _.is_jnr:
                gene = Gene(_, random.choice(day), random.choice(time) - 1)
            else:
                gene = Gene(_, random.choice(day), random.choice(time))
            return gene

    def crossover(self, parent2):
        child_chromosome = []

        for gene1, gene2 in zip(self.chromosome, parent2.chromosome):
            crossover_prob = random.random()
            if crossover_prob < lower_cross_prob:
                child_chromosome.append(gene1)

            elif crossover_prob < higher_cross_prob:
                child_chromosome.append(gene2)

            # Mutation
            else:
                m_gene = Timetable.get_new_gene(gene1.data)
                child_chromosome.append(m_gene)

        return Timetable(child_chromosome)

    def get_data_matrix_collisions(self):
        global day, time
        batch_collision = 0
        faculty_collision = 0
        room_collision = 0
        mat = np.zeros(shape=(len(day) + 1, len(set(time)) + 1), dtype='object')
        for gene in self.chromosome:
            d = gene.day
            t = gene.time
            for _ in range(gene.data.duration):
                if mat[d, t] == 0:
                    mat[d, t] = [set(), set(), set()]
                    if gene.data.batch_check:
                        mat[d, t][0].update(gene.data.batch)
                    if gene.data.faculty_check:
                        mat[d, t][1].update(gene.data.faculty)
                    if gene.data.room_check:
                        mat[d, t][2].update(gene.data.room)
                else:
                    # Section Check
                    if gene.data.batch_check:
                        if not (gene.data.batch.isdisjoint(mat[d, t][0])):
                            temp_set = gene.data.batch.difference(mat[d, t][0])
                            batch_collision += (len(gene.data.batch) - len(temp_set))
                            mat[d, t][0].update(temp_set)
                        else:
                            mat[d, t][0].update(gene.data.batch)

                    # Faculty Check
                    if gene.data.faculty_check:
                        if not (gene.data.faculty.isdisjoint(mat[d, t][1])):
                            temp_set = gene.data.faculty.difference(mat[d, t][1])
                            faculty_collision += (len(gene.data.faculty) - len(temp_set))
                            mat[d, t][1].update(temp_set)
                        else:
                            mat[d, t][1].update(gene.data.faculty)

                    # Room Check
                    if gene.data.room_check:
                        if not (gene.data.room.isdisjoint(mat[d, t][2])):
                            temp_set = gene.data.room.difference(mat[d, t][2])
                            room_collision += (len(gene.data.room) - len(temp_set))
                            mat[d, t][2].update(temp_set)
                        else:
                            mat[d, t][2].update(gene.data.room)
                t += 1
        # print('batch_collision: ' + str(batch_collision) + ' faculty_collision: ' + str(faculty_collision) + ' room_collision: ' + str(room_collision))
        return (batch_collision + faculty_collision + room_collision), mat

    def print_test(self):
        global day, time
        dic = {}
        for gene in self.chromosome:
            dic.setdefault(str(gene.data.batch), np.zeros(shape=(len(day) + 1, len(set(time)) + 1), dtype='object'))
            d = gene.day
            t = gene.time
            dur = gene.data.duration
            for _ in range(dur):
                dic[str(gene.data.batch)][d, t] = str(gene.data.course) + "-" + str(gene.data.room)
                t += 1
        for _ in dic:
            print(_, dic[_])
            print()
        return dic

    # Removing Pseudo Data and Saving "data" into Data Object
#     def save(self):
#         for gene in self.chromosome:
#             if gene.data.is_pseudo:


#             gene.data.slots.append((gene.day, gene.time))


    def swap(self, batch, first, second):
        global day, time
        col, mat = self.get_data_matrix_collisions()
        for gene in self.chromosome:
            if gene.data.batch == {batch} and ((gene.day, gene.time) == first):
                tg1 = gene
            if gene.data.batch == {batch} and ((gene.day, gene.time) == second):
                tg2 = gene
        d1 = tg1.data.duration
        d2 = tg2.data.duration
        # faculty
        if (d1 == d2 and tg2.data.faculty.isdisjoint(
                mat[first[0], first[1]][1] - tg1.data.faculty) and tg1.data.faculty.isdisjoint(
                mat[second[0], second[1]][1] - tg2.data.faculty)):
            if (d1 == 3 and tg2.room.isdisjoint(mat[first[0], first[1]][2] - tg1.room) and tg1.room.isdisjoint(
                    mat[second[0], second[1]][2] - tg2.room)):
                print("Swap successful - Lab")
                tg1.day, tg1.time, tg2.day, tg2.time = tg2.day, tg2.time, tg1.day, tg1.time
                return
            else:
                print("Swap successful ")
                tg1.day, tg1.time, tg2.day, tg2.time = tg2.day, tg2.time, tg1.day, tg1.time
                return
        print("Un successful Swap")


def initiation():
    course_list = []
    professor_list = []
    batch_list = []

    open_elective = ['OE', 'OE', 'OE']
    lectures = ['18PC1CS03', 'Software Engineering', 'SE',
                '18PC1IT03', 'Java Programming', 'JP', '18PC1IT04', 'Formal Languages and Automata Theory', 'FLAT',
                '18PC1CS04', 'Design and Analysis of Algorithms', 'DAA', '18PC1CS05', 'Database Management Systems',
                'DBMS']
    lab = ['18PC2IT02', 'Java Programming Laboratory', 'JAVA LAB', '18PC2CS02',
           'Database Management Systems Laboratory', 'DBMS LAB', '18PC2IT03', 'IT Workshop', 'ITWS']

    labs_room_choices = [['A 109', 'P 203'], ['B 315', 'B 317'], ['P 403']]

    for _ in range(0, len(open_elective), 3):
        c = Course()
        c.create_lecture(open_elective[_], open_elective[_ + 1], open_elective[_ + 2], 2, 2)
        course_list.append(c)
    for _ in range(0, len(lectures), 3):
        c = Course()
        c.create_lecture(lectures[_], lectures[_ + 1], lectures[_ + 2], 1, 4)
        course_list.append(c)
    for _ in range(0, len(lab), 3):
        c = Course()
        c.create_lab_course(lab[_], lab[_ + 1], lab[_ + 2], labs_room_choices[_ // 3])
        course_list.append(c)

    # print(course_list, len(course_list))

    prof = ['Dr.C.Kiran Mai', 'M.Gangappa', 'A.Kousar Nikhath', 'N.V.Sailaja', 'Chenna Basamma', 'Dr.K.Srinivas',
            'G.S.Ramesh', 'P.Bharath Kumar', 'Y.Bhanu Sree', 'Dr.M.Rajasekar', 'P.Radhika', 'A.Kousar Nikath',
            'Priyanka Singh', 'P.Rama Krishna', 'A.Madhavi', 'S.Swapna', 'G.Nagaraju', 'M.Venkata Krishna Rao',
            'Dr.A.Brahmananda Reddy', 'Priyanka singh', 'K.Bheema Lingappa', 'T.Gnana Prakash', 'R.Vijaya Saraswathi',
            'Dr.Y.Sagar', 'DR.K.MURALI KRISHNA', 'Priya Bhatnagar']

    for i, _ in enumerate(prof):
        t = Professor('CSE', i, _)
        professor_list.append(t)
    # print(professor_list, len(professor_list))

    b_room = ['R1', 'R2', 'R3', 'R4']
    for _ in range(4):
        t = Batch('CSE', 3, _ + 1, b_room[_], False)
        batch_list.append(t)
    # print(batch_list, len(batch_list))

    data = [
        Data().create_compound_data({batch_list[0], batch_list[1]}, {course_list[0]}),
        Data().create_lecture_data({batch_list[0]}, {course_list[1]}, {professor_list[7]}),
        Data().create_lecture_data({batch_list[0]}, {course_list[2]}, {professor_list[14]}),
        Data().create_lecture_data({batch_list[0]}, {course_list[3]}, {professor_list[16]}),
        Data().create_lecture_data({batch_list[0]}, {course_list[4]}, {professor_list[4]}),
        Data().create_lecture_data({batch_list[0]}, {course_list[5]}, {professor_list[3]}),
        Data().create_lab_data({batch_list[0]}, {course_list[6], course_list[7]},
                               {professor_list[14], professor_list[15], professor_list[3], professor_list[11]}, 3,
                               1),
        Data().create_lab_data({batch_list[0]}, {course_list[6], course_list[8]},
                               {professor_list[14], professor_list[15], professor_list[21], professor_list[20]}, 3, 1),
        Data().create_lab_data({batch_list[0]}, {course_list[7], course_list[8]},
                               {professor_list[3], professor_list[11], professor_list[21], professor_list[20]}, 3, 1),
        Data().create_pseudo_data({batch_list[0]}, 1, 3),

        # Data().create_compound_data({batch_list[1], batch_list[1]}, {course_list[0]}),
        Data().create_lecture_data({batch_list[1]}, {course_list[1]}, {professor_list[13]}),
        Data().create_lecture_data({batch_list[1]}, {course_list[2]}, {professor_list[10]}),
        Data().create_lecture_data({batch_list[1]}, {course_list[3]}, {professor_list[9]}),
        Data().create_lecture_data({batch_list[1]}, {course_list[4]}, {professor_list[8]}),
        Data().create_lecture_data({batch_list[1]}, {course_list[5]}, {professor_list[23]}),
        Data().create_lab_data({batch_list[1]}, {course_list[6], course_list[7]},
                               {professor_list[10], professor_list[25], professor_list[23], professor_list[8]}, 3,
                               1),
        Data().create_lab_data({batch_list[1]}, {course_list[6], course_list[8]},
                               {professor_list[10], professor_list[25], professor_list[12], professor_list[17]}, 3, 1),
        Data().create_lab_data({batch_list[1]}, {course_list[7], course_list[8]},
                               {professor_list[23], professor_list[8], professor_list[12], professor_list[17]}, 3, 1),
        Data().create_pseudo_data({batch_list[1]}, 1, 3),

    ]
    # print(data, len(data))
    return batch_list, professor_list, course_list, data


def scheduler():
    batch_list, professor_list, course_list, data = initiation()
    # print(batch_list, professor_list, course_list, data)

    # Start
    generation = 1
    terminate = False
    population = []

    for _ in range(POPULATION_SIZE):
        gnome = Timetable.create_genome(data)
        population.append(Timetable(gnome))

    while not terminate:

        # Sorting The Population with Increasing Order of Collisions
        population = sorted(population, key=lambda x: x.collisions)

        # Termination
        if population[0].collisions == 0:
            population[0].print_test()
            #Timetable.save(population[0])
            a, b, c, d = map(int, input().split())
            # Static Swap Function call in First Batch
            population[0].swap(batch_list[0], (a, b), (c, d))
            population[0].print_test()
            terminate = True
            # TODO: Start Here Data Updating in Data Objects
            break

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
        print("generation No : ", generation)
        print("Collisions : ", population[0].collisions)
