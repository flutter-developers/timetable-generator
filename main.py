import random
import numpy as np

POPULATION_SIZE = 20

# batch_courses = {1: {4, 8}, 2: {4, 3, 6, 5}, 3: {2, 1, 3}, 4: {7, 2, 5}}
# course_faculty = {1: {1}, 2: {1}, 3: {2}, 4: {3}, 5: {4}, 6: {3}, 7: {4}, 8: {2}}
# course_duration = {1: 10, 2: 8, 3: 4, 4: 8, 5: 8, 6: 4, 7: 10, 8: 8}
allSlots = {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [], 'Sat': []}
batch_deprecatedSlots = {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [], 'Sat': []}
day = [1, 2, 3, 4, 5, 6]
time = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6]
room = [101, 102, 201, 202]
batch_courses = {1: {4}, 2: {4}, 3: {4}}  # 2: {5}, 3: {2, 1, 3}, 4: {7, 2, 5}}
labs = ['A 109', 'P 203', 'B 315', 'B 317', 'P 403', 'P 404', 'P 410']
course_faculty = {1: {1}, 2: {1}, 3: {2, 3, 4}, 4: {3}, 5: {4}, 6: {3}, 7: {4}, 8: {2}}
course_duration = {1: (5, 1), 2: (5, 1), 3: (5, 1), 4: (3, 3), 5: (2, 2), 6: (5, 1), 7: (5, 1), 8: (5, 1)}


class Professor:
    def __init__(self, department, professor_id, professor_name, associated_courses):
        self.professor_id = professor_id
        self.professor_name = professor_name
        self.department = department
        self.associated_courses = associated_courses


class Course:
    def __init__(self, course_id, course_name, course_type, duration, frequency):
        self.course_id = course_id
        self.course_name = course_name
        self.course_type = course_type
        self.duration = duration
        self.frequency = frequency

    def __repr__(self):
        return str(self.course_name)


class Batch:
    def __init__(self, branch, year, section, class_coordinator):
        self.branch = branch
        self.year = year
        self.section = section
        self.class_coordinator = class_coordinator

    def __repr__(self):
        return str(self.year) + "-" + str(self.section)


class Gene:
    def __init__(self, batch, course, faculty, day, time, room):
        self.batch = batch
        self.course = course
        self.faculty = faculty
        self.day = day
        self.time = time
        self.room = room

    def __repr__(self):
        return str([self.batch,
                    self.course,
                    self.faculty,
                    self.day,
                    self.time,
                    self.room])


class Data:
    def __init__(self, batch, course, faculty, slots, room):
        self.batch = batch
        self.course = course
        self.faculty = faculty  # List Or Single []
        self.slots = slots  # [(),(),()]
        self.room = room  # Room (B-314)


