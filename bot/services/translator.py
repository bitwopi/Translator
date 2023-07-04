import asyncio
from aiohttp import ClientSession
import os

from dotenv import load_dotenv

load_dotenv()

IAM_TOKEN = os.getenv('IAM_TOKEN')
FOLDER_ID = os.getenv('FOLDER_ID')


# Translates texts
async def transfer(target_lang: str, text: str):
    try:
        async with ClientSession() as session:
            body = {
                "targetLanguageCode": target_lang,
                "texts": text,
                "folderId": FOLDER_ID,
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(IAM_TOKEN)
            }

            response = await session.post(
                'https://translate.api.cloud.yandex.net/translate/v2/translate',
                json=body,
                headers=headers
            )
            response_data = await response.json()
            return response_data['translations']
    except KeyError:
        return []


async def main():
    print(await transfer('ru', "engine"))


if __name__ == '__main__':
    asyncio.run(main())
