import asyncio


async def fetch_doc(doc):
    """
    Эмулируем загрузку документов
    """
    await asyncio.sleep(1)
    return doc


async def get_docs(docs, token):
    """
    Здесь генератора не будет
    Также будет передаваться token, чтобы понимать,
    нужно ли совершать кооперативную отмену
    """
    pages = []
    for cur_doc in docs:
        if token:
            pass