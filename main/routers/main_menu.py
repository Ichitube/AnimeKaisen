from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaAnimation, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from data import mongodb, character_photo
from filters.chat_type import ChatTypeFilter
from keyboards.builders import inline_builder, menu_button
from recycling import profile

router = Router()


@router.message(ChatTypeFilter(chat_type=["private"]), Command("menu"))
@router.message(
    ChatTypeFilter(chat_type=["private"]),
    F.text == "🪪 〢 Профиль"
)
@router.callback_query(F.data == "main_page")
async def main_menu(message: Message | CallbackQuery):
    user_id = message.from_user.id
    account = await mongodb.get_user(user_id)

    if account is not None and account['_id'] == user_id:

        universe = account['universe']
        character = account['character'][account['universe']]
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
            reply_markup=inline_builder(
                ["🏟️ Арена", "💮 Меню", "⛩️ Подземелье", "🪄 Крафт", "🥡 Инвентарь", "⚙️ Настройки", "🎁 Рефераль"],
                ["arena", "tokio", "dungeon", "craft", "inventory", "settings", "referral"],
                row_width=[1, 2, 2, 2])
        )
        if isinstance(message, CallbackQuery):
            if avatar_type == 'photo':
                media = InputMediaPhoto(media=avatar)
            else:
                media = InputMediaAnimation(media=avatar)
            inline_id = message.inline_message_id
            await message.message.edit_media(media, inline_id)
            await message.message.edit_caption(inline_id, **pattern)
        else:
            if avatar_type == 'photo':
                await message.answer_photo(avatar, **pattern)
            else:
                await message.answer_animation(avatar, **pattern)
    else:
        await message.answer("📄 Ты не регистрирован"
                             "\n── •✧✧• ────────────"
                             "\n ❖ Нужно зарегистрироваться "
                             "и получить первую 🎴 карту. "
                             "\n ❖ Для этого отправь команду /start")


@router.message(F.animation)
async def file_id(message: Message):
    if message.chat.id == -1002127262362:
        await message.reply(f"ID гифа, на который вы ответили: {message.animation.file_id}")


@router.message(F.photo)
async def file_id(message: Message):
    if message.chat.id == -1002127262362:
        await message.reply(f"ID фотографии, на которую вы ответили: {message.photo[-1].file_id}")


@router.message(Command("file_id"))
async def file_id(message: Message):
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await message.reply(f"ID фотографии, на которую вы ответили: {message.reply_to_message.photo[-1].file_id} IDgroup{message.chat.id}")
        elif message.reply_to_message.animation:
            await message.reply(f"ID гифа, на который вы ответили: {message.reply_to_message.animation.file_id}")
    else:
        await message.reply("Пожалуйста, ответьте на сообщение с фотографией или гифкой.")


@router.callback_query(F.data == "referral")
async def referral_link(callback: CallbackQuery):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    media = InputMediaAnimation(media="CgACAgIAAx0CfstymgACBb9lzLfhJnj3lcZBeK1j3YTPUX6wfgACYkYAAsywaUpw0JLo7c7pRzQE")
    count = len(account['account']['referrals'])
    deep_link = f'https://t.me/AnimeKaisenbot?start={user_id}'
    text = (f'\n── •✧✧• ────────────'
            f'\n ❃  🎐 Ты получил особое приглашение в сообщество Аниме битвы. '
            f'\n\n ❃  ⛩️ Там ты можешь насладиться плавной 🔮 Гачой, собирать своих 🎴 Персонажей, сражаться в '
            f'🏟️ Арене с другими игроками, стать самым ⚜️ сильным игроком и найти друзей'
            f'\n\n ❃  Заходи по моей ссылке ниже и получай 🎁 Бонусы при регистрации: \n\n'
            f' ⋗ {deep_link} '
            f'\n── •✧✧• ────────────'
            f'\nБудем рады тебя видеть :)')

    def share_keyboard():
        buttons = [
            [
                InlineKeyboardButton(text="🎁 Получить", switch_inline_query=f"{text}"),
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="main_page")
            ]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    await callback.message.edit_media(media)
    await callback.message.edit_caption(caption='\n── •✧✧• ────────────'
                                        f'\n ❃ 🎁 Вы получите 🧧 священный билет за каждых 3 приглашенных игроков. '
                                        f'\n\n ❃ ⛩️ Условия:'
                                        f'\n\n  ❖ Новые игроки считаються приглашенными только после того, как они '
                                        f'зарегистрировались по вашей реферальной ссылке и получили 🎴 первую карту'
                                        f'\n  ❖ Игроки которые уже зарегистрировались не считаються приглашенными'
                                        f'\n  ❖ Приглашая игроков вы поддерживаете развитие игры'
                                        f'\n\n ❃ 🎐 Ваша реферальная ссылка:'
                                        f'\n\n ⋗ {deep_link} '
                                        f'\n── •✧✧• ────────────'
                                        f'\n вы пригласили {count} человек', reply_markup=share_keyboard())


@router.message(ChatTypeFilter(chat_type=["private"]), Command("menu_button"))
async def call_button(message: Message):
    await message.answer(text='˗ˋˏ💮 Кнопки восстановленыˎˊ˗', reply_markup=menu_button())
