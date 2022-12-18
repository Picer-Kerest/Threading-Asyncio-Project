import asyncio
from asyncio import FIRST_EXCEPTION, ALL_COMPLETED

import aiohttp


class Photo:
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
    print(f'{task_name=}')
    if not isinstance(album, int):
        await asyncio.sleep(2)
        raise RuntimeError('Invalid album number')

    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'
    response = await session.get(url)
    photos_json = await response.json()

    sleeping_period = 3 if task_name == 't3' else 1
    # Период сна для тасок
    await asyncio.sleep(sleeping_period)

    print(f'Finished task={task_name}')
    return [Photo.from_json(photo) for photo in photos_json]


async def main_wait():
    async with aiohttp.ClientSession() as session:
        tasks = [
            photos_by_album('t1', 1, session),
            photos_by_album('t2', 2, session),
            photos_by_album('t3', 3, session),
            photos_by_album('ta', 'a', session),
            photos_by_album('t4', 4, session)
        ]

        photos = []

        done_tasks, pending_tasks = await asyncio.wait(tasks, return_when=ALL_COMPLETED)
        # asyncio.wait имеет параметр return_when=ALL_COMPLETED
        # Когда return_when=ALL_COMPLETED, то все правильно переданные таски выполняются
        # а невалидные таски прибиваются

        # Если return_when=FIRST_EXCEPTION, то при получении исключения
        # таски в состоянии pending отменяются

        for pending_task in pending_tasks:
            print(f'Cancelling {pending_task}')
            pending_task.cancel()

        for done_task in done_tasks:
            try:
                result = done_task.result()
                photos.extend(result)
            except Exception as ex:
                print(repr(ex))

        # print_photo_title(photos)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(main_wait())
        loop.run_forever()
    finally:
        print('Loop close')
        loop.close()

