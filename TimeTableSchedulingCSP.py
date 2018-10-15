"""
Constraints:
1. A proffesor should not be teaching in two different rooms at the same time****
2. For a day, each course should have only one lecture ****
3. For a week, each course should have only two lectures
"""

import numpy as np

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

c_p_dict = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:6, 13:7, 14:7, 15:8, 16:8, 17:9, 18:10, 19:11, 20:12}
#, 21:16, 22:17, 23:18, 24:19, 25:20
ConstraintsSatisfationProblem(course_prof_dict=c_p_dict)


