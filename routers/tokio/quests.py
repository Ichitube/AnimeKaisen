from datetime import datetime, timedelta

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.enums import ParseMode

from filters.chat_type import ChatTypeFilter, CallbackChatTypeFilter
from keyboards.builders import inline_builder
from data import mongodb

router = Router()


@router.message(ChatTypeFilter(chat_type=["private"]), F.text == "📜 Квесты")
@router.callback_query(F.data == "quests")
async def requisites(callback: CallbackQuery | Message):
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
        gold = "4"
        money = "2500"
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
            await mongodb.update_user(user_id, {'account.prime': False})
    else:
        emoji = ""
        gold = "2"
        money = "1400"
        msg = "\n💮Pass увеличивают награду"

    if "halloween" not in account['inventory']['items']:
        await mongodb.update_user(user_id, {"inventory.items.halloween": 0})

    now = datetime.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    delta = midnight - now
    hours, remainder = divmod(delta.seconds, 3600)
    minutes = remainder // 60
    time_until_reset = f"{hours} ч {minutes} мин"

    pattern = dict(
        caption=f"❖ 📃 Список ежедневных квестов:"
                f"\n── •✧✧• ────────────"
                f"\n<blockquote>{summon} • 🔮 Совершите призыв"
                f"\n{arena_fight} • ⚔️ Сразитесь в арене"
                f"\n{free_summon} • 🎴 Совершите граб"
                f"\n{dungeon} • ⛩ Продайте ресурсы"
                f"\n{shop_purchase} • 🏪 Совершите покупку</blockquote>"
                f"\n ❖ 🎁 Награды:"
                f"\n<blockquote> {emoji} {reward} • 🎫 {gold}х золотой билет"
                f"\n {emoji} {reward} • 💴 {money} ¥</blockquote>"
                f"{msg}"
                f"\n── •✧✧• ────────────"
                f"\n♻️ Обновятся через: ⏱️ {time_until_reset}",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🎁 Получить", "🔙 Меню"],
            ["get_quest_reward", "main_page"],
            row_width=[1, 1]
        )
    )

    media = 'AgACAgIAAx0CfstymgACHvFm7nfVl1UgyCpMV2em6oT-0fVueAAC0d8xG6zFeUuTGRHASLHNiwEAAwIAA3gAAzYE'

    media_id = InputMediaPhoto(media=media)

    if isinstance(callback, CallbackQuery):
        inline_id = callback.inline_message_id
        await callback.message.edit_media(media_id, inline_id)
        await callback.message.edit_caption(inline_id, **pattern)
    else:
        await callback.answer_photo(media, **pattern)


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
                # await mongodb.update_user(user_id, {
                #     "inventory.items.halloween": account["inventory"]["items"]["halloween"] + 100})
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
                    await mongodb.update_user(user_id, {'account.prime': False})
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
