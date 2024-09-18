from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaAnimation
from data import mongodb
from filters.chat_type import ChatTypeFilter
from keyboards.builders import inline_builder, profile, rm, get_common
from routers import main_menu
from routers.gacha import first_summon
from utils.states import Form

router = Router()


@router.message(ChatTypeFilter(chat_type=["private"]), Command("start"))
async def fill_profile(message: Message,  state: FSMContext):
    user_id = message.from_user.id

    # Разделите текст сообщения на части
    parts = message.text.split()
    # Если есть аргументы команды, они будут во второй части
    referral_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None

    account = await mongodb.get_user(user_id)
    if account is not None and account['_id'] == user_id:
        await main_menu.main_menu(message)
    else:
        await state.set_state(Form.name)
        await message.answer("❖ 💮 Добро пожаловать!"
                             f"\n── •✧✧• ────────────"
                             f"\n❖ 📜 Для начала нужно пройти регистрацию"
                             "\n\n❖ 1. 🪪 Придумать никнейм"
                             "\n❖ 2. 🗺 Выбрать вселенную"
                             "\n❖ 3. 🎴 Получить первую карту"
                             f"\n── •✧✧• ────────────")
        await message.answer("❖ 🪪  Введи никнейм: ", reply_markup=profile(message.from_user.first_name))
        if referral_id and referral_id != user_id:
            await state.update_data(referral=referral_id)
        # Если пользователь уже существует и у него есть referral_id, проверьте, существует ли реферал


@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    if len(message.text) < 10:

        await state.update_data(name=f"<a href='https://t.me/{message.from_user.username}'><b>{message.text}</b></a>")
        await state.set_state(Form.universe)
        media_id = "AgACAgIAAx0CfstymgACCxNl4ie8goZjHQ1rAV5rxcz2a9XLnQACBs8xG7-XGUsGHmby9061bgEAAwIAA3kAAzQE"
        await message.answer(f"\n\n ❖ ⚙️ Чтобы бот работал корректно и динамично, включи автозагрузку фото "
                             f"и видео в настройках телеграм и автовоспроизведение видео в настройках чата телеграм",
                             reply_markup=rm())
        pattern = dict(
            caption="❖ 🗺 Выбирай вселенную"
                    "\n── •✧✧• ────────────"
                    "\n❖ 🌐 Вселенные постепенно будут добавляться и дополняться"
                    "\n\n❖ 🔄 Всегда можно сменить вселенную в ⚙️ ️настройки",
            reply_markup=inline_builder(['🗺 Bleach'], ['Bleach'])
        )
        await message.answer_photo(media_id, **pattern)
    else:
        await message.answer("✖️ Ник слишком длинный. Введи вручную: ")


@router.callback_query(F.data.in_(['Bleach']))
async def get_first_free(callback: CallbackQuery, state: FSMContext):
    await state.update_data(universe=callback.data)
    media = InputMediaAnimation(media="CgACAgIAAx0CfstymgACCxZl5FxQpuMBOz7tFM8BU88VOEvMXgACtjwAAkLSIEtSvf16OnsuwTQE")
    await callback.message.edit_media(media=media)
    await callback.message.edit_caption(caption="❖ 🗺 Bleach"
                                        "\n── •✧✧• ────────────"
                                        "\n💮 События происходят на территории Японии, где проживает Ичиго Куросаки. "
                                        "Парень с ранних лет отличается от сверстников, ведь он умеет общаться с призраками. "
                                        "Однажды к нему в комнату залетает барышня, которую зовут Рукия Кучики. . .", reply_markup=get_common())


@router.callback_query(F.data == "get_first_free")
async def get_first_free(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    universe = data.get('universe')
    character, character_category, power = await first_summon(callback, universe)
    await mongodb.input_user(user_id, data.get('name'), universe, character, power)
    await mongodb.push(universe, character_category, character, user_id)
    referral_id = data.get('referral')
    # Если пользователь уже существует и у него есть referral_id, проверьте, существует ли реферал
    referral = await mongodb.get_user(referral_id)
    if referral:
        # Если реферал существует и новый пользователь еще не в списке приглашенных
        if user_id not in referral['account']['referrals']:
            # Добавьте нового пользователя в список приглашенных
            await mongodb.push_referral(referral_id, user_id)
            # Получите обновленные данные реферала
            updated_referral = await mongodb.get_user(referral_id)
            # Проверьте, достигло ли количество приглашенных 3
            if len(updated_referral['account']['referrals']) % 3 == 0:
                # Если достигло, увеличьте количество ключей на 1
                await mongodb.update_value(referral_id, {'inventory.items.tickets.keys': 1})
    await state.clear()
