import concurrent.futures
import threading
import requests

from multithreading.decorators import measure_time


thread_local = threading.local()
# Локальное хранилище для потока.
# То есть session будет создан один раз и больше создаваться не будет


def get_session():
    """
    Получаем Session
    Опирается на thread_local
    """
    if not hasattr(thread_local, 'session'):
        # Если в thread_local нет атрибута session, то мы его создаём.
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    """
    Если session уже создан, то он сюда прилетит
    """
    session = get_session()
    with session.get(url) as response:
        print(f'Read {len(response.content)} from {url}')


@measure_time
def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


if __name__ == '__main__':
    sites = [
        'https://offer.engineerspock.com/',
        'https://enterprisecraftsmanship.com/'
    ] * 80

    download_all_sites(sites)
    # Асинхронный, основанный на threading
    # 4 sec
