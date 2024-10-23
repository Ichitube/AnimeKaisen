from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaAnimation
from data import mongodb
from keyboards.builders import inline_builder
from routers import gacha

router = Router()


@router.callback_query(F.data == "banner")
async def banner(callback: CallbackQuery):
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    pattern = dict(
        caption=f"❖  🎐  <b>Баннеры</b>"
                f"\n── •✧✧• ────────────"
                f"\n❇️ <b><i>Текущие баннеры:</i></b>"
                f"\n\n ☆ • 👻 <b>Хэллоуин</b>"
                f"\n ☆ • 🔮 <b>Стандартный баннер</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["👻 Хэллоуин", "🔮 Ст. баннер", " 🔙 Назад"],
            ["halloween_banner", "standard", "tokio"],
            row_width=[1, 1, 1]
            )
    )

    if account['universe'] == "Bleach":
        media_id = "CgACAgIAAx0CfstymgACCxZl5FxQpuMBOz7tFM8BU88VOEvMXgACtjwAAkLSIEtSvf16OnsuwTQE"
    elif account['universe'] == "Naruto":
        media_id = "CgACAgIAAxkBAAKu-2bfz0QjhL_TZCnL-Zha1vsprdVLAAKCUQACzJcBS3N7PqOXSE2qNgQ"
    else:
        media_id = "CgACAgIAAx0CfstymgACEnpmnUiYllQQPMNY7B3y44Okelr6UgACsVEAApQD6UhAS-MzjVWVxTUE"
    media = InputMediaAnimation(media=media_id)
    await callback.message.edit_media(media, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)


@router.callback_query(F.data == "halloween_banner")
async def halloween(callback: CallbackQuery):
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    if account['universe'] != "Allstars":
        await callback.answer("❖ Этот баннер доступен только во вселенной Allstars", show_alert=True)
        return
    if "halloween" not in account['inventory']['items']:
        await mongodb.update_user(user_id, {"inventory.items.halloween": 0})
    account = await mongodb.get_user(user_id)
    items = account['inventory']['items']['halloween']

    pattern = dict(
        caption=f"❖  👻  <b>Хэллоуин</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖ <b><i>🧛 Ивент Хэллоуин:</i></b>"
                f"\n • 🧟 Соберите специальные 🎃 предметы события и учвствуйте в ивентовом банере"
                f"\n • ⚰️ В баннере присутствуют только специальные карты события 🕸Хэллоуин"
                f"\n── •✧✧• ────────────"
                f"\n❃  🎃 ⋗ <b>{items}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["Использовать 🎃100", " 🔙 Назад"],
            ["halloween_item", "banner"],
            row_width=[1]
            )
    )

    media_id = "CgACAgIAAx0CfstymgACJCdnF97OgftOVAIKHpJeXHyLC_xF2gAC2VsAAo5AwUgkkLpf0fTTtTYE"
    media = InputMediaAnimation(media=media_id)
    await callback.message.edit_media(media, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)


@router.callback_query(F.data == "soccer")
async def soccer_item(callback: CallbackQuery):
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    if account['universe'] != "Allstars":
        await callback.answer("❖ Этот баннер доступен только во вселенной Allstars", show_alert=True)
        return
    if "soccer" not in account['inventory']['items']:
        await mongodb.update_user(user_id, {"inventory.items.soccer": 0})
    account = await mongodb.get_user(user_id)
    items = account['inventory']['items']['soccer']

    pattern = dict(
        caption=f"❖  ⚽️  <b>Soccer</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖ <b><i>⚽️ Футбольный ивент:</i></b>"
                f"\n── •✧✧• ────────────"
                f"\n • ⚽️ Соберите специальные ⚽️ предметы события и учвствуйте в ивентовом банере"
                f"\n • ⚽️ В баннере присутствуют только специальные карты события ⚽️ Soccer"
                f"\n── •✧✧• ────────────"
                f"\n❃  ⚽️ ⋗ <b>{items}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["Использовать ⚽️100", " 🔙 Назад"],
            ["soccer_item", "banner"],
            row_width=[1]
            )
    )

    media_id = "CgACAgIAAx0CfstymgACI35nF2VmP_Vl5dPIu44-L8KsHVHNFQACQVwAAo5AuUhHh35J13Kc5jYE"
    media = InputMediaAnimation(media=media_id)
    await callback.message.edit_media(media, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)


