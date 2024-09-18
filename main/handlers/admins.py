from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command

from data import mongodb

router = Router()

admins = [6946183730]


@router.message(Command("cheat_defense"))
async def file_id(message: Message):
    if message.from_user.id in admins:
        await mongodb.set_money(message)
    else:
        await message.reply(text="❖ ✖️ Ты не админ")


@router.message(Command("users"))
async def users_count(message: Message):
    if message.from_user.id in admins:
        await message.reply(f"{mongodb.users()}")
    else:
        await message.reply("❖ ✖️ Ты не админ")


@router.message(Command("chats"))
async def chats_count(message: Message):
    if message.from_user.id in admins:
        await message.reply(f"{mongodb.chats()}")
    else:
        await message.reply("❖ ✖️ Ты не админ")
