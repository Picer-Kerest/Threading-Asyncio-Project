import threading
import time

event = threading.Event()
# Экземляр класса Event
# По умолчанию False


# Сначала будет идти подготовка потоков, а потом их запуск
# Когда все потоки будут запущены, только тогда код после event.wait() будет выполнен для всех потоков.


def image_handler():
    thr_num = threading.current_thread().name
    print(f'Идёт подготовка изображения из потока [{thr_num}]')
    event.wait()
    print(f'Изображение отправлено')


for t in range(10):
    threading.Thread(target=image_handler, name=str(t)).start()
    print(f'\nПоток [{t}] запущен')
    time.sleep(0.5)


if threading.active_count() >= 10:
    event.set()
# threading.active_count() используется для подсчета активных в данный момент или запущенных потоков.

