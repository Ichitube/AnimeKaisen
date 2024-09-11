from contextlib import suppress
from aiogram import Router, F
from typing import Match

from aiogram.types import Message, CallbackQuery, InputMediaAnimation, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from keyboards.builders import start_button, goto_bot, inline_builder, Pagination, pagination_group
from data import mongodb, character_photo
from recycling import profile

router = Router()


async def get_inventory(data):
    rarity, user_id = data.split('/')

    rarity_dict = {
        'gd': 'divine',
        'gm': 'mythical',
        'gl': 'legendary',
        'ge': 'epic',
        'gr': 'rare',
        'gc': 'common'
    }
    rarity = rarity_dict[rarity]

    account = await mongodb.get_user(int(user_id))
    invent = account['inventory']['characters']
    return invent[rarity]


@router.message(F.text.lower().in_(['кто я', 'профиль']))
async def main_chat(message: Message):
    user_id = message.from_user.id
    account = await mongodb.get_user(user_id)

    if account is not None and account['_id'] == user_id:

        universe = account['universe']
        character = account['character']
        avatar = character_photo.get_stats(universe, character, 'avatar')
        avatar_type = character_photo.get_stats(universe, character, 'type')

        await profile.update_rank(user_id, account["battle"]["stats"]['wins'])
        await profile.update_level(user_id, account["campaign"]["count"])

        rank = await profile.rerank(account['stats']['rank'])
        level = await profile.level(account['campaign']['level'])

        characters = account['inventory']['characters']

        total_characters = 0
        for outer_key in characters:
            for inner_key in characters[outer_key]:
                total_characters += len(characters[outer_key][inner_key])

        pattern = dict(
            caption=f"\n── •✧✧• ────────────"
                    f"\n 🪪  〢 Профиль {account['name']} "
                    f"\n── •✧✧• ────────────"
                    f"\n\n❖🎴 <b>{character}</b>"
                    f"\n❖🗺 Вселенная: {universe}"
                    f"\n❖🎐 <b>{rank}</b>"
                    f"\n❖⛩️ <b>{level}</b>"
                    f"\n\n── •✧✧• ────────────"
                    f"\n<i><b>❃💴 {account['account']['money']} ¥ ❃ {account['campaign']['power']} ⚜️ Мощи"
                    f"\n❃🀄️ {account['stats']['exp']} XP ❃ {total_characters} 🃏 Карт</b></i>",
            parse_mode=ParseMode.HTML,
            reply_markup=goto_bot()
        )
        if avatar_type == 'photo':
            await message.answer_photo(avatar, **pattern)
        else:
            await message.answer_animation(avatar, **pattern)
    else:
        media = "CgACAgIAAx0CfstymgACBbRlzDgYWpgLO50Lgeg0HImQEC9GEAAC7D4AAsywYUo5sbjTkVkCRjQE"
        await message.answer_animation(animation=media, caption="✧ • 📄 Ты не регистрирован"
                                                                f"\n── •✧✧• ────────────"
                                                                f"\n❖ 💮 Присоединяйся к нам и "
                                                                f"получи свою первую 🎴 карту"
                                                                f"\n── •✧✧• ────────────",
                                       reply_markup=start_button())


@router.message(F.text.lower().in_(['топ', 'стата']))
async def campaign_rank(message: Message):
    chat_id = message.chat.id
    rating = await mongodb.chat_rating(chat_id, '👑')

    await message.answer(f"❖  🏆  <b>Сильнейшие игроки чата</b>"
                         f"\n── •✧✧• ────────────"
                         f"{rating}", disable_web_page_preview=True)

