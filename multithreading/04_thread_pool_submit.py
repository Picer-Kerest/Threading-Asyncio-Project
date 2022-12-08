import concurrent.futures
import time


def div(divisor, limit):
    print(f'\nstarted div={divisor}')

    result = 0
    for x in range(1, limit):
        if x % divisor == 0:
            result += x
            # print(f'divisor={divisor}, x={x}')
        time.sleep(0.2)
    print(f'\nended div={divisor}', end='\n')
    return result


if __name__ == '__main__':
    print('started main')

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Потоки Foreground
        # Последовательный запуск, но вывод псевдо-параллельный
        futures.append(executor.submit(div, 5, 25))
        futures.append(executor.submit(div, 3, 25))
        # shutdown вызывается автоматически

        while futures[0].running() and futures[1].running():
            # Пока оба поток запущены
            print('.', end='')
            time.sleep(0.5)

        for f in futures:
            print(f'{f.result()}')
            # Вывод результата

    print('After with block')
    # Будет отображено после выполнения блока submit

    #  Без with
    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # executor.submit(div, 3, 25)
    # executor.submit(div, 5, 25)
    #
    # executor.shutdown(wait=False)
    # Если False, то отработает print сначала, а потом будет вывод функций
    # print('\nmain ended')
