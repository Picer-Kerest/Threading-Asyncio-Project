import threading
import time

throw = False


def count():
    i = 0

    # Делаем try except здесь, чтобы выловить исключение
    try:
        while True:
            if throw:
                raise ZeroDivisionError()

            i += 1
            print(f'{i=}')
            # output: i=1, i=2..
            time.sleep(1)
    except ZeroDivisionError:
        print('Exception occured')


if __name__ == '__main__':
    print('started main')

    t1 = threading.Thread(target=count)
    t1.start()

    # Если сделать try except здесь, то ничего не будет решено

    # В вызывающем Thread'e мы не можем обработать исключение

    time.sleep(3)

    throw = True
    # После этого будет выкинута ошибка, но приложение будет работать и цикл ниже
    # будет делать вывод без ошибок

    for x in range(1, 5):
        print(f'{x=}')
        time.sleep(1)

    print('ended main')