class Timetable:

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def create_genome(cls, data):
        global batch_courses, course_faculty, course_duration, day
        temp_timetable = []
        for _ in data:
            t = list(_.course)[0].frequency
            d = list(_.course)[0].duration
            for j in range(t):
                if d == 2:
                    gene = Gene(_.batch, _.course, _.faculty, random.choice(day),
                                random.choice([1, 2, 4, 5]), "OE")
                elif d == 3:
                    gene = Gene(_.batch, _.course, _.faculty, random.choice(day),
                                random.choice([1, 4]), set(random.sample(labs, 2)))
                else:
                    gene = Gene(_.batch, _.course, _.faculty, random.choice(day),
                                random.choice(time),
                                _.room)
                temp_timetable.append(gene)
        print(temp_timetable, len(temp_timetable))
        return temp_timetable

    def mutated_gene(self, duration):
        global day, time
        if duration == 2:
            return random.choice(day), random.choice([1, 2, 4, 5])
        elif duration == 3:
            return set(random.sample(labs, 2)), random.choice(day), random.choice([1,1,1,1,1,4,4,4])
        else:
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
                dur = list(gene1.course)[0].duration
                m_gene = self.mutated_gene(dur)
                if (dur == 3):
                    child_chromosome.append(
                        Gene(gene1.batch, gene1.course, gene1.faculty, m_gene[1], m_gene[2], m_gene[0]))
                else:
                    child_chromosome.append(
                        Gene(gene1.batch, gene1.course, gene1.faculty, m_gene[0], m_gene[1], gene1.room))

        return Timetable(child_chromosome)

    def cal_fitness(self):
        global day, time
        fitness = 0
        mat = np.zeros(shape=(len(day) + 1, len(set(time)) + 1), dtype='object')
        for gene in self.chromosome:
            d = gene.day
            t = gene.time
            g = set()
            g.update(gene.batch)
            dur = list(gene.course)[0].duration
            for _ in range(dur):
                if mat[d, t] == 0:
                    mat[d, t] = [set(), set(), set()]
                    mat[d, t][0].update(g)
                    mat[d, t][1].update(gene.faculty)
                    if (dur == 3):
                        mat[d, t][2].update(gene.room)
                else:
                    # Section Check
                    if not (g.isdisjoint(mat[d, t][0])):
                        temp_set = g.difference(mat[d, t][0])
                        if(len(g) == 2):
                            print("==="+ str(mat[d,t][0])
                                  +"===")
                        fitness += (len(g) - len(temp_set))
                        mat[d, t][0].update(temp_set)
                    else:
                        mat[d, t][0].update(g)

                    # Faculty Check
                    if not (gene.faculty.isdisjoint(mat[d, t][1])):
                        temp_set = gene.faculty.difference(mat[d, t][1])
                        fitness += (len(gene.faculty) - len(temp_set))
                        mat[d, t][1].update(temp_set)
                    else:
                        mat[d, t][1].update(gene.faculty)

                    # Room Check
                    if (dur == 3):
                        # print(gene.room)
                        if not (gene.room.isdisjoint(mat[d, t][2])):
                            temp_set = gene.room.difference(mat[d, t][2])
                            fitness += (len(gene.room) - len(temp_set))
                            mat[d, t][2].update(temp_set)
                        else:
                            mat[d, t][2].update(gene.room)
                t += 1
        return fitness

    def print_test(self):
        global day, time
        dic = {}
        for gene in self.chromosome:
            dic.setdefault(str(gene.batch), np.zeros(shape=(len(day) + 1, len(set(time)) + 1), dtype='object'))
            d = gene.day
            t = gene.time
            dur = list(gene.course)[0].duration
            for _ in range(dur):
                dic[str(gene.batch)][d, t] = str(gene.course) + "-" + str(gene.room)
                t += 1
        for _ in dic:
            print(_, dic[_])
            print()
        return dic

    def swap(self, batch, first, second):
        global day, time
        mat = np.zeros(shape=(len(day) + 1, len(time) + 1), dtype='object')
        for gene in self.chromosome:
            d = gene.day
            t = gene.time
            g = set()
            g.update(gene.batch)
            dur = list(gene.course)[0].duration
            for _ in range(dur):
                if mat[d, t] == 0:
                    mat[d, t] = [set(), set(), set()]
                    mat[d, t][0].update(g)
                    mat[d, t][1].update(gene.faculty)
                    if (dur == 3):
                        mat[d, t][2].update(gene.room)
                else:
                    # Batch Check
                    if not (g.isdisjoint(mat[d, t][0])):
                        temp_set = g.difference(mat[d, t][0])
                        mat[d, t][0].update(temp_set)
                    else:
                        mat[d, t][0].update(g)

                    # Faculty Check
                    if (len(gene.batch) >= 2):
                        continue
                    if not (gene.faculty.isdisjoint(mat[d, t][1])):
                        temp_set = gene.faculty.difference(mat[d, t][1])
                        mat[d, t][1].update(temp_set)
                    else:
                        mat[d, t][1].update(gene.faculty)
                    # Room Check
                    if (dur == 3):
                        # print(gene.room)
                        if not (gene.room.isdisjoint(mat[d, t][2])):
                            temp_set = gene.room.difference(mat[d, t][2])
                            mat[d, t][2].update(temp_set)
                        else:
                            mat[d, t][2].update(gene.room)
                t += 1
        # dic = {}
        # for gene in self.chromosome:
        #     dic.setdefault(str(gene.batch), [])
        #     dic[str(gene.batch)].append(gene)
        # for _ in dic:
        #     print(_, dic[_])
        #     print()
        for gene in self.chromosome:
            if (gene.batch == {batch} and ((gene.day, gene.time) == first)):
                tg1 = gene
            if (gene.batch == {batch} and ((gene.day, gene.time) == second)):
                tg2 = gene
        d1 = list(tg1.course)[0].duration
        d2 = list(tg2.course)[0].duration
        # faculty
        if (d1 == d2 and tg2.faculty.isdisjoint(mat[first[0], first[1]][1] - tg1.faculty) and tg1.faculty.isdisjoint(
                mat[second[0], second[1]][1] - tg2.faculty)):
            if (d1 == 3 and tg2.room.isdisjoint(mat[first[0], first[1]][2] - tg1.room) and tg1.room.isdisjoint(
                    mat[second[0], second[1]][2] - tg2.room)):
                print("Swap Succesful - 3")
                tg1.day, tg1.time, tg2.day, tg2.time = tg2.day, tg2.time, tg1.day, tg1.time
                return
            else:
                print("Swap Succesful - 1/2")
                tg1.day, tg1.time, tg2.day, tg2.time = tg2.day, tg2.time, tg1.day, tg1.time
                return
        print("Unsuccesful Swap")


