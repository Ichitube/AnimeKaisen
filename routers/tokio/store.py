from contextlib import suppress

from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaAnimation
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

from keyboards.builders import inline_builder
from ..slaves import slave_info
from data import mongodb, character_photo
from keyboards import builders

router = Router()


@router.callback_query(F.data == "store")
async def store(callback: CallbackQuery):
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    ticket_data = account['inventory']['items']['tickets']
    keys = ticket_data['keys']
    golden = ticket_data['golden']
    common = ticket_data['common']

    money = account['account']['money']
    pattern = dict(
        caption=f"❖  🏪  <b>Рынок</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖  Вы можете купить 🎫 золотые и 🎟 обычные билеты за 💴 ¥"
                f"\n\n❃  🎫 = 1000 💴"
                f"\n❃  🎟 = 100 💴"
                f"\n\n❖  Так же можете приобрести \n🧧 священный билет за 1 💲"
                f"\n── •✧✧• ────────────"
                f"\n❃  💴 {money} ¥  🧧 ⋗ <b>{keys}</b>  🎫 ⋗ <b>{golden}</b>  🎟 ⋗ <b>{common}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🧧 Купить ", "🎫 Купить", "🎟 Купить", "⛓ Рынок рабынь", "🏠 Рынок недвижимости", "🔙 Назад"],
            ["buy_keys", "buy_golden", "buy_common", "slaves_store", "buy_home", "tokio"],
            row_width=[1, 2, 1, 1, 1]
            )
    )

    media_id = "CgACAgIAAxkBAAIVAmXMvH4t4RtOQzePYbQgdnNEbFEeAAKOOwACeyZoSiAP4_7nfuBVNAQ"
    media = InputMediaAnimation(media=media_id)
    await callback.message.edit_media(media, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)


@router.callback_query(F.data == "buy_common")
async def buy_common(callback: CallbackQuery):
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    money = account['account']['money']
    pattern = dict(
        caption=f"❖  🏪  <b>Купить обычные билеты</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖  Вы можете купить 🎟 обычные билеты за 💴 ¥"
                f"\n\n❃  🎟 = 100 💴"
                f"\n\n❖  У вас есть {money} 💴 ¥"
                f"\n❖  Сколько билетов вы хотите купить?",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["1 🎟", "5 🎟", "🔙 Назад"],
            ["buy_common_1", "buy_common_5", "store"],
            row_width=[2, 1]
            )
    )

    await callback.message.edit_caption(inline_id, **pattern)


@router.callback_query(F.data == "buy_common_1")
async def buy_common_1(callback: CallbackQuery):
    await buy_common_ticket(callback, 1)


@router.callback_query(F.data == "buy_common_5")
async def buy_common_5(callback: CallbackQuery):
    await buy_common_ticket(callback, 5)


async def buy_common_ticket(callback: CallbackQuery, count: int):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    money = account['account']['money']
    if money >= 100 * count:
        await mongodb.update_user(user_id, {'account.money': money - 100 * count})
        await mongodb.update_user(
            user_id, {'inventory.items.tickets.common': account['inventory']['items']['tickets']['common'] + count}
        )
        await callback.answer(f"❖  🏪  Вы успешно приобрели {count} 🎟 обычных билетов", show_alert=True)
    else:
        await callback.answer(f"❖  🏪  У вас недостаточно 💴 ¥", show_alert=True)
    await store(callback)


@router.callback_query(F.data == "buy_golden")
async def buy_golden(callback: CallbackQuery):
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    money = account['account']['money']
    pattern = dict(
        caption=f"❖  🏪  <b>Купить золотые билеты</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖  Вы можете купить 🎫 золотые билеты за 💴 ¥"
                f"\n\n❃  🎫 = 1000 💴"
                f"\n\n❖  У вас есть {money} 💴 ¥"
                f"\n❖  Сколько билетов вы хотите купить?",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["1 🎫", "5 🎫", "🔙 Назад"],
            ["buy_golden_1", "buy_golden_5", "store"],
            row_width=[2, 1]
            )
    )

    await callback.message.edit_caption(inline_id, **pattern)


@router.callback_query(F.data == "buy_golden_1")
async def buy_golden_1(callback: CallbackQuery):
    await buy_golden_ticket(callback, 1)


@router.callback_query(F.data == "buy_golden_5")
async def buy_golden_5(callback: CallbackQuery):
    await buy_golden_ticket(callback, 5)


async def buy_golden_ticket(callback: CallbackQuery, count: int):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    money = account['account']['money']
    if money >= 1000 * count:
        await mongodb.update_user(user_id, {'account.money': money - 1000 * count})
        await mongodb.update_user(
            user_id, {'inventory.items.tickets.golden': account['inventory']['items']['tickets']['golden'] + count}
        )
        await callback.answer(f"❖  💮  Вы успешно приобрели {count} 🎫 золотых билетов", show_alert=True)
    else:
        await callback.answer(f"❖  💮  У вас недостаточно 💴 ¥", show_alert=True)
    await store(callback)


homes = character_photo.h_stats


