import re

from motor.motor_asyncio import AsyncIOMotorClient
from recycling import profile
from aiogram import Bot
from datetime import datetime, timedelta

client = AsyncIOMotorClient("mongodb+srv://dire:1243qwtr@animekaisen.8r7or8e.mongodb.net/?retryWrites=true&w=majority&appName=AnimeKaisen")  #mongodb+srv://dire:1243qwtr@animekaisen.8r7or8e.mongodb.net/?retryWrites=true&w=majority,

db = client["AnimeKaisen"]

collection = db["users"]
chat_collection = db["chats"]
promo_collection = db["promo"]
user_bosses = db["user_bosses"]
clans = db["clans"]


emoji_pattern = re.compile(
    "[\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "]+", flags=re.UNICODE)


async def input_user(user_id: int, name, universe, character, power):
    data = dict({
        '_id': user_id,
        'name': name,
        'universe': universe,
        'character': {
            universe: character
        },
        'clan': '',
        'account': {
            'prime': False,
            'money': 1000,
            'fragments': 0,
            'clan': '',
            'referrals': [],
            'awards': [],
            'clan_coins': 0
        },
        'stats': {
            'rank': 1,
            'exp': 0,
            'pts': 100,
        },
        'campaign': {
            'power': power,
            'level': 1,
            'stage': 1,
            'count': 0,
            'nephritis': 0,
            'gold': 0,
            'silver': 0,
            'bosses': []
        },
        'battle': {
            'stats': {
                'wins': 0,
                'loses': 0,
                'ties': 0
            },
            'battle': {
                'status': 0,
                'turn': False,
                'rid': "",
                'round': 1
            }
        },
        'inventory': {
            'characters': {
            },
            'items': {
                'tickets': {
                    'keys': 0,
                    'golden': 1,
                    'common': 3,
                }
            },
            'home': [],
            'slaves': []
        },
    })

    full_data = data

    await db.users.insert_one(full_data)


async def get_user_boss(user_id: int):
    boss = await db.user_bosses.find_one({"user_id": user_id})
    return boss


async def create_or_update_user_boss(user_id: int, boss_id: int, boss_hp: int):
    return await db.user_bosses.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "boss_id": boss_id,
                "current_hp": boss_hp,
                "damage_dealt": 0,
                "last_spawn": datetime.utcnow()
            }
        },
        upsert=True
    )


async def clan_exists(name):
    return await db.clans.find_one({"_id": name}) is not None


async def create_clan(data):
    await db.clans.insert_one(data)


async def get_user(user_id: int):
    user = await db.users.find_one({"_id": user_id})
    return user


async def get_clan(chat_id):
    clan = await db.clans.find_one({"_id": chat_id})
    return clan


async def update_user(user_id: int, data: dict):
    await db.users.update_one({"_id": user_id}, {"$set": data})


async def update_clan(clan_name: str, data: dict):
    await db.clans.update_one({"_id": clan_name}, {"$set": data})


async def delete_clan(clan_name: str):
    """
    Удаляет клан из базы данных.
    """
    result = await db.clans.delete_one({"_id": clan_name})
    if result.deleted_count == 0:
        raise ValueError("✖️ Клан не найден для удаления!")


async def rename_clan(old_name: str, new_name: str):
    """
    Переименовывает клан: копирует данные клана под новым _id и удаляет старый.
    Также обновляет клан у всех участников.
    """

    # Ищем клан по старому имени
    clan = await db.clans.find_one({"_id": old_name})
    if not clan:
        raise ValueError("✖️ Клан не найден!")

    # Проверяем, что нового имени ещё нет
    existing = await db.clans.find_one({"_id": new_name})
    if existing:
        raise ValueError("✖️ Клан с таким именем уже существует!")

    # Копируем клан под новым именем
    clan["_id"] = new_name
    await db.clans.insert_one(clan)

    # Удаляем старый клан
    await db.clans.delete_one({"_id": old_name})

    # Обновляем клан у всех участников
    members = clan.get("members", [])
    for uid in members:
        await db.users.update_one({"_id": uid}, {"$set": {"clan": new_name}})



