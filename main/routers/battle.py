import asyncio
import random
from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from routers.arena import arena
from aiogram.types import CallbackQuery, Message
from chat_handlers.chat_battle import bot
from data import characters, character_photo
from data import mongodb
from filters.chat_type import ChatTypeFilter, CallbackChatTypeFilter
from keyboards.builders import reply_builder, inline_builder, menu_button
from routers import main_menu
from battle_ai import ai

router = Router()

battle_data = {}

user_data = {}

win_animation = "CgACAgQAAx0CfstymgACDfFmFCIV11emoqYRlGWGZRTtrA46oQACAwMAAtwWDVNLf3iCB-QL9jQE"
lose_animation = "CgACAgQAAx0CfstymgACDfJmEvqMok4D9NPyOY0bevepOE4LpQAC9gIAAu-0jFK0picm9zwgKzQE"
draw_animation = "CgACAgQAAx0CfstymgACDfFmFCIV11emoqYRlGWGZRTtrA46oQACAwMAAtwWDVNLf3iCB-QL9jQE"


win_text = ("👑 Победа: 💀Соперник мертв"
            "\n<blockquote expandable>── •✧✧• ────────────"
            "\n  + 100🀄️ xp, "
            "\n  + 200💴 ¥</blockquote>")
lose_text = ("💀 Поражение"
             "\n<blockquote expandable>── •✧✧• ────────────"
             "\n  + 55🀄️ xp, "
             "\n  + 100💴 ¥</blockquote>")
draw_text = ("☠️ Ничья"
             "\n<blockquote expandable>── •✧✧• ────────────"
             "\n  + 80🀄️ xp, "
             "\n  + 150💴 ¥</blockquote>")
surrender_text = "🏴‍☠️ Поражение"
surrender_r_text = ("👑 Победа: 🏴‍☠️Соперник сдался"
                    "\n<blockquote expandable>── •✧✧• ────────────"
                    "\n  + 100🀄️ xp, "
                    "\n  + 200💴 ¥</blockquote>")
time_out_text = ("👑 Победа: 🕘Время вышло"
                 "\n<blockquote expandable>── •✧✧• ────────────"
                 "\n  + 100🀄️ xp, "
                 "\n  + 200💴 ¥</blockquote>")


def account_text(character):
    text = (f"                 {character.name}"
            f"\n\n❤️{character.health}"
            f" 🗡{character.attack}"
            f" 🛡{character.defense}"
            f" 🧪{character.mana}"
            f" 🪫{character.energy}"
            f"\n🩸К.ур: {character.crit_dmg}"
            f" 🩸К.шн: {character.crit_ch}"
            f" 🌐Щит: {character.shield}"
            f"\n\n✊🏻Сила: {character.strength}"
            f" 👣Лов.: {character.agility}"
            f" 🧠Инт.: {character.intelligence}"
            f"\n\n❤️‍🔥Пассивки: {character.passive_names}")
    return text


