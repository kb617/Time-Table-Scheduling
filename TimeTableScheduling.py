import numpy as np
import random
import copy
from matplotlib import pyplot

'''
Constraint: N < M
'''
R = 5   #day
C = 8   #time

M = 25  #course
N = 3   #rooms
P = 20  #prof

graph_values = []
time_table = []
initial_population = []

def define_random_chromosome():
    # course_days_dictionary = {}    #contains the days when the lectures are scheduled for a particular course
    # for i in range(1, M+1):
    #     course_days_dictionary[i] = (-1, -1)

    chromosome = np.zeros((R, C, N))
    # course_id = 1

    total_no_of_lectures = 2*M
    c = 0
    x = []
    while c<total_no_of_lectures:
        i = random.randint(0, R - 1)
        j = random.randint(0, C - 1)
        k = random.randint(0, N - 1)
        if chromosome[i][j][k] == 0:
            y = random.randint(1, M)
            # chromosome[i][j][k] = y
            # c += 1
            if x.count(y) < 2:
                chromosome[i][j][k] = y
                x.append(y)
                c += 1

    # while course_id<M+1:
    #     i = random.randint(0, R-1)
    #     j = random.randint(0, C-1)
    #     k = random.randint(0, N-1)
    #     if chromosome[i][j][k] == 0:
    #         chromosome[i][j][k] = course_id
    #         course_days_dictionary[course_id] = (i, -1)
    #         course_id += 1
    #
    #
    # course_id = 1
    # while course_id<M+1:
    #     i = random.randint(0, R-1)
    #     x, y = course_days_dictionary[course_id]
    #     if x == i:      # course_id already scheduled on same day then continue to generate the random no. again
    #         continue
    #     j = random.randint(0, C - 1)
    #     k = random.randint(0, N - 1)
    #     if chromosome[i][j][k] == 0:
    #         chromosome[i][j][k] = course_id
    #         x, y = course_days_dictionary[course_id]
    #         course_days_dictionary[course_id] = (x, i)
    #         course_id += 1

      # for i in range(R):
    #     for j in range(C):
    #         for k in range(N):
    #             fill_the_room = random.randint(0,1)
    #             if fill_the_room == 1:
    #                 course = random.randint(1, M)
    #                 chromosome[i][j][k] = course
    #             else:
    #                 continue

    return chromosome


'''
Reference for fitness function: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5705788&tag=1
'''
def evaluate_fitness_function(chromosome, course_prof_dict):
    c = 0
    '''
       *. When lecture for a subject is scheduled more than once in a day, then penalise with the count with which it exceeds
       b. When lecture for a subject is scheduled more than twice in a week, then penalise with the count with which it exceeds
       *. When a lecture taught by same professor is scheduled in same time slot.
    '''
    lectures_in_a_week = []
    for i in range(0, R):
        lectures_in_a_day = []
        for j in range(0, C):
            prof_ids = []
            lectures_in_a_slot = []
            for k in range(0, N):
                if chromosome[i][j][k] != 0:
                    course_id =  chromosome[i][j][k]
                    lectures_in_a_slot.append(course_id)            #keeps courseids whose lectures are in a particular slot
                    lectures_in_a_day.append(course_id)             #keeps courseids whose lectures are in a particular day
                    prof_ids.append(course_prof_dict[course_id])    #keeps profids whose lectures are in a particular slot
                    lectures_in_a_week.append(course_id)            #keeps courseids whose lectures are in a particular week

            if len(lectures_in_a_slot) > len(set(lectures_in_a_slot)):
                c += (len(lectures_in_a_slot) - len(set(lectures_in_a_slot)))   #avoids same course lectures in same slot
            if len(prof_ids) > len(set(prof_ids)):
                c += (len(prof_ids) - len(set(prof_ids)))                       #avoids same prof teaching in same slot
        if len(lectures_in_a_day) > len(set(lectures_in_a_day)):
            c += (len(lectures_in_a_day)-len(set(lectures_in_a_day)))           #avoids same course lectures in same day

    cid, count = np.unique(lectures_in_a_week, return_counts=True)
    for val in count:
        c += abs(val-2)

    return float(1/(1+c))


def generate_initial_population(population_size):
    for i in range(0, population_size):
        if i%20 == 0:
            print(i)
        initial_population.append(define_random_chromosome())
    return initial_population


