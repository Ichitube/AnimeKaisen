from data import mongodb


async def rerank(rank: int):
    if rank == 1:
        rank = 'Ронин 浪人 🎖️'
    elif rank == 2:
        rank = 'Самурай 侍 🎖️🎖️'
    elif rank == 3:
        rank = 'Сёгун 将軍 🎖️🎖️🎖️'
    elif rank == 4:
        rank = 'Аматэрасу 天照 🎖️🎖️🎖️🎖️'
    return rank


async def rerank_battle(rank: int):
    if rank == 1:
        rank = '🎖️'
    elif rank == 2:
        rank = '🎖️🎖️'
    elif rank == 3:
        rank = '🎖️🎖️🎖️'
    elif rank == 4:
        rank = '🎖️🎖️🎖️🎖️'
    return rank


async def update_rank(user_id: int, wins: int):
    if wins >= 600:
        await mongodb.update_user(user_id, {'stats.rank': 4})
    elif wins >= 300:
        await mongodb.update_user(user_id, {'stats.rank': 3})
    elif wins >= 100:
        await mongodb.update_user(user_id, {'stats.rank': 2})


async def level(lvl: int):
    if lvl == 1:
        lvl = 'Этаж 1'
    elif lvl == 2:
        lvl = 'Этаж 2'
    elif lvl == 3:
        lvl = 'Этаж 3'
    elif lvl == 4:
        lvl = 'Этаж 4'
    elif lvl == 5:
        lvl = 'Этаж 5'
    elif lvl == 6:
        lvl = 'Этаж 6'
    elif lvl == 7:
        lvl = 'Этаж 7'
    return lvl


async def update_level(user_id: int, count: int):
    if count >= 85:
        await mongodb.update_user(user_id, {'campaign.level': 7})
    elif count >= 70:
        await mongodb.update_user(user_id, {'campaign.level': 6})
    elif count >= 55:
        await mongodb.update_user(user_id, {'campaign.level': 5})
    elif count >= 40:
        await mongodb.update_user(user_id, {'campaign.level': 4})
    elif count >= 25:
        await mongodb.update_user(user_id, {'campaign.level': 3})
    elif count >= 10:
        await mongodb.update_user(user_id, {'campaign.level': 2})
