import asyncio

import aiohttp as aiohttp
import requests

from multithreading.decorators import async_measure_time, measure_time


class Photo:
    def __init__(self, album_id, photo_id, title, url, thumbnail_url):
        self.thumbnail_url = thumbnail_url
        self.url = url
        self.title = title
        self.photo_id = photo_id
        self.album_id = album_id

    @classmethod
    def from_json(cls, obj):
        return Photo(obj['albumId'], obj['id'], obj['title'], obj['url'], obj['thumbnailUrl'])


def print_photo_titles(photos):
    for photo in photos:
        print(f'{photo.title}', end='\n')


def photos_by_album(task_name, album_id, session):
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album_id}'

    response = requests.get(url)
    photos_json = response.json()

    return [Photo.from_json(photo) for photo in photos_json]


@measure_time
def main():
    with requests.Session() as ses:
        # photos = photos_by_album('Task 1', 3, ses)
        # photos_count = 0
        for i, album in enumerate(range(1, 101)):
            photos_in_albums = photos_by_album(f'Task {i + 1}', album, ses)
            # photos_count = sum([len(cur) for cur in photos_in_albums])
        # photos_in_albums = photos_by_album(f'Task {i + 1}', album, ses) for i, album in enumerate(range(2,30))
        # photos_count = sum([len(cur) for cur in photos_in_albums])
        # print(f'{photos_count=}')
    # with aiohttp.ClientSession() as session:
    #     photos = photos_by_album('Task 1', 3, session)
    #     print_photo_titles(photos)

    # async with aiohttp.ClientSession() as session:
    #     photos_in_albums = await asyncio.gather(*(photos_by_album(f'Task {i + 1}', album, session)
    #                                     for i, album in enumerate(range(2,30))))
    #
    #     photos_count = sum([len(cur) for cur in photos_in_albums])
    #     print(f'{photos_count=}')


if __name__ == '__main__':
    main()

    # loop = asyncio.get_event_loop()
    # try:
    #     loop.create_task(main())
    #     loop.run_forever()
    # finally:
    #     loop.close()
