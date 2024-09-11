from datetime import datetime, timedelta
import random
import asyncio

from aiogram import Router, F

from aiogram.enums import ParseMode
from aiogram.types import InputMediaAnimation, InputMediaPhoto, Message

from data import mongodb, character_photo
from keyboards.builders import inline_builder, start_button, menu_button, success, Ability

router = Router()

characters = {
    'Bleach': {
        'divine': ['Toshiro Hitsuyaga 🌠', 'Ulquiorra Cifer 🌠', 'Urahara Kisuke🌠', 'Toshiro Hitsuyaga🌠', 'Aizen Sosuke🌠', 'Aizen Sosuke 🌠', 'Aizen Sosuke 🌠 ', 'Aizen Sosuke  🌠', 'Ichigo Kurosaki 🌠', 'Ichigo Kurosaki  🌠', 'Ichigo Kurosaki 🌠 ', 'Ichigo Kurosaki🌠 ', 'Ichigo Kurosaki🌠'],
        'mythical': ['Toshiro Hitsuyaga 🌌', 'Urahara Kisuke🌌', 'Urahara Kisuke 🌌', 'Urahara Kisuke 🌌 ', 'Urahara Kisuke  🌌', 'Ulquiorra Cifer 🌌', 'Ulquiorra Cifer🌌', 'Aizen Sosuke 🌌', 'Aizen Sosuke🌌', 'Aizen Sosuke 🌌 ', 'Ichigo Kurosaki 🌌', 'Ichigo Kurosaki  🌌', 'Ichigo Kurosaki 🌌 '],
        'legendary': ['Ichigo Kurosaki 🌅'],
        'epic': ['Toshiro Hitsuyaga 🎆', 'Toshiro Hitsuyaga🎆', 'Aizen Sosuke 🎆', 'Ichigo Kurosaki 🎆', 'Ichigo Kurosaki 🎆', 'Ichigo Kurosaki🎆'],
        'rare': ['Toshiro Hitsuyaga 🎇', 'Toshiro Hitsuyaga🎇', 'Urahara Kisuke 🎇', 'Ichigo Kurosaki 🎇', 'Ichigo Kurosaki🎇', 'Ichigo Kurosaki 🎇 '],
        'common': ['Toshiro Hitsuyaga 🌁', 'Ulquiorra Cifer 🌁', 'Ulquiorra Cifer🌁', 'Urahara Kisuke 🌁', 'Urahara Kisuke🌁', 'Aizen Sosuke 🌁', 'Aizen Sosuke🌁', 'Toshiro Hitsuyaga🌁', 'Toshiro Hitsuyaga 🌁 ', 'Toshiro Hitsuyaga  🌁', 'Ichigo Kurosaki 🌁', 'Ichigo Kurosaki🌁', 'Ichigo Kurosaki 🌁 ', 'Ichigo Kurosaki  🌁']
    }
}


def common_gacha():
    rand_num = random.random()
    if rand_num < 0.0003:  # 0.03% шанс
        return 'divine'
    elif rand_num < 0.003:  # 0.3% шанс
        return 'mythical'
    elif rand_num < 0.023:  # 2.3% шанс
        return 'legendary'
    elif rand_num < 0.123:  # 12.3% шанс
        return 'epic'
    elif rand_num < 0.303:  # 30.3% шанс
        return 'rare'
    else:  # 50.87% шанс
        return 'common'


def golden_gacha():
    rand_num = random.random()
    if rand_num < 0.01:  # 1% шанс
        return 'divine'
    elif rand_num < 0.06:  # 6% шанс
        return 'mythical'
    elif rand_num < 0.21:  # 21% шанс
        return 'legendary'
    elif rand_num < 0.46:  # 46% шанс
        return 'epic'
    else:  # 26% шанс
        return 'rare'


def sacred_gacha():
    rand_num = random.random()
    if rand_num < 0.25:  # 25% шанс
        return 'divine'
    elif rand_num < 0.35:  # 35% шанс
        return 'mythical'
    else:  # 40% шанс
        return 'legendary'


