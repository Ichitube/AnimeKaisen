from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaAnimation
from aiogram.enums import ParseMode

from keyboards.builders import inline_builder
from recycling import profile
from data import mongodb

router = Router()


@router.callback_query(F.data == "stats")
async def stats(callback: CallbackQuery):

    user_id = callback.from_user.id

    account = await mongodb.get_user(user_id)

    rank = profile.rerank(account['stats']['rank'])

    await callback.message.edit_caption(
        caption=f"🧧 Ранг: <b>{rank}</b>"
                f"\n\n🔥 Победы: <b>{account['battle']['stats']['wins']}</b>"
                f"\n🩸 Ничьи: <b>{account['battle']['stats']['ties']}</b>",

        reply_markup=inline_builder(
            ["⛩️ Назад"],
            ["main_page"],
            row_width=[2, 2]
        )
    )
    await callback.answer()


@router.callback_query(F.data == "battle_system")
async def ranks(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="❖ 🎐 Ранги"
                f"\n── •✧✧• ────────────"
                "<b>\n • Аматэрасу 天照 🎖️🎖️🎖️🎖️ \n ─ 600 и более 👑 Побед</b>"
                "<b>\n\n • Сёгун 将軍 🎖️🎖️🎖️ \n ─ 300 и более 👑 Побед</b>"
                "<b>\n\n • Самурай 侍 🎖️🎖️ \n ─ 150 и более 👑 Побед</b>"
                "<b>\n\n • Ронин 浪人 🎖️ \n ─ менее 100 👑 Побед</b>",
        reply_markup=inline_builder(
            ["🔙 Назад"],
            ["battle_rating"],
            row_width=[1]
        )
    )
    await callback.answer()


@router.callback_query(F.data == "battle_rating")
async def campaign_rank(callback: CallbackQuery):
    account = await mongodb.get_user(callback.from_user.id)
    rating = await mongodb.wins_rating("battle.stats.wins", account, '👑')

    media = InputMediaAnimation(media="CgACAgIAAxkBAAIVQ2XOBCFYSQfjZfxblsVAZJ3PNGQWAAKIRwAC8utxSsak7XpiV9MnNAQ")
    await callback.message.edit_media(media=media)

    await callback.message.edit_caption(
        caption=f"❖  🏆  <b>Рейтинг самых сильных игроков</b>"
                f"\n── •✧✧• ────────────"
                f"{rating}"
                f"\n── •✧✧• ────────────"
                f"\n👑 Победы: {account['battle']['stats']['wins']}   ☠️ Ничьи: {account['battle']['stats']['ties']}",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🔙 Назад", "🎐 Ранги"],
            ["arena", "battle_system"],
            row_width=[2])
    )
    await callback.answer()


@router.callback_query(F.data == "battle_rules")
async def arena_rules(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="<b>❖ 🏟️ Правила битвы</b>"
                "\n── •✧✧• ────────────"
                "\n\n<b>❖ 💮 Цель игры:</b> Победить противника атакуя его или используя доступные навыки"
                "\n\n⚔️ <b>Битвы:</b> \n\n • 🔎 Игра начинается с поиска соперника"
                "\n\n • 🗡 В течении битвы игроки поочередно атакует друг друга или используют доступных навыков"
                "\n\n • ⏳ Ход начинает игрок который первый начал поиск соперника"
                "\n\n • 🕘 Игроки должны ходить в течении 60 секунд иначе они проиграют"
                "\n\n • 💀 Если у игрока останется меньше 1 ❤️ здоровье, он проиграет за исключением"
                "способностей воскрешение"
                "\n\n • 👑 За победу начисляется \n   + 100🀄️ опыта \n   + 200💴 денег"
                "\n\n • 💀 За поражение начисляется \n   + 55🀄️ опыта \n   + 100💴 денег"
                "\n\n • ☠️ За ничью начисляется по \n   + 80🀄️ опыта \n   + 150💴 денег"
                "\n\n • 🏴‍☠️ Если игрок сдается, то он проигрывает и не получает награду",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["⚔️ О статов игры", "🔙 Назад"],
            ["ability_rules", "arena"],
            row_width=[1, 1]
        )
    )
    await callback.answer()


@router.callback_query(F.data == "ability_rules")
async def arena_rules(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="<b>❖ ⚔️ О статов игры</b>"
                "\n── •✧✧• ────────────"
                "\n<b>Каждый персонаж имеет своих уникальных способностей и статов</b>"
                "\n\n • ✊🏻 <b>Сила:</b> в основном влияет на количество ❤️ здоровье, 🗡 урон, 🛡 защиты и 🩸 крит. урона"
                "\n\n • 👣 <b>Ловкость:</b> в основном влияет на 🗡 урон, 🛡 защиты и 🩸 крит. шанса"
                "\n\n • 🧠 <b>Интеллект:</b> в основном влияет на 🧪 маны, и немного другим статам"
                "\n\n❤️ Здоровье равняется: \n100 x ✊🏻Сила"
                "\n\n🗡 Урон равняется: \n✊🏻Сила + 👣Лвк + (🧠Инт : 2)"
                "\n\n🛡 Защита равняется: \n(✊🏻Сила + 👣Лвк + (🧠Инт : 2)) : 4"
                "\n\n🧪 Мана равняется: \n10 x 🧠Интеллект"
                "\n\n🪫 Энергия накапливается по 5 единиц каждый ⏳ ход"
                "\n\n🩸 Крит. урон: \n✊🏻Сила + (👣Лвк : 2) + (🧠Инт : 4)"
                "\n\n🩸 Крит. шанс: \n👣Лвк + (✊🏻Сила : 2) + (🧠Инт : 4)"
                "\n\n<i>Показатели ❤️ Здоровья, 🗡 Урона, 🛡 Защиты, 🧪 Маны являются фиксированными в отношении к "
                "основным статам персонажа перед началой битвы, а 🩸 Крит. урон и 🩸 Крит. шанс меняется каждый ход в "
                "зависимости от текущих статов персонажа</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=inline_builder(
            ["🔙 Назад"],
            ["battle_rules"],
            row_width=[2, 2]
        )
    )
    await callback.answer()

a = ("\n\n\n👥⚔️ <b>Командные битвы:</b> "
     "\n\n • 📋 Игроки регистрируется в группе и после делятся на две команды по равному количеству игроков."
     "\n\n • ✖️ Если количество игроков нечетное, то последный регистрируешься игрок выбивает."
     "\n\n • 🩸 Игра продолжется до тех пор, пока одна из команд не останется без игроков. "
     "\n\n • 🔥 Игроки Выжившей команды побеждают.")
