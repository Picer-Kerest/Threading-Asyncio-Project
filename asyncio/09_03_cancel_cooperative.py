import asyncio
import threading


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
        if token.is_set():
            # Event.is_set() проверяет внутренний флаг
            break
        doc = await fetch_doc(cur_doc)
        for page in doc:
            pages.append(page)
    return pages


def get_response(token):
    reply = input('Want to cancel or no? [y/n]: ')
    if reply == 'y':
        token.set()
        # Event.set() устанавливает значение внутреннего флага в True


async def main():
    """
    asyncio loop и loop обрабатывающий события,
    поступающие от пользователя, это разные потоки.
    """
    token = threading.Event()
    docs = ['doc1', 'doc2', 'doc3', 'doc4', 'doc5', 'doc6', 'doc7']
    task = asyncio.create_task(get_docs(docs, token))

    t = threading.Thread(target=get_response, args=(token, ))
    t.start()

    result = await task
    for doc in result:
        print(f'{doc}', end=' ')


if __name__ == '__main__':
    asyncio.run(main())