"""
@router.message((F.text == 'инвентарь') | (F.text == 'Инвентарь') | (F.text == 'карты')
                | (F.text == 'Карты') | (F.text == '🥡 Инвентарь'))
@router.callback_query(F.data.regexp("(g_inventory)\/([0-9]*)$").as_("data"))
async def inventory(message: Message | CallbackQuery, state: FSMContext):
    user_id = message.from_user.id
    account = await mongodb.get_user(user_id)

    if account is not None and account['_id'] == user_id:

        await state.update_data(id=user_id)
        media_id = "CgACAgIAAxkBAAIVCmXMvbzs7hde-fvY9_4JCwU8W6HpAAKgOwACeyZoSuedvZenkxDNNAQ"
        total_divine = len(account['inventory']['characters']['divine'])
        total_mythical = len(account['inventory']['characters']['mythical'])
        total_legendary = len(account['inventory']['characters']['legendary'])
        total_epic = len(account['inventory']['characters']['epic'])
        total_rare = len(account['inventory']['characters']['rare'])
        total_common = len(account['inventory']['characters']['common'])
        total_elements = sum(len(account['inventory']['characters'][sublist])
                             for sublist in account['inventory']['characters'])

        pattern = dict(caption=f"🥡 Инвентарь"
                               f"\n── •✧✧• ────────────"
                               f"\n❖ Здесь вы можете увидеть все ваши 🎴 карты"
                               f"\n\n❖ Выберите ✨ редкость карты, "
                               f"чтобы посмотреть их"
                               f"\n── •✧✧• ────────────"
                               f"\n❖ 🎴 Количество карт: {total_elements}",
                       reply_markup=inline_builder([f"🌠 Божественные 🌟 {total_divine}",
                                                    f"🌌 Мифические ⭐️ {total_mythical}",
                                                    f"🌅 Легендарные ⭐️ {total_legendary}",
                                                    f"🎆 Эпические ⭐️ {total_epic}",
                                                    f"🎇 Редкие ⭐️ {total_rare}",
                                                    f"🌁 Обычные ⭐️ {total_common}"],
                                                   [f"gd/{user_id}", f"gm/{user_id}", f"gl/{user_id}",
                                                    f"ge/{user_id}", f"gr/{user_id}", f"gc/{user_id}"], row_width=[1]))
        if isinstance(message, CallbackQuery):
            callback_id = message.inline_message_id
            await message.message.edit_caption(inline_message_id=callback_id, **pattern)
        else:
            await message.answer_animation(animation=media_id, **pattern)
    else:
        media = "CgACAgIAAx0CfstymgACBbRlzDgYWpgLO50Lgeg0HImQEC9GEAAC7D4AAsywYUo5sbjTkVkCRjQE"
        await message.answer_animation(animation=media, caption="✧ • 📄 Ты не регистрирован"
                                                                f"\n── •✧✧• ────────────"
                                                                f"\n❖ 💮 Присоединяйся к нам и "
                                                                f"получи свою первую 🎴 карту"
                                                                f"\n── •✧✧• ────────────",
                                       reply_markup=start_button())


@router.callback_query(F.data.regexp("(gd|gm|gl|ge|gr|gc)\/([0-9]*)$").as_("data"))
async def inventory(callback: CallbackQuery, state: FSMContext, data: Match[str]):
    g, user_id = data.groups()
    if callback.from_user.id != int(user_id):
        await callback.answer("❖ ✖️ Это не ваш инвентарь", show_alert=True)
        return

    await state.update_data(rarity=callback.data)
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    invent = await get_inventory(callback.data)
    if invent == []:
        await callback.answer("❖ ✖️ У вас нет карт данной редкости", show_alert=True)
        return
    await state.update_data(character=invent[0])
    file, file_type = character_photo.get_file_id(invent[0])
    if file_type == 'photo':
        photo = InputMediaPhoto(media=file)
    else:
        photo = InputMediaAnimation(media=file)
    stats = character_photo.get_stats(invent[0])
    await callback.message.edit_media(photo, inline_id)
    await callback.message.edit_caption(inline_id, f"🎴 {invent[0]}"
                                                   f"\n ── •✧✧• ────────────"
                                                   f"\n❖ ✨ Редкость: {stats[5]}"
                                                   f"\n\n ⚜️ Сила: {stats[0]}"
                                                   f"\n ❤️ Здоровье: {stats[1]}"
                                                   f"\n 🗡 Атака: {stats[2]}"
                                                   f"\n 🧪 Мана: {stats[3]}"
                                                   f"\n 🛡 Защита {stats[4]}"
                                                   f"\n──❀*̥˚──◌──◌──❀*̥˚────"
                                                   f"\n❖ 🔖 1 из {len(invent)}",
                                        reply_markup=pagination_group(user_id))


@router.callback_query(Pagination.filter(F.action.regexp("(g_prev|g_next)\/([0-9]*)$").as_("data")))
async def inventory(callback: CallbackQuery, callback_data: Pagination, state: FSMContext, data: Match[str]):
    await callback.answer("Успешно")
    inline_id = callback.inline_message_id
    page_num = int(callback_data.page)
    user_data = await state.get_data()

    g, user_id = data.groups()
    if callback.from_user.id != int(user_id):
        await callback.answer("❖ ✖️ Это не ваш инвентарь", show_alert=True)
        return

    invent = await get_inventory(user_data['rarity'])

    action, user_id = callback_data.action.split('/')

    if action == "g_next":
        page_num = (page_num + 1) % len(invent)
    elif action == "g_prev":
        page_num = (page_num - 1) % len(invent)

    with suppress(TelegramBadRequest):
        await state.update_data(character=invent[page_num])
        stats = character_photo.get_stats(invent[page_num])
        file, file_type = character_photo.get_file_id(invent[page_num])
        if file_type == 'photo':
            photo = InputMediaPhoto(media=file)
        else:
            photo = InputMediaAnimation(media=file)
        await callback.message.edit_media(photo, inline_id)
        await callback.message.edit_caption(
            inline_id,
            f"🎴 {invent[page_num]}"
            f"\n ── •✧✧• ────────────"
            f"\n❖ 🌠 Редкость: {stats[5]}"
            f"\n\n ⚜️ Сила: {stats[0]}"
            f"\n ❤️ Здоровье: {stats[1]}"
            f"\n 🗡 Атака: {stats[2]}"
            f"\n 🧪 Мана: {stats[3]}"
            f"\n 🛡 Защита {stats[4]}"
            f"\n──❀*̥˚──◌──◌──❀*̥˚────"
            f"\n❖ 🔖 {page_num + 1} из {len(invent)}",
            reply_markup=pagination_group(page_num)
        )
    await callback.answer()


@router.callback_query(F.data.regexp("(g_change_character)\/([0-9]*)$").as_("data"))
async def change_ch(callback: CallbackQuery, state: FSMContext, data: Match[str]):

    g, user_id = data.groups()
    if callback.from_user.id != int(user_id):
        await callback.answer("❖ ✖️ Это не ваш инвентарь", show_alert=True)
        return
    else:
        data = await state.get_data()
        await mongodb.update_user(user_id, {'character': data.get('character')})
        await callback.answer("🎴 ВЫ успешно изменили персонажа", show_alert=True)
"""
