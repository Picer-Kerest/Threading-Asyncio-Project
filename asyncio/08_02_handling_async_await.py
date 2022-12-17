import asyncio
import time

import aiohttp


class Photo:
    """
    async await исключение на нижнем уровне, которое не останавливает генератор
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
    # исключение если не подходит по типу
    if not isinstance(album, int):
        raise RuntimeError('invalid album number')
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'

    response = await session.get(url)
    photos_json = await response.json()

    return [Photo.from_json(photo) for photo in photos_json]


async def download_albums(albums):
    """
    Мы можем отловить исключение из photos_by_album здесь.
    Когда мы делаем await, то мы забираем значение.
    Если будет исключение, то мы его отловим и программа продолжит выполнение
    Программа не будет прибита

    Также можем отловить это на уровне async for
    Если сделать это же, но в async for, то до четвёрки мы не дойдём,
    так как после встречи исключения генератор останавливается
    """
    async with aiohttp.ClientSession() as session:
        for album in albums:
            try:
                yield await photos_by_album(f't{album}', album, session)
            except Exception as ex:
                print(repr(ex))


async def main():
    async for photos in download_albums([1, 2, 'a', 4]):
        print_photo_title(photos)


if __name__ == '__main__':
    asyncio.run(main())

    time.sleep(3)
    print('Main ended')