async def card_gacha(user_id, callback):

    account = await mongodb.get_user(user_id)
    universe = account['universe']
    inline_id = callback.inline_message_id

    if callback.data == "golden_key":
        if account['inventory']['items']['tickets']['keys'] < 1:
            await callback.answer(
                text="❖  💮 У вас нет  🧧 священнего билета. Приобретите его в рынке!",
                show_alert=True
            )
            return
        character_category = sacred_gacha()  # Используем новую функцию здесь
        await mongodb.update_value(user_id, {'inventory.items.tickets.keys': -1})
        icon = "🧧"
        button = "golden_key"
    elif callback.data == "golden":
        if account['inventory']['items']['tickets']['golden'] < 1:
            await callback.answer(
                text="❖  💮 У вас нет  🎫 золотого билета. Приобретите его в рынке!",
                show_alert=True
            )
            return
        character_category = golden_gacha()
        await mongodb.update_value(user_id, {'inventory.items.tickets.golden': -1})
        icon = "🎫"
        button = "golden"
    else:
        if account['inventory']['items']['tickets']['common'] < 1:
            await callback.answer(
                text="❖  💮 У вас нет  🎟 обычного билета. Приобретите его в рынке!",
                show_alert=True
            )
            return
        character_category = common_gacha()
        await mongodb.update_value(user_id, {'inventory.items.tickets.common': -1})
        icon = "🎟"
        button = "common_summon"

    character = random.choice(characters[universe][character_category])  # Выбираем случайного персонажа из списка
    avatar = character_photo.get_stats(universe, character, 'avatar')
    avatar_type = character_photo.get_stats(universe, character, 'type')
    ch_universe = character_photo.get_stats(universe, character, 'universe')
    rarity = character_photo.get_stats(universe, character, 'rarity')
    strength = character_photo.get_stats(universe, character, 'arena')['strength']
    agility = character_photo.get_stats(universe, character, 'arena')['agility']
    intelligence = character_photo.get_stats(universe, character, 'arena')['intelligence']
    power = character_photo.get_stats(universe, character, 'arena')['power']

    async def is_in_inventory():
        get_account = await mongodb.get_user(user_id)
        ch_characters = get_account['inventory'].get('characters')
        if characters:
            universe_characters = ch_characters.get(universe)
            if universe_characters:
                return character in universe_characters.get(character_category, [])
        return False

    if await is_in_inventory():
        fragments = 4
        # Если персонаж уже в инвентаре, увеличиваем только силу и деньги
        await mongodb.update_value(user_id, {'account.fragments': fragments})
        message = (f"\n❖ Вам попалась повторка:"
                   f"\n<i> Зачислены только бонусы"
                   f"\n + 2х 🧩 Осколков </i>")
    else:
        fragments = 2
        # Если персонажа нет в инвентаре, добавляем его и увеличиваем силу, деньги и количество персонажей
        await mongodb.push(universe, character_category, character, user_id)
        await mongodb.update_value(user_id, {'campaign.power': power})
        await mongodb.update_value(user_id, {'account.fragments': fragments})
        message = (f"\n❖ ✨ Редкость: {rarity}"
                   f"\n❖ 🗺 Вселенная: {ch_universe}"
                   f"\n\n   ✊🏻 Сила: {strength}"
                   f"\n   👣 Ловкость: {agility}"
                   f"\n   🧠 Интелект: {intelligence}"
                   f"\n   ⚜️ Мощь: {power}")

    pattern = dict(
        caption=f"\n ── •✧✧• ────────────"
                f"\n  🃏  〢 {character} "
                f"\n ── •✧✧• ────────────"
                f"{message}"
                f"\n──❀*̥˚──◌──◌──❀*̥˚────"
                f"\n<i> + {fragments}🧩 Осколков </i>",
        reply_markup=inline_builder(
            ["🎴 Навыки", " 🔙 ", f"{icon}"],
            [Ability(action="ability", universe=universe,
                     character=character, back='banner'), "banner", f"{button}"],
            row_width=[1, 2]),
        parse_mode=ParseMode.HTML
    )

    if character_category == 'divine':
        media_id = "CgACAgIAAx0CfstymgACBiVlzikq6HGeA2exxOQQbekNg_KImAACDEIAAsuUcUpNy3ouWDG9xTQE"
        time = 7
    elif character_category == 'mythical':
        media_id = "CgACAgIAAx0CfstymgACBiRlzikgAAEbiUWlzuHAYpT3rlL91O4AAgtCAALLlHFKEzbl8cFs3cg0BA"
        time = 6.2
    elif character_category == 'legendary':
        media_id = "CgACAgIAAx0CfstymgACBiNlzikdQ_RssBYRl4A0G--qgie-ewACCkIAAsuUcUo0j4VTQm0baDQE"
        time = 7.2
    elif character_category == 'epic':
        media_id = "CgACAgIAAx0CfstymgACBixlzivkRBW3Iki8XQ11VLPBx7nqXAACH0IAAsuUcUojWO7WBnMQlzQE"
        time = 7.3
    elif character_category == 'rare':
        media_id = "CgACAgIAAx0CfstymgACBitlzivdoGBCYVhnFaEGl6QWqoxXhgACHkIAAsuUcUqp4UhpJLR2LTQE"
        time = 7.2
    else:
        media_id = "CgACAgIAAx0CfstymgACBiplzivQmnDtjQTgUR23iW_IC4XYjwACHUIAAsuUcUoqWzNNWaav6zQE"
        time = 7.2

    media = InputMediaAnimation(media=media_id)

    await callback.message.edit_media(media, inline_id)

    await asyncio.sleep(time)

    if avatar_type == 'photo':
        media = InputMediaPhoto(media=avatar)
    else:
        media = InputMediaAnimation(media=avatar)

    await callback.message.edit_media(media, inline_id)

    await callback.message.edit_caption(inline_id, **pattern)


