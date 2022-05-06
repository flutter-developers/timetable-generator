from tkinter import *
import numpy as np
import random

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
                print('\n#################################################################')
                print('course id === ', c.course_id)
                print('course room === ', c.preferred_rooms)
                print('#################################################################\n')
                preferred_rooms = c.preferred_rooms.split(", ")
                _.room.add(random.choice(preferred_rooms))
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
            dic.setdefault(str(gene.data.batch), np.zeros(shape=(len(day)+1, len(set(time)) + 1), dtype='object'))
            d = gene.day
            t = gene.time
            dur = gene.data.duration
            for _ in range(dur):
                dic[str(gene.data.batch)][d, t] = "\n".join([str(gene.data.course),str(gene.data.room)])
                t += 1
            for _ in range(7):
                dic[str(gene.data.batch)][0, _] = str('Slot: ')+str(_+1)

        # for _ in dic:
        #     print(_, dic[_])
        #     print()
        return dic

    # # Removing Pseudo Data and Saving "data" into Data Object
    def save(self):
        for gene in self.chromosome:
            if gene.data.is_pseudo:
                gene.data.slots.append((gene.day, gene.time))

    def swap(self, batch, first, second):
        try:
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
        except:
            print("Un successful Swap")