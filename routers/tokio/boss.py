from datetime import datetime, timedelta
from aiogram import Router, F
from contextlib import suppress

from aiogram.types import CallbackQuery, InputMediaAnimation, InputMediaPhoto, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from data import mongodb
from data import character_photo
from data.character_photo import get_stats
from keyboards.builders import inline_builder, Pagination, pagination_boss

router = Router()

BOSSES = [
    {"name": "Огненный дракон", "hp": 1000, "damage": 100, 'class': 'Strength', 'defense': 20,
     "avatar": "CgACAgIAAx0CfstymgACPolna-3ni4cLL39VwuvlFiUQ8kQVVgACMmMAArowYUshoYqGQ-S3bjYE"},
    {"name": "Небесный дракон", "hp": 1000, "damage": 100, 'class': 'Agility', 'defense': 20,
     "avatar": "CgACAgIAAx0CfstymgACPn9na-1_e8cHSYA29Plm6gXFgBkzjQACK2MAArowYUsztOi5fvuTOTYE"},
]


@router.callback_query(F.data == "boss")
async def boss(callback: CallbackQuery):
    account = await mongodb.get_user(callback.from_user.id)
    user_id = callback.from_user.id

    # Текущее время
    current_datetime = datetime.now()
    if 'boss' not in account:
        # Если босса нет, создаем его
        account['boss'] = {
            "boss_id": 0,
            "name": BOSSES[0]["name"],
            "current_hp": BOSSES[0]["hp"],
            "avatar": BOSSES[0]["avatar"],
            "damage": BOSSES[0]["damage"],
            "class": BOSSES[0]["class"],
            "defense": BOSSES[0]["defense"],
            "last_spawn": current_datetime.isoformat(),
            "damage_dealt": 0
        }
        await mongodb.update_user(user_id, {"boss": account['boss']})
    account = await mongodb.get_user(user_id)
    last_spawn_raw = account['boss'].get('last_spawn')

    # Преобразуем last_spawn в datetime
    if isinstance(last_spawn_raw, str):
        last_spawn = datetime.fromisoformat(last_spawn_raw)
    else:
        last_spawn = last_spawn_raw or current_datetime

    # Вычисляем, сколько прошло времени
    elapsed = current_datetime - last_spawn

    # Если прошло больше 72 часов (3 дня)
    if elapsed >= timedelta(hours=72):
        current_boss_id = account['boss'].get("boss_id", 0)
        next_boss_id = (current_boss_id + 1) % len(BOSSES)  # Переход по кругу
        next_boss = BOSSES[next_boss_id]

        # Обновляем данные аккаунта
        account['boss'] = {
            "boss_id": next_boss_id,
            "name": next_boss["name"],
            "current_hp": next_boss["hp"],
            "avatar": next_boss["avatar"],
            "class": next_boss["class"],
            "last_spawn": current_datetime.isoformat(),
            "damage_dealt": 0
        }

        # ❗ не забудь сохранить обратно в базу, если используешь MongoDB:
        await mongodb.update_user(user_id, {"boss": account['boss']})

    # Отправляем сообщение с информацией о новом боссе
    boss_avatar = InputMediaAnimation(media=account['boss']['avatar'])
    await callback.message.edit_media(boss_avatar)
    if account['boss']['class'] == 'Strength':
        clas = "💪 Сила"
    elif account['boss']['class'] == 'Agility':
        clas = "🦶 Ловкость"
    else:
        clas = "🧠 Интеллект"

    # Время следующего респавна (72 часа после спавна)
    next_respawn = last_spawn + timedelta(hours=72)

    # Сколько осталось
    remaining = next_respawn - current_datetime

    if remaining.total_seconds() <= 0:
        text = "✅ Босс готов к обновлению!"
    else:
        total_minutes = int(remaining.total_seconds() // 60)
        days = total_minutes // (60 * 24)
        hours = (total_minutes // 60) % 24
        minutes = total_minutes % 60

        text = f"{days}д {hours}ч {minutes}мин"

    if "boss_squad" not in account:
        await mongodb.update_user(user_id, {"boss_squad": {
            "bg1": "empty",
            "bg1_universe": "empty",
            "bg2": "empty",
            "bg2_universe": "empty",
            "bg3": "empty",
            "bg3_universe": "empty",
            "bg4": "empty",
            "bg4_universe": "empty",
            "bg5": "empty",
            "bg5_universe": "empty",
            "bg6": "empty",
            "bg6_universe": "empty"
        }})
        account = await mongodb.get_user(user_id)

    await callback.message.edit_caption(
        caption=f"❖ 🐉 <b>{account['boss']['name']}</b>"
                f"\n── •✧✧• ────────────"
                f"\n<b>Класс: {clas}</b>"
                f"\n • ❤️ <b>{account['boss']['current_hp']}</b>"
                f"\n • ⚔️ <b>{account['boss']['damage']}</b>"
                f"\n • 🛡 <b>{account['boss']['defense']}</b>"
                f"\n⏱️ <b>Respawn:</b> {text}",
        parse_mode='HTML',
        reply_markup=inline_builder(
            ["🗡 Атаковать", "Отряд", "🔙 Назад"],
            ["battle_boss", "boss_squad", "tokio"],
            row_width=[1, 1, 1]
        )
    )


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


@router.callback_query(F.data == "boss_squad")
async def boss_squad(callback: CallbackQuery):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    universe = account['universe']

    deck = account.get("boss_squad", {})

    required_fields = {
        "bg1": "empty",
        "bg1_universe": "empty",
        "bg2": "empty",
        "bg2_universe": "empty",
        "bg3": "empty",
        "bg3_universe": "empty",
        "bg4": "empty",
        "bg4_universe": "empty",
        "bg5": "empty",
        "bg5_universe": "empty",
        "bg6": "empty",
        "bg6_universe": "empty"
    }

    for field, value in required_fields.items():
        if field not in deck:
            deck[field] = value

    await mongodb.update_user(user_id, {"boss_squad": deck})
    account = await mongodb.get_user(user_id)

    deck_data = account["boss_squad"]
    first = deck_data["bg1"]
    first_universe = deck_data["bg1_universe"]
    second = deck_data["bg2"]
    second_universe = deck_data["bg2_universe"]
    third = deck_data["bg3"]
    third_universe = deck_data["bg3_universe"]
    fourth = deck_data["bg4"]
    fourth_universe = deck_data["bg4_universe"]
    fifth = deck_data["bg5"]
    fifth_universe = deck_data["bg5_universe"]
    sixth = deck_data["bg6"]
    sixth_universe = deck_data["bg6_universe"]

    cards = [first, second, third, fourth, fifth, sixth]
    card_universes = [first_universe, second_universe, third_universe, fourth_universe, fifth_universe, sixth_universe]
    messages = []
    icons = []
    powers = []

    for card in cards:
        if card == "empty":
            messages.append(" • 🎴 <i> Пустое место </i>")
            icons.append("ℹ️")
            powers.append(0)
        else:
            p = get_stats(card_universes[cards.index(card)], card, 'arena')
            power = p.get('power')
            messages.append(deck_text(card, card_universes[cards.index(card)]))
            icons.append("✅")
            powers.append(power)

    # Доступ к результатам
    f1_msg, f2_msg, f3_msg, f4_msg, f5_msg, f6_msg = messages
    f1_icon, f2_icon, f3_icon, f4_icon, f5_icon, f6_icon = icons
    first, second, third, fourth, fifth, sixth = powers

    power = first + second + third + fourth + fifth + sixth

    if "empty" in deck_data.values():
        msg = "❃ ℹ️ Есть пустые места в отряде"
    else:
        msg = "❃ ✅ Ваш отряд готов к походу"

    pattern = dict(
        caption=f"<b>❖ 🕯 Отряд 🗡</b>"
                f"\n✧•───────────────────────•✧"
                f"\n<blockquote expandable>"
                f"{f1_msg}"
                f"\n\n{f2_msg}"
                f"\n\n{f3_msg}"
                f"\n\n{f4_msg}"
                f"\n\n{f5_msg}"
                f"\n\n{f6_msg}"
                f"</blockquote>"
                f"\n ⚜️ Сила отряда: {power}🗡"
                f"\n✧•───────────────────────•✧"
                f"\n{msg}",
        reply_markup=inline_builder(
            [f"{f1_icon}", f"{f2_icon}", f"{f3_icon}",
             f"{f4_icon}", f"{f5_icon}", f"{f6_icon}",
             "🔙 Назад"],
            ["bg1", "bg2", "bg3",
             "bg4", "bg5", "bg6",
             "dungeon"],
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
    if rarity == "bg_divine":
        rarity = "divine"
    elif rarity == "bg_mythical":
        rarity = "mythical"
    elif rarity == "bg_legendary":
        rarity = "legendary"
    elif rarity == "bg_epic":
        rarity = "epic"
    elif rarity == "bg_rare":
        rarity = "rare"
    elif rarity == "bg_common":
        rarity = "common"
    elif rarity == "bg_halloween":
        rarity = "halloween"
    elif rarity == "bg_soccer":
        rarity = "soccer"
    return invent[rarity], universe


@router.callback_query(F.data.in_(['bg1', 'bg2', 'bg3', 'bg4', 'bg5', 'bg6']))
async def inventory(callback: CallbackQuery | Message, state: FSMContext):
    await state.update_data(deck=callback.data)
    if callback.data == "bg1":
        await state.update_data(card_universe="bg1_universe")
    elif callback.data == "bg2":
        await state.update_data(card_universe="bg2_universe")
    elif callback.data == "bg3":
        await state.update_data(card_universe="bg3_universe")
    elif callback.data == "bg4":
        await state.update_data(card_universe="bg4_universe")
    elif callback.data == "bg5":
        await state.update_data(card_universe="bg5_universe")
    elif callback.data == "bg6":
        await state.update_data(card_universe="bg6_universe")
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
    msg = (f"\n❖ 🃏 Количество карт: {total_elements}"
           f"\n\n❖ 🌠 Божественные 🌟 {total_divine}"
           f"\n❖ 🌌 Мифические ⭐️ {total_mythical}"
           f"\n❖ 🌅 Легендарные ⭐️ {total_legendary}"
           f"\n❖ 🎆 Эпические ⭐️ {total_epic}"
           f"\n❖ 🎇 Редкие ⭐️ {total_rare}"
           f"\n❖ 🌁 Обычные ⭐️ {total_common}")
    buttons = [f"🌠 Божественные 🌟 {total_divine}", f"🌌 Мифические ⭐️ {total_mythical}", f"🌅 Легендарные ⭐️ {total_legendary}",
               f"🎆 Эпические ⭐️ {total_epic}", f"🎇 Редкие ⭐️ {total_rare}", f"🌁 Обычные ⭐️ {total_common}", "🔙 Назад"]
    callbacks = ["bg_divine", "bg_mythical", "bg_legendary", "bg_epic", "bg_rare", "bg_common", "boss_squad"]

    if universe == "Allstars":
        if "halloween" in account['inventory']['characters']['Allstars']:
            total_halloween = len(account['inventory']['characters']['Allstars'].get('halloween', {}))
            buttons.insert(0, f"👻 Halloween 🎃 {total_halloween}")
            callbacks.insert(0, "bg_halloween")
        # if "soccer" not in account['inventory']['characters']['Allstars']:
        #     account = await mongodb.get_user(user_id)
        #     await mongodb.update_user(user_id, {"inventory.characters.Allstars.soccer": []})
        #     total_soccer = len(account['inventory']['items'].get('soccer', {}))
        #     buttons.insert(0, f"⚽️ Soccer {total_soccer}")
        #     callbacks.insert(0, "soccer")

    pattern = dict(caption=f"🥡 Инвентарь"
                           f"\n── •✧✧• ────────────"
                           f"\n❖ Здесь вы можете увидеть все ваши 🃏 карты "
                           f"и выбрать 🎴 персонажа к 🏴отряду в подземелья"
                           f"\n\n❖ Выберите ✨ редкость карты, чтобы выбрать персонажа"
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


@router.callback_query(F.data.in_(['bg_soccer', 'bg_halloween', 'bg_common', 'bg_rare',
                                   'bg_epic', 'bg_legendary', 'bg_mythical', 'bg_divine']))
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
                                        reply_markup=pagination_boss())


@router.callback_query(Pagination.filter(F.action.in_(["bg_prev", "bg_next"])))
async def inventory(callback: CallbackQuery, callback_data: Pagination, state: FSMContext):
    try:
        inline_id = callback.inline_message_id
        page_num = int(callback_data.page)
        user_data = await state.get_data()
        invent, universe = await get_inventory(callback.from_user.id, user_data['rarity'])

        if callback_data.action == "bg_next":
            page_num = (page_num + 1) % len(invent)
        elif callback_data.action == "bg_prev":
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
                reply_markup=pagination_boss(page=page_num)
            )
        await callback.answer()
    except KeyError:
        await callback.answer("❖ 🔂 Идёт разработка бота связи с чем сессия была остановлена, вызовите "
                              "🥡 Инвентарь еще раз", show_alert=True)


@router.callback_query(F.data == "bg_choice_card")
async def change_ch(callback: CallbackQuery, state: FSMContext):
    try:
        user_id = callback.from_user.id
        account = await mongodb.get_user(user_id)
        deck = account["boss_squad"]
        data = await state.get_data()
        if data.get('character') in deck.values():
            await callback.answer("❖ 🔂 Этот персонаж уже есть в колоде", show_alert=True)
            return
        else:
            await mongodb.update_user(user_id, {f"boss_squad.{data.get('deck')}": data.get('character')})
            await mongodb.update_user(user_id, {f"boss_squad.{data.get('card_universe')}": data.get('universe')})
            await callback.answer("🎴 Вы успешно выбрали персонажа", show_alert=True)
            await boss_squad(callback)
    except KeyError:
        await callback.answer("❖ 🔂 Идёт разработка бота связи с чем сессия была остановлена, вызовите "
                              "🥡 Инвентарь еще раз", show_alert=True)
