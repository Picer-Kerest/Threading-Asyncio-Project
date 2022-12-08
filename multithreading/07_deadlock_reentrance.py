import threading

lock_obj = threading.RLock()
# RLock
# Реализует(release) объекты повторной блокировки
# Даёт разрешение на вторичный захват лишь тому потоку, который его уже захватил

print('Acquaire 1st time')
lock_obj.acquire()
# lock_obj = threading.Lock()
# Первый раз захватываем удачно
# Потом пытаемся захватить, но не можем, потому что ждём release, а его нет
# Поэтому застреваем здесь навсегда

print('Acquaire 2nd time')
lock_obj.acquire()

print('Releasing')
lock_obj.release()


# def reentrance():
#     """
#     Рекурсивный вызов функции
#     DeadLock
#     Застреваем на acquire, потому что нет освобождения
#     В любом случае данный код - бесконечная рекурсия
#     """
#     print('start')
#     lock_obj.acquire()
#     print('Acquired')
#     reentrance()
#
#
# reentrance()
