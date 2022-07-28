import csv
import os
import random
import time
from datetime import datetime
from pprint import pprint
from threading import Timer
import matplotlib.pyplot as plt

#### Приоритеты:
# 1. Нир = research
# 2. Кандидатский по НИР = practice
# 3. Зачеты = practice
# 4. ISTQB = istqb
# 5. CAE = cae
# 6. Проф.чтение (Ляпунов) = practice


ResearchQuestionsTimeout = 60 * 10
AwareLimit = 15
MathTasksNumber = 8
OrdersSearchTimeout = 60 * 10
OrdersPerformingTimeout = 60 * 15
Beat = 45


def istqb():
    ans = input('Study theory - 1 or solve tests - 2? ')
    if ans == "1":
        input('Open the istqb document. Are you ready? (enter to start) ')
        t = time.time()
        input('Закончила изучение? ')
    elif ans == "2":
        input('Открой тест. Enter to start ')
        t = time.time()
        input('Закончила изучение? ')
    sum_time = (time.time() - t) / 60
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "istqb", sum_time)
    print("Time: ", sum_time)


def orders():
    ans = input('Search new orders - 1 or solve mine - 2? ')
    input('Go to https://zaochnik1.com/author_v2/my-orders/started?page_size=25&tab=0. Are you ready? (enter to start '
          'timer) ')
    t = time.time()
    if ans == "1":
        timer = Timer(OrdersSearchTimeout, out_of_time)
        timer.start()
        input('Закончила подбор задач? Если тебя назначат - отметь данные в orders.scv ')
        timer.cancel()
    else:
        input('Закончила решение заказа? ')
    sum_time = (time.time() - t) / 60
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "orders", sum_time)
    print("Time: ", sum_time)


def out_of_time():
    os.system("say осталось 10 секунд")
    count_to(AwareLimit)
    os.system("say время вышло")


def wait_for_question_input(timeout):
    t = time.time()
    timer = Timer(timeout, out_of_time)
    timer.start()
    question_name = input('Какой есть вопрос? - ')
    timer.cancel()
    sum_time = (time.time() - t) / 60
    print("Time: ", sum_time)
    with open('research.csv', "a") as statistics_file:
        statistics_file.write(
            "\n" + datetime.today().strftime('%d.%m.%y') + "," + question_name + "," + str(sum_time) + "," + "active")
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "research", sum_time)


def research(timeout):
    ans = "да"
    i = 0
    while ans == "да":
        ans = input('Есть вопросы? (да/нет) ')
        if ans == "да":
            wait_for_question_input(timeout)
        ans = input('Начнем трудиться над ответами (да/нет)? ')
        if ans == "да":
            with open('research.csv') as tasks_file:
                tasks_data = csv.reader(tasks_file)
                lines = list(tasks_data)
                for row in lines:
                    if row[3] == 'active':
                        print('Текущий нерешенный вопрос: ')
                        print('\t', row[1])
                        t = time.time()
                        commit = input('\n Коммит готов -> название коммита (?): ')
                        if commit == '?':
                            wait_for_question_input(timeout)
                            break
                        else:
                            lines[i][3] = 'resolved'
                            lines[i].append(datetime.today().strftime('%d.%m.%y'))
                            lines[i].append(commit)
                            sum_time = (time.time() - t) / 60
                            lines[i].append(sum_time)
                            add_to_statistics(datetime.today().strftime('%d.%m.%y'), "research", sum_time)
                            writer = csv.writer(open('research.csv', 'w'))
                            writer.writerows(lines)
                            print(datetime.today().strftime('%d.%m.%y'))
                            print("Time: ", sum_time)
                            i += 1
                    else:
                        i += 1
                ans = input('Продолжаем разрешать вопросы? (да/нет) ')
                if ans == 'да':
                    continue
                else:
                    break
                print('No more active tasks! Create new. ')