def initiation():
    courselist = []
    professorlist = []
    batchlist = []
    l = ['18HM1MG01', 'Engineering Economics and Accountancy', '18PC1CS03', 'Software Engineering', '18PC1IT03',
         'Java Programming', '18PC1IT04', 'Formal Languages and Automata Theory', '18PC1CS04',
         'Design and Analysis of Algorithms', '18PC1CS05', 'Database Management Systems']
    ll = ['18PC2IT02', 'Java Programming Laboratory', '18PC2CS02', 'Database Management Systems Laboratory',
          '18PC2IT03', 'IT Workshop']
    for _ in range(0, len(l), 2):
        t = Course(l[_], l[_ + 1], "Lecture", 1, 4)
        courselist.append(t)
    for _ in range(0, len(ll), 2):
        t = Course(ll[_], ll[_ + 1], "Lab", 3, 1)
        courselist.append(t)
    print(courselist, len(courselist))
    # l = ['Dr. C.Kiran Mai', 'Dr.G.Ramesh chandra', 'Dr.N.Sandhya', 'Dr. P.Neelakantan', 'Dr.M. Rajasekhar',
    #      'Dr.B.V.Kiranmayee', 'V.Baby', 'Dr.S.Nagini', 'M. Gangappa', 'Dr.P.V.Siva Kumar', 'Dr.T.Sunil Kumar',
    #      'Dr.Y.Sagar', 'Dr.A.Brahmananda Reddy', 'Dr. Deepak Sukheja', 'Dr.P.Subhash', 'A.Madhavi', 'N.V. Sailaja',
    #      'A.Kousar Nikhath', 'D.N. Vasundhara', 'R. Vasavi', 'R. Vijaya Saraswathi', 'G.S. Ramesh', 'P. Radhika',
    #      'N. Sravani', 'T.Gnana Prakash', 'G.Nagaraju', 'R.Kranthi Kumar', 'P.Venkateswara Rao', 'Y.Bhanu Sree',
    #      'N. Sandeep Chaitanya', 'S. Jahnavi', 'M.Ravi Kanth', 'P Bharath kumar Chowdary', 'Priya Bhatnagar',
    #      'P Rama Krishna', 'Priyanka Singh', 'N Lakshmi Kalyani', 'S.Kranthi Kumar', 'K.Bheema Lingappa', 'L.Indira',
    #      'Dr.K.Srinivas', 'S.Swapna', 'Dr.Ch.Suresh', 'Krithi Ohri', 'K. Jhansi Lakshmi Bai', 'M.Venkata Krishna Rao',
    #      'S.Nyemeesha', 'V.Harish', 'Shaik Arshiya Julma', 'A.Chennabasamma', 'P.Jyothi', 'M.Sangeetha',
    #      'A.Manusha Reddy', 'Lakshmi Prasudha(Research Schollar)']
    # for i, _ in enumerate(l):
    #     t = Professor('CSE', i + 1, _, [])
    #     professorlist.append(t)
    # print(professorlist,len(professorlist))
    professorlist = []
    l = ['Dr.C.Kiran Mai', 'M.Gangappa', 'A.Kousar Nikhath', 'N.V.Sailaja', 'Chenna Basamma', 'Dr.K.Srinivas',
         'G.S.Ramesh', 'P.Bharath Kumar', 'Y.Bhanu Sree', 'Dr.M.Rajasekar', 'P.Radhika', 'A.Kousar Nikath',
         'Priyanka Singh', 'P.Rama Krishna', 'A.Madhavi', 'S.Swapna', 'G.Nagaraju', 'M.Venkata Krishna Rao',
         'Dr.A.Brahmananda Reddy', 'Priyanka singh', 'K.Bheema Lingappa', 'T.Gnana Prakash', 'R.Vijaya Saraswathi',
         'Dr.Y.Sagar', 'DR.K.MURALI KRISHNA', 'Priya Bhatnagar']
    for i, _ in enumerate(l):
        print(i, _)
        t = Professor('CSE', i + 1, _, [])
        professorlist.append(t)
    print(professorlist, len(professorlist))
    for _ in range(4):
        t = Batch('CSE', 3, _ + 1, None)
        batchlist.append(t)
    print(batchlist, len(batchlist))

    data = [Data({batchlist[0],batchlist[1]}, {courselist[0]}, set(), None, ""),
            Data({batchlist[0]}, {courselist[1]}, {professorlist[7]}, None, 'A103'),
            Data({batchlist[0]}, {courselist[2]}, {professorlist[14]}, None, 'A103'),
            Data({batchlist[0]}, {courselist[3]}, {professorlist[16]}, None, 'A103'),
            Data({batchlist[0]}, {courselist[4]}, {professorlist[4]}, None, 'A103'),
            Data({batchlist[0]}, {courselist[5]}, {professorlist[3]}, None, 'A103'),
            Data({batchlist[0]}, {courselist[6], courselist[7]},
                 {professorlist[14], professorlist[15], professorlist[3], professorlist[11]}, None, None),
            Data({batchlist[0]}, {courselist[6], courselist[8]},
                 {professorlist[14], professorlist[15], professorlist[21], professorlist[20]}, None, None),
            Data({batchlist[0]}, {courselist[7], courselist[8]},
                 {professorlist[3], professorlist[11], professorlist[21], professorlist[20]}, None, None),
            #Data({batchlist[1]}, {courselist[0]}, {professorlist[24]}, None, 'B414'),
            Data({batchlist[1]}, {courselist[1]}, {professorlist[13]}, None, 'B414'),
            Data({batchlist[1]}, {courselist[2]}, {professorlist[10]}, None, 'B414'),
            Data({batchlist[1]}, {courselist[3]}, {professorlist[9]}, None, 'B414'),
            Data({batchlist[1]}, {courselist[4]}, {professorlist[8]}, None, 'B414'),
            Data({batchlist[1]}, {courselist[5]}, {professorlist[23]}, None, 'B414'),
            Data({batchlist[1]}, {courselist[6], courselist[7]},
                 {professorlist[10], professorlist[25], professorlist[23], professorlist[8]}, None, None),
            Data({batchlist[1]}, {courselist[6], courselist[8]},
                 {professorlist[10], professorlist[25], professorlist[12], professorlist[17]}, None, None),
            Data({batchlist[1]}, {courselist[7], courselist[8]},
                 {professorlist[23], professorlist[8], professorlist[12], professorlist[17]}, None, None),
            #Data({batchlist[2]}, {courselist[0]}, {professorlist[24]}, None, 'A103'),
            # Data({batchlist[2]}, {courselist[1]}, {professorlist[7]}, None, 'A103'),
            # Data({batchlist[2]}, {courselist[2]}, {professorlist[14]}, None, 'A103'),
            # Data({batchlist[2]}, {courselist[3]}, {professorlist[16]}, None, 'A103'),
            # Data({batchlist[2]}, {courselist[4]}, {professorlist[4]}, None, 'A103'),
            # Data({batchlist[2]}, {courselist[5]}, {professorlist[3]}, None, 'A103'),
            # Data({batchlist[2]}, {courselist[6], courselist[7]},
            #      {professorlist[14], professorlist[15], professorlist[3], professorlist[11]}, None, None),
            # Data({batchlist[2]}, {courselist[6], courselist[8]},
            #      {professorlist[14], professorlist[15], professorlist[21], professorlist[20]}, None, None),
            # Data({batchlist[2]}, {courselist[7], courselist[8]},
            #      {professorlist[3], professorlist[11], professorlist[21], professorlist[20]}, None, None),
            ]
    print(data, len(data))
    return batchlist, professorlist, courselist, data


def main():
    batchlist, professorlist, courselist, data = initiation()
    print(batchlist, professorlist, courselist, data)
    # Start
    generation = 1
    terminate = False

    population = []

    for _ in range(POPULATION_SIZE):
        gnome = Timetable.create_genome(data)
        population.append(Timetable(gnome))
    #print(population, len(population))

    while not terminate:

        # Sorting The Population with Increasing Order of Fitness
        population = sorted(population, key=lambda x: x.fitness)

        # Termination
        if population[0].fitness == 0:
            population[0].print_test()
            a, b, c, d = map(int, input().split())
            population[0].swap(batchlist[0], (a, b), (c, d))
            population[0].print_test()
            print(str(population[0].fitness) + " Check Here")
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


if __name__ == '__main__':
    main()
