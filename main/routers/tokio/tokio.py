import random
from datetime import datetime, timedelta

from aiogram import Router, F

from aiogram.types import CallbackQuery, InputMediaAnimation, InputMediaPhoto, Message
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
        "CgACAgIAAx0CfstymgACBdxlzO0yxbOLTRm_B0ttpbA7WYEFdgACa0kAAsywaUoVOJ0ILUcy3jQE",
        "CgACAgIAAx0CfstymgACIB5nE7mXOOMrHrWyLobEDbk85ehs7QAC6FgAAqiJoEg5NN5yufK0QzYE",
        "CgACAgIAAx0CfstymgACIBRnE7ipKamfva-CfgqsiZJ-EKMGxwACxFgAAqiJoEijvBsGD_fnpjYE",
        "CgACAgIAAx0CfstymgACIBJnE7ih9KNvH8o3P1Yy1rTY4o7YVQACwlgAAqiJoEiVpQSxmKi5sjYE",
        "CgACAgIAAx0CfstymgACIBBnE7ibsUe_hxrML0hwjTHC0jWZXQACwVgAAqiJoEhlPEBRZo_wlTYE",
        "CgACAgIAAx0CfstymgACIA5nE7iRTMe8cH8bBZgvI8ZbeAW0tAACv1gAAqiJoEi3kcjjLHSleDYE",
        "CgACAgIAAx0CfstymgACIAxnE7iJXL7xxL4a5vmYVhL3zTuYZwACvVgAAqiJoEgvOYe5dmhxFjYE",
        "CgACAgIAAx0CfstymgACIApnE7h9jBb9jkmJNh_KJ792kiapEAACu1gAAqiJoEjYTH71QJA-TjYE"]


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
            ["🎐 Баннеры", "🪪 Профиль", "🏪 Рынок", "🏠 Дом", "📜 Квесты", "🃏 Битва", "🏯 Клан"],
            ["banner", "main_page", "store", "home", "quests", "card_battle", "clan"],
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
    user_id = callback.from_user.id
    current_date = datetime.today().date()
    current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
    account = await mongodb.get_user(user_id)
    yesterday_date = datetime.combine(current_date, datetime.time(datetime.now())) - timedelta(days=1)
    if "tasks" not in account:
        await mongodb.update_user(user_id, {"tasks": {
            "last_summon": yesterday_date,
            "last_arena_fight": yesterday_date,
            "last_shop_purchase": yesterday_date,
            "last_free_summon": yesterday_date,
            "last_dungeon": yesterday_date,
            "last_tasks_view": current_datetime,
            "last_get_reward": yesterday_date
        }})
        account = await mongodb.get_user(user_id)
    # Получаем tasks или создаем пустой словарь, если его нет
    tasks = account.get("tasks", {})

    # Список полей, которые должны быть в tasks
    required_fields = {
        "last_summon": yesterday_date,
        "last_arena_fight": yesterday_date,
        "last_shop_purchase": yesterday_date,
        "last_free_summon": yesterday_date,
        "last_dungeon": yesterday_date,
        "last_tasks_view": current_datetime,
        "last_get_reward": yesterday_date
    }

    # Проверяем и добавляем недостающие поля
    for field, value in required_fields.items():
        if field not in tasks:
            tasks[field] = value
    # Обновляем данные пользователя
    await mongodb.update_user(user_id, {"tasks": tasks})
    account = await mongodb.get_user(user_id)
    last_view_date = account["tasks"]["last_tasks_view"]
    last_view_date = last_view_date.date()
    if last_view_date != current_date:
        await mongodb.update_user(user_id, {"tasks.last_summon": yesterday_date})
        await mongodb.update_user(user_id, {"tasks.last_arena_fight": yesterday_date})
        await mongodb.update_user(user_id, {"tasks.last_shop_purchase": yesterday_date})
        await mongodb.update_user(user_id, {"tasks.last_dungeon": yesterday_date})
        await mongodb.update_user(user_id, {"tasks.last_free_summon": yesterday_date})
        await mongodb.update_user(user_id, {"tasks.last_tasks_view": current_datetime})
    reward = "ℹ️"
    last_get_reward = account["tasks"]["last_get_reward"].date()
    if last_get_reward == current_date:
        reward = "✅"
    account = await mongodb.get_user(user_id)
    summon = "ℹ️"
    if account["tasks"]["last_summon"].date() == current_date:
        summon = "✅"
    arena_fight = "ℹ️"
    if account["tasks"]["last_arena_fight"].date() == current_date:
        arena_fight = "✅"
    dungeon = "ℹ️"
    if account["tasks"]["last_dungeon"].date() == current_date:
        dungeon = "✅"
    free_summon = "ℹ️"
    if account["tasks"]["last_free_summon"].date() == current_date:
        free_summon = "✅"
    shop_purchase = "ℹ️"
    if account["tasks"]["last_shop_purchase"].date() == current_date:
        shop_purchase = "✅"

    if account['account']['prime']:
        # Получаем текущую дату
        current_date = datetime.today().date()
        emoji = "💮"
        gold = "5"
        money = "2500"
        hall = "100"
        msg = ""
        current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))

        # Извлекаем дату истечения пасса из базы данных (предполагаем, что это объект даты)
        if 'pass_expiration' in account:
            pass_expires = account['pass_expiration']
        else:
            expiration_date = current_datetime + timedelta(days=30)
            await mongodb.update_user(user_id, {"pass_expiration": expiration_date})
            pass_expires = expiration_date

        # Проверяем, истек ли пасс
        if current_datetime > pass_expires:
            # Обновляем статус prime на False
            await mongodb.update_value(user_id, {'account.prime': False})
    else:
        emoji = ""
        gold = "3"
        money = "1400"
        hall = "65"
        msg = "\n\nКупите 💮Pass чтобы увеличить награду"

    if "halloween" not in account['inventory']['items']:
        await mongodb.update_user(user_id, {"inventory.items.halloween": 0})

    pattern = dict(
        caption=f"❖  📜  <b>Квесты</b>"
                f"\n── •✧✧• ────────────"
                f"\n ❖ 📃 Список ежедневных квестов:"
                f"\n\n  {summon} • 🔮 Совершите призыв"
                f"\n  {arena_fight} • ⚔️ Сразитесь в арене"
                f"\n  {free_summon} • 🎴 Совершите бесплатный призыв"
                f"\n  {dungeon} • ⛩ Продайте ресурсы в подземелье"
                f"\n  {shop_purchase} • 🏪 Совершите покупку на рынке"
                f"\n\n ❖ 🎁 Награда:"
                f"\n\n {emoji} {reward} • 🎫 {gold}х золотой билет"
                f"\n {emoji} {reward} • 💴 {money} ¥"
                f"\n {emoji} {reward} • 🎃 {hall} Тыквы"
                f"{msg}"
                f"\n── •✧✧• ────────────"
                f"\n❃ ♻️ Квесты обновляются каждый день в 00:00",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🎁 Получить", "🔙 Меню"],
            ["get_quest_reward", "tokio"],
            row_width=[1, 1]
        )
    )

    media_id = InputMediaPhoto(media='AgACAgIAAx0CfstymgACHvFm7nfVl1UgyCpMV2em6oT-0fVueAAC0d8xG6zFeUuTGRHASLHNiwEAAwIAA3gAAzYE')

    inline_id = callback.inline_message_id
    await callback.message.edit_media(media_id, inline_id)
    await callback.message.edit_caption(inline_id, **pattern)

    # await callback.answer(f"❖  📜 Задании в разработке", show_alert=True)


