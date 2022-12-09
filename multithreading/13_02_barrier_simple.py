import time
import threading
from threading import current_thread

# Противоположный Semaphore'y
# Заранее указываем количество потоков
# Они запускаются, и когда они дойдут до вызова метода wait,
# то будут ждать пока эти 5 потоков не вызовут этот же метод wait,
# только после того как все 5 потоков его вызвали, только тогда мы разблокируемся и продолжим выполнение


def test(barrier):
    time.sleep(2)
    print(f'Поток [{current_thread().name}] запущен')

    barrier.wait()
    # Всем потокам нужно будет ждать пока они не дойдут до вызова wait
    # Как только они дойдут до вызова wait, тогда мы продолжим выполнение кода ниже
    print(f'Поток [{current_thread().name}] преодолел барьер')


# Барьер будет ждать выполнения пяти потоков
bar = threading.Barrier(5)
for i in range(5):
    threading.Thread(target=test, args=(bar, ), name=f'thr-{i}').start()

