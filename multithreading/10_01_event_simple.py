import threading
import time

event = threading.Event()
# Экземляр класса Event
# По умолчанию False


def test():
    """
    Все потоки продолжат выполнение, когда Event=True
    Тогда мы разблокируем значение wait и пойдём ниже
    event.clear() - сбросить до False
    event.is_set() - Проверка на истинность
    event.set() - установить event=True
    """
    # while not event.is_set()
    while True:
        # Сработает если event=True
        event.wait()
        # Метод Event.wait() блокирует выполнение до тех пор, пока внутренний флаг не станет истинным True.
        print('test')
        time.sleep(2)


event.clear()
# Для сбрасывания значения к False

threading.Thread(target=test).start()