def anki_start():
    input('Anki - первый короткий подход. Открыла? ')
    t = time.time()
    input('Решила колоду с новым словом? ')
    sum_time = (time.time() - t) / 60
    print("Time: ", sum_time)
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "cae", sum_time)


def anki_finish():
    input('Anki - заключительный подход. Открыла? ')
    t = time.time()
    input('Повторила все колоды? ')
    sum_time = (time.time() - t) / 60
    print("Time: ", sum_time)
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "cae", sum_time)


def cae_listening():
    input('CAE Listening ')
    print("Go to https://engexam.info/cae-listening-practice-tests/ ")
    with open('cae_listening.csv') as tasks_file:
        tasks_data = csv.reader(tasks_file)
        for row in tasks_data:
            n = row
    print("Прошлый раз был тест №: ", row[0])
    test_name = input('Какой тест решаем? ')
    print("Прошлый раз была часть: ", row[1])
    part_name = input('Какую часть решаем? ')
    ans = "нет"
    t = time.time()
    while ans == "нет":
        ans = input('Прочитай вопросы теста. Понятно? (да/нет) ')
    input('Послушай первый раз аудио, жми, когда готово ')
    ans = input('Попробуй решить тесты. Все решила? Все ли ясно и прозрачно? (да/нет) ')
    if ans != "да":
        input('Послушай еще раз аудио, жми, когда готово ')
        ans = input('Попробуй снова решить тесты. Все ли ясно и прозрачно? (да/нет) ')
        if ans != "да":
            input('Прочитай транскрипт. Поняла? ')
            input('Послушай еще раз аудио, жми, когда готово ')
            input('Попробуй снова решить тесты. Все ли ясно и прозрачно? (да/нет) ')
    ans = input('Открой ответы и напиши результат - количество правильных ответов из скольки ')
    input('Разбери ошибки, если есть. Готово? ')
    input('Выпиши незнакомые фразы в анки. Готово? ')
    print(datetime.today().strftime('%d.%m.%y'))
    sum_time = (time.time() - t) / 60
    print("Time: ", sum_time)
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "cae", sum_time)
    with open('cae_listening.csv', "a") as statistics_file:
        statistics_file.write("\n" + test_name + "," + part_name + "," + str(sum_time) + "," + ans)


def generate_example():
    num1 = random.randint(12, 99)
    str_num1 = str(num1)
    num2 = random.randint(12, 19)
    str_num2 = str(num2)
    left_side = str_num1 + " на " + str_num2
    right_side = num1 * num2
    print(num1, "*", num2, "=")
    return left_side, right_side


def get_answer(ans):
    while True:
        try:
            user_line = input('Your answer: ')
            if int(user_line) == ans:
                pprint("Yep! ")
                return
            else:
                os.system("say нет")
                pprint("Try again ")
        except ValueError:
            pprint("Parsing error... ")


def start_calculus(num_ex):
    input('Multiplication ..*.. ')
    t = time.time()
    for i in range(num_ex):
        command, ans = generate_example()
        os.system("say " + command)
        get_answer(ans)
    sum_time = (time.time() - t) / 60
    print("Time: ", sum_time)
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "math", sum_time)


def count_to(t, num_beat=60):
    for i in range(t):
        command = str(i + 1)
        time.sleep(num_beat / 60)
        os.system("say " + command)


def start_stretch(beat):
    input('Stretch ')
    with open('stretch.csv') as tasks_file:
        tasks_data = csv.reader(tasks_file)
        t = time.time()
        for row in tasks_data:
            if "#" == row[0][0]:
                continue
            else:
                task = row[0]
                length = int(row[1])
                os.system("say " + task + ' ' + str(length))
                count_to(length, beat)
    print(datetime.today().strftime('%d.%m.%y'))
    sum_time = (time.time() - t) / 60
    print("Time: ", sum_time)
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "stretch", sum_time)


