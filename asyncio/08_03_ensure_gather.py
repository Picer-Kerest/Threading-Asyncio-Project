import asyncio
import time

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
    try:
        result = await task1
    except Exception as ex:
        print(repr(ex))

    print('sleeping in main')
    await asyncio.sleep(3)
    print('after sleep')


def handle_result(fut):
    print(fut.result())


async def main2():
    task1 = asyncio.create_task(download_albums([1, 2, 'a', 4]))
    task1.add_done_callback(handle_result)

    print('sleeping in main')
    await asyncio.sleep(3)
    print('after sleep')


async def main_gather():
    async with aiohttp.ClientSession() as session:

        tasks = [
            photos_by_album('t1', 1, session),
            photos_by_album('t2', 2, session),
            photos_by_album('ta', 'a', session),
            photos_by_album('t4', 4, session),

        ]
        photos = []
        # Без использования return_exceptions=True, gather не выведет результат работы исправных тасков.
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
