import csv
import random


def generate_task_id_rows(task_id_amount):
    data = []

    for task_id in range(task_id_amount):
        data.append([task_id, 'task' + str(task_id), 1, 1])

    return data


def set_task_id(task_id_path, task_id_amount):
    header = ['ID', 'Name', 'Value', 'Rank']
    data = generate_task_id_rows(task_id_amount)

    with open(task_id_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def generate_task_rows(task_amount):
    data = []

    for task_id in range(task_amount):
        data.append([task_id, '01-Jan'])
        data.append([task_id, '02-Jan'])
        data.append([task_id, '03-Jan'])

    return data


def set_task_list(task_list_path, task_amount):
    header = ['ID', 'Date']
    data = generate_task_rows(task_amount)

    with open(task_list_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def generate_soldiers_rows(soldiers_amount, soldiers_list):
    data = []
    soldiers_list = []

    task_id_shuffle = []
    for task_id in range(soldiers_amount):
        task_id_shuffle.append(str(task_id))

    if not soldiers_list:
        for task_id in range(soldiers_amount):
            random.shuffle(task_id_shuffle)
            temp_id = random.randint(100000000, 999999999)
            soldiers_list.append(temp_id)
            data.append([temp_id, 1, ",".join(task_id_shuffle)])
    else:
        counter = 0
        for task_id in range(soldiers_amount):
            random.shuffle(task_id_shuffle)
            temp_id = soldiers_list[counter]
            soldiers_list.append(temp_id)
            data.append([temp_id, 1, ",".join(task_id_shuffle)])
            counter += 1

    return data, soldiers_list


def set_soldiers_list(soldiers_list_path, soldiers_amount, soldiers_list):
    header = ['ID', 'Rank', 'constraints_task_id']
    data, soldiers_list = generate_soldiers_rows(soldiers_amount, soldiers_list)

    with open(soldiers_list_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    return soldiers_list


def generate_input_file(task_id_amount, soldiers_list):
    task_id_path = "tasks_ids.csv"
    task_list_path = "tasks_list.csv"
    soldiers_list_path = "soldiers_list.csv"

    task_amount = task_id_amount
    soldiers_amount = task_amount

    set_task_id(task_id_path, task_id_amount)
    set_task_list(task_list_path, task_amount)
    soldiers_list = set_soldiers_list(soldiers_list_path, soldiers_amount, soldiers_list)
    return soldiers_list
