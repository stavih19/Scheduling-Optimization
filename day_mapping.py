import datetime

months_name_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6}
months_num_name = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun'}


def get_serial(date):
    date = date.split('-')

    month = months_name_num[date[1]]
    day = int(date[0])

    return (month - 1) * 31 + day - 1


def get_date(serial):
    month = months_num_name[int(serial / 31) + 1]
    day = serial % 31
    return str(day) + '-' + str(month)