async def set_money(message):
    result = await db.users.update_many(
        {"account.money": {"$gt": 50000}},  # Условие: money больше 100000
        {"$set": {"account.money": 100}}  # Действие: установить money в 100
    )

    await message.answer(text=f"Modified {result.modified_count} documents.")


async def users():
    user_count = await db.users.count_documents({})
    return user_count


async def chats():
    chat_count = await db.chats.count_documents({})
    return chat_count


async def change_char(user_id: int, universe, character):
    await db.users.update_one(
        {"_id": user_id},
        {"$set": {f"character.{universe}": character}}
    )


async def update_many(data, update):
    await db.users.update_many(data, update)


async def update_value(user_id: int, data: dict):
    await db.users.update_one({"_id": user_id}, {"$inc": data})


async def find_opponent():
    status = await db.users.find_one({"battle.battle.status": 1})
    return status


async def find_card_opponent():
    status = await db.users.find_one({"battle.battle.status": 3})
    return status


async def in_battle():
    status = await db.users.count_documents({"battle.battle.status": 2})
    card = await db.users.count_documents({"battle.battle.status": 4})
    status += card
    return status


async def push(universe, character_category, character, user_id: int):
    await db.users.update_one(
        {'_id': user_id},
        {'$push': {f'inventory.characters.{universe}.{character_category}': character}})


async def pull(universe, character_category, character, user_id: int):
    await db.users.update_one(
        {'_id': user_id},
        {'$pull': {f'inventory.characters.{universe}.{character_category}': character}}
    )


async def push_home(user_id: int, home):
    await db.users.update_one({'_id': user_id}, {'$push': {'inventory.home': home}})


async def push_slave(user_id: int, slave):
    await db.users.update_one({'_id': user_id}, {'$push': {'inventory.slaves': slave}})


async def push_referral(user_id: int, new_user):
    await db.users.update_one({'_id': user_id}, {'$push': {'account.referrals': new_user}})


async def send_rating(var, account, icon):
    higher_pts_count = await db.users.count_documents({var: {'$gt': account['campaign']['power']}})

    user_position = higher_pts_count + 1
    user_name = account['name']
    user_power = account['campaign']['power']
    level = await profile.level(account['campaign']['level'])

    cursor = db.users.find()

    sorted_cursor = cursor.sort(var, -1)

    top_accounts_cursor = sorted_cursor.limit(10)

    rating_table = "\n\n"
    index = 1
    async for account in top_accounts_cursor:
        level = await profile.level(account['campaign']['level'])
        rating_table += (f"╭┈๋જ‌›{account['name']} "
                         f"\n{index}┄{account['campaign']['power']} {icon} ⛩️ {level} \n")
        index += 1

    rating_table += f"╰── Вы: {user_position}. {user_name} - {user_power} {icon} ──╯"
    return rating_table


async def wins_rating(var, account, icon):
    if account is not None:
        higher_pts_count = await db.users.count_documents({var: {'$gt': account['battle']['stats']['wins']}})
        user_position = higher_pts_count + 1
        name = account['name']
        wins = account['battle']['stats']['wins']
        user_rank = await profile.rerank_battle(account['stats']['rank'])
        text = f"╰── Вы: {user_position}. {name} - {wins} {icon} Побед • {user_rank} ──╯"
    else:
        text = "╰── Вы не зарегистрированы ──╯"
    cursor = db.users.find()

    sorted_cursor = cursor.sort(var, -1)

    top_accounts_cursor = sorted_cursor.limit(10)

    rating_table = "\n"
    index = 1
    async for account in top_accounts_cursor:
        rank = await profile.rerank_battle(account['stats']['rank'])
        rating_table += (f"╭┈๋જ‌›{account['name']} - "
                         f"\n{index}┄{account['battle']['stats']['wins']} {icon} Побед • {rank} \n")
        index += 1

    table = "<blockquote>" + rating_table + "</blockquote>" + f"{text}"

    return table

