import random
import string

from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command

from data import mongodb

router = Router()

admins = [6946183730, 6462809130]


@router.message(Command("cheat_defense"))
async def file_id(message: Message):
    if message.from_user.id in admins:
        await mongodb.set_money(message)
    else:
        await message.reply(text="❖ ✖️ Ты не админ")


@router.message(Command("users"))
async def users_count(message: Message):
    if message.from_user.id in admins:
        await message.reply(f"{1000 + mongodb.users()}")
    else:
        await message.reply("❖ ✖️ Ты не админ")


@router.message(Command("chats"))
async def chats_count(message: Message):
    if message.from_user.id in admins:
        await message.reply(f"{mongodb.chats()}")
    else:
        await message.reply("❖ ✖️ Ты не админ")


@router.message(Command("slaves_0000"))
async def chats_count(message: Message):
    if message.from_user.id in admins:
        await mongodb.clear_slaves_for_all_users()
        await message.reply("успешно")
    else:
        await message.reply("❖ ✖️ Ты не админ")


@router.message(Command("slave_0000"))
async def chats_count(message: Message):
    if message.from_user.id in admins:
        await mongodb.clear_slave_for_all_users()
        await message.reply("успешно")
    else:
        await message.reply("❖ ✖️ Ты не админ")


@router.message(Command("user_id"))
async def chats_count(message: Message):
    await message.reply(f"{message.from_user.id}")


def generate_promo_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@router.message(Command("promo_generate"))
async def chats_count(message: Message):
    if message.from_user.id in admins:
        promo_code = generate_promo_code()
        await mongodb.add_promo_code(promo_code, "5000¥💴  3🎫 5🎟")
        await message.reply(f"📦 New Promo: {promo_code}")
    else:
        await message.reply("❖ ✖️ Ты не админ")
