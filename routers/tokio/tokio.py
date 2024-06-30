import random

from aiogram import Router, F

from aiogram.types import CallbackQuery, InputMediaAnimation, Message
from aiogram.enums import ParseMode

from keyboards.builders import inline_builder
from data import mongodb
from filters.chat_type import ChatTypeFilter

router = Router()

menu = ["CgACAgIAAxkBAAIVCWXMvbya7qFOU8F85SXUu24hM5wgAAKfOwACeyZoShH4z6iUPi8kNAQ",
        "CgACAgIAAxkBAAIVCGXMva_F1yC11Mw3o1gv27ZgOmICAAKdOwACeyZoSqKFTee3GFhiNAQ",
        "CgACAgIAAxkBAAIVBmXMvQTWWfC3KX66Wy4evn7cWtHuAAKUOwACeyZoSsragGfIS2gINAQ",
        "CgACAgIAAxkBAAIVAWXMvHhsXaPhuLALMBuumsH-TO4dAAKNOwACeyZoSjQXaqlcQ_ZPNAQ",
        "CgACAgIAAxkBAAIU_mXMvCAB6-_wn8o6hpUwwaR-EF6IAAJ4RQACzLBpSgF57_JwVq60NAQ",
        "CgACAgIAAxkBAAIVAAFlzLxX7B3NqbKxkBbz_SAosLc8eQACjDsAAnsmaEo-TETgyUqmcjQE",
        "CgACAgIAAxkBAAIU_2XMvDvTFeOYOdwd5QRQsPUdhGPlAAKKOwACeyZoSpr5AQNXbnVENAQ",
        "CgACAgIAAxkBAAIU_WXMvB2fCF7pcS9cZDdEMNeeWIe2AAKFOwACeyZoSqkPzi4qGFdvNAQ",
        "CgACAgIAAxkBAAIU-GXMuu17Zb88QyTyVxOEwPFjeCRJAAJoOwACeyZoSp9AqDTjvy4lNAQ",
        "CgACAgIAAxkBAAIU-WXMuv67-KrxO8NKeQgUw4LsrDSSAAJqOwACeyZoSvtrR6TF1C2BNAQ",
        "CgACAgIAAxkBAAIVA2XMyQ7c7bzjIhd4ecf9W6TGWm6eAAKPOwACeyZoSsm5IEXYiJoKNAQ",
        "CgACAgIAAx0CfstymgACBd5lzO0zU05NJEIDdrzbQNLwSMi_XgACbUkAAsywaUqtbVk4cEzxrzQE",
        "CgACAgIAAx0CfstymgACBd1lzO0zAm8ov_iX9BAY7_QVIkf3NQACbEkAAsywaUoWn4BRgx1huTQE",
        "CgACAgIAAx0CfstymgACBdxlzO0yxbOLTRm_B0ttpbA7WYEFdgACa0kAAsywaUoVOJ0ILUcy3jQE"]


@router.message(
    ChatTypeFilter(chat_type=["private"]),
    F.text == "💮 Меню"
)
@router.callback_query(F.data == "tokio")
async def tokio(callback: CallbackQuery | Message):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)

    money = account['account']['money']

    pattern = dict(
        caption=f"❖  💮  <b>Меню</b>"
                f"\n── •✧✧• ────────────"
                f"\n ❖ 🌊 Добро пожаловать в нашу уникальную вселенную, где каждый игрок вносит свой вклад в создание "
                f"неповторимого мира"
                f"\n\n ❖ 💫 Приглашая друзей или купив священных билетов вы поддерживаете проект "
                f"для дальнейшего развития"
                f"\n\n ❖ 🏵 Спасибо за вашу поддержку!"
                f"\n── •✧✧• ────────────"
                f"\n❃ 💴 {money} ¥",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🔮 Призыв", "🪪 Профиль", "🏪 Рынок", "🃏 Битва", "🏯 Клан", "🏠 Дом", "📜 Задании"],
            ["banner", "main_page", "store", "card_battle", "clan", "home", "quests"],
            row_width=[1, 2, 2]
            )
    )

    media_id = random.choice(menu)

    if isinstance(callback, CallbackQuery):
        inline_id = callback.inline_message_id
        media = InputMediaAnimation(media=media_id)

        await callback.message.edit_media(media, inline_id)
        await callback.message.edit_caption(inline_id, **pattern)
    else:
        await callback.answer_animation(media_id, **pattern)


homes_photo = {'🏠 home_1': 'CgACAgIAAxkBAAIU-2XMuzNmOsXp4JxBcGGDbpD_XENiAAJwOwACeyZoSsgIg-cm-c8iNAQ',
               '🏠 home_2': 'CgACAgIAAxkBAAIU_GXMuza-voX5wQABXHuYInkx0vGpQwACcTsAAnsmaEr83Z9UehDa5jQE',
               '🏠 home_3': 'CgACAgIAAxkBAAIU-mXMuxgz2RBDeRa8TE0AAaSXD_mKSAACbDsAAnsmaEqm72YZnRGekjQE',
               '🏠 home_4': 'CgACAgIAAx0CfstymgACBSZlxMJQZb7FFLh9iPFdSpXOklwDqQACaD4AAgrXEEpTmie8hGfs1zQE',
               '🏠 home_5': 'CgACAgIAAx0CfstymgACBdtlzO0rWNF9QoR6R4_5ZaHZDVb37wACakkAAsywaUpFT0CPnQYM5TQE'
               }


@router.callback_query(F.data == "clan")
async def clan(callback: CallbackQuery):
    await callback.answer(f"❖  🏯 Кланы в разработке", show_alert=True)


@router.callback_query(F.data == "card_battle")
async def card_battle(callback: CallbackQuery):
    await callback.answer(f"❖  🃏 Карточная битва в разработке", show_alert=True)


@router.callback_query(F.data == "quests")
async def requisites(callback: CallbackQuery):
    await callback.answer(f"❖  📜 Задании в разработке", show_alert=True)
