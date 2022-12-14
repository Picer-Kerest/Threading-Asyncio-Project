import asyncio
# import time

from multithreading.decorators import async_measure_time


async def tick():
    """
    Всё что ест много времени, должно быть асинхронно
    time.sleep(1) = asyncio.sleep(1)
    Код после await'a будет исполняться после того завершится асинхронный вызов await
    Как только вызов завершится, то исполнение продолжится со строчки: print('Tock')

    Все 3 потока пришли сюда, сделали принт Tick, далее подождали секунду и сделали вывод Tock

    Вызов не блокирующий
    """
    print('Tick')
    await asyncio.sleep(1)
    print('Tock')


@async_measure_time
async def main():
    """
    Чтобы запустить несколько функций и использовать await,
    нужно использовать asyncio.gather
    """
    await asyncio.gather(tick(), tick(), tick())
    # for _ in range(3):
    #     tick()


if __name__ == '__main__':
    asyncio.run(main())
    # Event Loop

