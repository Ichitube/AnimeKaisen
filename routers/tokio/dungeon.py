import asyncio

from aiogram import Router, F

from aiogram.types import CallbackQuery, InputMediaAnimation
from aiogram.enums import ParseMode

from keyboards.builders import inline_builder
from data import mongodb
from recycling import profile

router = Router()

tasks = {}


@router.callback_query(F.data == "dungeon")
async def dungeon(callback: CallbackQuery):
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    await profile.update_level(user_id, account["campaign"]["count"])

    async def get_army_power(uid):
        user = await mongodb.get_user(uid)
        power = user['campaign']['power']
        return power

    nephritis_per_minute = account['campaign']['power'] // 7000 * account['campaign']['level']
    gold_per_minute = account['campaign']['power'] // 500 * account['campaign']['level']
    silver_per_minute = account['campaign']['power'] // 30 * account['campaign']['level']

    async def increase_resources(uid, power):
        nephritis = power // 7000
        gold = power // 500
        silver = power // 30

        await mongodb.update_value(uid, {'campaign.nephritis': nephritis})
        await mongodb.update_value(uid, {'campaign.gold': gold})
        await mongodb.update_value(uid, {'campaign.silver': silver})

    async def resource_increase_loop(uid):
        while True:
            power = await get_army_power(uid)
            await increase_resources(uid, power)
            await asyncio.sleep(60)

    level = await profile.level(account['campaign']['level'])
    pattern = dict(
        caption=f"❖  ⛩️  <b>Подземелье</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖  Очищаем подземелье от монстров и получаем ресурсы 💰. . ."
                f"\n\n ⚜️ Сила карты: {account['campaign']['power']}"
                f"\n ⛩️ {level}"
                f"\n\n   💠 Нефрит: {account['campaign']['nephritis']}"
                f"\n   📀 Золото: {account['campaign']['gold']}"
                f"\n   💿 Серебро: {account['campaign']['silver']}"
                f"\n\n── •✧✧• ────────────"
                f"\n💠/м: {nephritis_per_minute}"
                f" 📀/м: {gold_per_minute}"
                f" 💿/м: {silver_per_minute}",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["💰 Продать 💴", "👾 Босс", "⚜️ Рейтинг", "📋 Правила", "🔙 Назад"],
            ["sell_resources", "boss", "campaign_rank", "campaign_rules", "main_page"],
            row_width=[2, 2, 1]
            )
    )

    media_id = "CgACAgIAAx0CfstymgACBcJlzMqX7Mtt96VNg0aD00EKQwGWLgAClTsAAnsmaEpgAq2WiSsm5TQE"
    media = InputMediaAnimation(media=media_id)
    await callback.message.edit_media(media, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)

    if user_id not in tasks or tasks[user_id].done():
        tasks[user_id] = asyncio.create_task(resource_increase_loop(user_id))


@router.callback_query(F.data == "sell_resources")
async def sell_resources(callback: CallbackQuery):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    nephritis = account['campaign']['nephritis']
    gold = account['campaign']['gold'] // 3
    silver = account['campaign']['silver'] // 70

    await mongodb.update_user(user_id, {'account.money': account['account']['money'] + nephritis + gold + silver})

    await mongodb.update_user(user_id, {'campaign.nephritis': 0})
    await mongodb.update_user(user_id, {'campaign.gold': 0})
    await mongodb.update_user(user_id, {'campaign.silver': 0})

    await callback.answer(f"❖  💰 Ресупсы проданы за 💴 {nephritis + gold + silver} ¥", show_alert=True)


@router.callback_query(F.data == "boss")
async def boss(callback: CallbackQuery):
    await callback.answer("❖  👾 Босс еще не появился", show_alert=True)


@router.callback_query(F.data == "campaign_rank")
async def campaign_rank(callback: CallbackQuery):
    account = await mongodb.get_user(callback.from_user.id)
    rating = await mongodb.send_rating("campaign.power", account, '⚜️')

    media = InputMediaAnimation(media="CgACAgIAAxkBAAIVQ2XOBCFYSQfjZfxblsVAZJ3PNGQWAAKIRwAC8utxSsak7XpiV9MnNAQ")
    await callback.message.edit_media(media=media)

    await callback.message.edit_caption(
        caption=f"❖  ⚜️  <b>Рейтинг самых сильных игроков</b>"
                f"\n── •✧✧• ────────────"
                f"{rating}"
                f"\n── •✧✧• ────────────",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🔙 Назад"],
            ["dungeon"],
            row_width=[2, 2])
    )
    await callback.answer()


@router.callback_query(F.data == "campaign_rules")
async def campaign_rules(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=f"❖  📋  <b>Правила Подземелье</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖  ⛩️ В подземелье персонажи из ваших карт сражаются "
                f"автоматически с монстрами и получают 💰 ресурсы. "
                f"\n\n❖ 👾 Нужно убить босса, чтобы перейти в новый ⛩️ Этаж."
                f"\n\n❖Чем выше ⛩️ этаж, тем больше 💰 ресурсы."
                f"\n\n❖ ⚜️ Сила вашей команды зависит от общей силы ваших карт."
                f"\n\n❖ 💰 Количество добычи зависит от ⚜️ Cилы карт и ⛩️ этажа."
                f"\n\n❖ 💰 Ресурсы можно продать за 💴 ¥"
                f"\n── •✧✧• ────────────",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🔙 Назад"],
            ["dungeon"],
            row_width=[2, 2]
        )
    )
    await callback.answer()
