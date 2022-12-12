import threading
import time

from multithreading.count_three_sum import read_ints


class StoppableThread(threading.Thread):
    """
    Мы создали объект, который является задачей и мы манипулируем им как Thread'ом
    super(StoppableThread, self). Так принято
    """
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.stop_event = threading.Event()

    def stop(self):
        """
        set True in stop_event
        Event.set() устанавливает значение внутреннего флага в True
        """
        self.stop_event.set()

    def stopped(self):
        """
        Флажок для понимания статуса stop_event
        Event.is_set() проверяет внутренний флаг
        """
        return self.stop_event.is_set()


class ThreeSumUnitOfWork(StoppableThread):
    """
    Unit of Work абстрагирует поток. Это задача, исполняемая в потоке
    """

    def __init__(self, ints, name='TestThread'):
        """
        super(), потому что нужно обратиться к базовому классу Thread.
        ints передаётся как аргумент, а name - атрибут Thread

        stop_event здесь определять не нужно, он есть в базовом классе
        """
        super().__init__(name=name)
        self.ints = ints
        #  self.stop_event = threading.Event()

    def run(self):
        """
        Переопределяем run()
        Вызывается автоматически, из-за наследования Thread.
        Поэтому на объекте нашего класса можно будет вызывать start()

        Thread.getName() используется для получения имени потока.
        """

        print(f'{self.name} starts')

        self.count_three_sum(self.ints)

        print(f'{self.name} ends')

    # def stop(self):
    #     self.stop_event.set()

    def count_three_sum(self, ints):
        print(f'started count_three_sum')

        n = len(ints)
        counter = 0

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if super().stopped():
                        print('Task was Cancelled')
                        counter = -1
                        return counter

                    if ints[i] + ints[j] + ints[k] == 0:
                        counter += 1
                        print(f'Triple found: {ints[i]}, {ints[j]}, {ints[k]}', end='\n')

        print(f'ended count_three_sum. Triplets counter={counter}')
        return counter


if __name__ == '__main__':
    print('started main')

    ints = read_ints('..\\data\\1Kints.txt')

    task = ThreeSumUnitOfWork(ints)
    task.start()

    time.sleep(3)

    task.stop()

    task.join()

    print(f'Flag status: {task.stopped()}')
    print('ended main')
