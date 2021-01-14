import csv
import sys

from ortools.linear_solver import pywraplp

from day_mapping import get_date


def is_solution(num_days, num_soldier, num_tasks, shifts_table, costs_tasks, rank_tasks, rank_soldier, limit,
                soldiers_constrains_and_ranks_by_id, tasks_name):
    # Create the mip solver with the SCIP backend.
    model = pywraplp.Solver.CreateSolver('SCIP')
    # Variables
    x = setting_variables(num_days, num_soldier, num_tasks, shifts_table, model)

    # Constraints
    setting_constraints(num_days, num_soldier, num_tasks, shifts_table, costs_tasks, rank_tasks, rank_soldier,
                        x, model, limit)
    # Objective
    setting_objective(num_days, num_soldier, num_tasks, shifts_table, costs_tasks, x, model)
    # Solve
    return solve_func(num_days, num_tasks, shifts_table, costs_tasks, x, model,
                      soldiers_constrains_and_ranks_by_id, tasks_name)


def solve(ranks_constrains_by_ids_tasks, values_by_ids_tasks, tasks_by_day, ranks_of_soldiers,
          soldiers_constrains_and_ranks_by_id, tasks_name):
    # get tables from files
    shifts_table, rank_soldier, rank_tasks, costs_tasks, num_days, num_soldier, num_tasks, soldiers_constrains_and_ranks_by_id = create_tabeks_from_files(
        ranks_constrains_by_ids_tasks, values_by_ids_tasks, tasks_by_day, ranks_of_soldiers,
        soldiers_constrains_and_ranks_by_id)

    # get minimum limit
    min_limit, max_limit, jumps = get_limits(shifts_table, costs_tasks, num_soldier)
    limit = min_limit
    prev_limit = 0
    solution = False

    while solution is not True:
        jumps = 1
        while limit <= max_limit:
            answer_flag = is_solution(num_days, num_soldier, num_tasks, shifts_table, costs_tasks, rank_tasks,
                                      rank_soldier, limit,
                                      soldiers_constrains_and_ranks_by_id, tasks_name)
            if answer_flag:
                max_limit = prev_limit
                break
            else:
                prev_limit = limit
                limit += jumps
                jumps *= 2
        if limit > max_limit:
            limit = max_limit
        jumps = 1
        solution = True
        while limit >= min_limit:
            answer_flag = is_solution(num_days, num_soldier, num_tasks, shifts_table, costs_tasks, rank_tasks,
                                      rank_soldier, limit,
                                      soldiers_constrains_and_ranks_by_id, tasks_name)
            if answer_flag:
                prev_limit = limit
                limit -= jumps
                jumps *= 2
                solution = False
            else:
                min_limit = prev_limit
                break
    return limit


def get_limits(shifts_table, costs_tasks, num_soldier):
    values_counter = 0
    for day in shifts_table:
        for task_id in range(len(day)):
            if day[task_id][0] != 0:
                values_counter += costs_tasks[task_id]
    jump = sys.maxsize
    for i in range(len(costs_tasks) - 1):
        element1 = costs_tasks[i]
        j = i + 1
        while j < len(costs_tasks):
            element2 = costs_tasks[j]
            gap = abs(element1 - element2)
            if gap < jump:
                jump = gap
            j += 1
    return round(values_counter / num_soldier), values_counter, (jump + 10)


def create_tabeks_from_files(ranks_constrains_by_ids_tasks, values_by_ids_tasks, tasks_by_day, ranks_of_soldiers,
                             soldiers_constrains_and_ranks_by_id):
    shifts_table = tasks_by_day
    rank_soldier = ranks_of_soldiers
    rank_tasks = ranks_constrains_by_ids_tasks
    costs_tasks = values_by_ids_tasks
    num_days = 186
    num_soldier = len(ranks_of_soldiers)
    num_tasks = len(ranks_constrains_by_ids_tasks)

    return shifts_table, rank_soldier, rank_tasks, costs_tasks, num_days, num_soldier, num_tasks, soldiers_constrains_and_ranks_by_id