ADMIN_ID = 6462809130

async def auto_reset_rating(bot, rating_type: str, field: str, reset_value, days: int = 14):
    """
    rating_type: 'referrals' или 'wins'
    field: поле в MongoDB ('account.referrals' или 'battle.stats.wins')
    reset_value: [] для списка, 0 для int
    days: период сброса (по умолчанию 14 дней)
    """

    current_date = datetime.today().date()
    meta_id = f"{rating_type}_reset"

    reset_info = await db.meta.find_one({"_id": meta_id})
    if not reset_info:
        next_reset = datetime.combine(current_date, datetime.min.time()) + timedelta(days=days)
        await db.meta.update_one({"_id": meta_id}, {"$set": {"next_reset": next_reset}}, upsert=True)
        return None  # ещё рано сбрасывать

    next_reset = reset_info["next_reset"]

    if datetime.now() >= next_reset:
        # готовим топ-10
        if rating_type == "referrals":
            pipeline = [
                {
                    "$addFields": {
                        "count": {
                            "$cond": {
                                "if": {"$isArray": "$account.referrals"},
                                "then": {"$size": "$account.referrals"},
                                "else": 0
                            }
                        }
                    }
                },
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
        else:  # wins
            pipeline = [
                {"$addFields": {"count": "$battle.stats.wins"}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]

        winners = db.users.aggregate(pipeline)

        # сообщение для админа
        text_admin = f"🏆 Итоги рейтинга {rating_type}\n\n"
        index = 1
        rewards = {1: "🌟 ×150", 2: "🌟 ×100", 3: "🌟 ×50"}

        async for acc in winners:
            reward = rewards.get(index, "🌟 ×25")
            text_admin += (
                f"{index}. {acc['name']} (ID: {acc['_id']}) — "
                f"{acc.get('count', 0)} 👥/🏆 {reward}\n"
            )
            index += 1

        await bot.send_message(ADMIN_ID, text_admin, parse_mode="HTML")

        # сообщение всем пользователям
        all_users = db.users.find()
        async for user in all_users:
            try:
                await bot.send_message(
                    user["_id"],
                    f"♻️ Акция {rating_type} завершена!\n\n"
                    f"🏆 Скоро начнётся новый рейтинг, готовьтесь!"
                )
            except Exception as e:
                print(f"Не удалось отправить {user['_id']}: {e}")

        # сброс значений
        await db.users.update_many({}, {"$set": {field: reset_value}})

        # устанавливаем новую дату сброса
        new_reset = datetime.combine(current_date, datetime.min.time()) + timedelta(days=days)
        await db.meta.update_one({"_id": meta_id}, {"$set": {"next_reset": new_reset}})

async def invite_rating(var, account):
    # авто-сброс рефералов
    await auto_reset_rating(Bot, "referrals", "account.referrals", [])

    # достаём дату следующего сброса
    reset_info = await db.meta.find_one({"_id": "referrals_reset"})
    next_reset = reset_info["next_reset"] if reset_info else None

    pipeline = [
        {
            "$addFields": {
                "referrals_count": {
                    "$cond": {
                        "if": {"$isArray": "$account.referrals"},
                        "then": {"$size": "$account.referrals"},
                        "else": 0
                    }
                }
            }
        },
        {"$sort": {"referrals_count": -1}},
        {"$limit": 10}
    ]
    winners = db.users.aggregate(pipeline)

    text = "🏆 <b>Рейтинг приглашений</b>\n<blockquote>"
    index = 1
    rewards = {1: "🌟 ×150", 2: "🌟 ×100", 3: "🌟 ×50"}

    async for acc in winners:
        reward = rewards.get(index, "🌟 ×25")

        if index == 1:
            place = "🥇"
        elif index == 2:
            place = "🥈"
        elif index == 3:
            place = "🥉"
        else:
            place = f"{index}."

        text += f"{place} {acc['name']} — {acc.get('referrals_count', 0)} человек 👥 {reward}\n"
        index += 1

    # позиция текущего пользователя
    user_refs = len(account.get("account", {}).get("referrals", []))
    higher_pts_count = await db.users.count_documents({
        "$expr": {
            "$gt": [
                {
                    "$cond": {
                        "if": {"$isArray": "$account.referrals"},
                        "then": {"$size": "$account.referrals"},
                        "else": 0
                    }
                },
                user_refs
            ]
        }
    })
    user_position = higher_pts_count + 1
    user_name = account['name']

    text += f"╰── Вы: {user_position}. {user_name} — {user_refs} человек 👥 ──╯"
    text += "</blockquote>"

    # добавляем таймер
    if next_reset:

        if next_reset:
            delta = next_reset - datetime.now()
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60

            if days > 0:
                left_text = f"{days} дн. {hours} ч. {minutes} мин."
            elif hours > 0:
                left_text = f"{hours} ч. {minutes} мин."
            else:
                left_text = f"{minutes} мин."

            text += f"\n♻️ До сброса: ⏱️ {left_text}"

    return text



async def reset_referrals(account):
    pipeline = [
        {
            "$addFields": {
                "referrals_count": {
                    "$cond": {
                        "if": {"$isArray": "$account.referrals"},
                        "then": {"$size": "$account.referrals"},
                        "else": 0
                    }
                }
            }
        },
        {"$sort": {"referrals_count": -1}},
        {"$limit": 10}
    ]
    winners = db.users.aggregate(pipeline)

    text = "🏆 <b>Итоги рейтинга приглашений</b>\n<blockquote>"
    index = 1
    rewards = {1: "🌟 ×150", 2: "🌟 ×100", 3: "🌟 ×50"}

    async for acc in winners:
        reward = rewards.get(index, "🌟 ×25")

        if index == 1:
            place = "🥇."
        elif index == 2:
            place = "🥈."
        elif index == 3:
            place = "🥉."
        else:
            place = f"{index}."

        text += f"{place} {acc['name']} — {acc.get('referrals_count', 0)} человек 👥 {reward}\n"
        index += 1

    # позиция текущего пользователя
    user_refs = len(account.get("account", {}).get("referrals", []))
    higher_pts_count = await db.users.count_documents({
        "$expr": {
            "$gt": [
                {
                    "$cond": {
                        "if": {"$isArray": "$account.referrals"},
                        "then": {"$size": "$account.referrals"},
                        "else": 0
                    }
                },
                user_refs
            ]
        }
    })
    user_position = higher_pts_count + 1
    user_name = account['name']

    text += f"╰── Вы: {user_position}. {user_name} — {user_refs} человек 👥 ──╯"
    text += "</blockquote>\n❇️ Победители получат награды"

    # сброс
    await db.users.update_many({}, {"$set": {"account.referrals": []}})

    return text


async def wins_rat(account):
    # авто-сброс побед
    await auto_reset_rating(Bot, "wins", "battle.stats.wins", 0)

    # достаём дату следующего сброса
    reset_info = await db.meta.find_one({"_id": "wins_reset"})
    next_reset = reset_info["next_reset"] if reset_info else None

    pipeline = [
        {"$addFields": {"wins_count": "$battle.stats.wins"}},
        {"$sort": {"wins_count": -1}},
        {"$limit": 10}
    ]
    winners = db.users.aggregate(pipeline)

    text = "🏆 <b>Рейтинг побед</b>\n<blockquote>"
    index = 1
    rewards = {1: "🌟 ×150", 2: "🌟 ×100", 3: "🌟 ×50"}

    async for acc in winners:
        reward = rewards.get(index, "🌟 ×25")

        if index == 1:
            place = "🥇"
        elif index == 2:
            place = "🥈"
        elif index == 3:
            place = "🥉"
        else:
            place = f"{index}."

        text += f"{place} {acc['name']} — {acc.get('wins_count', 0)} Побед 🏆 {reward}\n"
        index += 1

    # позиция текущего пользователя
    user_wins = account.get("battle", {}).get("stats", {}).get("wins", 0)
    higher_pts_count = await db.users.count_documents(
        {"battle.stats.wins": {"$gt": user_wins}}
    )
    user_position = higher_pts_count + 1
    user_name = account['name']

    text += f"╰── Вы: {user_position}. {user_name} — {user_wins} Побед 🏆 ──╯"
    text += "</blockquote>"

    # добавляем таймер
    # добавляем таймер
    if next_reset:

        if next_reset:
            delta = next_reset - datetime.now()
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60

            if days > 0:
                left_text = f"{days} дн. {hours} ч. {minutes} мин."
            elif hours > 0:
                left_text = f"{hours} ч. {minutes} мин."
            else:
                left_text = f"{minutes} мин."

            text += f"\n♻️ До сброса: ⏱️ {left_text}"

    return text


async def reset_wins(account):
    pipeline = [
        {
            "$addFields": {
                "wins_count": "$battle.stats.wins"
            }
        },
        {"$sort": {"wins_count": -1}},
        {"$limit": 10}
    ]
    winners = db.users.aggregate(pipeline)

    text = "🏆 <b>Итоги рейтинга побед</b>\n<blockquote>"
    index = 1
    rewards = {1: "🌟 ×150", 2: "🌟 ×100", 3: "🌟 ×50"}

    async for acc in winners:
        reward = rewards.get(index, "🌟 ×25")

        if index == 1:
            place = "🥇."
        elif index == 2:
            place = "🥈."
        elif index == 3:
            place = "🥉."
        else:
            place = f"{index}."

        text += f"{place} {acc['name']} — {acc.get('wins_count', 0)} Побед 🏆 {reward}\n"
        index += 1

    # позиция текущего пользователя
    user_wins = account.get("battle", {}).get("stats", {}).get("wins", 0)
    higher_pts_count = await db.users.count_documents(
        {"battle.stats.wins": {"$gt": user_wins}}
    )
    user_position = higher_pts_count + 1
    user_name = account['name']

    text += f"\n╰── Вы: {user_position}. {user_name} — {user_wins} Побед 🏆 ──╯"
    text += "</blockquote>\n❇️ Победители получат награды"

    # сброс побед всем
    await db.users.update_many({}, {"$set": {"battle.stats.wins": 0}})

    return text



# здесь обработка чатов


async def start_chat(chat_id, title, link, universe):
    data = dict({
        '_id': chat_id,
        'link': link,
        'title': title,
        'universe': universe,
        'top': {},
        'battle': {
            'status': 0,
            'stats': {}
        }
    })

    chat_data = data

    await db.chats.insert_one(chat_data)


async def change_chat_name(chat_id, title):
    await db.chats.update_one({'_id': chat_id}, {'$set': {'title': title}})


async def change_chat_universe(chat_id, universe):
    await db.chats.update_one({'_id': chat_id}, {'$set': {'universe': universe}})


async def insert_win(chat_id, user, name):
    user = str(user)  # преобразование user в строку
    chat = await db.chats.find_one({'_id': chat_id})
    if user in chat['top']:
        await db.chats.update_one({'_id': chat_id}, {'$inc': {f'top.{user}.wins': 1}})
        await db.chats.update_one({'_id': chat_id}, {'$set': {f'top.{user}.name': name}})
    else:
        await db.chats.update_one({'_id': chat_id}, {'$set': {f'top.{user}': {'wins': 1, 'name': name}}})


async def chat_rating(chat_id, icon):
    chat = await db.chats.find_one({'_id': chat_id})

    top = chat['top']
    top = dict(sorted(top.items(), key=lambda item: item[1]['wins'], reverse=True))
    rating_table = "\n"
    index = 1
    for user in top:
        rating_table += f"{index}. {top[user]['name']} - {top[user]['wins']} {icon} Побед\n"
        index += 1

    return rating_table


async def update_get_card(user_id, date):
    await db.users.update_one({'_id': user_id}, {'$set': {'last_call_time': date}}, upsert=True)


async def update_time(user_id, data, date):
    await db.users.update_one({'_id': user_id}, {'$set': {data: date}}, upsert=True)


async def clear_slaves_for_all_users():
    await db.users.update_many(
        {},  # Пустой фильтр означает обновление всех документов
        {"$set": {"inventory.slaves": []}}  # Устанавливаем пустой массив для всех
    )


async def clear_slave_for_all_users():
    await db.users.update_many(
        {},  # Пустой фильтр означает обновление всех документов
        {"$set": {"inventory.slave": []}}  # Устанавливаем пустой массив для всех
    )


async def find_promo(promo_code):
    promo = await db.promo_collection.find_one({"code": promo_code})
    return promo


async def update_promo(promo_code, user_id):
    await db.promo_collection.update_one(
        {"code": promo_code},
        {"$push": {"used_by": user_id}}
    )


async def add_promo_code(promo_code, reward):
    await db.promo_collection.insert_one({
        "code": promo_code,
        "reward": reward,
        "used_by": []
    })


async def give_to_all(data, message):
    await db.users.update_many({}, {"$inc": data})
    await message.answer("❖ ✅ Всем выдано")


async def remove_emojis():
    cursor = db.users.find({})
    async for document in cursor:
        name = document.get('name', '')
        if name:
            # Удаление эмодзи из name
            new_name = emoji_pattern.sub(r'', name)
            if new_name != name:
                # Обновление документа
                await db.users.update_one({'_id': document['_id']}, {'$set': {'name': new_name}})


async def install_zero():
    current_date = datetime.today().date()
    current_date_minus_one = current_date - timedelta(days=1)
    current_datetime = datetime.combine(current_date_minus_one, datetime.time(datetime.now()))
    await db.users.update_many({}, {"$set": {"last_call_time": current_datetime}})


async def migrate_characters():
    async for user in db.users.find():
        inventory = user.get("inventory", {})
        characters = inventory.get("characters", {})

        # Если "Allstars(old)" существует в персонажах
        if "Allstars(old)" in characters:
            old_allstars = characters["Allstars(old)"]

            # Перебор редкостей
            for rarity, char_list in old_allstars.items():
                if rarity not in characters.get("Allstars", {}):
                    characters.setdefault("Allstars", {})[rarity] = []

                # Добавляем персонажей, которых ещё нет в "Allstars"
                for char in char_list:
                    if char not in characters["Allstars"][rarity]:
                        characters["Allstars"][rarity].append(char)

            # Удаляем "Allstars(old)"
            del characters["Allstars(old)"]

            # Обновляем инвентарь
            await db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"inventory.characters": characters}}
            )

        # Обновление значения "universe"
        if user.get("universe") == "Allstars(old)":
            await db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"universe": "Allstars"}}
            )


async def get_top10_text() -> str:
    cursor = db.users.find({"campaign.power": {"$exists": True}}).sort("campaign.power", -1).limit(5)
    top_accounts = await cursor.to_list(length=5)

    result = [
        f"{i + 1}. 🪪 {acc.get('name', 'Неизвестно')} ᐷ ⚜️ {acc.get('campaign', {}).get('power', 0)}"
        for i, acc in enumerate(top_accounts)
    ]

    return "\n".join(result)


