import asyncio
import time

import aiohttp


class Photo:
    """
    Переброс исключения из callback, навешенного на create_task
    Gather Return_exceptions=true
    Позволяет взять результаты из успешно выполненных задач и получить список исключений из проваленных.
    Для этого нужно проставить аргумент
    """
    def __init__(self, album_id, photo_id, title, url, thumbnail_url):
        self.url = url
        self.thumbnail_url = thumbnail_url
        self.title = title
        self.photo_id = photo_id
        self.album_id = album_id

    @classmethod
    def from_json(cls, obj):
        return Photo(obj['albumId'], obj['id'], obj['title'], obj['url'], obj['thumbnailUrl'])


def print_photo_title(photos):
    for photo in photos:
        print(f'{photo.title}', end='\n')


async def photos_by_album(task_name, album, session):
    if not isinstance(album, int):
        raise RuntimeError('invalid album number')

    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'

    response = await session.get(url)
    photos_json = await response.json()

    return [Photo.from_json(photo) for photo in photos_json]


async def download_albums(albums):
    async with aiohttp.ClientSession() as session:
        photos = []
        for album in albums:
            photos.extend(await photos_by_album(f't{album}', album, session))
    return photos


async def main1():
    task1 = asyncio.create_task(download_albums([1, 2, 'a', 4]))

    # result = await task1
    # Если сделать так запустить,
    # то будет выброшено исключение и приложение упадёт,
    # то есть всё что ниже выполнено не будет
    # Если сделать то же самое в блоке try/except,
    # то исключение будет отловлено и программа не будет убита
    # Здесь мы callback на task'y не навешивали
    # Здесь мы сделали await на task'e

    try:
        result = await task1
    except Exception as ex:
        print(repr(ex))

    print('sleeping in main')
    await asyncio.sleep(3)
    print('after sleep')


def handle_result(fut):
    """
    Исключение будет выкинуто, но приложение продолжит работу

    Если вы хотите чтобы это убило приложение, то ничего не получится
    Нужно делать либо await на task'e
    Либо сделать так, чтобы переменная была доступна в main thread'e
    """
    print(fut.result())


async def main2():
    """
    Future.add_done_callback() добавляет обратный вызов callback,
    который будет запускаться, когда объект Future будет выполнен
    В нашем случае когда будет выполнен handle_result
    """
    task1 = asyncio.create_task(download_albums([1, 2, 'a', 4]))
    task1.add_done_callback(handle_result)

    print('sleeping in main')
    await asyncio.sleep(3)
    print('after sleep')


async def main_gather():
    """
    Сессия для передачи параметра

    Если return_exceptions=True нет:
    Если в одной из task'ок исключение,
    то результата не увидим даже из тех task'ок, которые завершены успешно

    Если хочется получить результаты, несмотря на исключение,
    то нужно использовать return_exceptions=True
    Теперь мы сможем увидеть и то, что выполнилось успешно и то, что выполнилось с ошибкой
    """
    async with aiohttp.ClientSession() as session:
        tasks = [
            photos_by_album('t1', 1, session),
            photos_by_album('t2', 2, session),
            photos_by_album('ta', 'a', session),
            photos_by_album('t4', 4, session),

        ]
        photos = []
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, Exception):
                print(repr(res))
            else:
                photos.extend(res)

        print_photo_title(photos)


if __name__ == '__main__':
    asyncio.run(main_gather())

    time.sleep(3)
    print('Main ended')
