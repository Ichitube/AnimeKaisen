from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InputMediaAnimation, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from keyboards.builders import inline_builder, menu_button
from data import mongodb, character_photo
from recycling import profile
from filters.chat_type import ChatTypeFilter

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
