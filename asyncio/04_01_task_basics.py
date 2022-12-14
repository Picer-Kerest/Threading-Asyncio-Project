import asyncio


async def tick():
    print("Tick")
    await asyncio.sleep(1)
    print("Tock")
    return 'Tick-Tock'


async def main():
    t1 = asyncio.create_task(tick(), name='Tick-1')
    t2 = asyncio.ensure_future(tick())
    # ensure_future не может принимать аргумента name

    # Для запуска по очереди
    # await t1
    # await t2

    # запускает
    results = await asyncio.gather(t1, t2)

    print(f'{t1.get_name()}. Done = {t1.done()}')
    print(f'{t2.get_name()}. Done = {t2.done()}')

    # выводит результаты благодаря return 'Tick-Tock'
    for x in results:
        print(x)

if __name__ == '__main__':
    asyncio.run(main())




