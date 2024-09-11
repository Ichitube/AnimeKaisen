from contextlib import suppress
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaAnimation, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from filters.chat_type import ChatTypeFilter
from keyboards import builders
from data import mongodb, character_photo

router = Router()


async def get_inventory(user_id, rarity):
    account = await mongodb.get_user(user_id)
    universe = account['universe']
    invent = account['inventory']['characters'][universe]
    return invent[rarity], universe


@router.message(
    ChatTypeFilter(chat_type=["private"]),
    F.text == "🥡 Инвентарь"
)
@router.callback_query(F.data == "inventory")
async def inventory(callback: CallbackQuery | Message):
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
    pattern = dict(caption=f"🥡 Инвентарь"
                           f"\n── •✧✧• ────────────"
                           f"\n❖ Здесь вы можете увидеть все ваши 🃏 карты "
                           f"и установить их в качестве 🎴 персонажа"
                           f"\n\n❖ Выберите ✨ редкость карты, чтобы посмотреть"
                           f"\n── •✧✧• ────────────"
                           f"\n❖ 🃏 Количество карт: {total_elements}",
                   reply_markup=builders.inline_builder(
                       [f"🌠 Божественные 🌟 {total_divine}", f"🌌 Мифические ⭐️ {total_mythical}",
                        f"🌅 Легендарные ⭐️ {total_legendary}", f"🎆 Эпические ⭐️ {total_epic}",
                        f"🎇 Редкие ⭐️ {total_rare}", f"🌁 Обычные ⭐️ {total_common}", "🔙 Назад"],
                       ["divine", "mythical", "legendary", "epic", "rare", "common", "main_page"], row_width=[1]))
    if isinstance(callback, CallbackQuery):
        inline_id = callback.inline_message_id
        media = InputMediaAnimation(media=media_id)
        await callback.message.edit_media(media, inline_id)
        await callback.message.edit_caption(inline_id, **pattern)
    else:
        await callback.answer_animation(media_id, **pattern)


@router.callback_query(F.data.in_(['common', 'rare', 'epic', 'legendary', 'mythical', 'divine']))
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
                                        reply_markup=builders.pagination_keyboard(universe, invent[0]))


@router.callback_query(builders.Pagination.filter(F.action.in_(["prev", "next"])))
async def inventory(callback: CallbackQuery, callback_data: builders.Pagination, state: FSMContext):
    inline_id = callback.inline_message_id
    page_num = int(callback_data.page)
    user_data = await state.get_data()
    invent, universe = await get_inventory(callback.from_user.id, user_data['rarity'])

    if callback_data.action == "next":
        page_num = (page_num + 1) % len(invent)
    elif callback_data.action == "prev":
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
            reply_markup=builders.pagination_keyboard(universe=universe, character=invent[page_num], page=page_num)
        )
    await callback.answer()


@router.callback_query(F.data == "change_character")
async def change_ch(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    await mongodb.change_char(user_id, data.get('universe'), data.get('character'))
    await callback.answer("🎴 Вы успешно изменили персонажа", show_alert=True)
