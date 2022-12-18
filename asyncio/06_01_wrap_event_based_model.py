import asyncio
import threading
import time


class Terminal:

    async def start(self):
        """
        Оборачиваем работу, которая исполняется в отдельном потоке
        Результат возвращаем клиенту для этого:
        1. Получаем запущенный цикл событий
        2. Создаём Future, в который будет записываться результат

        В итоге обернули паттерн работы с callback'om,
        который шёл через отдельный Thread, в паттерн AsyncAwait
        Отдали корутину, с которой можно работать через Await
        """
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        t = threading.Thread(target=self.run_cmd, args=(loop, future, ))
        t.start()

        return await future

    def run_cmd(self, loop, future):
        """
        После трёх секунд простоя, которые делаются синхронно,
        но в отдельном Thread'e, делаем вызов

        loop.call_soon_threadsafe() потокобезопасный обратный вызов

        Future.set_result() Присваивает результат объекту Future

        loop.call_soon_threadsafe(future.set_result, 1)
        Единица - то, что будет выведено при завершении программы

        В итоге во Future запишется результат,
        """
        time.sleep(3)
        loop.call_soon_threadsafe(future.set_result, 'Successful')


async def main():
    t = Terminal()
    result = await t.start()
    print(result)


if __name__ == '__main__':
    asyncio.run(main())

