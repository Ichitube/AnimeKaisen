from motor.motor_asyncio import AsyncIOMotorClient

from recycling import profile

client = AsyncIOMotorClient("mongodb+srv://dire:1243qwtr@animekaisen.8r7or8e.mongodb.net/?retryWrites=true&w=majority&appName=AnimeKaisen")  #mongodb+srv://dire:1243qwtr@animekaisen.8r7or8e.mongodb.net/?retryWrites=true&w=majority,

db = client["AnimeKaisen"]

collection = db["users"]
chat_collection = db["chats"]


async def input_user(user_id: int, name, universe, character, power):
    data = dict({
        '_id': user_id,
        'name': name,
        'universe': universe,
        'character': {
            universe: character
        },
        'account': {
            'prime': False,
            'money': 1000,
            'fragments': 0,
            'clan': '',
            'referrals': [],
            'awards': []
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


async def get_user(user_id: int):
    user = await db.users.find_one({"_id": user_id})
    return user


async def update_user(user_id: int, data: dict):
    await db.users.update_one({"_id": user_id}, {"$set": data})


async def set_money(message):
    result = await db.users.update_many(
        {"account.money": {"$gt": 10000}},  # Условие: money больше 100000
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


async def in_battle():
    status = await db.users.count_documents({"battle.battle.status": 2})
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

    cursor = db.users.find()

    sorted_cursor = cursor.sort(var, -1)

    top_accounts_cursor = sorted_cursor.limit(10)

    rating_table = "\n\n"
    index = 1
    async for account in top_accounts_cursor:
        level = await profile.level(account['campaign']['level'])
        rating_table += f"{index}. {account['name']} - {account['campaign']['power']} {icon} ⛩️ {level} \n"
        index += 1

    rating_table += f"\nВаша место в рейтинге: {user_position}"

    return rating_table


async def wins_rating(var, account, icon):
    if account is not None:
        higher_pts_count = await db.users.count_documents({var: {'$gt': account['battle']['stats']['wins']}})
        user_position = higher_pts_count + 1
        name = account['name']
        wins = account['battle']['stats']['wins']
        user_rank = await profile.rerank_battle(account['stats']['rank'])
        text = (f"──────────────────"
                f"\n❖ Ваша место в рейтинге: \n{user_position}. {name} - {wins} {icon} Побед • {user_rank}")
    else:
        text = "\n❖ Вы не зарегистрированы"
    cursor = db.users.find()

    sorted_cursor = cursor.sort(var, -1)

    top_accounts_cursor = sorted_cursor.limit(10)

    rating_table = "\n"
    index = 1
    async for account in top_accounts_cursor:
        rank = await profile.rerank_battle(account['stats']['rank'])
        rating_table += (f"{index}. {account['name']} - "
                         f"{account['battle']['stats']['wins']} {icon} Побед • {rank} \n")
        index += 1

    rating_table += f"{text}"

    return rating_table


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
    db.users.update_one({'_id': user_id}, {'$set': {'last_call_time': date}}, upsert=True)


async def update_time(user_id, data, date):
    db.users.update_one({'_id': user_id}, {'$set': {data: date}}, upsert=True)