async def first_summon(callback, universe):
    inline_id = callback.inline_message_id
    character_category = common_gacha()

    character = random.choice(characters[universe][character_category])  # Выбираем случайного персонажа из списка
    avatar = character_photo.get_stats(universe, character, 'avatar')
    avatar_type = character_photo.get_stats(universe, character, 'type')
    ch_universe = character_photo.get_stats(universe, character, 'universe')
    rarity = character_photo.get_stats(universe, character, 'rarity')
    strength = character_photo.get_stats(universe, character, 'arena')['strength']
    agility = character_photo.get_stats(universe, character, 'arena')['agility']
    intelligence = character_photo.get_stats(universe, character, 'arena')['intelligence']
    power = character_photo.get_stats(universe, character, 'arena')['power']

    pattern = dict(
        caption=f"\n ── •✧✧• ────────────"
                f"\n  🎴  〢 {character} "
                f"\n ── •✧✧• ────────────"
                f"\n❖ ✨ Редкость: {rarity}"
                f"\n❖ 🗺 Вселенная: {ch_universe}"
                f"\n\n   ✊🏻 Сила: {strength}"
                f"\n   👣 Ловкость: {agility}"
                f"\n   🧠 Интелект: {intelligence}"
                f"\n   ⚜️ Мощь: {power}"
                f"\n──❀*̥˚──◌──◌──❀*̥˚────",
        reply_markup=success(),
        parse_mode=ParseMode.HTML
    )

    if avatar_type == 'photo':
        new_photo = InputMediaPhoto(media=avatar)
    else:
        new_photo = InputMediaAnimation(media=avatar)

    if character_category == 'divine':
        media_id = "CgACAgIAAx0CfstymgACBiVlzikq6HGeA2exxOQQbekNg_KImAACDEIAAsuUcUpNy3ouWDG9xTQE"
        time = 7
    elif character_category == 'mythical':
        media_id = "CgACAgIAAx0CfstymgACBiRlzikgAAEbiUWlzuHAYpT3rlL91O4AAgtCAALLlHFKEzbl8cFs3cg0BA"
        time = 6.2
    elif character_category == 'legendary':
        media_id = "CgACAgIAAx0CfstymgACBiNlzikdQ_RssBYRl4A0G--qgie-ewACCkIAAsuUcUo0j4VTQm0baDQE"
        time = 7.2
    elif character_category == 'epic':
        media_id = "CgACAgIAAx0CfstymgACBixlzivkRBW3Iki8XQ11VLPBx7nqXAACH0IAAsuUcUojWO7WBnMQlzQE"
        time = 7.3
    elif character_category == 'rare':
        media_id = "CgACAgIAAx0CfstymgACBitlzivdoGBCYVhnFaEGl6QWqoxXhgACHkIAAsuUcUqp4UhpJLR2LTQE"
        time = 7.2
    else:
        media_id = "CgACAgIAAx0CfstymgACBiplzivQmnDtjQTgUR23iW_IC4XYjwACHUIAAsuUcUoqWzNNWaav6zQE"
        time = 7.2

    media = InputMediaAnimation(media=media_id)

    await callback.message.edit_media(media, inline_id)

    await asyncio.sleep(time)

    await callback.message.edit_media(new_photo, inline_id)

    await callback.message.edit_caption(inline_message_id=inline_id, **pattern)
    await callback.message.answer("❖ Добро пожаловать", reply_markup=menu_button())
    return character, character_category, power


