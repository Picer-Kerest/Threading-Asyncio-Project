import concurrent.futures
import threading
import time


class BankAccount:
    def __init__(self):
        self.balance = 100  # shared data/resource
        self.lock_obj = threading.Lock()
    #     Зачастую lock_obj создаётся именно здесь.

    def update(self, transaction, amount):
        print(f'{transaction} started')

        with self.lock_obj:
            # Вместо вызова acquire & release используем with, чтобы вызов происходил автоматически.
            # Из двух потоков lock_obj захватит какой-нибудь первым и пока поток,
            # который захватил lock_obj не исполнит код ниже, второй поток, который пришёл к with,
            # не сможет исполнить этот код
            # В кусок кода, ограждённый lock'ом, может зайти только 1 поток за раз
            tmp_amount = self.balance
            tmp_amount += amount
            time.sleep(1)
            self.balance = tmp_amount
        print(f'{transaction} ended')


if __name__ == '__main__':
    # lock_obj = threading.Lock()
    # print(lock_obj.locked())
    # Метод Lock.locked() возвращает True, если блокировка получена.

    # lock_obj.acquire()
    # print(lock_obj.locked())
    # Как только вызвана acquire, то любой другой поток в защищённый кусок кода зайти не может.

    # lock_obj.release()
    # print(lock_obj.locked())

    acc = BankAccount()
    print(f'Main started. acc.balance = {acc.balance}')

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.map(acc.update, ('refill', 'withdraw'), (100, -200))

    print(f'End of main. Balance = {acc.balance}')
