import time
from threading import Thread, BoundedSemaphore, current_thread


max_connection = 5
# Максимальное количество потоков, которые могут работать одновременно

pool = BoundedSemaphore(value=max_connection)
# Блокировщик. Проверяет, не превышает ли его текущее значение его начальное значение value.
# Если это так, то возникает исключение ValueError.


def test():
    """
    Выводит имя пяти, потому что max=5, далее спит,
    освобождает потоки и на их место вставляет новые.
    Далее выводит имена остальных пяти, спустя 3 секунды.
    """
    with pool:
        slp = 1
        print(current_thread().name)
        time.sleep(slp)


for i in range(10):
    Thread(target=test).start()