async def surrender_f(user_id, r, mes):
    await asyncio.sleep(60)
    if not user_data[user_id][r]:
        user_data[user_id][r] = True  # Обновляем состояние
        account = await mongodb.get_user(user_id)

        if account["battle"]["battle"]["status"] == 2:
            rival = await mongodb.get_user(account["battle"]["battle"]["rid"])
            await bot.send_animation(chat_id=user_id, animation=lose_animation,
                                     caption=surrender_text, reply_markup=menu_button())
            current_date = datetime.today().date()
            current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
            await mongodb.update_user(account["battle"]["battle"]["rid"], {"tasks.last_arena_fight": current_datetime})
            await mongodb.update_value(account["_id"], {"battle.stats.loses": 1})
            await mongodb.update_value(account["battle"]["battle"]["rid"], {"battle.stats.wins": 1})
            await mongodb.update_value(account["battle"]["battle"]["rid"], {"stats.exp": 100})
            await mongodb.update_value(account["battle"]["battle"]["rid"], {"account.money": 200})
            await mongodb.update_many(
                {"_id": {"$in": [account["_id"]]}},
                {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
            )
            await mongodb.update_many(
                {"_id": {"$in": [rival["_id"]]}},
                {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
            )
            await bot.send_animation(chat_id=rival["_id"], animation=win_animation,
                                     caption=time_out_text, reply_markup=menu_button())
        await bot.edit_message_text(chat_id=user_id, message_id=mes.message_id,
                                    text=f"✖️ Время вышло 🕘", reply_markup=None)


# @router.callback_query(F.data == "battle_arena")
# async def b_arena(callback: CallbackQuery | Message):
#     account = await mongodb.get_user(callback.from_user.id)
#     if account['universe'] in ['Allstars', 'Allstars(old)']:
#         await callback.answer(
#             text="💢 Пока не доступно в вашой вселеноой!",
#             show_alert=True
#         )
#         return
#     await profile.update_rank(callback.from_user.id, account["battle"]["stats"]['wins'])
#     in_battle = await mongodb.in_battle()
#
#     buttons = ["⚔️ PvP 🎃", "✨ AI", "🔙 Назад", "📜 Правила",]
#     calls = ["search_opponent", "ai_battle", "arena", "battle_rules",]
#
#     pattern = dict(
#         caption=f"❖  🏟️ <b>Арена</b>  ⚔️"
#                 f"\n── •✧✧• ────────────"
#                 f"\n❖⚔️ PvP - Битва против реального игрока который так же ищет соперника"
#                 f"\n\n❖✨ AI - Битва против Искуственного Интелекта. Удобно для тренировок "
#                 f"\n\n── •✧✧• ────────────"
#                 f"\n<i>🌊 В битве ⚔️ {in_battle} игроков</i> 🌊",
#         parse_mode=ParseMode.HTML,
#         reply_markup=inline_builder(
#             buttons,
#             calls,
#             row_width=[2, 2])
#     )
#
#     media = InputMediaPhoto(
#         media='AgACAgIAAxkBAAEBGppm6oI246rBQNH-lZFRiZFD6TbJlgACeuUxG1fhUEt5QK8VqfcCQQEAAwIAA3gAAzYE'
#     )
#     await callback.message.edit_media(media)
#     await callback.message.edit_caption(**pattern)


@router.message(ChatTypeFilter(chat_type=["private"]), Command("search"))
@router.callback_query(F.data == "search_opponent")
async def search_opponent(callback: CallbackQuery | Message):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    universe = account['universe']

    if account['universe'] in ['Allstars', 'Allstars(old)']:
        await callback.answer(
            text="💢 Пока не доступно в вашой вселеноой!",
            show_alert=True
        )
        return

    if isinstance(callback, CallbackQuery):
        await callback.message.delete()

    if account["battle"]["battle"]["status"] == 0:
        rival = await mongodb.find_opponent()

        await mongodb.update_user(user_id, {"battle.battle.status": 1})

        if rival is None:
            await bot.send_animation(
                user_id, animation="CgACAgIAAx0CfstymgACBaNly1ESV41gB1s-k4M3VITaGbHvHwACPj8AAlpyWEpUUFtvRlRcpjQE",
                caption=f"\n 💡 <blockquote expandable>{random.choice(character_photo.quotes[universe])}</blockquote>"
                        f"\n── •✧✧• ────────────"
                        f"\n❖ 🔎 Поиск соперника . . . . .",
                reply_markup=reply_builder("✖️ Отмена"))
        else:
            ident = account["_id"]
            name = account["name"]
            character = account['character'][account['universe']]
            avatar = character_photo.get_stats(universe, character, 'avatar')
            avatar_type = character_photo.get_stats(universe, character, 'type')
            rarity = character_photo.get_stats(universe, character, 'rarity')
            strength = character_photo.get_stats(universe, character, 'arena')['strength']
            agility = character_photo.get_stats(universe, character, 'arena')['agility']
            intelligence = character_photo.get_stats(universe, character, 'arena')['intelligence']
            ability = character_photo.get_stats(universe, character, 'arena')['ability']
            power = character_photo.get_stats(universe, character, 'arena')['power']
            slave = None
            if account['inventory']['slaves']:
                slave = account['inventory']['slaves'][0]

            b_character = characters.Character(ident, name, character, strength, agility, intelligence, ability, 1,
                                               False, rival["_id"], slave, 0)

            battle_data[account["_id"]] = b_character

            r_ident = rival["_id"]
            r_name = rival["name"]
            r_universe = rival['universe']
            r_character = rival['character'][rival['universe']]
            r_avatar = character_photo.get_stats(r_universe, r_character, 'avatar')
            r_avatar_type = character_photo.get_stats(r_universe, r_character, 'type')
            r_rarity = character_photo.get_stats(r_universe, r_character, 'rarity')
            r_strength = character_photo.get_stats(r_universe, r_character, 'arena')['strength']
            r_agility = character_photo.get_stats(r_universe, r_character, 'arena')['agility']
            r_intelligence = character_photo.get_stats(r_universe, r_character, 'arena')['intelligence']
            r_ability = character_photo.get_stats(r_universe, r_character, 'arena')['ability']
            r_power = character_photo.get_stats(r_universe, r_character, 'arena')['power']
            r_slave = None
            if rival['inventory']['slaves']:
                r_slave = rival['inventory']['slaves'][0]

            rb_character = characters.Character(r_ident, r_name, r_character, r_strength, r_agility, r_intelligence,
                                                r_ability, 1, False, account["_id"], r_slave, 0)

            battle_data[rival["_id"]] = rb_character

            user_text = (f" ⚔️ Cоперник Найден! "
                         f"\n── •✧✧• ────────────"
                         f"\n<blockquote expandable> 🪪  〢 {rival['name']} "
                         f"\n── •✧✧• ────────────"
                         f"\n❖ ✨ Редкость: {r_rarity}"
                         f"\n❖ 🗺 Вселенная: {r_universe}"
                         f"\n\n   ✊🏻 Сила: {r_strength}"
                         f"\n   👣 Ловкость: {r_agility}"
                         f"\n   🧠 Интелект: {r_intelligence}"
                         f"\n   ⚜️ Мощь: {r_power}</blockquote>"
                         f"\n── •✧✧• ────────────"
                         f"\n<i>🀄️ Опыт: {rival['stats']['exp']} XP </i>")

            rival_text = (f"⚔️ Cоперник Найден! "
                          f"\n── •✧✧• ────────────"
                          f"\n<blockquote expandable> 🪪  〢 {account['name']} "
                          f"\n── •✧✧• ────────────"
                          f"\n❖ ✨ Редкость: {rarity}"
                          f"\n❖ 🗺 Вселенная: {universe}"
                          f"\n\n   ✊🏻 Сила: {strength}"
                          f"\n   👣 Ловкость: {agility}"
                          f"\n   🧠 Интелект: {intelligence}"
                          f"\n   ⚜️ Мощь: {power}</blockquote>"
                          f"\n── •✧✧• ────────────"
                          f"\n<i>🀄️ Опыт: {account['stats']['exp']} XP </i>")

            await mongodb.update_user(account["_id"], {"battle.battle.status": 2, "battle.battle.rid": rival["_id"]})
            await mongodb.update_user(rival["_id"], {"battle.battle.status": 2, "battle.battle.rid": account["_id"]})

            if r_avatar_type == 'photo':
                await bot.send_photo(photo=r_avatar, chat_id=account["_id"], caption=user_text,
                                     reply_markup=reply_builder("🏴‍☠️ Сдаться"))
            else:
                await bot.send_animation(animation=r_avatar, chat_id=account["_id"], caption=user_text,
                                         reply_markup=reply_builder("🏴‍☠️ Сдаться"))

            if avatar_type == 'photo':
                await bot.send_photo(photo=avatar, chat_id=rival["_id"], caption=rival_text,
                                     reply_markup=reply_builder("🏴‍☠️ Сдаться"))
            else:
                await bot.send_animation(animation=avatar, chat_id=rival["_id"], caption=rival_text,
                                         reply_markup=reply_builder("🏴‍☠️ Сдаться"))

            await bot.send_message(account["_id"], text="⏳ Ход соперника")
            mes = await bot.send_message(rival["_id"], text=f".                    ˗ˋˏ💮 Раунд {rb_character.b_round}ˎˊ˗"
                                                            f"\n✧•───────────────────────•✧"
                                                            f"\n<blockquote expandable>{account_text(rb_character)}"
                                                            f"\n✧•───────────────────────•✧"
                                                            f"\n{account_text(b_character)}</blockquote>"
                                                            f"\n✧•───────────────────────•✧"
                                                            f"\n🔸 Ваш ход:",
                                         reply_markup=inline_builder(r_ability, r_ability, row_width=[2, 2]),
                                         parse_mode=ParseMode.HTML)
            # Инициализируем состояние пользователя
            user_data[rival["_id"]] = {rb_character.b_round: False}
            user_data[user_id] = {b_character.b_round: True}

            # Запускаем таймер
            await surrender_f(rival["_id"], rb_character.b_round, mes)

    elif account["battle"]["battle"]["status"] == 1:
        if isinstance(callback, CallbackQuery):
            await callback.answer(
                text="💢 Вы уже находитесь в поиске соперника!",
                show_alert=True
            )
        else:
            await callback.answer(text="💢 Вы уже находитесь в поиске соперника!")

    elif account["battle"]["battle"]["status"] == 2:
        if isinstance(callback, CallbackQuery):
            await callback.answer(
                text="💢 Вы уже находитесь в битве!",
                show_alert=True
            )
        else:
            await callback.answer(text="💢 Вы уже находитесь в битве!")


@router.message(ChatTypeFilter(chat_type=["private"]), Command("cancel"))
@router.message(F.text.lower().contains("✖️ отмена"))
async def cancel_search(message: Message):

    user_id = message.from_user.id
    account = await mongodb.get_user(user_id)

    if account["battle"]["battle"]["status"] == 1:
        await mongodb.update_user(user_id, {"battle.battle.status": 0})
        await message.answer("✖️ Поиск отменен", reply_markup=menu_button())
        await main_menu.main_menu(message)


@router.message(ChatTypeFilter(chat_type=["private"]), Command("surrender"))
@router.message(F.text == "🏴‍☠️ Сдаться")
async def surrender(message: Message):
    user_id = message.from_user.id
    account = await mongodb.get_user(user_id)

    if account["battle"]["battle"]["status"] == 2:
        if account["battle"]["battle"]["rid"] != user_id * 10:
            rival = await mongodb.get_user(account["battle"]["battle"]["rid"])
        await bot.send_animation(chat_id=user_id, animation=lose_animation,
                                 caption=surrender_text, reply_markup=menu_button())

        await mongodb.update_value(account["_id"], {"battle.stats.loses": 1})
        if account["battle"]["battle"]["rid"] != user_id * 10:
            await mongodb.update_value(account["battle"]["battle"]["rid"], {"battle.stats.wins": 1})
            await mongodb.update_value(account["battle"]["battle"]["rid"], {"stats.exp": 100})
            await mongodb.update_value(account["battle"]["battle"]["rid"], {"account.money": 200})
            current_date = datetime.today().date()
            current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
            await mongodb.update_user(account["battle"]["battle"]["rid"], {"tasks.last_arena_fight": current_datetime})
        await mongodb.update_many(
            {"_id": {"$in": [account["_id"]]}},
            {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
        )
        if account["battle"]["battle"]["rid"] != user_id * 10:
            await mongodb.update_many(
                {"_id": {"$in": [rival["_id"]]}},
                {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
            )
            await bot.send_animation(chat_id=rival["_id"], animation=win_animation,
                                     caption=surrender_r_text, reply_markup=menu_button())


@router.callback_query(CallbackChatTypeFilter(chat_type=["private"]), F.data.startswith("˹"))
async def battle(callback: CallbackQuery):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    try:
        action = callback.data
        character = battle_data.get(account["_id"])
        r_character = battle_data.get(character.rid)

        if account["battle"]["battle"]["status"] == 2:
            if character.b_turn:
                return await bot.send_message(user_id, "✖️ Вы уже сделали ход!")

            mana, energy = await characters.turn(character, bot, action, r_character, 0)

            if not mana:
                await callback.answer("✖️ Недостаточно маны 🧪", show_alert=True)
                return

            if not energy:
                await callback.answer("✖️ Недостаточно энергии 🪫", show_alert=True)
                return

            await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)

            battle_data[character.ident] = character
            battle_data[r_character.ident] = r_character

            async def send_round_photo():
                if r_character.stun == 0:
                    character.b_round += 1
                    battle_data[r_character.ident].b_turn = False
                    battle_data[character.ident].b_turn = True
                    if r_character.ident != character.ident * 10:
                        mes = await bot.send_message(r_character.ident,
                                                     text=f".                    ˗ˋˏ💮 Раунд {r_character.b_round}ˎˊ˗"
                                                          f"\n✧•───────────────────────•✧"
                                                          f"\n<blockquote expandable>{account_text(r_character)}"
                                                          f"\n✧•───────────────────────•✧"
                                                          f"\n{account_text(character)}</blockquote>"
                                                          f"\n✧•───────────────────────•✧"
                                                          f"\n🔸 Ваш ход:",
                                                     reply_markup=inline_builder(r_character.ability, r_character.ability,
                                                                                 row_width=[2, 2]),
                                                     parse_mode=ParseMode.HTML)
                    else:
                        await ai(r_character)
                    user_data[user_id][character.b_round - 1] = True  # Обновляем состояние
                    # Инициализируем состояние пользователя
                    user_data[r_character.ident][r_character.b_round] = False
                    # Запускаем таймер
                    if r_character.ident != character.ident * 10:
                        await surrender_f(r_character.ident, r_character.b_round, mes)
                else:
                    character.b_round += 1
                    r_character.b_round += 1
                    battle_data[character.rid].b_turn = True
                    battle_data[character.ident].b_turn = False
                    if r_character.ident != character.ident * 10:
                        await bot.send_message(r_character.ident,
                                               text=f".                    ˗ˋˏ💮 Раунд {r_character.b_round - 1}ˎˊ˗"
                                                    f"\n✧•───────────────────────•✧"
                                                    f"\n<blockquote expandable>{account_text(r_character)}"
                                                    f"\n✧•───────────────────────•✧"
                                                    f"\n{account_text(character)}"
                                                    f"\n✧•───────────────────────•✧</blockquote>"
                                                    f"\n💫 Вы под действием оглушения",
                                               parse_mode=ParseMode.HTML)
                    mes = await bot.send_message(user_id,
                                                 text=f".                    ˗ˋˏ💮 Раунд {character.b_round}ˎˊ˗"
                                                      f"\n✧•───────────────────────•✧"
                                                      f"\n<blockquote expandable>{account_text(character)}"
                                                      f"\n✧•───────────────────────•✧"
                                                      f"\n{account_text(r_character)}</blockquote>"
                                                      f"\n✧•───────────────────────•✧"
                                                      f"\n🔸 Ваш ход:",
                                                 reply_markup=inline_builder(character.ability, character.ability,
                                                                             row_width=[2, 2]),
                                                 parse_mode=ParseMode.HTML)
                    user_data[r_character.ident][r_character.b_round - 1] = True  # Обновляем состояние
                    user_data[character.ident][character.b_round - 1] = True  # Обновляем состояние
                    # Инициализируем состояние пользователя
                    user_data[user_id][character.b_round] = False
                    # Запускаем таймер
                    if r_character.ident != character.ident * 10:
                        await bot.send_message(chat_id=r_character.ident, text="⏳ Ход соперника")
                        await surrender_f(character.ident, character.b_round, mes)

            if character.health <= 0 and r_character.health <= 0:
                await bot.send_animation(chat_id=user_id, animation=draw_animation,
                                         caption=draw_text, reply_markup=menu_button())
                if r_character.ident != character.ident * 10:
                    await bot.send_animation(chat_id=r_character, animation=draw_animation,
                                             caption=draw_text, reply_markup=menu_button())

                # await mongodb.update_many(
                #     {"_id": {"$in": [account["_id"], character.rid]}},
                #     {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
                # )
                #
                # await mongodb.update_many(
                #     {"_id": {"$in": [account["_id"], character.rid]}},
                #     {"$inc": {"stats.exp": 80, "battle.stats.ties": 1, "account.money": 150}}
                # )

                await mongodb.update_value(account["_id"], {"battle.stats.ties": 1})
                await mongodb.update_value(account["_id"], {"stats.exp": 80})
                await mongodb.update_value(account["_id"], {"account.money": 150})
                current_date = datetime.today().date()
                current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
                await mongodb.update_user(account["_id"], {"tasks.last_arena_fight": current_datetime})
                await mongodb.update_user(account["_id"], {"battle.battle.status": 0})
                await mongodb.update_user(account["_id"], {"battle.battle.rid": ""})
                await mongodb.update_value(account["_id"], {"inventory.items.halloween": 4})
                if r_character.ident != character.ident * 10:
                    await mongodb.update_value(character.rid, {"battle.stats.ties": 1})
                    await mongodb.update_value(character.rid, {"stats.exp": 80})
                    await mongodb.update_value(character.rid, {"account.money": 150})
                    await mongodb.update_user(character.rid, {"tasks.last_arena_fight": current_datetime})
                    await mongodb.update_user(character.rid, {"battle.battle.status": 0})
                    await mongodb.update_user(character.rid, {"battle.battle.rid": ""})
                    await mongodb.update_value(character.rid, {"inventory.items.halloween": 4})

            elif character.health <= 0:
                if character.b_round != r_character.b_round:
                    await bot.send_animation(chat_id=user_id, animation=lose_animation,
                                             caption=lose_text, reply_markup=menu_button())
                    if r_character.ident != character.ident * 10:
                        await bot.send_animation(chat_id=character.rid, animation=lose_animation,
                                                 caption=win_text, reply_markup=menu_button())

                    await mongodb.update_value(account["_id"], {"battle.stats.loses": 1})
                    await mongodb.update_value(account["_id"], {"stats.exp": 55})
                    await mongodb.update_value(account["_id"], {"account.money": 100})
                    current_date = datetime.today().date()
                    current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
                    await mongodb.update_user(account["_id"], {"tasks.last_arena_fight": current_datetime})
                    await mongodb.update_user(account["_id"], {"battle.battle.status": 0})
                    await mongodb.update_user(account["_id"], {"battle.battle.rid": ""})
                    await mongodb.update_value(account["_id"], {"inventory.items.halloween": 2})
                    if r_character.ident != character.ident * 10:
                        await mongodb.update_value(character.rid, {"battle.stats.wins": 1})
                        await mongodb.update_value(character.rid, {"stats.exp": 100})
                        await mongodb.update_value(character.rid, {"account.money": 200})
                        await mongodb.update_user(character.rid, {"tasks.last_arena_fight": current_datetime})
                        await mongodb.update_user(character.rid, {"battle.battle.status": 0})
                        await mongodb.update_user(character.rid, {"battle.battle.rid": ""})
                        await mongodb.update_value(character.rid, {"inventory.items.halloween": 5})

                else:
                    await send_round_photo()

            elif r_character.health <= 0:
                if character.b_round != r_character.b_round:
                    await bot.send_animation(chat_id=user_id, animation=win_animation,
                                             caption=win_text, reply_markup=menu_button())
                    if r_character.ident != character.ident * 10:
                        await bot.send_animation(chat_id=character.rid, animation=lose_animation,
                                                 caption=lose_text, reply_markup=menu_button())

                    current_date = datetime.today().date()
                    current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
                    if r_character.ident != character.ident * 10:
                        await mongodb.update_value(character.rid, {"battle.stats.loses": 1})
                        await mongodb.update_value(character.rid, {"stats.exp": 55})
                        await mongodb.update_value(character.rid, {"account.money": 100})
                        await mongodb.update_user(character.rid, {"tasks.last_arena_fight": current_datetime})
                        await mongodb.update_user(character.rid, {"battle.battle.status": 0})
                        await mongodb.update_user(character.rid, {"battle.battle.rid": ""})
                        await mongodb.update_value(character.rid, {"inventory.items.halloween": 2})
                    await mongodb.update_user(account["_id"], {"battle.battle.status": 0})
                    await mongodb.update_user(account["_id"], {"battle.battle.rid": ""})
                    await mongodb.update_user(account["_id"], {"tasks.last_arena_fight": current_datetime})
                    await mongodb.update_value(account["_id"], {"battle.stats.wins": 1})
                    await mongodb.update_value(account["_id"], {"stats.exp": 100})
                    await mongodb.update_value(account["_id"], {"account.money": 200})
                    await mongodb.update_value(account["_id"], {"inventory.items.halloween": 5})

                else:
                    await send_round_photo()
            else:
                await send_round_photo()

    except AttributeError as e:
        # Обработка ошибки AttributeError
        await callback.message.answer("❖ 🔂 Идёт разработка бота связи с чем битва была остановлена",
                                      reply_markup=menu_button())
        await mongodb.update_many(
            {"_id": {"$in": [account["_id"]]}},
            {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
        )

        if account["battle"]["battle"]["rid"] != account["_id"] * 10:
            await bot.send_message(account["battle"]["battle"]["rid"],
                                   "❖ 🔂 Идёт разработка бота связи с чем битва была остановлена")
            await mongodb.update_many(
                {"_id": {"$in": [account["battle"]["battle"]["rid"]]}},
                {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
            )
        await arena(callback, stop=1)
