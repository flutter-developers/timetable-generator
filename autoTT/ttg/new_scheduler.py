import random
from tkinter import *
from tkinter import ttk

from ttg.model import *

import ttg.timetable as timetable

# from open_electives import open_elective
# from labs import lab
# from lectures import lectures
# from labs_room_choices import labs_room_choices
# from professors import prof

POPULATION_SIZE = 25

def tk_print(d):
        class Table:

            def __init__(self, root, temp):
                total_rows = len(temp)
                total_columns = len(temp[0])

                # code for creating table
                for i in range(total_rows):
                    for j in range(total_columns):
                        # self.e = Entry(root, fg='black',width=20,
                        #                font=('Arial', 16, 'bold'))
                        e = Text(root, fg='white',bg = 'black',height=2, width=21,font=('Arial', 16, 'bold'))
                        e.grid(row=i, column=j)
                        e.insert(END, temp[i][j])

                    # take the data

        # create root window
        root = Tk()
        root.title("Tab Widget")
        tabControl = ttk.Notebook(root)
        for i, _ in enumerate(d):
            title = ttk.Frame(tabControl)
            tabControl.add(title, text=str(_))
            t = Table(title, d[_])
        tabControl.pack(expand=1, fill="both")
        root.mainloop()


def initiation(course_list,professor_list,batch_list):
    # course_list = []
    # professor_list = []
    # batch_list = []

    # for _ in range(0, len(open_elective), 3):
    #     c = Course()
    #     c.create_lecture(open_elective[_], open_elective[_ + 1], open_elective[_ + 2], 2, 2)
    #     course_list.append(c)

    # for _ in range(0, len(lectures), 3):
    #     c = Course()
    #     c.create_lecture(lectures[_], lectures[_ + 1], lectures[_ + 2], 1, 4)
    #     course_list.append(c)

    # for _ in range(0, len(lab), 3):
    #     c = Course()
    #     c.create_lab_course(lab[_], lab[_ + 1], lab[_ + 2], labs_room_choices[_ // 3])
    #     course_list.append(c)
        
    # # print(course_list, len(course_list))

    # for i, _ in enumerate(prof):
    #     t = Professor('CSE', i, _)
    #     professor_list.append(t)
    # # print(professor_list, len(professor_list))

    # b_room = ['R1', 'R2', 'R3', 'R4']
    # for _ in range(4):
    #     t = Batch('CSE', 3, _ + 1, b_room[_], False)
    #     batch_list.append(t)

    # b_room = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8',
	# 	'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16']
    # for _ in range(16):
    #     t = Batch('CSE', 4, _ + 1, b_room[_], False)
    #     batch_list.append(t)
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


def scheduler(course_list,professor_list,batch_list):
    batch_list, professor_list, course_list, data = initiation(course_list,professor_list,batch_list)
    # print(batch_list, professor_list, course_list, data)
    print('\n#################################################################')
    print('data === ', data)
    print('#################################################################\n')

    # Start
    generation = 1
    terminate = False
    population = []

    for _ in range(POPULATION_SIZE):
        gnome = timetable.Timetable.create_genome(data)
        population.append(timetable.Timetable(gnome))

    while not terminate:

        # Sorting The Population with Increasing Order of Collisions
        population = sorted(population, key=lambda x: x.collisions)

        # Termination
        if population[0].collisions == 0:
            d = population[0].print_test()
            # Timetable.save(population[0])
            # population[0].tk_print(d)
            # tk_print(d)
            return d
            ch = input('Enter Swap Choice: ')
            while ch == 'y':
                print('Enter Coordinates: ')
                a, b, c, d = map(int, input().split())
                # Static Swap Function call in First Batch
                population[0].swap(batch_list[0], (a, b), (c, d))
                d = population[0].print_test()
                print('Printing...')
                # population[0].tk_print(d)
                # tk_print(d)
                return d
                ch = input('Do you want to Continue Swapping')
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

        if generation > 4000:
            print("Re-Schedule")
            scheduler()
