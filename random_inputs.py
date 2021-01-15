import csv
import random
import threading
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
            writer.writerow([i, "task" + str(i), random.randint(1, 10), random.randint(1, 4)])
    return file_name


def get_tasks_list_file(csv_id, number_of_tasks_id, number_of_tasks):
    file_name = 'csv files/tasks_list' + str(csv_id) + '.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date"])
        for i in range(number_of_tasks):
            writer.writerow([random.randint(0, number_of_tasks_id - 1), get_date(random.randint(0, 185))])
    return file_name


def get_soldiers_file(csv_id, number_of_soldiers, number_of_tasks_id):
    file_name = 'csv files/soldiers_list' + str(csv_id) + '.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Rank", "constraints_task_id"])
        for i in range(number_of_soldiers):
            writer.writerow([random_soldiers_id(), random.randint(1, number_of_tasks_id), random.randint(1, 4)])
    return file_name


def get_csvs(csv_id, number_of_tasks_id, number_of_tasks, number_of_soldiers):
    tasks_ids_csv = get_tasks_id_file(csv_id, number_of_tasks_id)
    tasks_list_csv = get_tasks_list_file(csv_id, number_of_tasks_id, number_of_tasks)
    tasks_soldiers_csv = get_soldiers_file(csv_id, number_of_soldiers, number_of_tasks_id)

    return tasks_ids_csv, tasks_list_csv, tasks_soldiers_csv


def main():
    average_num = 5
    file_name = 'Outputs/output_soldiers_long.csv'
    num_examples = 30

    number_of_tasks_id = 20
    number_of_soldiers = 10
    number_of_tasks = 13 * number_of_soldiers
    time_couples_averages = []
    print("seconds" + " " + "id" + " " + "so" + " " + "tasks" + " " + "limit")
    with open(file_name, 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Seconds", "Task id", "Soldiers numbers", "Number of tasks", "limit"])
        for i in range(num_examples):
            time_couples = []
            limits = []
            for j in range(average_num):
                tasks_ids_file, tasks_list_file, tasks_soldiers_file = get_csvs(i, number_of_tasks_id, number_of_tasks,
                                                                                number_of_soldiers)
                start_time = time.time()
                limit = run(tasks_list_file, tasks_ids_file, tasks_soldiers_file)
                limits.append(limit)
                end_time = time.time()
                time_couples.append(end_time - start_time)
                # print(str(end_time - start_time)[:4] + "    " + str(number_of_tasks_id) + " " + str(
                #    number_of_soldiers) + " " + str(number_of_tasks) + "   " + str(limit))
            average = sum(time_couples) / average_num
            print(str(average)[:4] + "    " + str(number_of_tasks_id) + " " + str(
                number_of_soldiers) + " " + str(number_of_tasks) + "   " + str(
                sum(limits) / average_num) + "   average")
            time_couples_averages.append(average)

            writer.writerow([str(average)[:4], str(number_of_tasks_id), str(number_of_soldiers), str(number_of_tasks),
                             str(sum(limits) / average_num)])

            # number_of_tasks_id += 2
            number_of_soldiers += 5
            # number_of_tasks += (13 * 5)
        print(time_couples_averages)


def main2():
    average_num = 5
    file_name = 'Outputs/output_tasks_long.csv'
    num_examples = 30

    number_of_tasks_id = 20
    number_of_soldiers = 10
    number_of_tasks = 13 * number_of_soldiers
    time_couples_averages = []
    print("seconds" + " " + "id" + " " + "so" + " " + "tasks" + " " + "limit")
    with open(file_name, 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Seconds", "Task id", "Soldiers numbers", "Number of tasks", "limit"])
        for i in range(num_examples):
            time_couples = []
            limits = []
            for j in range(average_num):
                tasks_ids_file, tasks_list_file, tasks_soldiers_file = get_csvs(i, number_of_tasks_id, number_of_tasks,
                                                                                number_of_soldiers)
                start_time = time.time()
                limit = run(tasks_list_file, tasks_ids_file, tasks_soldiers_file)
                limits.append(limit)
                end_time = time.time()
                time_couples.append(end_time - start_time)
                # print(str(end_time - start_time)[:4] + "    " + str(number_of_tasks_id) + " " + str(
                #    number_of_soldiers) + " " + str(number_of_tasks) + "   " + str(limit))
            average = sum(time_couples) / average_num
            print(str(average)[:4] + "    " + str(number_of_tasks_id) + " " + str(
                number_of_soldiers) + " " + str(number_of_tasks) + "   " + str(
                sum(limits) / average_num) + "   average")
            time_couples_averages.append(average)

            writer.writerow([str(average)[:4], str(number_of_tasks_id), str(number_of_soldiers), str(number_of_tasks),
                             str(sum(limits) / average_num)])

            # number_of_tasks_id += 2
            # number_of_soldiers += 5
            number_of_tasks += (13 * 5)
        print(time_couples_averages)


def main3():
    average_num = 5
    file_name = 'Outputs/output_both_long.csv'
    num_examples = 30

    number_of_tasks_id = 20
    number_of_soldiers = 10
    number_of_tasks = 13 * number_of_soldiers
    time_couples_averages = []
    print("seconds" + " " + "id" + " " + "so" + " " + "tasks" + " " + "limit")
    with open(file_name, 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Seconds", "Task id", "Soldiers numbers", "Number of tasks", "limit"])
        for i in range(num_examples):
            time_couples = []
            limits = []
            for j in range(average_num):
                tasks_ids_file, tasks_list_file, tasks_soldiers_file = get_csvs(i, number_of_tasks_id, number_of_tasks,
                                                                                number_of_soldiers)
                start_time = time.time()
                limit = run(tasks_list_file, tasks_ids_file, tasks_soldiers_file)
                limits.append(limit)
                end_time = time.time()
                time_couples.append(end_time - start_time)
                # print(str(end_time - start_time)[:4] + "    " + str(number_of_tasks_id) + " " + str(
                #    number_of_soldiers) + " " + str(number_of_tasks) + "   " + str(limit))
            average = sum(time_couples) / average_num
            print(str(average)[:4] + "    " + str(number_of_tasks_id) + " " + str(
                number_of_soldiers) + " " + str(number_of_tasks) + "   " + str(
                sum(limits) / average_num) + "   average")
            time_couples_averages.append(average)

            writer.writerow([str(average)[:4], str(number_of_tasks_id), str(number_of_soldiers), str(number_of_tasks),
                             str(sum(limits) / average_num)])

            # number_of_tasks_id += 2
            number_of_soldiers += 5
            number_of_tasks += (13 * 5)
        print(time_couples_averages)


# soldiers_file = 'Outputs/output_soldiers_long.csv'
# tasks_file = 'Outputs/output_tasks_long.csv'
# both_file = 'Outputs/output_both_long.csv'

main()
main2()
main3()

'''threads = []
try:
    threads.append(threading.Thread(target=main))
    threads.append(threading.Thread(target=main2))
    threads.append(threading.Thread(target=main3))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
except:
    print("error")'''