def mutation(chromosome):
    # for i in range(0, R):
    #     for j in range(0, C):
    #         for k in range(0, N):
    #             if chromosome[i][j][k] != '':
    #                 make_blank = random.randint(0,1)
    #                 if make_blank == 0:
    #                     course_id = random.randint(1, M)
    #                     room_id = random.randint(1, N)
    #                     chromosome[i][j][k] = str(course_id)+'_'+str(room_id)
    no_of_cells_to_mutate = 5
    n=0
    big_count = 0
    while n<no_of_cells_to_mutate and big_count<20:
        i1 = random.randint(0, R-1)
        j1 = random.randint(0, C-1)
        k1 = random.randint(0, N-1)

        i2 = random.randint(0, R-1)
        j2 = random.randint(0, C-1)
        k2 = random.randint(0, N-1)

        if chromosome[i1][j1][k1] != 0 and chromosome[i2][j2][k2] != 0:
            temp = chromosome[i1][j1][k1]
            chromosome[i1][j1][k1] = chromosome[i2][j2][k2]
            chromosome[i2][j2][k2] = temp
            n += 1
        else:
            big_count += 1

    # for i in range(0, R):
    #     for j in range(0, C):
    #         x = 0
    #         for k in range(0, N):
    #             if chromosome[i][j][k] != '':
    #                 x += 1
    #         if x > P:
    #             k = random.randint(0, N-1)
    #             chromosome[i][j][k] = ''

    return chromosome


def crossover(chromosome1, chromosome2):
    i = random.randint(int(R/2), R-1)
    # j = random.randint(int(C/2), C-1)
    # k = random.randint(int(N/2), N-1)
    # c12 = chromosome1[i:R][j:C][k:N]
    # c22 = chromosome2[i:R][j:C][k:N]
    temp = np.copy(chromosome1[i:R][:][:])
    chromosome1[i:R][:][:] = chromosome2[i:R][:][:]
    chromosome2[i:R][:][:] = temp
    # print(chromosome1.shape)
    # print(chromosome2.shape)
    chromosome_list = [chromosome1, chromosome2]

    for chromosome in chromosome_list:
        courses = {}
        for i in range(1, M+1):
            courses[i] = []

        for i in range(0, R):
            for j in range(0, C):
                for k in range(0, N):
                    x = chromosome[i][j][k]
                    if x != 0:
                        courses[x].append(i)
                        courses[x].append(j)
                        courses[x].append(k)

        no_of_slots_for_each_course = []
        for i in range(1, M+1):
            l = len(courses[i])/3
            no_of_slots_for_each_course.append(l)

        while max(no_of_slots_for_each_course) != 2 and min(no_of_slots_for_each_course) != 2:
            MAX = np.argmax(no_of_slots_for_each_course)+1
            MIN = np.argmin(no_of_slots_for_each_course)+1
            list_max = courses[MAX]
            k, j, i = list_max[len(list_max)-1], list_max[len(list_max)-2], list_max[len(list_max)-3]
            chromosome[i][j][k] = MIN
            courses[MAX].pop()
            courses[MAX].pop()
            courses[MAX].pop()
            no_of_slots_for_each_course[MAX-1] -= 1
            no_of_slots_for_each_course[MIN-1] += 1



    return chromosome1, chromosome2

def selection_operator(population, course_prof_dict):
    population_size = len(population)
    fitness = []
    for chromosome in population:
        f = evaluate_fitness_function(chromosome, course_prof_dict)
        fitness.append(f)
    print('f_val: ', max(fitness))

    if max(fitness) == 1:
        time_table.append(population[np.argmax(fitness)])

    graph_values.append(max(fitness))
    fitter_population = []
    k = 80
    while k>0:
        fitter_population.append(population[np.argmax(fitness)])
        fitness[np.argmax(fitness)] = -1
        k -= 1
    # print('FITTER POPULATION')
    # print(fitter_population)
    return fitter_population


#source: lecture-7 GA2 slides @ https://sites.google.com/a/iiitd.ac.in/ai2018/lecture-slides
def memetic_algorithm(course_prof_dict):
    init_population_size = 100
    population = copy.deepcopy(initial_population)
    iterations = 0

    optimized_population = []
    new_population = []

    for chromosome in population:
        optimized_population.append(generate_neighbours(chromosome, course_prof_dict))

    population = copy.deepcopy(selection_operator(optimized_population, course_prof_dict))

    while iterations<200 and len(population)>0 and graph_values[len(graph_values)-1]!=1:
        i = 0
        fitness_value = []
        optimized_population = []
        # print(iterations, ': ', 'Sorting ', len(population), ' population ')
        for chromosome in population:
            fitness_value.append(evaluate_fitness_function(chromosome, course_prof_dict))
        sorted_population = []
        kk = 0
        while kk < len(population):
            kk += 1
            ind = np.argmax(fitness_value)
            fitness_value[ind] = -1
            sorted_population.append(population[ind])

        # print(iterations, ': Crossing over ', len(sorted_population), ' chromosomes consecutively')
        while i<len(sorted_population):
            c1, c2 = crossover(sorted_population[i], sorted_population[i+1])
            i += 2
            new_population.append(c1)
            new_population.append(c2)

        for chromosome in new_population:
            optimized_population.append(generate_neighbours(chromosome, course_prof_dict))

        # print(iterations, ': Selecting top k from ', len(optimized_population))
        population = copy.deepcopy(selection_operator(optimized_population, course_prof_dict))

        new_population = []
        iterations += 1
        # print()

    if graph_values[len(graph_values) - 1] == 1:
        print("MA Converged")
        # print('Time Table [courseIds]')
        for i in range(len(time_table[len(time_table)-1])):
            print('\nDAY :', i+1)
            for j in range(len(time_table[len(time_table)-1][i])):
                print(time_table[len(time_table)-1][i][j], end=' ')
        print()
    else:
        print('Iterations exceeded')



