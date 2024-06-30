import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from routers import registration, battle, gacha, banner, settings, navigation, main_menu, inventory, craft, slaves
from data import character_photo
from routers.tokio import tokio, dungeon, store, Pay, home
from handlers import chat_commands
from chat_handlers import chat_battle
from callbacks import callback
from middlewares.AntiFloodMiddleWare import AntiFloodMiddleware, AntiFloodMiddlewareM

bot = Bot(token="6776753252:AAH4FKaWyegHYHnh_RBJINk2sEhtaebxWrk", default=DefaultBotProperties(parse_mode=ParseMode.HTML))


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
        home.router
    )

    dp.callback_query.middleware(AntiFloodMiddleware())
    dp.message.middleware(AntiFloodMiddlewareM())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=[])

if __name__ == "__main__":
    asyncio.run(main())
