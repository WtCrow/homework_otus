from scipy.stats import norm
from statistics import mean
from math import sqrt


def check_hypothesis():
    """Проверка гипотезы A/B-тестирования

    Вводятся результаты A/B-тестирования, уровень значимости и знак альтернативной гипотезы.

    В ответ будут выведены значение статистики критерия, P-val, доверительные интервалы
    и ответ, отвергается гипотеза или принимается

    P. S. Формат вводимых данных не проверяется

    """
    # n11, n12
    print('Введите кол-во "успехов" 1-ой серии')
    successes_A = int(input())
    print('Введите кол-во "неудач" 1-ой серии')
    fails_A = int(input())
    # n1.
    sum_A = successes_A + fails_A

    # n21, n22
    print('Введите кол-во "успехов" 2-ой серии')
    successes_B = int(input())
    print('Введите кол-во "неудач" 2-ой серии')
    fails_B = int(input())
    # n2.
    sum_B = successes_B + fails_B

    # n, n.1
    total_cases = sum_A + sum_B
    sum_successes = successes_A + successes_B

    # значение статистики критерия
    T = (successes_A / sum_A - successes_B / sum_B)\
        / sqrt((sum_successes / total_cases) * (1 - sum_successes / total_cases) * (1 / sum_A + 1 / sum_B))

    print('Введите уровень значимости')
    a = float(input())

    print('Введите знак альтернативной гипотезы (Ha) (<, >, !=)')
    sign = input()
    confidence_interval = {'<': (norm.ppf(a), float('inf')),
                           '>': (-float('inf'), norm.ppf(1 - a)),
                           '!=': (norm.ppf(a / 2), norm.ppf(1 - a / 2))
                           }[sign]
    # answer = 'принимается' if confidence_interval[0] < T < confidence_interval[1] else 'отвергается'

    # P-value
    P = {'<': norm.cdf(T),
         '>': 1 - norm.cdf(T),
         '!=': min(2 * norm.cdf(T), 2 - 2 * norm.cdf(T))
         }[sign]
    answer = 'принимается' if a < P else 'отвергается'

    print(f'Значение статистики критерия: {T}')
    print(f'P-value: {round(P, 5)}')
    print(f'Доверительный интервал: ({confidence_interval[0]}, {confidence_interval[1]})')
    print(f'При уровне значимости {a} основная гипотеза (p1 == p2) {answer}')


def check_wilcoxon():
    """Проверка гипотезы с помощью критерия Вилкоксона

    Через пробел вводятся результаты наблюдений, уровень значимости и знак альтернативной гипотезы

    В ответ будут выведены значение критерия Вилкоксона, P-val, доверительные интервалы
    и ответ, отвергается гипотеза или принимается

    P. S. Формат вводимых данных не проверяется

    """
    print('Введите результат 1-го наблюдения (через пробел)')
    X = input().strip().split(' ')
    X = [{'val': float(x), 'set': 1} for x in X]
    m = len(X)

    print('Введите результат 2-го наблюдения (через пробел)')
    Y = input().strip().split(' ')
    Y = [{'val': float(y), 'set': 2} for y in Y]
    n = len(Y)

    # объединяем массивы
    united_array = X + Y
    united_array.sort(key=lambda x: x['val'])
    # каждому элементу присваиваем ранк равный номеру элемента
    for ind, item in enumerate(united_array):
        item['rank'] = ind + 1

    # усредняем ранк одинаковых элементов
    skip_item = None  # элемент условия для уменьшения кол-ва рассчетов
    for item in united_array:
        if item['val'] == skip_item:
            continue

        # если элементов с таким val > 1, то считаем средний ранк и присваиваем его всем подобным элементам
        ranks = [x['rank'] for x in united_array if item['val'] == x['val']]
        if len(ranks) > 1:
            rank = mean(ranks)
            for temp_item in united_array:
                if temp_item['val'] == item['val']:
                    temp_item['rank'] = rank
            skip_item = item['val']  # пропускаем последующие элементы с таким же val

    W = sum([item['rank'] for item in united_array if item['set'] == 2])
    M = (n / 2) * (m + n + 1)  # мат ожидание
    D = (m * n / 12) * (m + n + 1)  # дисперсия
    W_criterion = (W - M) / sqrt(D)

    print('Введите уровень значимости')
    a = float(input())

    print('Введите знак альтернативной гипотезы (Ha) (<, >, !=)')
    sign = input()
    confidence_interval = {'<': (norm.ppf(a), float('inf')),
                           '>': (-float('inf'), norm.ppf(1 - a)),
                           '!=': (norm.ppf(a / 2), norm.ppf(1 - a / 2))
                           }[sign]
    # answer = 'принимается' if confidence_interval[0] < W_ < confidence_interval[1] else 'отвергается'

    P = {'<': norm.cdf(W_criterion),
         '>': 1 - norm.cdf(W_criterion),
         '!=': min(2 * norm.cdf(W_criterion), 2 - 2 * norm.cdf(W_criterion))
         }[sign]
    answer = 'принимается' if a < P else 'отвергается'

    print(f'Значение критерия Вилкоксона: {W_criterion}')
    print(f'P-value: {round(P, 5)}')
    print(f'Доверительный интервал: ({confidence_interval[0]}, {confidence_interval[1]})')
    print(f'При уровне значимости {a} основная гипотеза (θ == 0) {answer}')


check_hypothesis()
check_wilcoxon()