def start_equilibrium(beat):
    input('Equilibrium ')
    with open('equilibrium.csv') as tasks_file:
        tasks_data = csv.reader(tasks_file)
        t = time.time()
        for row in tasks_data:
            if "#" == row[0][0]:
                continue
            else:
                task = row[0]
                length = int(row[1])
                os.system("say " + task + ' ' + str(length))
                count_to(length, beat)
    print(datetime.today().strftime('%d.%m.%y'))
    sum_time = (time.time() - t) / 60
    print("Time: ", sum_time)
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "equilibrium", sum_time)


def show_statistics():
    fig, ax = plt.subplots()
    stat_task_dict = {}
    with open('statistics.csv', "r") as statistics_file:
        data = csv.reader(statistics_file)
        for row in data:
            stat_task_dict[row[0]] = {}

    with open('statistics.csv', "r") as statistics_file:
        data = csv.reader(statistics_file)
        for row in data:
            try:
                if isinstance(stat_task_dict[row[0]][row[1]], list):
                    stat_task_dict[row[0]][row[1]] = stat_task_dict[row[0]][row[1]][0] + float(row[2])
                else:
                    stat_task_dict[row[0]][row[1]] = [float(row[2])]
            except KeyError:
                stat_task_dict[row[0]][row[1]] = [float(row[2])]

    dates = []
    math = []
    stretch = []
    for date in stat_task_dict:
        dates.append(date)
        try:
            if isinstance(stat_task_dict[date]['math'], list):
                math.append(stat_task_dict[date]['math'][0])
            else:
                math.append(stat_task_dict[date]['math'])
        except KeyError:
            math.append(0)
        try:
            if isinstance(stat_task_dict[date]['stretch'], list):
                stretch.append(stat_task_dict[date]['stretch'][0])
            else:
                stretch.append(stat_task_dict[date]['stretch'])
        except KeyError:
            stretch.append(0)

    ax.bar(dates, math, color='b')
    ax.bar(dates, stretch, bottom=math, color='r')
    plt.show()


def add_to_statistics(timestamp, task, duration):
    with open('statistics.csv', "a") as statistics_file:
        statistics_file.write("\n" + timestamp + "," + task + "," + str(duration))


def practice():
    activity = input('What activity are you going to do? ')
    t = time.time()
    now_date = datetime.now().strftime('%d.%m.%y(%H:%M:%S)')
    input('Are you finish? ')
    sum_time = (time.time() - t) / 60
    print("Time: ", sum_time)
    add_to_statistics(datetime.today().strftime('%d.%m.%y'), "math", sum_time)
    with open('math_activities.csv', "a") as math_activities_file:
        math_activities_file.write("\n" + now_date + "," + activity + "," + str(sum_time))


def start_activity():
    task = input("What are you going to do (math - 1, cae - 2, acrobatics - 3, istqb - 4)? ")
    if task == "1":
        task = input("Namely (research - 1, calculate - 2, practice - 3, orders - 4)? ")
        if task == "1":
            research(timeout=ResearchQuestionsTimeout)
        elif task == "2":
            start_calculus(num_ex=MathTasksNumber)
        elif task == "3":
            practice()
        elif task == "4":
            orders()
        else:
            print("Sorry!.. don't know such task, teach me! ")
    elif task == "2":
        task = input("Namely (words - 1, listening - 2)? ")
        if task == "1":
            task = input("Is anything new to learn (yes - 1, no - 2)? ")
            if task == "1":
                anki_start()
            elif task == "2":
                anki_finish()
            else:
                print("Sorry!.. don't know such task, teach me! ")
        elif task == "2":
            cae_listening()
        else:
            print("Sorry!.. don't know such task, teach me! ")
    elif task == "3":
        task = input("Namely (stretch - 1, equilibrium - 2)? ")
        if task == "1":
            start_stretch(beat=Beat)
        elif task == "2":
            start_equilibrium(beat=Beat)
        else:
            print("Sorry!.. don't know such task, teach me! ")
    elif task == "4":
        istqb()
    else:
        print("Sorry!.. don't know such task, teach me! ")


start_activity()
