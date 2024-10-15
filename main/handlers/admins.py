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
        await message.reply(f"{mongodb.users()}")
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
