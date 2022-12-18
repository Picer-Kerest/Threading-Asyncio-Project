import asyncio

from multithreading.decorators import async_measure_time


async def fetch_doc(doc):
    """
    Эмулируем загрузку документов
    """
    await asyncio.sleep(0.1)
    return doc


async def get_pages(docs):
    """
    Генератор с async for
    """
    for cur_doc in docs:
        doc = await fetch_doc(cur_doc)
        for page in doc:
            await asyncio.sleep(0.3)
            yield page


@async_measure_time
async def main():
    async for page in get_pages(['doc1', 'doc2']):
        print(f'finally {page}')

if __name__ == '__main__':
    asyncio.run(main())
