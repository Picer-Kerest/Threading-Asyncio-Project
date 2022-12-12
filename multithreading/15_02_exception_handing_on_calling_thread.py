import concurrent.futures
import time
from concurrent.futures import CancelledError


def div(divisor, limit):
    """
    Обработка исключения на верхней уровне
    Thread не может обработать исключение на верхнем уровне,
    поэтому используем ThreadPoolExecutor
    """
    print(f'started div = {divisor}')

    result = 0
    for x in range(1, limit):
        if x % divisor == 0:
            result += x
            print(f'divisor={divisor}, x={x}')
        time.sleep(0.2)

    print('raise exception from def')
    raise Exception('bad thing happen!')

    return result


# Пример с Map
if __name__ == '__main__':
    print('started main')

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        res_list = executor.map(div, (3, 5), (15, 25))
        while res_list:
            # Берём результат работы каждого запуска, пока есть элементы
            try:
                cur_res = next(res_list)
                # Следующий элемент
            except StopIteration:
                print('stop iteration excepted')
                break
            except Exception as ex:
                # Одна ошибка на все потоки
                print('generalized exception from main')
                print(repr(ex))

    print('main ended')


# Пример с Submit
# if __name__ == '__main__':
#     print('started main')
#     with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
#         future = executor.submit(div, 3, 15)
#
#         time.sleep(5)
#         print('Nothing happens until...')
#
# Если не проверять результат, то исключение остаётся незамеченным
# Чтобы выявить ошибку, нужно использовать метод result()
# result выкинет исключение, если оно произошло в запущенной функции, в другом Thread'e
# Так как это main Thread, то исключение убьёт программу
# Чтобы обработать это, можно завернуть future в try/except и программа не умрёт
#         try:
#             res = future.result()
#         except CancelledError as ex:
#             print(repr(ex))
#         except TimeoutError as ex:
#             print(repr(ex))
#         except Exception as ex:
#             print(repr(ex))
#              output: Exception('bad thing happen!')
#
#     print('main ended')
