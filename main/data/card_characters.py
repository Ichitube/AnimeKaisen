import asyncio
import inspect
import random

from aiogram import Bot
from data import character_photo
from data.mongodb import db


class CardCharacters:
    def __init__(self, ident, p_name, universe, name, slave, rid, data):
        avatar = character_photo.get_stats(universe, name, 'avatar')
        avatar_type = character_photo.get_stats(universe, name, 'type')
        rarity = character_photo.get_stats(universe, name, 'rarity')
        strength = character_photo.get_stats(universe, name, 'arena')['strength']
        agility = character_photo.get_stats(universe, name, 'arena')['agility']
        intelligence = character_photo.get_stats(universe, name, 'arena')['intelligence']
        clas = character_photo.get_stats(universe, name, 'arena')['class']

        self.ident = ident
        self.p_name = p_name
        self.universe = universe
        self.avatar = avatar
        self.avatar_type = avatar_type
        self.rarity = rarity
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.shield = 0
        self.stun = 0
        self.health = strength * 75
        self.attack = strength * 5 + agility * 5 + intelligence * 5
        self.defense = (strength + agility + (intelligence // 2)) // 4
        self.mana = intelligence * 10
        self.crit_dmg = strength + (agility // 2) + (intelligence // 4)
        self.crit_ch = agility + (strength // 2) + (intelligence // 4)
        self.clas = clas
        self.b_round = 1
        self.b_turn = True
        self.rid = rid
        self.slave = slave
        self.status = "🎴"
        self.data = data