@router.message((F.text == 'Получить карту') | (F.text == 'получить карту')
                | (F.text == 'призыв') | (F.text == 'Призыв') | (F.text == '🎴 Получить карту'))
async def campaign_rank(message: Message):
    user_id = message.from_user.id
    account = await mongodb.get_user(user_id)
    universe = account['universe']

    if account is not None and account['_id'] == user_id:
        # Если 'last_call_time' не существует, установите его в текущее время
        if 'last_call_time' not in account or datetime.now() - account['last_call_time'] >= timedelta(hours=4):
            now = datetime.now()
            await mongodb.update_get_card(user_id, now)
            # Извлеките обновленные данные после обновления
            character_category = golden_gacha()
            character = random.choice(characters[universe][character_category])
            avatar = character_photo.get_stats(universe, character, 'avatar')
            avatar_type = character_photo.get_stats(universe, character, 'type')
            ch_universe = character_photo.get_stats(universe, character, 'universe')
            rarity = character_photo.get_stats(universe, character, 'rarity')
            strength = character_photo.get_stats(universe, character, 'arena')['strength']
            agility = character_photo.get_stats(universe, character, 'arena')['agility']
            intelligence = character_photo.get_stats(universe, character, 'arena')['intelligence']

            async def is_in_inventory():
                get_account = await mongodb.get_user(user_id)
                if universe in get_account['inventory']['characters'] and character_category in \
                        get_account['inventory']['characters'][universe]:
                    return character in get_account['inventory']['characters'][universe][character_category]
                else:
                    return False

            if await is_in_inventory():
                fragments = 4
                # Если персонаж уже в инвентаре, увеличиваем только силу и деньги
                await mongodb.update_value(user_id, {'account.fragments': fragments})
                msg = (f"\n❖ Вам попалась повторка:"
                       f"\n<i> Зачислены только бонусы"
                       f"\n + 2х 🧩 Осколков </i>")
            else:
                fragments = 2
                character_category = account['inventory']['characters'][universe].get('character_category', None)
                await mongodb.push(universe, character_category, character, user_id)
                await mongodb.update_value(user_id, {'account.fragments': fragments})
                msg = (f"\n❖ ✨ Редкость: {rarity}"
                       f"\n\n   🗺 Вселенная: {ch_universe}"
                       f"\n\n   ✊🏻 Сила: {strength}"
                       f"\n   👣 Ловкость: {agility}"
                       f"\n   🧠 Интелект: {intelligence}")

            pattern = dict(
                caption=f"\n ── •✧✧• ────────────"
                        f"\n  🃏  〢 {character} "
                        f"\n ── •✧✧• ────────────"
                        f"{msg}"
                        f"\n\n──❀*̥˚──◌──◌──❀*̥˚────"
                        f"\n<i> + {fragments}🧩 Осколков </i>",
                reply_markup=inline_builder(["🎴 Навыки"],
                                            [Ability(action="ability", universe=universe, character=character),
                                             "banner", "golden"],
                                            row_width=[1]),
                parse_mode=ParseMode.HTML
            )

            if character_category == 'divine':
                media_id = "CgACAgIAAx0CfstymgACBiVlzikq6HGeA2exxOQQbekNg_KImAACDEIAAsuUcUpNy3ouWDG9xTQE"
                time = 7
            elif character_category == 'mythical':
                media_id = "CgACAgIAAx0CfstymgACBiRlzikgAAEbiUWlzuHAYpT3rlL91O4AAgtCAALLlHFKEzbl8cFs3cg0BA"
                time = 6.2
            elif character_category == 'legendary':
                media_id = "CgACAgIAAx0CfstymgACBiNlzikdQ_RssBYRl4A0G--qgie-ewACCkIAAsuUcUo0j4VTQm0baDQE"
                time = 7.2
            elif character_category == 'epic':
                media_id = "CgACAgIAAx0CfstymgACBixlzivkRBW3Iki8XQ11VLPBx7nqXAACH0IAAsuUcUojWO7WBnMQlzQE"
                time = 7.3
            elif character_category == 'rare':
                media_id = "CgACAgIAAx0CfstymgACBitlzivdoGBCYVhnFaEGl6QWqoxXhgACHkIAAsuUcUqp4UhpJLR2LTQE"
                time = 7.2
            else:
                media_id = "CgACAgIAAx0CfstymgACBiplzivQmnDtjQTgUR23iW_IC4XYjwACHUIAAsuUcUoqWzNNWaav6zQE"
                time = 7.2

            gacha_msg = await message.reply_animation(media_id)

            await asyncio.sleep(time)

            if avatar_type == 'photo':
                new_photo = InputMediaPhoto(media=avatar)
            else:
                new_photo = InputMediaAnimation(media=avatar)

            await gacha_msg.edit_media(new_photo)
            await gacha_msg.edit_caption(**pattern)

        else:
            # Вычислите, сколько времени осталось
            remaining_time = timedelta(hours=4) - (datetime.now() - account['last_call_time'])
            remaining_seconds = int(remaining_time.total_seconds())
            remaining_hours = remaining_seconds // 3600
            remaining_minutes = (remaining_seconds % 3600) // 60

            await message.reply_animation(
                animation="CgACAgIAAx0CfstymgACBzpl0I7O2WanntSMhoK4cXEfBxt33AAC4j8AAvasiUp11UMJwtm8UTQE",
                caption="\n ── •✧✧• ────────────"
                f"\n✶ 🔮 Мжно совершить бесплатный 🎫 золотой призыв раз в ⏳ 4 часа"
                f"\n ── •✧✧• ────────────"
                f"\n⏳ подожди еще {remaining_hours}ч {remaining_minutes}мин")
    else:
        media = "CgACAgIAAx0CfstymgACBbRlzDgYWpgLO50Lgeg0HImQEC9GEAAC7D4AAsywYUo5sbjTkVkCRjQE"
        await message.answer_animation(animation=media, caption="✧ • 📄 Ты не регистрирован"
                                                                f"\n── •✧✧• ────────────"
                                                                f"\n❖ 💮 Присоединяйся в мир битв и "
                                                                f"получи своего первого 🎴 персонажа"
                                                                f"\n\n── •✧✧• ────────────",
                                       reply_markup=start_button())
