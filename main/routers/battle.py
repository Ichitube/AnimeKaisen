import asyncio
import random
from aiogram import Router, F

from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.filters import Command
from aiogram.enums import ParseMode

from keyboards.builders import reply_builder, inline_builder, menu_button, Ability, rm
from filters.chat_type import ChatTypeFilter, CallbackChatTypeFilter
from recycling import profile
from routers import main_menu
from data import characters, character_photo
from data import mongodb
from data.mongodb import db
from chat_handlers.chat_battle import bot

router = Router()

battle_data = {}

user_data = {}

win_animation = "CgACAgQAAx0CfstymgACDfFmFCIV11emoqYRlGWGZRTtrA46oQACAwMAAtwWDVNLf3iCB-QL9jQE"
lose_animation = "CgACAgQAAx0CfstymgACDfJmEvqMok4D9NPyOY0bevepOE4LpQAC9gIAAu-0jFK0picm9zwgKzQE"
draw_animation = "CgACAgQAAx0CfstymgACDfFmFCIV11emoqYRlGWGZRTtrA46oQACAwMAAtwWDVNLf3iCB-QL9jQE"

win_text = ("👑 Победа: 💀Соперник мертв"
            "\n── •✧✧• ────────────"
            "\n  + 100🀄️ xp, "
            "\n  + 200💴 ¥")
lose_text = ("💀 Поражение"
             "\n── •✧✧• ────────────"
             "\n  + 55🀄️ xp, "
             "\n  + 100💴 ¥")
draw_text = ("☠️ Ничья"
             "\n── •✧✧• ────────────"
             "\n  + 80🀄️ xp, "
             "\n  + 150💴 ¥")
surrender_text = "🏴‍☠️ Поражение"
surrender_r_text = ("👑 Победа: 🏴‍☠️Соперник сдался"
                    "\n── •✧✧• ────────────"
                    "\n  + 100🀄️ xp, "
                    "\n  + 200💴 ¥")
time_out_text = ("👑 Победа: 🕘Время вышло"
                 "\n── •✧✧• ────────────"
                 "\n  + 100🀄️ xp, "
                 "\n  + 200💴 ¥")


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


@router.message(Command("post"))
async def fill_profile(message: Message):
    if message.from_user.id == 6946183730:
        async def forward_post_to_all_users(channel_id, message_id):
            users = db.users.find()  # замените 'users' на имя вашей коллекции пользователей
            async for user in users:
                try:
                    await bot.forward_message(chat_id=user['_id'], from_chat_id=channel_id, message_id=message_id)
                except Exception as e:
                    print(f"Не удалось переслать сообщение пользователю {user['_id']}: {e}")

        await forward_post_to_all_users(channel_id=-1002042458477, message_id=23)
    else:
        await message.answer("У вас нет прав на выполнение этой команды")


@router.message(Command("rm"))
async def fill_profile(message: Message):
    await bot.send_message(message.chat.id, 'клавитура удалена', reply_markup=rm())


async def surrender_f(user_id, r, mes):
    await asyncio.sleep(60)
    if not user_data[user_id][r]:
        user_data[user_id][r] = True  # Обновляем состояние
        account = await mongodb.get_user(user_id)

        if account["battle"]["battle"]["status"] == 2:
            rival = await mongodb.get_user(account["battle"]["battle"]["rid"])
            await bot.send_animation(chat_id=user_id, animation=lose_animation,
                                     caption=surrender_text, reply_markup=menu_button())

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


@router.message(
    ChatTypeFilter(chat_type=["private"]),
    F.text == "🏟️ Арена"
)
@router.callback_query(F.data == "arena")
async def arena(callback: CallbackQuery | Message):
    account = await mongodb.get_user(callback.from_user.id)
    await profile.update_rank(callback.from_user.id, account["battle"]["stats"]['wins'])

    rank = await profile.rerank(account['stats']['rank'])
    in_battle = await mongodb.in_battle()
    universe = account['universe']
    character = account['character']
    exp = account['stats']['exp']
    wins = account['battle']['stats']['wins']
    strength = character_photo.get_stats(universe, character, 'arena')['strength']
    agility = character_photo.get_stats(universe, character, 'arena')['agility']
    intelligence = character_photo.get_stats(universe, character, 'arena')['intelligence']
    power = character_photo.get_stats(universe, character, 'arena')['power']

    pattern = dict(
        caption=f"❖  🏟️  <b>Арена</b>  ⚔️"
                f"\n── •✧✧• ────────────"
                f"\n❖🎴 <b>{character}</b>"
                f"\n❖🎐 <b>{rank}</b>"
                f"\n\n   ✊🏻 Сила: {strength}"
                f"\n   👣 Ловкость: {agility}"
                f"\n   🧠 Интелект: {intelligence}"
                f"\n   ⚜️ Мощь: {power}"
                f"\n\n 👑 {wins} Побед 👑 | 🀄️ {exp} XP"
                f"\n── •✧✧• ────────────"
                f"\n<i>🌊 В битве ⚔️ {in_battle} игроков</i> 🌊",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["⚔️ Битва", "🎴 Навыки", "⛓ Рабыня", "🏆 Рейтинг", "📜 Правила", "🔙 Назад"],
            ["search_opponent", Ability(action="ability", universe=universe, character=character, back='arena'),
             "slave", "battle_rating", "battle_rules", "main_page"],
            row_width=[1, 2, 2, 1])
    )

    if isinstance(callback, CallbackQuery):
        media = InputMediaPhoto(
            media='AgACAgIAAx0CfstymgACBaJly1EK8HvqMmJjmPe7B4Uf4uiDHAACldcxG1pyWEqTZtRfQzuM-gEAAwIAA3kAAzQE'
        )
        await callback.message.edit_media(media)
        await callback.message.edit_caption(**pattern)
    else:
        media = 'AgACAgIAAx0CfstymgACBaJly1EK8HvqMmJjmPe7B4Uf4uiDHAACldcxG1pyWEqTZtRfQzuM-gEAAwIAA3kAAzQE'
        await callback.answer_photo(media, **pattern)


