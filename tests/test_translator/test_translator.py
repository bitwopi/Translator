import pytest
from pytest_aiohttp.plugin import aiohttp_client
from aiohttp import web

from bot.services.translator import transfer

target_lang = 'ru'
text = 'Hello, world!'


@pytest.mark.asyncio
async def test_transfer():

    translations = await transfer(target_lang=target_lang, text=text)

    assert translations[0]['text'] == "Привет, мир!"
    assert translations[0]['detectedLanguageCode'] == "en"


