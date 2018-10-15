"""
Constraints:
1. A proffesor should not be teaching in two different rooms at the same time****
2. For a day, each course should have only one lecture ****
3. For a week, each course should have only two lectures
"""

import numpy as np
import random

R = 5
C = 8

M = 20   #course
N = 2   #room
P = 12   #prof

courses = np.zeros((2, M))
time_table = np.zeros((R, C, N))

def ConstraintsSatisfationProblem(course_prof_dict):
    global time_table
    restricted_courses_for_a_week = []


    # for row_ind in range(courses.shape[0]):
    #     for col_ind in range(courses.shape[1]):
    #         # x = course_prof_dict[col_ind]   #gives corresponding prof to a course
    #         for i in range(0, R):
    #             restricted_courses_for_a_day = []
    #             for j in range(0, C):
    #                 restricted_profs_for_a_slot = []
    #                 for k in range(0, N):
    #                     print(i, j, k, col_ind+1, restricted_profs_for_a_slot)
    #                     if time_table[i][j][k] == 0 and \
    #                     course_prof_dict[col_ind+1] not in restricted_profs_for_a_slot and \
    #                     (col_ind+1) not in restricted_courses_for_a_day and \
    #                     restricted_courses_for_a_week.count(col_ind+1) <2:
    #                         time_table[i][j][k] = col_ind+1
    #                         restricted_profs_for_a_slot.append(course_prof_dict[col_ind+1])
    #                         restricted_courses_for_a_day.append(col_ind+1)
    #                         restricted_courses_for_a_week.append(col_ind+1)
    #                     else:
    #                         continue
    # print(time_table)


    for i in range(0, R):
        restricted_courses_for_a_day = []
        for j in range(0, C):
            restricted_profs_for_a_slot = []
            for k in range(0, N):
                for row_ind in range(0, courses.shape[0]):
                    for col_ind in range(0, courses.shape[1]):
                        if time_table[i][j][k] == 0 and \
                        course_prof_dict[col_ind+1] not in restricted_profs_for_a_slot and \
                        (col_ind+1) not in restricted_courses_for_a_day and \
                        restricted_courses_for_a_week.count(col_ind+1) <2:
                            time_table[i][j][k] = col_ind+1
                            restricted_profs_for_a_slot.append(course_prof_dict[col_ind+1])
                            restricted_courses_for_a_day.append(col_ind+1)
                            restricted_courses_for_a_week.append(col_ind+1)
                        else:
                            continue
    print(time_table)
    for i in range(0, len(time_table)):
        print('\nDAY :', i + 1)
        for j in range(0, len(time_table[0])):
            print(time_table[i][j], end=' ')
    print()

    # verifying if constraints are violated
    print('This should be 1 for non-violating TT: ', evaluate_fitness_function(time_table, course_prof_dict))
    print()


def ModifiedConstraintsSatisfationProblem(course_prof_dict):
    global time_table
    available_slots = []            #stores available time slots as (day,time,room)

    for i in range(0, R):
        for j in range(0,C):
            for k in range(0, N):
                available_slots.append((i,j,k))

    no_of_lectures = 2*M            #each course has 2 lectures
    course_day = {}
    prof_day_slot = {}

    for i in range(1, M+1):
        course_day[i] = -1          #dictionary to map the day when one of the 2 letures is scheduled for a course

    for i in range(1, P+1):
        prof_day_slot[i] = []       #dictionary to map a profs's schedule as (day,time), i.e. the prof is busy at (day,time)

    lecture = 1
    while no_of_lectures>0:
        random.shuffle(available_slots)
        i,j,k = available_slots[0]
        '''
        Condition 1 [if]: Check if no lecture for the course has been scheduled so far and 
                     if the prof for the course is not busy during the (day,time) slot 
        Condition 2 [elif, if]: Check if the a lecture for the course has not been scheduled the same day and
                                if the prof for the course is not busy during the (day,time) slot
        '''
        if course_day[lecture] == -1 and (i,j) not in prof_day_slot[course_prof_dict[lecture]]:
            time_table[i][j][k] = lecture
            course_day[lecture] = i
            prof_day_slot[course_prof_dict[lecture]].append((i,j))         #prof is busy at (day,time) now
            available_slots.remove((i,j,k))                                #slot not available anymore
        elif course_day[lecture] != -1 and (i,j) not in prof_day_slot[course_prof_dict[lecture]]:
            day = course_day[lecture]
            if i!=day:
                time_table[i][j][k] = lecture
                course_day[lecture] = i
                prof_day_slot[course_prof_dict[lecture]].append((i, j))         #prof is busy at (day,time) now
                available_slots.remove((i,j,k))                                 #slot not available anymore
            else:
                continue
        else:
            continue

        if no_of_lectures % 2 != 0:
            lecture += 1
        no_of_lectures -= 1

    for i in range(0, len(time_table)):
        print('\nDAY :', i + 1)
        for j in range(0, len(time_table[0])):
            print(time_table[i][j], end=' ')
    print()

    #verifying if constraints are violated
    print('This should be 1 for non-violating TT: ', evaluate_fitness_function(time_table, course_prof_dict))


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


c_p_dict = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:6, 13:7, 14:7, 15:8, 16:8, 17:9, 18:10, 19:11, 20:12}
#, 21:16, 22:17, 23:18, 24:19, 25:20
ConstraintsSatisfationProblem(course_prof_dict=c_p_dict)


