import asyncio
import time

import aiohttp


class Photo:
    """
    Async For Исключение в главном Thread'e
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
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'

    response = await session.get(url)
    photos_json = await response.json()

    return [Photo.from_json(photo) for photo in photos_json]


async def download_albums(albums):
    async with aiohttp.ClientSession() as session:
        for album in albums:
            # Асинхронный генератор
            if not isinstance(album, int):
                # Если album не типа int, то будет выкинута ошибка и async for прекратит выполнение
                # main enden не будет выполнен. Приложение будет прибито
                raise RuntimeError('invalid album number')
            yield await photos_by_album(f't{album}', album, session)


async def main():
    """
    Нужно заворачивать в try/except не внутренность async for, а сам async for
    """
    try:
        async for photos in download_albums([1, 2, 'a', 4]):
            print_photo_title(photos)
    except Exception as ex:
        print(repr(ex))


if __name__ == '__main__':
    asyncio.run(main())

    time.sleep(3)
    print('Main ended')
