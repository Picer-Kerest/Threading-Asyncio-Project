import asyncio


async def tick():
    print('Tick')
    await asyncio.sleep(1)
    print('Tock')

    # возвращает текущий EventLoop
    loop = asyncio.get_running_loop()
    if loop.is_running():
        print('loop is still running')


async def main():
    awaitable_obj = asyncio.gather(tick(), tick(), tick())
    # gather возвращает awaitable_obj
    # asyncio.all_tasks() возвращает множество еще незавершенных задач asyncio.Task, запущенных циклом loop.
    for task in asyncio.all_tasks():
        print(task, end='\n')

    # Делаем await на awaitable_obj
    await awaitable_obj


if __name__ == '__main__':

    # get_event_loop вызывает set_event_loop и возвращает объект event loop
    # Также делает цикл событий основным

    loop = asyncio.new_event_loop()
    # Создает новый объект цикла событий.
    asyncio.set_event_loop(loop)
    # Устанавливает loop как текущий цикл событий для текущего потока ОС.
    try:
        loop.create_task(main())
        # Планируем выполнение корутины
        loop.run_forever()
        # run_forever() запускает цикл обработки событий, пока не будет вызван stop().
        print('coroutines have finished')
    # Для выхода с помощью Ctrl + C
    except KeyboardInterrupt:
        print('Manually closed app')
    finally:
        loop.close()
        print('loop is closed')
        print(f'loop is closed = {loop.is_closed()}')