@router.callback_query(F.data == "standard")
async def standard(callback: CallbackQuery):
    inline_id = callback.inline_message_id
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    ticket_data = account['inventory']['items']['tickets']
    keys = ticket_data['keys']
    golden = ticket_data['golden']
    common = ticket_data['common']

    pattern = dict(
        caption=f"❖ 🔮 <b>Стандартный баннер</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖ <b><i>Категории 🃏 карт:</i></b>"
                f"\n── •✧✧• ────────────"
                f"\n☆  🌠 <b>Божественные карты 🂡</b>"
                f"\n☆  🌌 <b>Мифические карты 🂡</b>"
                f"\n☆  🌅 <b>Легендарные карты 🂡</b>"
                f"\n☆  🎆 <b>Эпические карты 🂡</b>"
                f"\n☆  🎇 <b>Редкие карты 🂡</b>"
                f"\n☆  🌁 <b>Обычные карты 🂡</b>"
                f"\n── •✧✧• ────────────"
                f"\n❃  🧧 ⋗ <b>{keys}</b>   🎫 ⋗ <b>{golden}</b>   🎟 ⋗ <b>{common}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🧧 Открыть", "🎫 Призвать", "🎟 Призвать", " 🔙 Назад", "📋 Правила"],
            ["golden_key", "golden", "common_summon", "banner", "banner_rules"],
            row_width=[1, 2, 2]
            )
    )

    media_id = "CgACAgIAAx0CfstymgACBallzDJIAALy9W358H_8M540_3wQqAAC2T4AAsywYUqtJ3fOrELTrjQE"
    media = InputMediaAnimation(media=media_id)
    await callback.message.edit_media(media, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)


@router.callback_query(F.data == "soccer_item")
async def soccer_item(callback: CallbackQuery):
    await gacha.card_gacha(callback.from_user.id, callback)


@router.callback_query(F.data == "halloween_item")
async def halloween_item(callback: CallbackQuery):
    await gacha.card_gacha(callback.from_user.id, callback)


@router.callback_query(F.data == "golden_key")
async def golden_key(callback: CallbackQuery):
    await gacha.card_gacha(callback.from_user.id, callback)


@router.callback_query(F.data == "golden")
async def golden(callback: CallbackQuery):
    await gacha.card_gacha(callback.from_user.id, callback,)


@router.callback_query(F.data == "common_summon")
async def common(callback: CallbackQuery):
    await gacha.card_gacha(callback.from_user.id, callback)


@router.callback_query(F.data == "banner_rules")
async def banner_rules(callback: CallbackQuery):
    await callback.message.answer(
        f"❖ 📋 Правила Баннера"
        "\n── •✧✧• ────────────"
        "\nhttps://teletype.in/@dire_hazard/x1#S1Pc",
        reply_markup=inline_builder(["☑️"], ["delete"], row_width=[1])
    )
    await callback.answer()


@router.callback_query(F.data == "chance")
async def chance(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=f"❖  🔮 <b>Шансы Призыва</b>"
                f"\n── •✧✧• ────────────"
                f"\n 🧧 <b><i>Шансы священного призыва:</i></b>"
                f"\n\n   🌠 Божественные карты ⋗ <i>25%</i>"
                f"\n\n   🌌 Мифические карты ⋗ <i>35%</i>"
                f"\n\n   🌅 Легендарные карты ⋗ <i>40%</i>"
                f"\n── •✧✧• ────────────"
                f"\n 🎫 <b><i>Шансы золотого призыва:</i></b>"
                f"\n\n 🌠 Божественные карты ⋗ <i>1%</i>"
                f"\n\n   🌌 Мифические карты ⋗ <i>6%</i>"
                f"\n\n   🌅 Легендарные карты ⋗ <i>21%</i>"
                f"\n\n   🎆 Эпические карты ⋗ <i>46%</i>"
                f"\n\n   🎇 Редкие карты ⋗ <i>26%</i>"
                f"\n── •✧✧• ────────────"
                f"\n 🎟 <b><i>Шансы обычного призыва:</i></b>"
                f"\n\n 🌠 Божественные карты ⋗ <i>0.03%</i>"
                f"\n\n   🌌 Мифические карты ⋗ <i>0.3%</i>"
                f"\n\n   🌅 Легендарные карты ⋗ <i>2.3%</i>"
                f"\n\n   🎆 Эпические карты ⋗ <i>12.3%</i>"
                f"\n\n   🎇 Редкие карты ⋗ <i>30.3%</i>"
                f"\n\n   🌁 Обычные карты ⋗ <i>50.87%</i> "
                f"\n── •✧✧• ────────────",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🔙 Назад"],
            ["banner_rules"],
            row_width=[2, 2]
        )
    )
    await callback.answer()