@router.callback_query(F.data == "buy_home")
async def inventory(callback: CallbackQuery, state: FSMContext):
    inline_id = callback.inline_message_id
    result = character_photo.home_stats(list(homes.keys())[0])
    photo = InputMediaAnimation(media=result[0])
    await state.update_data(home=list(homes.keys())[0])
    await callback.message.edit_media(photo, inline_id)
    await callback.message.edit_caption(inline_id, f"❖ ⚜️ Сила: {result[1]}"
                                                   f"\n ── •✧✧• ────────────"
                                                   f"\n❖  Вы можете 🔑 купить этот дом за {result[1]} 💴 ¥",
                                        reply_markup=builders.pagination_store())


@router.callback_query(builders.Pagination.filter(F.action.in_(["prevv", "nextt"])))
async def inventory(callback: CallbackQuery, callback_data: builders.Pagination, state: FSMContext):
    inline_id = callback.inline_message_id
    page_num = int(callback_data.page)

    if callback_data.action == "nextt":
        page_num = (page_num + 1) % len(homes)
    elif callback_data.action == "prevv":
        page_num = (page_num - 1) % len(homes)

    with suppress(TelegramBadRequest):
        result = character_photo.home_stats(list(homes.keys())[page_num])
        photo = InputMediaAnimation(media=result[0])
        await state.update_data(home=list(homes.keys())[page_num])
        await callback.message.edit_media(photo, inline_id)
        await callback.message.edit_caption(
            inline_id,
            f"❖ ⚜️ Сила: {result[1]}"
            f"\n ── •✧✧• ────────────"
            f"\n❖  Вы можете 🔑 купить этот дом за {result[1]} 💴 ¥",
            reply_markup=builders.pagination_store(page_num)
        )
    await callback.answer()


@router.callback_query(F.data == "buy_store_home")
async def buy_home(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    data = await state.get_data()
    result = character_photo.home_stats(data['home'])
    money = account['account']['money']
    if data.get('home') in account['inventory']['home']:
        await callback.answer(f"❖  🏪  У вас уже есть этот дом", show_alert=True)
        return
    else:
        if money >= result[1]:
            await mongodb.update_user(user_id, {'account.money': money - result[1]})
            await mongodb.update_value(user_id, {'campaign.power': result[1]})
            await mongodb.push_home(user_id, data.get('home'))
            await callback.answer(f"❖  🏪  Вы успешно приобрели дом 🔑", show_alert=True)
        else:
            await callback.answer(f"❖  🏪  У вас недостаточно 💴 ¥", show_alert=True)
    await store(callback)


slaves = character_photo.s_stats


@router.callback_query(F.data == "slaves_store")
async def store_slaves(callback: CallbackQuery, state: FSMContext):
    inline_id = callback.inline_message_id
    result = character_photo.slaves_stats(list(slaves.keys())[0])
    photo = InputMediaAnimation(media=result[0])
    info = slave_info(result[3], result[2])
    await state.update_data(slave=list(slaves.keys())[0])
    await callback.message.edit_media(photo, inline_id)
    await callback.message.edit_caption(inline_id, f"❖ 🔖 {result[1]}"
                                                   f"\n──❀*̥˚──◌──◌──❀*̥˚────"
                                                   f"\n{info}"
                                                   f"\n──❀*̥˚──◌──◌──❀*̥˚────"
                                                   f"\n❖  Вы можете 🔖 купить эту рабыню за {result[4]} 💴 ¥",
                                        reply_markup=builders.slaves_store())


@router.callback_query(builders.Pagination.filter(F.action.in_(["prev_s", "next_s"])))
async def inventory(callback: CallbackQuery, callback_data: builders.Pagination, state: FSMContext):
    inline_id = callback.inline_message_id
    page_num = int(callback_data.page)

    if callback_data.action == "next_s":
        page_num = (page_num + 1) % len(slaves)
    elif callback_data.action == "prev_S":
        page_num = (page_num - 1) % len(slaves)

    with suppress(TelegramBadRequest):
        result = character_photo.slaves_stats(list(slaves.keys())[page_num])
        photo = InputMediaAnimation(media=result[0])
        info = slave_info(result[3], result[2])
        await state.update_data(slave=list(slaves.keys())[page_num])
        await callback.message.edit_media(photo, inline_id)
        await callback.message.edit_caption(
            inline_id,
            f"❖ 🔖 {result[1]}"
            f"\n──❀*̥˚──◌──◌──❀*̥˚────"
            f"\n{info}"
            f"\n──❀*̥˚──◌──◌──❀*̥˚────"
            f"\n❖  Вы можете 🔖 купить эту рабыню за {result[4]} 💴 ¥",
            reply_markup=builders.slaves_store(page_num)
        )
    await callback.answer()


@router.callback_query(F.data == "buy_slave")
async def buy_home(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    data = await state.get_data()
    result = character_photo.slaves_stats(data['slave'])
    money = account['account']['money']
    if data.get('slave') in account['inventory']['slaves']:
        await callback.answer(f"❖  ✖️  У вас уже есть эта рабыня", show_alert=True)
        return
    else:
        if money >= result[4]:
            await mongodb.update_user(user_id, {'account.money': money - result[4]})
            await mongodb.push_slave(user_id, data.get('slave'))
            await callback.answer(f"❖  🔖  Вы успешно приобрели рабыню", show_alert=True)
        else:
            await callback.answer(f"❖  ✖️  У вас недостаточно 💴 ¥", show_alert=True)
    await store(callback)
