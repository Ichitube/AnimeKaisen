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

    ticket_data = account['inventory']['items']['tickets']
    keys = ticket_data['keys']
    golden = ticket_data['golden']
    common = ticket_data['common']

    pattern = dict(
        caption=f"❖  🔮  <b>Призыв</b>"
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
            ["golden_key", "golden", "common_summon", "tokio", "banner_rules"],
            row_width=[1, 2, 2]
            )
    )

    media_id = "CgACAgIAAx0CfstymgACBallzDJIAALy9W358H_8M540_3wQqAAC2T4AAsywYUqtJ3fOrELTrjQE"
    media = InputMediaAnimation(media=media_id)
    await callback.message.edit_media(media, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)


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
    await callback.message.edit_caption(
        caption=f"❖  📋  <b>Правила Баннера</b>"
                f"\n── •✧✧• ────────────"
                f"\n❖  🔮 <b>Баннер</b> - это специальные призывы, которые дают возможность получить "
                f"🎴 карты высокого уровня "
                f"\n\n❖  🔮 Каждый призыв имеет свои шансы на получение 🃏 карты 🂡"
                f"\n\n❖  🧧 <b>Священные призывы</b> дают возможность получить 🃏 карты 🂡 только высокого уровня"
                f"\n\n❖  🎫 <b>Золотой призыв</b> - Дает возможность получить 🃏 карты 🂡 высокого уровня наивысшим шансом"
                f"\n\n❖  🎟 <b>Обычный призыв</b> - Дает возможность получить 🃏 карты 🂡 высокого уровня"
                f"\n\n❖  За каждый призыв вы получаете 💴 деньги ¥, ⚜️ Мощи и 🧩 оскольков "
                f"\n\n❖  Если вы призвали персонажа которого уже у вас есть, "
                f"то зачисляеться только 2Х 🧩 оскольков и 💴 денег ¥"
                f"\n\n❖💴 Можно использовать в рынке, а за 🧩 оскольков можно 🪄 скрафтить карты любого уровня"
                f"\n── •✧✧• ────────────",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🔙 Назад", "🔮 Шансы"],
            ["banner", "chance"],
            row_width=[2, 2]
        )
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