@router.message(ChatTypeFilter(chat_type=["private"]), Command("search"))
@router.callback_query(F.data == "search_opponent")
async def search_opponent(callback: CallbackQuery | Message):
    if isinstance(callback, CallbackQuery):
        await callback.message.delete()
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    universe = account['universe']

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
            character = account['character']
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
            r_character = rival['character']
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
        rival = await mongodb.get_user(account["battle"]["battle"]["rid"])
        await bot.send_animation(chat_id=user_id, animation=lose_animation,
                                 caption=surrender_text, reply_markup=menu_button())

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
                                 caption=surrender_r_text, reply_markup=menu_button())


@router.callback_query(CallbackChatTypeFilter(chat_type=["private"]), F.data.startswith("˹"))
async def battle(callback: CallbackQuery):
    action = callback.data

    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

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

        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)

        battle_data[character.ident] = character
        battle_data[r_character.ident] = r_character

        async def send_round_photo():
            if r_character.stun == 0:
                character.b_round += 1
                battle_data[r_character.ident].b_turn = False
                battle_data[character.ident].b_turn = True
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
                user_data[user_id][character.b_round - 1] = True  # Обновляем состояние
                # Инициализируем состояние пользователя
                user_data[r_character.ident][r_character.b_round] = False
                # Запускаем таймер
                await surrender_f(r_character.ident, r_character.b_round, mes)
            else:
                character.b_round += 1
                r_character.b_round += 1
                battle_data[character.rid].b_turn = True
                battle_data[character.ident].b_turn = False
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
                await bot.send_message(r_character.ident, "⏳ Ход соперника")
                await surrender_f(character.ident, character.b_round, mes)

        if character.health <= 0 and r_character.health <= 0:
            await bot.send_animation(chat_id=user_id, animation=draw_animation,
                                     caption=draw_text, reply_markup=menu_button())
            await bot.send_animation(chat_id=r_character, animation=draw_animation,
                                     caption=draw_text, reply_markup=menu_button())

            await mongodb.update_many(
                {"_id": {"$in": [account["_id"], character.rid]}},
                {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
            )

            await mongodb.update_many(
                {"_id": {"$in": [account["_id"], character.rid]}},
                {"$inc": {"stats.exp": 80, "battle.stats.ties": 1, "account.money": 150}}
            )

        elif character.health <= 0:
            if character.b_round != r_character.b_round:
                await bot.send_animation(chat_id=user_id, animation=lose_animation,
                                         caption=lose_text, reply_markup=menu_button())
                await bot.send_animation(chat_id=character.rid, animation=lose_animation,
                                         caption=win_text, reply_markup=menu_button())

                await mongodb.update_many(
                    {"_id": {"$in": [account["_id"], character.rid]}},
                    {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
                )

                await mongodb.update_value(account["_id"], {"battle.stats.loses": 1})
                await mongodb.update_value(account["_id"], {"stats.exp": 55})
                await mongodb.update_value(account["_id"], {"account.money": 100})
                await mongodb.update_value(character.rid, {"battle.stats.wins": 1})
                await mongodb.update_value(character.rid, {"stats.exp": 100})
                await mongodb.update_value(character.rid, {"account.money": 200})

            else:
                await send_round_photo()

        elif r_character.health <= 0:
            if character.b_round != r_character.b_round:
                await bot.send_animation(chat_id=user_id, animation=win_animation,
                                         caption=win_text, reply_markup=menu_button())
                await bot.send_animation(chat_id=character.rid, animation=lose_animation,
                                         caption=lose_text, reply_markup=menu_button())

                await mongodb.update_many(
                    {"_id": {"$in": [account["_id"], character.rid]}},
                    {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
                )

                await mongodb.update_value(character.rid, {"battle.stats.loses": 1})
                await mongodb.update_value(character.rid, {"stats.exp": 55})
                await mongodb.update_value(character.rid, {"account.money": 100})
                await mongodb.update_value(account["_id"], {"battle.stats.wins": 1})
                await mongodb.update_value(account["_id"], {"stats.exp": 100})
                await mongodb.update_value(account["_id"], {"account.money": 200})

            else:
                await send_round_photo()
        else:
            await send_round_photo()
