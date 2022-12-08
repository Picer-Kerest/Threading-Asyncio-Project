import concurrent.futures

from multithreading.count_three_sum import read_ints, count_three_sum

if __name__ == '__main__':
    print('started main')

    # data = read_ints("..\\data\\1Kints.txt")
    data = read_ints('../data/1Kints.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Последовательный запуск, но вывод псевдо-параллельный
        # Вместо огромного количества вызова submit, используем map.
        results = executor.map(count_three_sum, (data, data), ('t1', 't2'))
        # results = executor.map(count_three_sum, (data, data, data, data), ('t1', 't2', 't3', 't4'))
        # Если max_workers = 2, а аргументов 4, то сначала отработает t1, t2, а потом t3, t4
        # Первый аргумент и второй аргумент. Передаются в виде кортежа. Перечисляется то, что будет передаваться
        # в функцию в качестве параметра.
        # map возвращает генератор
        # map вызывается target=count_three_sum столько раз, сколько указано аргументов.
        # max_workers может быть 4, но аргументов две пары, значит map будет вызван 2 раза

        print('After map')
        for r in results:
            print(f'{r=}')
        print('End of map')
        # Блокирующий вызов. Не будет выведено, пока потоки активны

    print('ended main')
