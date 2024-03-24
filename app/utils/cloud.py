import yadisk


async def create_folder_disk(y: yadisk.AsyncClient, path: str):
    if not await y.exists(path):
        await y.mkdir(path)
