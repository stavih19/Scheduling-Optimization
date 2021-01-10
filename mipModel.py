from mip.constants import OptimizationStatus, BINARY
from mip.model import minimize, xsum, Model

m = Model()

# Data
tasks = [
    [0, 1, 1, 0],
    [1, 0, 1, 1],
    [0, 0, 1, 1],
]
num_days = len(tasks)

costs = [
    [1, 2, 3, 2],
    [1, 2, 3, 2],
    [1, 2, 3, 2],
    [1, 2, 3, 2],
    [1, 2, 3, 2],
    [1, 2, 3, 2],
]
num_workers = len(costs)
num_tasks = len(costs[0])

# Variables
# x[i, j] is an array of 0-1 variables, which will be 1 if worker i is assigned to task j.
x = {}
for worker in range(num_workers):
    for task in range(num_tasks):
        for date in range(num_days):
            x[worker, task, date] = m.add_var(var_type=BINARY)

# Constraints
# Each (worker, date) is assigned to at most 1 task.
for worker in range(num_workers):
    for date in range(num_days):
        m += (xsum([x[worker, task, date] for task in range(num_tasks)]) <= 1)

# Each (task,day) is assigned to exacsetly one worker.
worker = 0
for task in range(num_tasks):
    for date in range(num_days):
        if tasks[date][task] == 1:
            m += (xsum([x[worker, task, date] for worker in range(num_workers)]) == 1)

worker = 0
for worker in range(num_workers):
    max_worker_score = 0
    for task in range(num_tasks):
        for date in range(num_days):
            max_worker_score = max_worker_score + costs[worker][task] * x[worker, task, date]
    m += (max_worker_score <= 3)

# for objective
average = 0
objective_terms = []
for i in range(num_workers):
    for j in range(num_tasks):
        for k in range(3):  # num days
            average = average + (costs[i][j] * x[i, j, k])
average = average / num_workers

# Objective
objective_worker_score = []
average_objective = []
for worker in range(num_workers):
    worker_score = 0
    for task in range(num_tasks):
        for date in range(num_days):
            if tasks[date][task] == 1:
                worker_score = worker_score + (costs[worker][task] * x[worker, task, date])
    objective_worker_score.append(worker_score)

''''
sum_score = 0
for worker_score in objective_worker_score:
    sum_score += worker_score
#m.objective = minimize(sum_score)
'''
m.objective = minimize(xsum(objective_worker_score))

m.max_gap = 0.05
status = m.optimize(max_seconds=300)
if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost {} found'.format(m.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for v in m.vars:
        if abs(v.x) > 1e-6:  # only printing non-zeros
            line = '{} : {}'.format(v.name, v.x)
            print(line)
