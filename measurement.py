import csv
import time


def get_ids_map(task_ids):
    tasks_ids_matrix = {}
    with open(task_ids, encoding="utf8") as file:
        reader = csv.reader(file)
        fields = next(reader)
        for line in reader:
            t_id = int(line[0])
            tasks_name = line[1]
            tasks_ids_matrix[tasks_name] = t_id
    return tasks_ids_matrix


def get_preferences_map(soldiers_list):
    preferences_map = {}
    # time.sleep(2)
    with open(soldiers_list, encoding="utf8") as file:
        reader = csv.reader(file)
        fields = next(reader)
        for line in reader:
            s_id = int(line[0])
            preferences_list = line[2]
            preferences_map[s_id] = preferences_list
    return preferences_map


def get_dissatisfaction(task_id, preferences):
    return preferences.split(",").index(str(task_id))


def get_measurement(shift_soldiers, ids_map, soldiers_preferences):
    soldiers_dissatisfaction = {}
    max_single_dissatisfaction = 0
    all_soldiers_dissatisfaction = 0
    with open(shift_soldiers, encoding="utf8") as file:
        reader = csv.reader(file)
        fields = next(reader)
        for line in reader:
            s_id = int(line[0])
            date = line[1]
            t_name = line[2]
            a = ids_map[t_name]
            b = soldiers_preferences[s_id]
            soldiers_dissatisfaction[s_id] = get_dissatisfaction(a, b)
            if max_single_dissatisfaction < soldiers_dissatisfaction[s_id]:
                max_single_dissatisfaction = soldiers_dissatisfaction[s_id]
            all_soldiers_dissatisfaction += soldiers_dissatisfaction[s_id]
    return max_single_dissatisfaction, all_soldiers_dissatisfaction


def measurement(index):
    shift_soldiers = "soldiers_shifts.csv"
    task_ids = "tasks_ids.csv"
    soldiers_list = "soldiers_list.csv"

    ids_map = get_ids_map(task_ids)
    soldiers_preferences = get_preferences_map(soldiers_list)
    single_measurement, all_measurement = get_measurement(shift_soldiers, ids_map, soldiers_preferences)

    print('Measurement for max single soldier in "' + index + '" index method: ' + str(single_measurement))
    print('Measurement for all soldiers in "' + index + '" index method: ' + str(all_measurement))

    return single_measurement, all_measurement