@router.callback_query(F.data == "get_quest_reward")
async def get_quest_reward(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_date = datetime.today().date()
    current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
    account = await mongodb.get_user(user_id)
    last_get_reward = account["tasks"]["last_get_reward"]
    last_get_reward = last_get_reward.date()
    if last_get_reward == current_date:
        await callback.answer(f"❖ ✅ Награда уже получена, 🎁 возвращайтесь завтра!", show_alert=True)
        return
    else:
        if "halloween" not in account['inventory']['items']:
            await mongodb.update_user(user_id, {"inventory.items.halloween": 0})
        if (account["tasks"]["last_summon"].date() == current_date and account["tasks"]["last_arena_fight"].date() == current_date
                and account["tasks"]["last_dungeon"].date() == current_date and account["tasks"]["last_free_summon"].date() == current_date
                and account["tasks"]["last_shop_purchase"].date() == current_date):
            if account['account']['prime']:
                await mongodb.update_user(user_id, {"account.money": account["account"]["money"] + 2500})
                await mongodb.update_user(user_id, {
                    "inventory.items.tickets.golden": account["inventory"]["items"]["tickets"]["golden"] + 5})
                await mongodb.update_user(user_id, {
                    "inventory.items.halloween": account["inventory"]["items"]["halloween"] + 100})
                await mongodb.update_user(user_id, {"tasks.last_get_reward": current_datetime})
                await callback.answer(f"❖ ✅ Награда получена", show_alert=True)
                return
                # Получаем текущую дату
                current_date = datetime.today().date()
                current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))

                # Извлекаем дату истечения пасса из базы данных (предполагаем, что это объект даты)
                if 'pass_expiration' in account:
                    pass_expires = account['pass_expiration']
                else:
                    expiration_date = current_datetime + timedelta(days=30)
                    await mongodb.update_user(user_id, {"pass_expiration": expiration_date})
                    pass_expires = expiration_date

                # Проверяем, истек ли пасс
                if current_datetime > pass_expires:
                    # Обновляем статус prime на False
                    await mongodb.update_value(user_id, {'account.prime': False})
            else:
                await mongodb.update_user(user_id, {"account.money": account["account"]["money"] + 1400})
                await mongodb.update_user(user_id, {"inventory.items.tickets.golden": account["inventory"]["items"]["tickets"]["golden"] + 3})
                await mongodb.update_user(user_id, {"inventory.items.halloween": account["inventory"]["items"]["halloween"] + 65})
                await mongodb.update_user(user_id, {"tasks.last_get_reward": current_datetime})
                await callback.answer(f"❖ ✅ Награда получена", show_alert=True)
                return
        else:
            await callback.answer(f"❖ ✖️ Не все задания выполнены", show_alert=True)
            return
