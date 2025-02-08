import asyncio
import random
from datetime import datetime

from aiogram import Router, F, Bot
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InputMediaAnimation
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from data import mongodb, character_photo, card_characters
from filters.chat_type import ChatTypeFilter, CallbackChatTypeFilter
from keyboards.builders import inline_builder, Pagination, pagination_card, reply_builder, menu_button

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


def round_text(side, character, faze, rd):
    text = (f"        『{side}』"
            f"\n༺ Фаза: {faze} Раунд: {rd} ༻"
            f"\n\n ⟬{character.name}⟭"
            f"\n\n❤️{character.health}"
            f" 🗡{character.attack}"
            f" 🛡{character.defense}"
            f"\n\n✊🏻Сила: {character.strength}"
            f" 👣Лов.: {character.agility}"
            f" 🧠Инт.: {character.intelligence}")
    return text


def account_text(ident):
    nested_dict = user_data[ident]  # Получаем вложенный словарь
    key = list(nested_dict.keys())[0]

    d1 = battle_data[ident]["deck"]["d1"]
    d2 = battle_data[ident]["deck"]["d2"]
    d3 = battle_data[ident]["deck"]["d3"]
    d4 = battle_data[ident]["deck"]["d4"]
    d5 = battle_data[ident]["deck"]["d5"]
    d6 = battle_data[ident]["deck"]["d6"]
    text = (f".                    ˗ˋˏ💮 Раунд {key}ˎˊ˗"
            f"\n✧•───────────────────────•✧"
            f"\n❖  🃏<b> Ваша колода:</b>"
            f"\n<blockquote expandable> • {d1.status}  {d1.name}"
            f"\n ┗➤ ┏➤ • ♥️{d1.health} • ⚔️{d1.attack} • 🛡️{d1.defense}"
            f"\n     ┗➤ • ✊{d1.strength} • 👣{d1.agility} • 🧠{d1.intelligence} ✧ {d1.clas}"
            f"\n\n • {d2.status}  {d2.name} "
            f"\n ┗➤ ┏➤ • ♥️{d2.health} • ⚔️{d2.attack} • 🛡️{d2.defense}"
            f"\n     ┗➤ • ✊{d2.strength} • 👣{d2.agility} • 🧠{d2.intelligence} ✧ {d2.clas}"
            f"\n\n • {d3.status}  {d3.name}"
            f"\n ┗➤ ┏➤ • ♥️{d3.health} • ⚔️{d3.attack} • 🛡️{d3.defense}"
            f"\n     ┗➤ • ✊{d3.strength} • 👣{d3.agility} • 🧠{d3.intelligence} ✧ {d3.clas}"
            f"\n\n • {d4.status}  {d4.name}"
            f"\n ┗➤ ┏➤ • ♥️{d4.health} • ⚔️{d4.attack} • 🛡️{d4.defense}"
            f"\n     ┗➤ • ✊{d4.strength} • 👣{d4.agility} • 🧠{d4.intelligence} ✧ {d4.clas}"
            f"\n\n • {d5.status}  {d5.name}"
            f"\n ┗➤ ┏➤ • ♥️{d5.health} • ⚔️{d5.attack} • 🛡️{d5.defense}"
            f"\n     ┗➤ • ✊{d5.strength} • 👣{d5.agility} • 🧠{d5.intelligence} ✧ {d5.clas}"
            f"\n\n • {d6.status}  {d6.name}"
            f"\n ┗➤ ┏➤ • ♥️{d6.health} • ⚔️{d6.attack} • 🛡️{d6.defense}"
            f"\n     ┗➤ • ✊{d6.strength} • 👣{d6.agility} • 🧠{d6.intelligence} ✧ {d6.clas}</blockquote>"
            f"\n✧•───────────────────────•✧")
    status = [d1.status, d2.status, d3.status, d4.status, d5.status, d6.status]
    user_cb = [f"{d1.cb}", f"{d2.cb}", f"{d3.cb}", f"{d4.cb}", f"{d5.cb}", f"{d6.cb}"]
    return text, status, user_cb, key


