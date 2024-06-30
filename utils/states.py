from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    universe = State()


class Name(StatesGroup):
    name = State()


class Character(StatesGroup):
    character = State()


class Universe(StatesGroup):
    universe = State()
