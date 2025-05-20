import sys
import os

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from routers import (registration, battle, gacha, banner, settings, navigation, main_menu, inventory, craft, slaves,
                     arena, battle_ai, card_battle, card_battle_ai)
from data import character_photo
from routers.tokio import tokio, dungeon, store, Pay, home, quests, clans, boss
from handlers import chat_commands, admins
from payments import stars
from chat_handlers import chat_battle
from callbacks import callback
from middlewares.AntiFloodMiddleWare import AntiFloodMiddleware, AntiFloodMiddlewareM
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis

# Твой Redis-клиент (асинхронный)
redis_client = redis.Redis(
    host='redis-13363.c328.europe-west3-1.gce.redns.redis-cloud.com',
    port=13363,
    decode_responses=True,
    username='default',
    password="BFTJgAh9jM5SH1HY8m9KqzFqFnpuDyPl",  # вставь свой пароль
    ssl=True
)

# FSM-хранилище на Redis
storage = RedisStorage(redis=redis_client)

# Подключаем хранилище к диспетчеру
dp = Dispatcher(storage=storage)

bot = Bot(token="6776753252:AAH4FKaWyegHYHnh_RBJINk2sEhtaebxWrk",
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


async def main():
    dp = Dispatcher()

    dp.include_routers(
        registration.router,
        callback.router,
        main_menu.router,
        navigation.router,
        battle.router,
        chat_battle.router,
        gacha.router,
        banner.router,
        settings.router,
        tokio.router,
        dungeon.router,
        store.router,
        Pay.router,
        inventory.router,
        craft.router,
        chat_commands.router,
        character_photo.router,
        slaves.router,
        home.router,
        admins.router,
        stars.router,
        arena.router,
        battle_ai.router,
        card_battle.router,
        card_battle_ai.router,
        quests.router,
        clans.router,
        boss.router
    )

    # dp.callback_query.middleware(AntiFloodMiddleware())
    # dp.message.middleware(AntiFloodMiddlewareM())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=[])

if __name__ == "__main__":
    asyncio.run(main())
