import threading
import time

cond = threading.Condition()

# Можно давать уведомление одному потоку или всем потокам


def f1():
    while True:
        with cond:
            # Прописываем менеджер контекста, чтобы захватить и освободить объект автоматически
            cond.wait()
            # метод wait продолжит выполнение после вызова notify
            print('Событие получено')


def f2():
    for i in range(100):
        if i % 10 == 0:
            with cond:
                cond.notify()
        else:
            print(f'Empty For: {i}')
        time.sleep(0.1)


threading.Thread(target=f1).start()
threading.Thread(target=f2).start()

