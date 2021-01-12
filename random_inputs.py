import csv
import random
import time

from convertCSV import run
from day_mapping import get_date

soldiers_id = {}


def random_soldiers_id():
    rnd_id = random.randint(100000000, 1000000000)
    while rnd_id in soldiers_id:
        rnd_id = random.randint(100000000, 1000000000)
    soldiers_id[str(rnd_id)] = 1
    return rnd_id


def get_tasks_id_file(csv_id, number_of_tasks_id):
    file_name = 'csv files/tasks_ids' + str(csv_id) + '.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Value", "Rank"])
        for i in range(number_of_tasks_id):
            writer.writerow([i, "task" + str(i), random.randint(1, 30), random.randint(1, 4)])
    return file_name


def get_tasks_list_file(csv_id, number_of_tasks_id, number_of_tasks):
    file_name = 'csv files/tasks_list' + str(csv_id) + '.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date"])
        for i in range(number_of_tasks):
            writer.writerow([random.randint(0, number_of_tasks_id - 1), get_date(random.randint(0, 185))])
    return file_name


def get_soldiers_file(csv_id, number_of_soldiers):
    file_name = 'csv files/soldiers_list' + str(csv_id) + '.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Rank", "constraints_task_id"])
        for i in range(number_of_soldiers):
            writer.writerow([random_soldiers_id(), random.randint(1, 4), random.randint(1, 4)])
    return file_name


def get_csvs(csv_id, number_of_tasks_id, number_of_tasks, number_of_soldiers):
    tasks_ids_csv = get_tasks_id_file(csv_id, number_of_tasks_id)
    tasks_list_csv = get_tasks_list_file(csv_id, number_of_tasks_id, number_of_tasks)
    tasks_soldiers_csv = get_soldiers_file(csv_id, number_of_soldiers)

    return tasks_ids_csv, tasks_list_csv, tasks_soldiers_csv


def main():
    num_examples = 10
    number_of_tasks_id = 10
    number_of_soldiers = 10
    number_of_tasks = 26 * number_of_soldiers
    time_couples_averages = []
    print("seconds" + " " + "id" + " " + "so" + " " + "tasks")
    for i in range(num_examples):
        time_couples = []
        tasks_ids_file, tasks_list_file, tasks_soldiers_file = get_csvs(i, number_of_tasks_id, number_of_tasks,
                                                                        number_of_soldiers)
        for j in range(10):
            start_time = time.time()
            run(tasks_list_file, tasks_ids_file, tasks_soldiers_file)
            end_time = time.time()
            time_couples.append(end_time - start_time)
            # print(end_time - start_time)
        average = sum(time_couples) / 10
        time_couples_averages.append(average)
        print(str(average)[:4] + "    " + str(number_of_tasks_id) + " " + str(number_of_soldiers) + " " + str(
            number_of_tasks))

        number_of_tasks_id += 2
        number_of_soldiers += 5
        number_of_tasks = 26 * number_of_soldiers
    print(time_couples_averages)


main()
