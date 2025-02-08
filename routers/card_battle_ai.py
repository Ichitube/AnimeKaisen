import asyncio
import random
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from data import characters, character_photo
from data import mongodb
from data.mongodb import db
from filters.chat_type import ChatTypeFilter, CallbackChatTypeFilter
from keyboards.builders import reply_builder, inline_builder, menu_button, Ability, rm
from recycling import profile
from routers import main_menu, gacha

router = Router()

battle_data = {}

user_data = {}