def deck_text(character, universe):
    strength = character_photo.get_stats(universe, character, 'arena')['strength']
    agility = character_photo.get_stats(universe, character, 'arena')['agility']
    intelligence = character_photo.get_stats(universe, character, 'arena')['intelligence']
    clas = character_photo.get_stats(universe, character, 'arena')['class']
    hp = strength * 75
    attack = strength * 5 + agility * 5 + intelligence * 5
    defense = (strength + agility + (intelligence // 2)) // 4

    text = (f" • 🎴 {character} "
            f"\n ┗➤ • ♥️{hp} • ⚔️{attack} • 🛡️{defense}"
            f"\n     ┗➤ • ✊{strength} • 👣{agility} • 🧠{intelligence} ✧ {clas}")
    return text


@router.callback_query(F.data == "deck")
async def choose_card(callback: CallbackQuery):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    universe = account['universe']
    if "deck" not in account:
        await mongodb.update_user(user_id, {"deck": {
            "d1": "empty",
            "d2": "empty",
            "d3": "empty",
            "d4": "empty",
            "d5": "empty",
            "d6": "empty"
        }})
        account = await mongodb.get_user(user_id)

    deck = account.get("deck", {})

    required_fields = {
        "d1": "empty",
        "d2": "empty",
        "d3": "empty",
        "d4": "empty",
        "d5": "empty",
        "d6": "empty"
    }

    for field, value in required_fields.items():
        if field not in deck:
            deck[field] = value

    await mongodb.update_user(user_id, {"deck": deck})
    account = await mongodb.get_user(user_id)

    deck_data = account["deck"]
    first = deck_data["d1"]
    second = deck_data["d2"]
    third = deck_data["d3"]
    fourth = deck_data["d4"]
    fifth = deck_data["d5"]
    sixth = deck_data["d6"]

    if first == "empty":
        f1_msg = f" • 🎴 <i> Пустой слот </i>"
        f1_icon = "ℹ️"
    else:
        f1_msg = deck_text(first, universe)
        f1_icon = "✅"
    if second == "empty":
        f2_msg = f" • 🎴 <i> Пустой слот </i>"
        f2_icon = "ℹ️"
    else:
        f2_msg = deck_text(second, universe)
        f2_icon = "✅"
    if third == "empty":
        f3_msg = f" • 🎴 <i> Пустой слот </i>"
        f3_icon = "ℹ️"
    else:
        f3_msg = deck_text(third, universe)
        f3_icon = "✅"
    if fourth == "empty":
        f4_msg = f" • 🎴 <i> Пустой слот </i>"
        f4_icon = "ℹ️"
    else:
        f4_msg = deck_text(fourth, universe)
        f4_icon = "✅"
    if fifth == "empty":
        f5_msg = f" • 🎴 <i> Пустой слот </i>"
        f5_icon = "ℹ️"
    else:
        f5_msg = deck_text(fifth, universe)
        f5_icon = "✅"
    if sixth == "empty":
        f6_msg = f" • 🎴 <i> Пустой слот </i>"
        f6_icon = "ℹ️"
    else:
        f6_msg = deck_text(sixth, universe)
        f6_icon = "✅"

    if "empty" in deck_data.values():
        msg = "❃ ℹ️ Есть пустые слоты в колоде"
    else:
        msg = "❃ ✅ Ваша колода готова к битве"

    pattern = dict(
        caption=f"❖  🃏<b> Ваша колода:</b>"
                f"\n✧•───────────────────────•✧"
                f"\n<blockquote expandable>"
                f"{f1_msg}"
                f"\n\n{f2_msg}"
                f"\n\n{f3_msg}"
                f"\n\n{f4_msg}"
                f"\n\n{f5_msg}"
                f"\n\n{f6_msg}"
                f"</blockquote>"
                f"\n✧•───────────────────────•✧"
                f"\n{msg}",
        reply_markup=inline_builder(
            [f"{f1_icon}", f"{f2_icon}", f"{f3_icon}",
             f"{f4_icon}", f"{f5_icon}", f"{f6_icon}",
             "🔙 Назад"],
            ["d1", "d2", "d3",
             "d4", "d5", "d6",
             "battle_arena"],
            row_width=[3, 3, 1]
        )
    )

    media_id = InputMediaPhoto(media='AgACAgIAAx0CfstymgACPb1nWiwJUdQC-37DUnytEI6vUZd25wACMvQxG_bt0Epw17D9NcuZQAEAAwIAA3kAAzYE')

    inline_id = callback.inline_message_id
    await callback.message.edit_media(media_id, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)


async def get_inventory(user_id, rarity):
    account = await mongodb.get_user(user_id)
    universe = account['universe']
    invent = account['inventory']['characters'][universe]
    if rarity == "d_divine":
        rarity = "divine"
    elif rarity == "d_mythical":
        rarity = "mythical"
    elif rarity == "d_legendary":
        rarity = "legendary"
    elif rarity == "d_epic":
        rarity = "epic"
    elif rarity == "d_rare":
        rarity = "rare"
    elif rarity == "d_common":
        rarity = "common"
    elif rarity == "d_halloween":
        rarity = "halloween"
    elif rarity == "d_soccer":
        rarity = "soccer"
    return invent[rarity], universe


@router.callback_query(F.data.in_(['d1', 'd2', 'd3', 'd4', 'd5', 'd6']))
async def inventory(callback: CallbackQuery | Message, state: FSMContext):
    await state.update_data(deck=callback.data)
    media_id = "CgACAgIAAxkBAAIVCmXMvbzs7hde-fvY9_4JCwU8W6HpAAKgOwACeyZoSuedvZenkxDNNAQ"
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    universe = account['universe']
    total_divine = len(account['inventory']['characters'][universe].get('divine', {}))
    total_mythical = len(account['inventory']['characters'][universe].get('mythical', {}))
    total_legendary = len(account['inventory']['characters'][universe].get('legendary', {}))
    total_epic = len(account['inventory']['characters'][universe].get('epic', {}))
    total_rare = len(account['inventory']['characters'][universe].get('rare', {}))
    total_common = len(account['inventory']['characters'][universe].get('common', {}))
    total_elements = 0
    for sublist in account['inventory']['characters'][universe].values():
        for item in sublist:
            if isinstance(item, str):
                total_elements += 1
    buttons = [f"🌠 Божественные 🌟 {total_divine}", f"🌌 Мифические ⭐️ {total_mythical}", f"🌅 Легендарные ⭐️ {total_legendary}",
               f"🎆 Эпические ⭐️ {total_epic}", f"🎇 Редкие ⭐️ {total_rare}", f"🌁 Обычные ⭐️ {total_common}", "🔙 Назад"]
    callbacks = ["d_divine", "d_mythical", "d_legendary", "d_epic", "d_rare", "d_common", f"{callback.data}"]

    if universe == "Allstars":
        if "halloween" in account['inventory']['characters']['Allstars']:
            total_halloween = len(account['inventory']['characters']['Allstars'].get('halloween', {}))
            buttons.insert(0, f"👻 Halloween 🎃 {total_halloween}")
            callbacks.insert(0, "halloween")
        # if "soccer" not in account['inventory']['characters']['Allstars']:
        #     account = await mongodb.get_user(user_id)
        #     await mongodb.update_user(user_id, {"inventory.characters.Allstars.soccer": []})
        #     total_soccer = len(account['inventory']['items'].get('soccer', {}))
        #     buttons.insert(0, f"⚽️ Soccer {total_soccer}")
        #     callbacks.insert(0, "soccer")

    pattern = dict(caption=f"🥡 Инвентарь"
                           f"\n── •✧✧• ────────────"
                           f"\n❖ Здесь вы можете увидеть все ваши 🃏 карты "
                           f"и выбрать их в качестве 🎴 персонажа на слот в колоде"
                           f"\n\n❖ Выберите ✨ редкость карты, чтобы посмотреть"
                           f"\n── •✧✧• ────────────"
                           f"\n❖ 🃏 Количество карт: {total_elements}",
                   reply_markup=inline_builder(
                       buttons,
                       callbacks, row_width=[1]))
    if isinstance(callback, CallbackQuery):
        inline_id = callback.inline_message_id
        media = InputMediaAnimation(media=media_id)
        await callback.message.edit_media(media, inline_id)
        await callback.message.edit_caption(inline_id, **pattern)
    else:
        await callback.answer_animation(animation=media_id, **pattern)


@router.callback_query(F.data.in_(['d_soccer', 'd_halloween', 'd_common', 'd_rare',
                                   'd_epic', 'd_legendary', 'd_mythical', 'd_divine']))
async def inventory(callback: CallbackQuery, state: FSMContext):
    await state.update_data(rarity=callback.data)
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    invent, universe = await get_inventory(user_id, callback.data)
    if invent == []:
        await callback.answer("❖ ✖️ У вас нет карт данной редкости", show_alert=True)
        return
    await state.update_data(character=invent[0])
    await state.update_data(universe=universe)
    avatar = character_photo.get_stats(universe, invent[0], 'avatar')
    avatar_type = character_photo.get_stats(universe, invent[0], 'type')
    if avatar_type == 'photo':
        photo = InputMediaPhoto(media=avatar)
    else:
        photo = InputMediaAnimation(media=avatar)
    rarity = character_photo.get_stats(universe, invent[0], 'rarity')
    msg = f"\n❖ ✨ Редкость: {rarity}"
    if universe not in ['Allstars', 'Allstars(old)']:
        strength = character_photo.get_stats(universe, invent[0], 'arena')['strength']
        agility = character_photo.get_stats(universe, invent[0], 'arena')['agility']
        intelligence = character_photo.get_stats(universe, invent[0], 'arena')['intelligence']
        power = character_photo.get_stats(universe, invent[0], 'arena')['power']
        msg = (f"\n❖ ✨ Редкость: {rarity}"
               f"\n❖ 🗺 Вселенная: {universe}"
               f"\n\n   ✊🏻 Сила: {strength}"
               f"\n   👣 Ловкость: {agility}"
               f"\n   🧠 Интелект: {intelligence}"
               f"\n   ⚜️ Мощь: {power}")
    await callback.message.edit_media(photo, inline_id)
    await callback.message.edit_caption(inline_id, caption=f"🎴 {invent[0]}"
                                                           f"\n ── •✧✧• ────────────"
                                                           f"{msg}"
                                                           f"\n──❀*̥˚──◌──◌──❀*̥˚────"
                                                           f"\n❖ 🔖 1 из {len(invent)}",
                                        reply_markup=pagination_card())


@router.callback_query(Pagination.filter(F.action.in_(["d_prev", "d_next"])))
async def inventory(callback: CallbackQuery, callback_data: Pagination, state: FSMContext):
    try:
        inline_id = callback.inline_message_id
        page_num = int(callback_data.page)
        user_data = await state.get_data()
        invent, universe = await get_inventory(callback.from_user.id, user_data['rarity'])

        if callback_data.action == "d_next":
            page_num = (page_num + 1) % len(invent)
        elif callback_data.action == "d_prev":
            page_num = (page_num - 1) % len(invent)

        with suppress(TelegramBadRequest):
            await state.update_data(character=invent[page_num])
            avatar = character_photo.get_stats(universe, invent[page_num], 'avatar')
            avatar_type = character_photo.get_stats(universe, invent[page_num], 'type')
            if avatar_type == 'photo':
                photo = InputMediaPhoto(media=avatar)
            else:
                photo = InputMediaAnimation(media=avatar)
            rarity = character_photo.get_stats(universe, invent[page_num], 'rarity')
            msg = f"\n❖ ✨ Редкость: {rarity}"
            if universe not in ['Allstars', 'Allstars(old)']:
                strength = character_photo.get_stats(universe, invent[page_num], 'arena')['strength']
                agility = character_photo.get_stats(universe, invent[page_num], 'arena')['agility']
                intelligence = character_photo.get_stats(universe, invent[page_num], 'arena')['intelligence']
                power = character_photo.get_stats(universe, invent[page_num], 'arena')['power']
                msg = (f"\n❖ ✨ Редкость: {rarity}"
                       f"\n❖ 🗺 Вселенная: {universe}"
                       f"\n\n   ✊🏻 Сила: {strength}"
                       f"\n   👣 Ловкость: {agility}"
                       f"\n   🧠 Интелект: {intelligence}"
                       f"\n   ⚜️ Мощь: {power}")

            await callback.message.edit_media(photo, inline_id)
            await callback.message.edit_caption(
                inline_id,
                caption=f"🎴 {invent[page_num]}"
                        f"\n ── •✧✧• ────────────"
                        f"{msg}"
                        f"\n──❀*̥˚──◌──◌──❀*̥˚────"
                        f"\n❖ 🔖 {page_num + 1} из {len(invent)}",
                reply_markup=pagination_card(page=page_num)
            )
        await callback.answer()
    except KeyError:
        await callback.answer("❖ 🔂 Идёт разработка бота связи с чем сессия была остановлена, вызовите "
                              "🥡 Инвентарь еще раз", show_alert=True)


@router.callback_query(F.data == "d_choice_card")
async def change_ch(callback: CallbackQuery, state: FSMContext):
    try:
        user_id = callback.from_user.id
        account = await mongodb.get_user(user_id)
        deck = account["deck"]
        data = await state.get_data()
        if data.get('character') in deck.values():
            await callback.answer("❖ 🔂 Этот персонаж уже есть в колоде", show_alert=True)
            return
        else:
            await mongodb.update_user(user_id, {f"deck.{data.get('deck')}": data.get('character')})
            await callback.answer("🎴 Вы успешно выбрали персонажа", show_alert=True)
            await choose_card(callback)
    except KeyError:
        await callback.answer("❖ 🔂 Идёт разработка бота связи с чем сессия была остановлена, вызовите "
                              "🥡 Инвентарь еще раз", show_alert=True)


async def surrender_f(user_id, r, mes, bot):
    await asyncio.sleep(60)
    if not user_data[user_id][r]:
        user_data[user_id][r] = True  # Обновляем состояние
        account = await mongodb.get_user(user_id)

        if account["battle"]["battle"]["status"] == 4:
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


@router.callback_query(F.data == "card_opponent")
async def search_opponent(callback: CallbackQuery | Message, bot: Bot):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    universe = account['universe']

    if isinstance(callback, CallbackQuery):
        await callback.message.delete()

    if account["battle"]["battle"]["status"] == 0:
        rival = await mongodb.find_card_opponent()

        await mongodb.update_user(user_id, {"battle.battle.status": 3})

        if rival is None:
            await bot.send_animation(
                chat_id=user_id,
                animation="CgACAgIAAx0CfstymgACBaNly1ESV41gB1s-k4M3VITaGbHvHwACPj8AAlpyWEpUUFtvRlRcpjQE",
                caption=f"\n 💡 <blockquote expandable>В разработке</blockquote>"
                        f"\n── •✧✧• ────────────"
                        f"\n❖ 🔎 Поиск соперника . . . . .",
                reply_markup=reply_builder("✖️ Отмена"))
        else:

            ident = account["_id"]
            name = account["name"]
            u_deck = account["deck"]
            character = account['character'][account['universe']]
            avatar = character_photo.get_stats(universe, character, 'avatar')
            avatar_type = character_photo.get_stats(universe, character, 'type')
            slave = None
            if account['inventory']['slaves']:
                slave = account['inventory']['slaves'][0]

            u1_character = card_characters.CardCharacters(ident, name, universe, f"┋{u_deck["d1"]}┋", u_deck["d1"], slave, rival["_id"], "d1")
            u2_character = card_characters.CardCharacters(ident, name, universe, f"┋{u_deck["d2"]}┋", u_deck["d2"], slave, rival["_id"], "d2")
            u3_character = card_characters.CardCharacters(ident, name, universe, f"┋{u_deck["d3"]}┋", u_deck["d3"], slave, rival["_id"], "d3")
            u4_character = card_characters.CardCharacters(ident, name, universe, f"┋{u_deck["d4"]}┋", u_deck["d4"], slave, rival["_id"], "d4")
            u5_character = card_characters.CardCharacters(ident, name, universe, f"┋{u_deck["d5"]}┋", u_deck["d5"], slave, rival["_id"], "d5")
            u6_character = card_characters.CardCharacters(ident, name, universe, f"┋{u_deck["d6"]}┋", u_deck["d6"], slave, rival["_id"], "d6")

            battle_data[ident] = {
                "deck": {"d1": u1_character,
                         "d2": u2_character,
                         "d3": u3_character,
                         "d4": u4_character,
                         "d5": u5_character,
                         "d6": u6_character,
                         },
                "rival": rival["_id"],
                "round": 1,
                "faze": 1,
                "turn": False,
                "last_win": False,
                "current": None,
                "current_cb": None
            }

            user_data[user_id] = {1: True}

            r_ident = rival["_id"]
            r_universe = rival['universe']
            r_name = rival["name"]
            ru_deck = rival["deck"]
            r_avatar = character_photo.get_stats(r_universe, ru_deck["d1"], 'avatar')
            r_avatar_type = character_photo.get_stats(r_universe, ru_deck["d1"], 'type')
            r_slave = None
            if rival['inventory']['slaves']:
                r_slave = rival['inventory']['slaves'][0]

            r1_character = card_characters.CardCharacters(r_ident, r_name, r_universe, f"┋{ru_deck["d1"]}┋", ru_deck["d1"], r_slave, ident, "d1")
            r2_character = card_characters.CardCharacters(r_ident, r_name, r_universe, f"┋{ru_deck["d2"]}┋", ru_deck["d2"], r_slave, ident, "d2")
            r3_character = card_characters.CardCharacters(r_ident, r_name, r_universe, f"┋{ru_deck["d3"]}┋", ru_deck["d3"], r_slave, ident, "d3")
            r4_character = card_characters.CardCharacters(r_ident, r_name, r_universe, f"┋{ru_deck["d4"]}┋", ru_deck["d4"], r_slave, ident, "d4")
            r5_character = card_characters.CardCharacters(r_ident, r_name, r_universe, f"┋{ru_deck["d5"]}┋", ru_deck["d5"], r_slave, ident, "d5")
            r6_character = card_characters.CardCharacters(r_ident, r_name, r_universe, f"┋{ru_deck["d6"]}┋", ru_deck["d6"], r_slave, ident, "d6")

            battle_data[r_ident] = {
                "deck": {"d1": r1_character,
                         "d2": r2_character,
                         "d3": r3_character,
                         "d4": r4_character,
                         "d5": r5_character,
                         "d6": r6_character
                         },
                "rival": ident,
                "round": 1,
                "faze": 1,
                "turn": False,
                "current": None,
                "current_cb": None
            }

            user_data[rival["_id"]] = {1: True}

            user_text = (f" ⚔️ Cоперник Найден! "
                         f"\n── •✧✧• ────────────"
                         f"\n 🪪  〢 {rival['name']} "
                         f"\n── •✧✧• ────────────"
                         f"\n<i>🀄️ Опыт: {rival['stats']['exp']} XP </i>")

            rival_text = (f"⚔️ Cоперник Найден! "
                          f"\n── •✧✧• ────────────"
                          f"\n 🪪  〢 {account['name']} "
                          f"\n── •✧✧• ────────────"
                          f"\n<i>🀄️ Опыт: {account['stats']['exp']} XP </i>")

            await mongodb.update_user(account["_id"], {"battle.battle.status": 4, "battle.battle.rid": rival["_id"]})
            await mongodb.update_user(rival["_id"], {"battle.battle.status": 4, "battle.battle.rid": account["_id"]})

            if r_avatar_type == 'photo':
                await bot.send_photo(chat_id=user_id, caption=user_text, photo=r_avatar,
                                     reply_markup=reply_builder("🏳️ Сдаться"))
            else:
                await bot.send_animation(chat_id=user_id, caption=user_text, animation=r_avatar,
                                         reply_markup=reply_builder("🏳️ Сдаться"))

            if avatar_type == 'photo':
                await bot.send_photo(chat_id=rival["_id"], caption=rival_text, photo=avatar,
                                     reply_markup=reply_builder("🏳️ Сдаться"))
            else:
                await bot.send_animation(chat_id=rival["_id"], caption=rival_text, animation=avatar,
                                         reply_markup=reply_builder("🏳️ Сдаться"))



            # user_text, user_status, user_cb, u_round = account_text(ident)
            # await bot.send_message(account["_id"], text=f"{user_text}"
            #                                             f"\n🔸 Слепой ход:",
            #                        reply_markup=inline_builder(user_status, user_cb, row_width=[3, 3]),
            #                        )
            #
            # rival_text, rival_status, rival_cb, r_round = account_text(r_ident)
            # mes = await bot.send_message(rival["_id"], text=f"{rival_text}"
            #                                                 f"\n🔸 Слепой ход:",
            #                              reply_markup=inline_builder(rival_status, rival_cb, row_width=[3, 3]),
            #                              )

            await surrender_f(rival["_id"], r_round, mes, bot)

    elif account["battle"]["battle"]["status"] == 1 or account["battle"]["battle"]["status"] == 3:
        if isinstance(callback, CallbackQuery):
            await callback.answer(
                text="💢 Вы уже находитесь в поиске соперника!",
                show_alert=True
            )
        else:
            await callback.answer(text="💢 Вы уже находитесь в поиске соперника!")

    elif account["battle"]["battle"]["status"] == 2 or account["battle"]["battle"]["status"] == 4:
        if isinstance(callback, CallbackQuery):
            await callback.answer(
                text="💢 Вы уже находитесь в битве!",
                show_alert=True
            )
        else:
            await callback.answer(text="💢 Вы уже находитесь в битве!")


@router.callback_query(CallbackChatTypeFilter(chat_type=["private"]), F.data.startswith("┋"))
async def start_battle(callback: CallbackQuery, bot: Bot):
    cb = callback.data
    player_id = callback.from_user.id
    rival_id = battle_data[player_id]["rival"]

    if battle_data[player_id]["round"] == 1:
        char = cb.replace("┋", "")
        battle_data[player_id]["current"] = char

        card, char_object = None, None
        for card_key, card_obj in battle_data[player_id]["deck"].items():
            if getattr(card_obj, "name", None) == char:  # Проверяем имя персонажа
                card, char_object = card_key, card_obj
                break  # Прерываем, если нашли

        user_text = round_text("Вы", char_object, battle_data[player_id]["round"], battle_data[player_id]["faze"])
        rival_text = round_text("Соперник", char_object, battle_data[player_id]["round"], battle_data[player_id]["faze"])

        avatar = character_photo.get_stats(char_object.universe, char_object.name, 'avatar')
        avatar_type = character_photo.get_stats(char_object.universe, char_object.name, 'type')

        if avatar_type == 'photo':
            await bot.send_photo(photo=avatar, chat_id=player_id, caption=user_text)
        else:
            await bot.send_animation(animation=avatar, chat_id=player_id, caption=user_text)

        if avatar_type == 'photo':
            await bot.send_photo(photo=avatar, chat_id=rival_id, caption=rival_text)
        else:
            await bot.send_animation(animation=avatar, chat_id=rival_id, caption=rival_text)


@router.message(ChatTypeFilter(chat_type=["private"]), Command("card_surrender"))
@router.message(F.text == "🏳️ Сдаться")
async def surrender(message: Message, bot: Bot):
    user_id = message.from_user.id
    account = await mongodb.get_user(user_id)

    if account["battle"]["battle"]["status"] == 4:
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
