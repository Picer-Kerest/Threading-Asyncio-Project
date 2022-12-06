import threading

from multithreading.count_three_sum import read_ints, count_three_sum

if __name__ == '__main__':
    print('started main\n')

    ints = read_ints('../data/1Kints.txt')


    # Foreground Thread
    t1 = threading.Thread(target=count_three_sum, args=(ints, ), daemon=True)  # аргументы передаются либо списком, либо tuple
    t1.start() #                        kwargs=dict(ints=ints)
    #                                   Чтобы передавать аргументы именованно
    # Параллельного выполнения здесь быть не может.
    # Сначала один поток, потом другой
    t1.join()

    # Если сделать поток BackGround, то он будет завершён как только основной поток завершит работу
    # В данном случае напечает строки
    print('\nBye!')
    print('ended main\n')
