import asyncio


class ErrorThatShouldCancelOtherTasks(Exception):
    pass

# Ситуация когда cancel на Future не работает


async def my_sleep(secs):
    print(f'task {secs}')
    await asyncio.sleep(secs)
    print(f'task {secs} finished sleeping')

    if secs == 5:
        raise ErrorThatShouldCancelOtherTasks('5 is forbidden')
    print(f'slept for {secs} secs')


async def main_cancel_tasks():
    """
    gather на тасках
    Если есть ошибка, то отменяет таски в цикле
    Первая отработает, вторая улетит в ошибку, а остальные отменятся

    Поэтому всегда нужно делать отмену на тасках
    Отмену на Future делать не нужно
    """
    tasks = [asyncio.create_task(my_sleep(secs)) for secs in [2, 5, 7]]
    sleepers = asyncio.gather(*tasks)
    print('awaiting')
    try:
        await sleepers
    except ErrorThatShouldCancelOtherTasks:
        print(f'Fatal Error. Canceling...')
        for t in tasks:
            # print(f'cancelling {t}')
            # print(t.cancel())
            t.cancel()
    finally:
        await asyncio.sleep(5)


async def main_cancel_future():
    """
    Мы должны провалиться на второй таске
    При выводе будет видно, что третья таска отработала, несмотря на ошибку второй.
    Чтобы решить эту проблему, нужно воспользоваться тасками
    """
    sleepers = asyncio.gather(*[my_sleep(secs) for secs in [2, 5, 7]])
    print('awaiting')
    try:
        await sleepers
    except ErrorThatShouldCancelOtherTasks:
        print(f'Fatal Error. Canceling...')
        sleepers.cancel()
    finally:
        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main_cancel_tasks())
