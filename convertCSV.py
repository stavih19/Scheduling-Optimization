import csv
from day_mapping import get_serial
from soldiers_shifts import solve


def get_tasks_dictionary(tasks_ids_file):
    tasks_ids_matrix = {}
    tasks_name = []
    tasks_values = []
    with open(tasks_ids_file, encoding="utf8") as file:
        reader = csv.reader(file)
        fields = next(reader)
        for line in reader:
            t_id = int(line[0])
            tasks_name.append(line[1])
            t_value = int(line[2])
            category_id_list = int(line[3])
            tasks_ids_matrix[t_id] = category_id_list
            tasks_values.append(t_value)
    return tasks_ids_matrix, tasks_values, tasks_name


def get_tasks_matrix(tasks_list_file, task):
    days = 186
    task_matrix = [[[0, 0] for i in range(task)] for j in range(days)]

    with open(tasks_list_file, encoding="utf8") as file:
        reader = csv.reader(file)
        fields = next(reader)
        for line in reader:
            if line[0] == '':
                break
            row = get_serial(line[1])
            task_id = int(line[0])
            task_matrix[row][task_id][0] = 1
            task_matrix[row][task_id][1] += 1
    return task_matrix


def get_soldiers_list(soldiers_list_file):
    soldiers_ids = []
    soldiers_ids1 = []
    soldiers_constrains_matrix = []
    with open(soldiers_list_file, encoding="utf8") as file:
        reader = csv.reader(file)
        fields = next(reader)
        for line in reader:
            s_rank = int(line[1])
            soldiers_ids1.append(s_rank)
            constrains_task_id = line[2].split(',')  # receive list
            for i in range(0, len(constrains_task_id)):
                if constrains_task_id[0] == '':
                    break
                constrains_task_id[i] = int(constrains_task_id[i])
            soldiers_ids.append(s_rank)
            properties = [int(line[0]), s_rank, constrains_task_id]
            soldiers_constrains_matrix.append(properties)
    return soldiers_ids1, soldiers_constrains_matrix


def get_tasks_list_file(file_name):
    tasks_list_file = file_name
    print('Selected:', tasks_list_file)


def get_tasks_ids_file(file_name):
    tasks_ids_file = file_name
    print('Selected:', tasks_ids_file)


def get_soldiers_list_file(file_name):
    soldiers_list_file = file_name
    print('Selected:', soldiers_list_file)


def run(tasks_list_file, tasks_ids_file, soldiers_list_file):
    tasks_list_file_check = tasks_list_file.split("/")[-1]
    tasks_ids_file_check = tasks_ids_file.split("/")[-1]
    soldiers_list_file_check = soldiers_list_file.split("/")[-1]

    if tasks_list_file_check != "tasks_list.csv":
        print("wrong tasks list file")
        return 0
    if tasks_ids_file_check != "tasks_ids.csv":
        print("wrong tasks ids file")
        return 0
    if soldiers_list_file_check != "soldiers_list.csv":
        print("wrong soldiers list file")
        return 0

    ranks_constrains_by_ids_tasks, values_by_ids_tasks, tasks_name = get_tasks_dictionary(tasks_ids_file)
    tasks_by_day = get_tasks_matrix(tasks_list_file, len(values_by_ids_tasks))
    ranks_of_soldiers, soldiers_constrains_and_ranks_by_id = get_soldiers_list(soldiers_list_file)

    limit = solve(ranks_constrains_by_ids_tasks, values_by_ids_tasks, tasks_by_day, ranks_of_soldiers,
                  soldiers_constrains_and_ranks_by_id, tasks_name)
    return limit
