import asyncio
import ssl

from aiogram import types, Dispatcher, Bot
from aiohttp import web

import backend.music.text
from consts import config
from frontend.handlers import DP
from frontend.core import events
from utils import scheduler


APP = web.Application()
ROUTES = web.RouteTableDef()


@ROUTES.get("/gettext/{name}")
async def gettext(request):
    if not (name := request.match_info.get('name')):
        return web.Response(text="Использование: /gettext/имя_песни")
    if not (res := await backend.music.text.search_text(name)):
        return web.Response(text="Ошибка поиска")
    title, text = res
    return web.Response(text=f"{title} \n\n{text}")


@ROUTES.get("/playlist")
async def history_save(request):
    # https://HOST:PORT/playlist?artist=%artist%&title%title%&casttitle=%casttitle%&len=%seconds%&path=%path%&pass=pass
    args = request.rel_url.query
    if args.get('pass') != config.RADIOBOSS_DATA[2]:
        return web.Response(text='neok')
    fields = {
        'artist': args.get('artist'),
        'title': args.get('title'),
        'casttitle': args.get('casttitle'),
        'path': args.get('path'),
    }
    await events.send_history(fields)
    return web.Response(text='ok')


@ROUTES.post(config.WEBHOOK_PATH)
async def webhook_handle(request):
    update = await request.json()
    update = types.Update(**update)

    Bot.set_current(DP.bot)  # без этого не работает
    Dispatcher.set_current(DP)
    asyncio.create_task(DP.process_update(update))

    return web.Response(text='ok')


async def on_startup(_):
    if (await config.BOT.get_webhook_info()).url != config.WEBHOOK_URL:
        await config.BOT.set_webhook(config.WEBHOOK_URL, certificate=config.SSL_CERT.open('rb'))

    asyncio.create_task(scheduler.start())
    await events.start_up()


async def on_shutdown(_):
    await events.shut_down()


def start():
    APP.add_routes(ROUTES)
    APP.on_startup.append(on_startup)
    APP.on_shutdown.append(on_shutdown)

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_cert_chain(config.SSL_CERT, config.SSL_PRIV)

    web.run_app(
        APP,
        host='0.0.0.0',
        port=config.PORT,
        ssl_context=context
    )


if __name__ == "__main__":
    start()