def setting_variables(num_days, num_soldier, num_tasks, shifts_table, model):
    # x[soldier, task, date] is an array of 0-1 variables
    # which will be 1 if the soldier is assigned to this task in this date.
    x = {}
    for soldier in range(num_soldier):
        for date in range(num_days):
            for task in range(num_tasks):
                for i in range(shifts_table[date][task][1]):
                    x[soldier, task, i, date] = model.IntVar(0, 1, '')
    return x


def setting_constraints(num_days, num_soldier, num_tasks, shifts_table, costs_tasks, rank_tasks, rank_soldier, x,
                        model, objective_max):
    # Each (soldier, date) is assigned to at most one task.
    for soldier in range(num_soldier):

        for date in range(num_days):
            total_task_for_soldier = 0
            for task in range(num_tasks):
                for i in range(shifts_table[date][task][1]):
                    total_task_for_soldier += x[soldier, task, i, date]
            model.Add(total_task_for_soldier <= 1)

    # Each (task,day) is assigned to exactly one worker.
    for date in range(num_days):
        for task in range(num_tasks):
            if shifts_table[date][task][0] == 1:
                for i in range(shifts_table[date][task][1]):
                    model.Add(model.Sum([x[soldier, task, i, date] for soldier in range(num_soldier)]) == 1)

    # Any soldier with rank X can be assigned to task with rank<X
    for date in range(num_days):
        for task in range(num_tasks):
            # rank = rank_tasks[task]
            rank = rank_tasks.get(task)
            for i in range(shifts_table[date][task][1]):
                for soldier in range(num_soldier):
                    if rank_soldier[soldier] < rank:
                        model.Add(x[soldier, task, i, date] == 0)

    # Each soldier can accumulate maximum of x points
    for soldier in range(num_soldier):
        max_soldier_score = 0
        for date in range(num_days):
            for task in range(num_tasks):
                for i in range(shifts_table[date][task][1]):
                    max_soldier_score = max_soldier_score + costs_tasks[task] * x[soldier, task, i, date]
        model.Add(max_soldier_score <= objective_max)


def setting_objective(num_days, num_soldier, num_tasks, shifts_table, costs_tasks, x, model):
    objective_worker_score = []
    for soldier in range(num_soldier):
        worker_score = 0
        for date in range(num_days):
            for task in range(num_tasks):
                for i in range(shifts_table[date][task][1]):
                    worker_score = worker_score + (costs_tasks[task] * x[soldier, task, i, date])
        objective_worker_score.append(worker_score)
    sum_score = 0
    for worker_score in objective_worker_score:
        sum_score += worker_score
    model.Minimize(sum_score)


def solve_func(num_days, num_tasks, shifts_table, costs_tasks, x, model,
               soldiers_constrains_and_ranks_by_id, tasks_name):
    # Solve
    status = model.Solve()
    # Print solution
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        # print('solution:')
        with open('soldiers_shifts.csv', 'w', encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Task_ID", "Soldier_ID"])
            # print('Total cost = ', model.Objective().Value(), '\n')
            for date in range(num_days):
                for task in range(num_tasks):
                    for i in range(shifts_table[date][task][1]):
                        for soldier in range(len(soldiers_constrains_and_ranks_by_id)):
                            # Test if x[soldier, task, date] is 1 (with tolerance for floating point arithmetic).
                            if x[soldier, task, i, date].solution_value() > 0.5:
                                # print('Worker %d assigned to task %d in day %d.  Cost = %d' %(soldier, task, date, costs_tasks[task]))
                                ids = soldiers_constrains_and_ranks_by_id[soldier][0]
                                date_time = get_date(date)
                                name = tasks_name[task]
                                writer.writerow([ids, date_time, name])
        return True
    else:
        return False