def genetic_algorithm(course_prof_dict):
    init_population_size = 100
    population = copy.deepcopy(generate_initial_population(init_population_size))

    # print('len: ', len(population))
    iterations = 0
    new_population = []
    # mutated_population = []
    # print('Mutating initial poulation')
    # for chromosome in population:
    #     mutated_population.append(mutation(chromosome))
    #
    # population = population + mutated_population

    # print('Selecting top k from init')
    population = copy.deepcopy(selection_operator(population, course_prof_dict))

    while iterations<100 and len(population)>0 and graph_values[len(graph_values)-1]!=1:
        i = 0
        fitness_value = []
        # print(iterations,': ', 'Sorting ', len(population), ' population ')
        for chromosome in population:
            fitness_value.append(evaluate_fitness_function(chromosome, course_prof_dict))
        sorted_population = []
        kk = 0
        while kk<len(population):
            kk += 1
            ind = np.argmax(fitness_value)
            fitness_value[ind] = -1
            sorted_population.append(population[ind])
        # print(iterations, ': Crossing over ', len(sorted_population), ' chromosomes consecutively')
        while i<len(sorted_population):
            c1, c2 = crossover(sorted_population[i], sorted_population[i+1])
            i += 2
            new_population.append(c1)
            new_population.append(c2)

        # print(iterations, ': Mutating ', len(sorted_population), ' chromosomes')
        # mutated_population = []
        # for chromosome in sorted_population:
        #     mutated_population.append(mutation(chromosome))

        # new_population = mutated_population + new_population

        # print(iterations, ': Selecting top k from ', len(new_population))
        population = copy.deepcopy(selection_operator(new_population, course_prof_dict))

        new_population = []
        iterations += 1
        print()

    if graph_values[len(graph_values) - 1] == 1:
        print("GA Converged")
        print('Time Table [courseIds]')
        for i in range(len(time_table[len(time_table)-1])):
            print('\nDAY :', i+1)
            for j in range(len(time_table[len(time_table)-1][i])):
                print(time_table[len(time_table)-1][i][j], end=' ')
        print()
    else:
        print('Iterations exceeded')


def generate_neighbours(chromosome, course_prof_dict):
    neighbours = []
    no_of_neighbours = 4
    neighbours.append(chromosome)

    #choose a random point in existing chromosome
    i = random.randint(0,R-1)
    j = random.randint(0,C-1)
    k = random.randint(0,N-1)
    # for i in range(R):
    #     for j in range(C):
    #         for k in range(N):

    while no_of_neighbours>0:
        # choose a random target point in existing chromosome
        i_prime = random.randint(0, R-1)

        x = np.copy(chromosome[i][j][k])     #original value
        chromosome[i][j][k] = np.copy(chromosome[i_prime][j][k])
        chromosome[i_prime][j][k] = np.copy(x)
        neighbours.append(chromosome)
        chromosome[i][j][k] = np.copy(x)     #restore original chromosome
        no_of_neighbours -= 1

    #select fittest chromosome among original chromosome and all the neighbours
    fval = -1
    ind = -1
    for ii in range(0, len(neighbours)):
        xx = evaluate_fitness_function(neighbours[ii], course_prof_dict)
        if xx >= fval:
            fval = xx
            ind = ii
    return neighbours[ind]





def plot_graph(f_val, caption, x):
    i=1
    generations = []
    for v in f_val:
        generations.append(i)
        i += 1
    pyplot.subplot(x)
    pyplot.title(caption + ': Plot: '+'For '+str(len(f_val))+' iterations')
    pyplot.plot(generations, f_val, color = 'blue', marker = 'o', markersize = 5)

    if x==122:
        pyplot.show()

# def print_time_table(tt):
#     for i in range(0, tt.shape[0]):
#         for j in range(0, tt.shape[1]):
#             for k in range(0, tt.shape[1]):
#                 print(tt[i][j][k])


c_p_dict = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:7, 13:8, 14:9, 15:10, 16:11, 17:12, 18:13, 19:14, 20:15, 21:16, 22:17, 23:18, 24:19, 25:20}
# , 11:6, 12:6, 13:7, 14:7, 15:8, 16:8, 17:9, 18:9, 19:10, 20:10

genetic_algorithm(c_p_dict)
plot_graph(graph_values, 'GA', 121)
graph_values = []
memetic_algorithm(c_p_dict)
plot_graph(graph_values, 'MA', 122)

