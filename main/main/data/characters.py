import asyncio
import inspect
import random

from data import character_photo


async def send_action(bot, self, enemy, chat_id, gif, text):
    if self.chat_id == 0:
        await bot.send_animation(chat_id=self.ident, animation=gif, caption=text)
        await bot.send_animation(chat_id=enemy.ident, animation=gif, caption=text)
    else:
        await bot.send_animation(chat_id=chat_id, animation=gif, caption=text)


def calculate_critical_chance(crit):
    # Пример: Шанс критической атаки = 1% + 0.5% за каждый пункт crit
    base_chance = 1  # Базовый шанс (например, 1%)
    additional_chance_per_crit = 0.5  # Дополнительный шанс за каждый пункт crit (например, 0.5%)
    critical_chance = base_chance + additional_chance_per_crit * crit
    return critical_chance


def calculate_critical_damage(damage, base_damage, crit):
    if random.randint(1, 100) < crit:
        critical_damage = base_damage * 2
        msg = f"🩸 Критического"
        return critical_damage, msg
    else:
        msg = ''
        return damage, msg


def calculate_shield(enemy, damage):
    if enemy.shield >= (damage - enemy.defense):
        enemy.shield -= (damage - enemy.defense)
    else:
        enemy.health -= ((damage - enemy.defense) - enemy.shield)
        enemy.shield = 0


async def calculate_mana(self, mana):
    if self.mana < mana:
        return False
    self.mana -= mana
    return True


async def calculate_energy(self, energy):
    if self.energy < energy:
        return False
    self.energy -= energy
    return True


def change_skills(player, new_skills):
    player.ability = new_skills


def fix_effects(_player, _points):
    pass


def undo_change_skills(player, _):
    player.ability = player.initial_skills


def bash(player, points):
    player.stun += points


def undo_bash(player, _):
    player.stun = 0  # возвращаем атаку к исходному значению


def immunity(player, _):
    player.immunity = True


def undo_immunity(player, _):
    player.immunity = False


def increase_hp(player, points):
    player.health += points


def decrease_hp(player, points):
    player.health -= points


def block_hp(player, _points):
    hp = player.pre_hp - player.health
    player.health += hp


def increase_attack(player, points):
    player.attack += points


def decrease_attack(player, points):
    player.attack -= points


def return_attack(player, _):
    player.attack = player.initial_attack


def increase_defense(player, points):
    player.defense += points


def decrease_defense(player, points):
    player.defense -= points


def return_defense(player, _):
    player.defense = player.initial_defense


def increase_strength(player, points):
    player.strength += points


def decrease_strength(player, points):
    player.strength -= points


def return_strength(player, _):
    player.strength = player.initial_strength


def increase_agility(player, points):
    player.agility += points


def decrease_agility(player, points):
    player.agility -= points


def return_agility(player, _):
    player.agility = player.initial_agility


async def undo_hollow(player, bot):
    gif = 'CgACAgIAAx0CfstymgACC7pmAZimyPqU6JibxYpK5b0S2GL_5AACzUYAAr96-UsFPb6DYW9sXjQE'
    if player.chat_id == 0:
        await bot.send_animation(player.ident, animation=gif)
        await bot.send_animation(player.rid, animation=gif)
    else:
        await bot.send_animation(player.chat_id, animation=gif)


async def undo_second(player, bot):
    gif = 'CgACAgIAAx0CfstymgACECpmH6n2ouJ3Q-jCK-_ilD_28UPY2wACeDsAAkXDAAFJ9jwVlQdfS3M0BA'
    if player.chat_id == 0:
        await bot.send_animation(player.ident, animation=gif)
        await bot.send_animation(player.rid, animation=gif)
    else:
        await bot.send_animation(player.chat_id, animation=gif)


async def undo_stage(player, bot):
    gif = 'CgACAgIAAx0CfstymgACC7pmAZimyPqU6JibxYpK5b0S2GL_5AACzUYAAr96-UsFPb6DYW9sXjQE'
    if player.chat_id == 0:
        await bot.send_animation(player.ident, animation=gif)
        await bot.send_animation(player.rid, animation=gif)
    else:
        await bot.send_animation(player.chat_id, animation=gif)


async def undo_gg(player, bot):
    new_skills = ["˹🗡Атака˼", "˹🌙Гецуга⊛Теншоу˼"]
    player.ability = new_skills

    gif = 'CgACAgQAAx0CfstymgACC7NmAZfDDlBzUZDrWEd_JlbZzgWeawACtQQAAiwDxFJHdMP4lU3bDDQE'
    text = "⊛ Ичиго заполучил сила Квинси"
    if player.chat_id == 0:
        await bot.send_animation(player.ident, animation=gif, caption=text)
        await bot.send_animation(player.rid, animation=gif, caption=text)
    else:
        await bot.send_animation(player.chat_id, animation=gif, caption=text)


async def undo_minazuki(player, bot):
    gif = 'CgACAgIAAx0CfstymgACD-9mIIc0hO6z7NH2cuX2yZQn9w2c-wAC2zcAAkXDAAFJEcm4Q5VkHho0BA'
    player.hp = 0
    if player.chat_id == 0:
        await bot.send_animation(player.ident, animation=gif)
        await bot.send_animation(player.rid, animation=gif)
    else:
        await bot.send_animation(player.chat_id, animation=gif)


async def undo_g(player, bot):
    player.add_passive(Passive("✖️ Гецуга", bash, undo_bash, 5, 1, apply_once=True))
    player.add_passive(Passive("⇩🛡⇩", decrease_defense, return_defense, 5, points=player.defense, apply_once=True))
    player.add_passive(Passive("⇩🗡⇩", decrease_attack, return_attack, 5, points=player.attack, apply_once=True))
    player.add_passive(Passive("✖️ Гецуга", fix_effects, undo_gg, 5, bot, apply_once=True))

    gif = 'CgACAgIAAx0CfstymgACC4Rl_tub6K6DxR0-SRyTXHZOqeqY9wACq04AAv0v8EscO-Ttmfzf4DQE'
    if player.chat_id == 0:
        await bot.send_animation(player.ident, animation=gif)
        await bot.send_animation(player.rid, animation=gif)
    else:
        await bot.send_animation(player.chat_id, animation=gif)


class Passive:
    def __init__(self, name, effect, undo_effect, duration, points=None, apply_once=False):
        self.name = name
        self.effect = effect
        self.undo_effect = undo_effect
        self.duration = duration
        self.points = points
        self.applied = False
        self.apply_once = apply_once

    def apply_effect(self, player):
        if not self.applied or not self.apply_once:
            self.effect(player, self.points)
            self.applied = True
        self.duration -= 1

    def undo_effect(self, player):
        if self.duration == 0 and self.undo_effect is not None:
            self.undo_effect(player, self.points)


class Character:
    def __init__(self, ident, p_name, name, strength, agility, intelligence,
                 ability, b_round, b_turn, rid, slave, chat_id):
        self.ident = ident
        self.p_name = p_name
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.shield = 0
        self.stun = 0
        self.passives = []
        self.passive_names = []
        self.health = strength * 100
        self.attack = strength + agility + (intelligence // 2)
        self.defense = (strength + agility + (intelligence // 2)) // 4
        self.mana = intelligence * 10
        self.crit_dmg = strength + (agility // 2) + (intelligence // 4)
        self.crit_ch = agility + (strength // 2) + (intelligence // 4)
        self.ability = ability
        self.b_round = b_round
        self.b_turn = b_turn
        self.rid = rid
        self.pre_hp = self.health
        self.initial_skills = ability.copy()
        self.initial_attack = self.attack
        self.initial_defense = self.defense
        self.initial_strength = self.strength
        self.initial_agility = self.agility
        self.immortal = 0
        self.energy = 0
        self.immunity = False
        self.slave = slave
        self.chat_id = chat_id

    def add_passive(self, passive):
        self.passives.append(passive)
        if passive.name not in self.passive_names:
            self.passive_names.append(passive.name)

    def update_passives(self):
        for passive in self.passives:
            passive.apply_effect(self)
            if passive.duration == 0:
                if inspect.iscoroutinefunction(passive.undo_effect):
                    asyncio.create_task(passive.undo_effect(self, passive.points))
                else:
                    passive.undo_effect(self, passive.points)
                if not any(p.name == passive.name for p in self.passives if p is not passive):
                    self.passive_names.remove(passive.name)
            self.passives = [p for p in self.passives if p.duration > 0]


async def turn(self, bot, action, enemy, chat_id):

    self.crit_dmg = self.strength + self.attack - (enemy.strength // 4) + (self.intelligence // 4)
    self.crit_ch = self.agility - (enemy.agility + enemy.intelligence // 4) + (self.intelligence // 4)
    enemy.pre_hp = enemy.health

    if action == '˹🗡Атака˼':
        chance = calculate_critical_chance(self.crit_ch)
        damage, msg = calculate_critical_damage(self.attack, self.crit_dmg, chance)

        calculate_shield(enemy, damage)

        if chat_id == 0:
            await bot.send_message(self.ident, f"˹{self.name} нанес(ла) {damage} {msg} 🗡 урона˼")
            await bot.send_message(enemy.ident, f"˹{self.name} нанес(ла) {damage} {msg} 🗡 урона˼")
        else:
            await bot.send_message(chat_id, f"˹{self.name} нанес(ла) {damage} {msg} 🗡 урона˼")

# Ichigo Kurosaki

    elif action == '˹▫️Слэш˼':
        mana = await calculate_mana(self, 10)
        if not mana:
            return False, True

        damage = self.attack * 2
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC3Jl_VkwRxYdJ5H07Ijm28oYOJEH5QACtkgAAv0v8EtrXYxNcPx0dDQE'
        caption = (f"▫️Слэш"
                   f"\n\nИчиго нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹◽️Поступь˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.strength
        self.health += self.strength

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC3dl_Vz2TTu7KeI--jvzfvKFElSg9wAC2EgAAv0v8EtdmGJdFwkcUDQE'
        caption = (f"◽️Поступь"
                   f"\n\nИчиго нанес {damage} 🗡 урона"
                   f"\n + {self.strength}❤️ hp")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹◻️Гецуга Теншоу˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.attack * 2 + self.intelligence + self.strength + self.agility

        calculate_shield(enemy, damage)

        gif = 'CgACAgQAAx0CfstymgACCzBl9fvaeK6nqo-0B95KKPEf9t-qPwACKwMAAmEHDFO0UwUbOXRxjjQE'
        caption = (f"◻️Гецуга Теншоу"
                   f"\n\nИчиго нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹◾️Тенса࿖Зангецу˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹🟥Гецуга◼️Теншоу˼", "˹💀Пустой˼"]
        skills_change = Passive("Банкай ࿖", change_skills, undo_change_skills, 8, new_skills)
        attack_up = Passive("⇪🗡⇪", increase_attack, decrease_attack, 8, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)

        gif = 'CgACAgIAAx0CfstymgACCzZl8T9WLPOCuQG34Qcjn4xCiP6KXAACWD8AAvSEkUtsDKXUVPoFeTQE'
        caption = (f"Банкай ࿖: Tensa Zangetsu"
                   f"\n\n🗡Урон +200 8⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🟥Гецуга◼️Теншоу˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence + self.strength + self.agility

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC29l_VY2zFxjirZIIdOwlfhygw05rwACjEgAAv0v8EuhD_HwUkIBHzQE'
        caption = (f"Гецуга Теншоу"
                   f"\n\nИчиго нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹💀Пустой˼':
        mana = await calculate_mana(self, 45)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹🟥Гецуга Теншоу˼"]
        skills_change = Passive("💀Пустой", change_skills, undo_change_skills, 5, new_skills)
        im = Passive("💥", immunity, undo_immunity, 5, 1, apply_once=True)
        strength_up = Passive("↑✊🏻↑", increase_strength, decrease_strength, 5, 100, apply_once=True)
        agility_up = Passive("↑👣↑", increase_agility, decrease_agility, 5, 100, apply_once=True)
        attack_enemy = Passive("🗡", decrease_hp, fix_effects, 5, 100)

        self.add_passive(skills_change)
        self.add_passive(strength_up)
        self.add_passive(agility_up)
        enemy.add_passive(attack_enemy)
        self.add_passive(im)

        gif = 'CgACAgIAAx0CfstymgACC3pl_WW2_gyHJDns-4FGMlmEfkb6GwACL0kAAv0v8EtwrnW1K81WEDQE'
        caption = (f"💀Сила Пустого"
                   f"\n\n  ✊🏻Сила +100 5⏳"
                   f"\n  👣Лвк +100 5⏳"
                   f"\n🗡Автоатака 100🗡 5⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🟥Гецуга Теншоу˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACCyxl8SWxVYrXROiEsZDYy1xJ1czIDAACKEkAAvSEiUtyJh4oGxC1tzQE'
        caption = (f"Гецуга Теншоу"
                   f"\n\nИчиго нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹◾️Финал⛓Гецуга◾️˼':
        energy = await calculate_energy(self, 70)
        if not energy:
            return True, False

        new_skills = ["˹◾️⛓Мугецу⛓◾️˼"]
        skills_change = Passive("⛓Гецуга◾️", change_skills, undo_change_skills, 3, new_skills, apply_once=True)
        im = Passive("💥", immunity, undo_immunity, 3, 1, apply_once=True)
        over_g = Passive("⛓Гецуга◾️", fix_effects, undo_g, 3, bot, apply_once=True)
        defense_up = Passive("⇪🛡⇪", increase_defense, fix_effects, 3, 900, apply_once=True)
        attack_up = Passive("⇪🗡⇪", increase_attack, fix_effects, 3, 1000, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(over_g)
        self.add_passive(defense_up)
        self.add_passive(attack_up)
        enemy.add_passive(im)

        gif = 'CgACAgIAAx0CfstymgACC4ll_c3Iv9lZgb5gNHy_i9vCDgcs3AACBU8AAv0v8EuVgi04yq7GzjQE'
        caption = (f"Финальная Гецуга Теншоу"
                   f"\n\n🗡Атака +1000 2⏳"
                   f"\n🛡Защита +900 2⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹◾️⛓Мугецу⛓◾️˼':
        damage = self.attack * 4
        enemy.health -= damage

        gif = 'CgACAgIAAx0CfstymgACC4Bl_WxyumX77FXeGkcaaKF6ZIhWwAACh0kAAv0v8Evl3Ud_DK97oDQE'
        caption = (f"Мугецу"
                   f"\n\nИчиго нанес {damage} 🗡 чистого урона"
                   f"\n💥невосприимчивый контроли")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌙Гецуга⊛Теншоу˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False
        damage = self.attack * 4 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgQAAx0CfstymgACCy5l_epOERFh-2XQSUu-pGQNR7W8QAACXAQAAtpKjFNNpRCVY58cTjQE'
        caption = (f"Гецуга Теншоу"
                   f"\n\nИчиго нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹☄️Гран Рей Серо˼':
        damage = self.attack * 3 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC7ll_ttMnKMi5xOFBHaZfm9HDyfaVgACzEYAAr96-UuNLgc1LY6fDzQE'
        caption = (f"Гран Рей Серо"
                   f"\n\nИчиго нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Toshiro Hitsugaya

    elif action == '˹❄️Хёкецу˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True

        damage = self.attack // 2 + self.intelligence + self.strength + self.agility

        stun = Passive("❄️Заморозка", bash, undo_bash, 2, 1, apply_once=True)

        enemy.add_passive(stun)

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC_lmBPL3pSbME9k2QgfKNG4cpCnxHQACtz0AAu4mKEh95WRm0QiIljQE'
        caption = (f"❄️Хёкецу "
                   f"\n\nТоширо нанес {damage} 🗡 урона"
                   f"\n❄️Замарозка 1⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹❄️Рокуи Хёкецу˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        stun = Passive("❄️Заморозка", bash, undo_bash, 3, 1, apply_once=True)

        enemy.add_passive(stun)

        gif = 'CgACAgIAAx0CfstymgACC9VmArOmFW2UktJMe5UVcdw_EVP3ywACIUEAAjWZGEhwP4MJgfBpRjQE'
        caption = (f"❄️Рокуи Хёкецу "
                   f"\n❄️Замарозка 1⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌫Тенсо Джурин˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        defense_down = Passive("⇩🛡⇩", decrease_defense, fix_effects, 20, 10)
        agility_down = Passive("⇩👣⇩", decrease_agility, fix_effects, 20, 5)

        enemy.add_passive(defense_down)
        enemy.add_passive(agility_down)

        gif = 'CgACAgIAAx0CfstymgACC7Rl_rLFBP-evK5ZB1gxTlZyku5ZqgACMUEAAr968Utj5nMkb3VDmTQE'
        caption = (f"🌫Тенсо Джурин"
                   f"\n\n⇩🛡⇩ -10 защ. противника 20⏳"
                   f"\n⇩👣⇩ -5 лвк. противника 20⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🐉Хёринмару˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        dragon = Passive("🐉", decrease_hp, fix_effects, 3, self.intelligence * 3)

        enemy.add_passive(dragon)

        gif = 'CgACAgIAAx0CfstymgACC8hmAppm1k9qPHl9_a3xf6Tj9i_X6wACDUAAAjWZGEj9QF5SvD-6xjQE'
        caption = (f"🐉Хёринмару"
                   f"\n\n🐉Ледяной дракон ─ 🗡{self.intelligence * 3} 3⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹❄️Синку но Кори˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.attack // 2 + self.intelligence + self.strength + self.agility

        stun = Passive("❄️Заморозка", bash, undo_bash, 3, 1)
        defense_down = Passive("⇩🛡⇩", decrease_defense, increase_defense, 3, 25)

        enemy.add_passive(stun)
        enemy.add_passive(defense_down)

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC8xmAqIL3VyHxOHaEt8GkmnWS629rgACWkAAAjWZGEgtDq4VnBawUDQE'
        caption = (f"❄️Синку но Кори"
                   f"\n\nТоширо нанес {damage} 🗡 урона"
                   f"\n❄️Замарозка 3⏳"
                   f"\n⇩🛡⇩ -25 защ. противника 3⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🧊Рёджин Хёхеки˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        self.shield += self.intelligence * 10

        gif = 'CgACAgIAAx0CfstymgACC9FmAqmtGKYDbv8qs2m9CDUDjUu0DAACpUAAAjWZGEiSD0D15ioK0zQE'
        caption = (f"🧊Рёджин Хёхеки"
                   f"\n\n🧊 Ледяная стена ─ +{self.intelligence * 10}🌐 Щит")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹❆Дайгурен🪽Хёринмару˼':
        mana = await calculate_mana(self, 65)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 40)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹❤️‍🩹Лечение🪽˼", "˹🧊Рюсенька˼", "˹🧊Сеннен Хёро˼",
                      "˹❄️Гунчо Цурара˼", "˹🌫Хётен🪽Хяккасо˼", "˹❄️Хёрю Сенби˼"]
        skills_change = Passive("Банкай 🪽", change_skills, undo_change_skills, 20, new_skills)
        attack_up = Passive("⇪🗡⇪", increase_attack, decrease_attack, 5, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)

        gif = 'CgACAgIAAx0CfstymgACC9lmArelFbpDJmVZoG6SfaaaQ4yO8gACVUEAAjWZGEgIRJjtP0Il-jQE'
        caption = (f"Банкай ❆: Дайгурен Хёринмару"
                   f"\n\n🗡Урон +200 5⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹❤️‍🩹Лечение🪽˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        healing = (self.strength + self.intelligence) * 5

        self.health += healing

        gif = 'CgACAgIAAx0CfstymgACC-FmBAbx3J4kOqwFhs9vSNT1xY1JVAACcEYAAoZPIEhqQCLHc865fDQE'
        caption = (f"Восстановление"
                   f"\n\n+{healing}❤️ hp")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🧊Рюсенька˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = (self.attack + self.intelligence + self.strength + self.agility) * 2

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC-1mBOFg7B3TgN3Fe77w4FWefUPsBgACDUsAAoZPIEgP_-MC0jP7PDQE'
        caption = (f"Рюсенька"
                   f"\n\nТоширо нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🧊Сеннен Хёро˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack

        stun = Passive("🧊Дизейбл", bash, undo_bash, 4, 1)

        enemy.add_passive(stun)

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC-xmBOFavairOTLhjlyAl-Pu04wkQwACDEsAAoZPIEgbMqG7fJ1gaDQE'
        caption = (f"Сеннен Хёро"
                   f"\n\nТоширо нанес {damage} 🗡 урона"
                   f"\n🧊Дизейбл 4⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹❄️Гунчо Цурара˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        damage = (self.attack + self.intelligence + self.strength + self.agility) * 4

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC-lmBOFDZq-98wrU7DajX5-utwhIlwACBEsAAoZPIEjGGiJsVwPCKjQE'
        caption = (f"Синку но Кори"
                   f"\n\nТоширо нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌫Хётен🪽Хяккасо˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        damage = self.attack + self.intelligence + self.strength + self.agility

        stun = Passive("🧊Дизейбл", bash, undo_bash, 5, 1)
        attack = Passive("Хётен Хяккасо", decrease_hp, fix_effects, 5, damage)

        enemy.add_passive(stun)
        enemy.add_passive(attack)

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC-tmBOFSNR61cUUt0t53RS0sPN9-tgACC0sAAoZPIEgNwZMu0q6GtzQE'
        caption = (f"Хётен Хяккасо"
                   f"\n\n🧊Дизейбл 5⏳"
                   f"\n❄️Хётен Хяккасо {damage}🗡 5⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹❄️Хёрю Сенби˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False

        damage = (self.attack + self.intelligence + self.strength + self.agility) * 10

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC-pmBOFLN3i2uFuQTnn7N8EWo2JaewACBUsAAoZPIEistatyBH8IHDQE'
        caption = (f"Хёрю Сенби Зекку"
                   f"\n\nТоширо нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Aizen Sousuke

    elif action == '˹Данку˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False
        hp = self.pre_hp - self.health
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACEAdmH0jevycWW8JRoi1P5mXHsKKUIAAC5jcAAkXDAAFJSWPSJfynz6w0BA'
        caption = (f"Хадо #81 Данку"
                   f"\n\nАйзен блокировал {hp} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹⚡️Райхоко˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8JmHz-7RxoM5Cy7osaNS91GlqovVwACoUUAA9zYSEvATkwOWQvwNAQ'
        caption = (f"Хадо #63 ⚡️Райхоко"
                   f"\n\nАйзен нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🔶Мильон Эскудо˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False
        hp = self.pre_hp - self.health

        block = Passive("🪞", block_hp, fix_effects, 1, hp, apply_once=True)
        self.add_passive(block)

        calculate_shield(enemy, hp)

        gif = 'CgACAgIAAx0CfstymgACD8BmHz9000pc48CLJIiGlTCTa_WpswACrTcAAkXDAAFJ9MpYhplmZGw0BA'
        caption = (f"🔶Мильон Эскудо"
                   f"\n\nАйзен блокировал и нанес {hp} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹◼️Курохицуги˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = self.attack * 4 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8NmHz-7x6Zz8uVMrbU2Lvm-IepPRAACEEYAA9zYSBvlrcaxfeYrNAQ'
        caption = (f"Хадо #90 ◼️Курохицуги"
                   f"\n\nАйзен нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🐉Горьюу Теммецу˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False

        dragon = Passive("🐉", decrease_hp, fix_effects, 5, self.intelligence * 6)

        enemy.add_passive(dragon)

        gif = 'CgACAgIAAx0CfstymgACD8VmHz-7iRGASjkV8HrZRq4fjalL5gACh0YAA9zYSPSqspK-7kLKNAQ'
        caption = (f"Хадо #99 Горьюу Теммецу"
                   f"\n\n🐉Вихревые драконы ─ 🗡{self.intelligence * 6} 5⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹⬛️Курохицуги˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = self.attack * 10 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8RmHz-7pWskknJCngtdfjuWYctsdAACVkYAA9zYSBMfNH3F4RXDNAQ'
        caption = (f"Хадо #90 ⬛️Курохицуги"
                   f"\n\nАйзен нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🟣Фрагор˼':
        damage = self.attack * 50 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD75mHz8MQpJnkKdAjdvLxphn3gU2sAACqzcAAkXDAAFJ6Prn_DkXPsk0BA'
        caption = (f"🟣Фрагор"
                   f"\n\nАйзен нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Urahara Kisuke

    elif action == '˹Хаинава˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack // 4
        stun = Passive("💫", bash, undo_bash, 1, 1, apply_once=True)

        enemy.add_passive(stun)
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD91mH6wGmjSsSiDvYL1dZQQ8N1eypgACyTcAAkXDAAFJ76h9EQuWqyc0BA'
        caption = (f"Бакудо #4 Хаинава"
                   f"\n\nУрахара нанес {damage} 🗡 урона"
                   f"💫Оглушение 1⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Цурибоши˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack // 3
        stun = Passive("💫", bash, undo_bash, 1, 1, apply_once=True)

        enemy.add_passive(stun)
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD95mH6wnU7d0bBy1Nv12kgOrWS4tIAACyjcAAkXDAAFJIZudXnjXTfs0BA'
        caption = (f"Бакудо #37 Цурибоши"
                   f"\n\nУрахара нанес {damage} 🗡 урона"
                   f"💫Оглушение 1⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Саджо Сабаку˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack // 2
        stun = Passive("💫", bash, undo_bash, 1, 1, apply_once=True)

        enemy.add_passive(stun)
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD91mH6wGmjSsSiDvYL1dZQQ8N1eypgACyTcAAkXDAAFJ76h9EQuWqyc0BA'
        caption = (f"Бакудо #63 Саджо Сабаку"
                   f"\n\nУрахара нанес {damage} 🗡 урона"
                   f"💫Оглушение 1⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Гочью Теккан˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack
        stun = Passive("💫", bash, undo_bash, 3, 1, apply_once=True)

        enemy.add_passive(stun)
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD-BmH6xVlpzPPIGfNeL14xwaGv19cAACzDcAAkXDAAFJreAq68JLIs80BA'
        caption = (f"Бакудо #75 Гочью Теккан"
                   f"\n\nУрахара нанес {damage} 🗡 урона"
                   f"💫Оглушение 2⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Джугеки Бьякурай˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 5 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9NmH2FzA0xXKiGWNuhQb7soYUfyZQACvDcAAkXDAAFJbF6l8QMxhf80BA'
        caption = (f"Джугеки Бьякурай"
                   f"\n\nУрахара нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Окасен˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 6 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9VmH2LkCz4q5Ikf69MreHppyOD02gACvjcAAkXDAAFJS0yJhugsU5M0BA'
        caption = (f"Хадо #32 Окасен"
                   f"\n\nУрахара нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Хайхен˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 4 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9tmH2X9To9mil3tn8mvvW3V3cRqgAACxzcAAkXDAAFJzYJxNJjvge80BA'
        caption = (f"Хадо #54 Хайхен"
                   f"\n\nУрахара нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Фусатсу Какеи˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 30)
        if not energy:
            return True, False

        damage = (enemy.strength + enemy.intelligence + enemy.agility + self.intelligence) * 2
        burning = Passive("🔥", decrease_hp, fix_effects, 5, damage)

        enemy.add_passive(burning)

        gif = 'CgACAgIAAx0CfstymgACEAtmH1GwGy0NkdFCKTc26FBF6I6OmAACHTgAAkXDAAFJDnElH4dR4ow0BA'
        caption = (f"Фусатсу Какеи"
                   f"\n\n🔥Жжение изнутри ─ 🗡{damage} 5⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Какафумецу˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False
        stun = Passive("Печать", bash, undo_bash, 2, 1, apply_once=True)
        enemy.add_passive(stun)

        gif = 'CgACAgIAAx0CfstymgACD9dmH2ZlZLnUmXy9xzqlvMIOEtpLHwACwDcAAkXDAAFJHKExH1vAs1c0BA'
        caption = (f"Кьюджюроккей Какафумецу"
                   f"\n\n"
                   f"\nПечать 5⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Данку ˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False
        hp = self.pre_hp - self.health
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACD-JmIIUBYifLHlxjtlDL84xAij0h-wACzjcAAkXDAAFJHCuuszBp6tU0BA'
        caption = (f"Хадо #81 Данку"
                   f"\n\nУрахара блокировал {hp} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Бенхиме˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹Наке Бенхиме˼", "˹Чикасуми но тате˼", '˹Шинтен Райхо˼', '˹Котен Тайхо˼',
                      "˹Камисори Бенхиме˼", "˹Шибари Бенхиме˼", "˹🪡Бенхиме Аратаме˼"]
        skills_change = Passive("Банкай ࿖", change_skills, undo_change_skills, 10, new_skills)
        attack_up = Passive("⇪🗡⇪", increase_attack, decrease_attack, 10, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)

        gif = 'CgACAgIAAx0CfstymgACEBtmH2kiAyY6VX5-kxc1JDL6ElLxogACyjgAAkXDAAFJCyOIbv_PK7o0BA'
        caption = (f"Шикай: Бенхиме"
                   f"\n\n🗡Урон +200 10⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Наке Бенхиме˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 3 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD-FmH2nUweMLP1MifHPDGFzHquv8ZgACzTcAAkXDAAFJJOQ8tyUGiCw0BA'
        caption = (f"Наке Бенхиме"
                   f"\n\nУрахара нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Чикасуми но тате˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False
        hp = self.pre_hp - self.health

        block = Passive("🪞", block_hp, fix_effects, 1, hp, apply_once=True)
        self.add_passive(block)

        calculate_shield(enemy, hp)

        gif = 'CgACAgIAAx0CfstymgACD9pmH2oPhr2JX6HZqcxufZDX1lUrdQACwzcAAkXDAAFJRxsJjn8M1Ms0BA'
        caption = (f"Чикасуми но тате"
                   f"\n\nУрахара блокировал и нанес {hp} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Шинтен Райхо˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 6 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9xmH6qmgOptrihj1rlsclKz6szoiQACyDcAAkXDAAFJYjsNaNiAxD80BA'
        caption = (f"Хадо #88 Хирю Гекузоку Шинтен Райхо"
                   f"\n\nУрахара нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Котен Тайхо˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 10 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9lmH2V61lVXDYwf4mxthNn0nozwoAACwjcAAkXDAAFJrw1dl3Vlb3k0BA'
        caption = (f"Хадо #91 Сенджу Котен Тайхо"
                   f"\n\nУрахара нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Камисори Бенхиме˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 4 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9hmH2o6yOPXwNlbMlx0HDLW5YDvngACwTcAAkXDAAFJOcUqETV9sX40BA'
        caption = (f"Камисори Бенхиме"
                   f"\n\nУрахара нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Шибари Бенхиме˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 5 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9ZmH2pl3a6dY9UV0agd60h41nLMiAACvzcAAkXDAAFJlkO3COVHqBc0BA'
        caption = (f"Шибари Бенхиме"
                   f"\n\nУрахара нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🪡Бенхиме Аратаме˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False

        heal = Passive("❤️", increase_hp, fix_effects, 5, self.intelligence * 5)
        block = Passive("🪡", block_hp, fix_effects, 5, 1)
        attack = Passive("🪡", decrease_hp, fix_effects, 5, self.intelligence * 5)
        im = Passive("🪽", immunity, fix_effects, 5, 1, apply_once=True)
        self.add_passive(im)
        self.add_passive(heal)
        self.add_passive(block)
        enemy.add_passive(attack)

        gif = 'CgACAgIAAx0CfstymgACD3ZmH2uFV-s36WQ5RmiWZqQF3X9ZFgACpUcAAlhE8Eiz1NElbTRwCTQE'
        caption = (f"Бенхиме Аратаме"
                   f"\n\n❤️Лечение ─ + ❤️{self.intelligence * 5} 5⏳"
                   f"\n🪡Постоянно шьет раны делая себя неуязвимым 5⏳"
                   f"\n🪡Постоянно перекраиваеть тела противника вскрывая его 5⏳"
                   f"\n💥невосприимчивый контроли 5⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Unohana Retsu

    elif action == '˹Хяппоранкан˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack // 2
        stun = Passive("💫", bash, undo_bash, 1, 1, apply_once=True)

        enemy.add_passive(stun)
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD-hmIIKiR6GyelhLQZGwMlojlLV-JAAC1DcAAkXDAAFJrvPpYNIEMKE0BA'
        caption = (f"Бакудо #62 Хяппоранкан"
                   f"\n\nУнохана нанесла {damage} 🗡 урона"
                   f"💫Оглушение 1⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Саджосабаку˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack // 2 + self.intelligence
        stun = Passive("💫", bash, undo_bash, 1, 1, apply_once=True)

        enemy.add_passive(stun)
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD-VmIILW285qDQSyhi04Ymt-ccqYcwACSkkAAoxtAUkv6QewQEmrhzQE'
        caption = (f"Бакудо #63 Саджосабаку"
                   f"\n\nУнохана нанесла {damage} 🗡 урона"
                   f"💫Оглушение 1⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Гочью Теккан ˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence
        stun = Passive("💫", bash, undo_bash, 3, 1, apply_once=True)

        enemy.add_passive(stun)
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD-lmH7bSl9akeM8k6Ss7ufuetXRaKQAC1TcAAkXDAAFJ3cn905-zbo40BA'
        caption = (f"Бакудо #75 Гочью Теккан"
                   f"\n\nУнохана нанесла {damage} 🗡 урона"
                   f"💫Оглушение 2⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹ Данку ˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False
        hp = self.pre_hp - self.health
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACD-dmIIWr0NQGRJreCKZ6jaZNyIgztQAC0zcAAkXDAAFJQ7sL5Gzp7Uo0BA'
        caption = (f"Хадо #81 Данку"
                   f"\n\nУнохана блокировала {hp} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🐋 Миназуки˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        hp = self.intelligence * 3

        scot = Passive("🐋", increase_hp, fix_effects, 5, hp)

        self.add_passive(scot)

        gif = 'CgACAgIAAx0CfstymgACD-tmII2gqdYCNJNLwBxYNy2f-IafxQAC1zcAAkXDAAFJVOIyI0vIU7o0BA'
        caption = (f"Шикай: Миназуки"
                   f"\n\n🐋 Лечение ─ ❤️{hp} 5⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🧊 Щит ˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        shield = self.intelligence * 15
        self.shield += shield

        gif = 'CgACAgIAAx0CfstymgACD-pmII7cPB4_OlHZ3p63QMyNQfqTmQAC1jcAAkXDAAFJwHh-XhQ2rH80BA'
        caption = (f"🧊 Щит"
                   f"\n\n🧊 ─  +{shield}🌐 Щит")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Шинтен Райхо ˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 6 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD-ZmIIRPb0DpjBthdU8MX9nCJ-6oUAAC0jcAAkXDAAFJDJFVxK81rNY0BA'
        caption = (f"Хадо 88 Хирю Гекузоку Шинтен Райхо"
                   f"\n\nУнохана нанесла {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Миназуки 🩸˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹Лечение🩸˼", "˹Лезвие🩸˼", "˹Защитная сфера🩸˼"]
        skills_change = Passive("🩸", change_skills, undo_minazuki, 20, new_skills)
        attack_up = Passive("⇪🗡⇪", increase_attack, decrease_attack, 20, 400, apply_once=True)
        agility_up = Passive("⇪👣⇪", increase_agility, decrease_agility, 20, 200, apply_once=True)
        strength_up = Passive("⇪✊🏻⇪", increase_strength, decrease_strength, 20, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)
        self.add_passive(agility_up)
        self.add_passive(strength_up)

        gif = 'CgACAgIAAx0CfstymgACD-xmIIezCd3-a2Ek84w5VsAXFGinmwAC2DcAAkXDAAFJ5Zi36HeBGK00BA'
        caption = (f"Миназуки Банкай🩸"
                   f"\n\n🗡Урон +400 10⏳"
                   f"\n👣Ловкость +200 10⏳"
                   f"\n✊🏻Сила +200 10⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Лечение🩸˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False
        hp = self.intelligence * 6
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACD-1mIIqmBocH4hZNYN5NTIO2MoZ6swAC2TcAAkXDAAFJii0kD3uJgRE0BA'
        caption = (f"Восстановление"
                   f"\n\n❤️Лечение ─ + ❤️{hp}")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Лезвие🩸˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False
        damage = self.attack + self.strength * 2
        calculate_shield(enemy, damage * 3)

        gif = 'CgACAgIAAx0CfstymgACEF9mIIs1edgNVzBSCr8SK5Es9d9s7wAC5UYAAkXDCEn4R-hkPI10RzQE'
        caption = (f"Лезвие🩸"
                   f"\n\nУнохана нанесла {damage}x3 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Защитная сфера🩸˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False
        hp = self.pre_hp - self.health
        attack = self.attack * 3

        block = Passive("🪞", block_hp, fix_effects, 1, hp, apply_once=True)
        self.add_passive(block)

        calculate_shield(enemy, attack)

        gif = 'CgACAgIAAx0CfstymgACD-5mIJBWsTfgCjqU92QsX3d_KSG69QAC2jcAAkXDAAFJBFo7StF3My80BA'
        caption = (f"Защитная сфера🩸˼"
                   f"\n\nУнохана блокировала {hp} 🗡 урона"
                   f"\nИ нанесла {attack} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Ulquiorra scifer

    elif action == '˹Серо˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8dmH7whDVX42I55DqsYKAkelDoCSwACrjcAAkXDAAFJtqCbWeaufuA0BA'
        caption = (f"Серо"
                   f"\n\nУлькиорра нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Мурсьелаго 🦇˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹Гран Рей Серо˼", "˹Луз дэ ла Луна˼", "˹Сэгунда Этапа 🦇˼"]
        skills_change = Passive("🦇", change_skills, undo_change_skills, 10, new_skills)
        attack_up = Passive("⇪🗡⇪", increase_attack, decrease_attack, 10, 200, apply_once=True)
        agility_up = Passive("⇪👣⇪", increase_agility, decrease_agility, 10, 100, apply_once=True)
        strength_up = Passive("⇪✊🏻⇪", increase_strength, decrease_strength, 10, 100, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)
        self.add_passive(agility_up)
        self.add_passive(strength_up)

        gif = 'CgACAgIAAx0CfstymgACD8hmH8rOTwAB4OuK07Jbyh966mMDUnQAAq83AAJFwwABSfYOi7l9klFpNAQ'
        caption = (f"Мурсьелаго 🦇"
                   f"\n\n🗡Урон +200 10⏳"
                   f"\n👣Ловкость +100 10⏳"
                   f"\n✊🏻Сила +100 10⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Гран Рей Серо˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = self.attack * 2 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8dmH7whDVX42I55DqsYKAkelDoCSwACrjcAAkXDAAFJtqCbWeaufuA0BA'
        caption = (f"Гран Рей Серо"
                   f"\n\nУлькиорра нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Луз дэ ла Луна˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        damage = (self.attack + self.intelligence + self.strength + self.agility) * 3
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8lmH8bvr11Ul2Hg0S44JxWO9DTBKQACsDcAAkXDAAFJHwpiKkkIM6Y0BA'
        caption = (f"Луз дэ ла Луна"
                   f"\n\nУлькиорра нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Сэгунда Этапа 🦇˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹Латиго˼", "˹Серо Оскурас˼", "˹Ланза дэль Рэлампаго˼", "˹Лечение ˼"]
        skills_change = Passive("🦇", change_skills, undo_change_skills, 10, new_skills)
        attack_up = Passive("⇪🗡⇪", increase_attack, decrease_attack, 10, 400, apply_once=True)
        agility_up = Passive("⇪👣⇪", increase_agility, decrease_agility, 10, 200, apply_once=True)
        strength_up = Passive("⇪✊🏻⇪", increase_strength, decrease_strength, 10, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)
        self.add_passive(agility_up)
        self.add_passive(strength_up)

        gif = 'CgACAgIAAx0CfstymgACEEtmH_ueh2NqxoTZ_KnWCTRHN6LVVQACwkAAAkXDAAFJpRvMV5DKE7Y0BA'
        caption = (f"Сэгунда Этапа 🦇"
                   f"\n\n🗡Урон +400 10⏳"
                   f"\n👣Ловкость +200 10⏳"
                   f"\n✊🏻Сила +200 10⏳")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Латиго˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8pmH8E6nQZVWZu9GDPqkFa1P-ZuBAACsjcAAkXDAAFJxhp_ox-JR040BA'
        caption = (f"Латиго"
                   f"\n\nУлькиорра нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Серо Оскурас˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = (self.attack + self.intelligence + self.strength + self.agility) * 2
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD81mH8gHfBd1aMZm2MBu6Dmtfj88oAACtzcAAkXDAAFJR62LOrhWBL80BA'
        caption = (f"Серо Оскурас"
                   f"\n\nУлькиорра нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Ланза дэль Рэлампаго˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False
        damage = (self.attack + self.intelligence + self.strength + self.agility) * 6
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD85mH8cIcMxuDdMJyoJgJUGxqMK95gACuDcAAkXDAAFJeq-VqqzVpkU0BA'
        caption = (f"Ланза дэль Рэлампаго"
                   f"\n\nУлькиорра нанес {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹Лечение ˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False
        hp = self.intelligence * 5
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACD9ZmH8e3t2ZpN6ZLzZ8Z5eQ3h2ZoWQACtzcAAkXDAAFJ8Qp1Z7Qp7U0BA'
        caption = (f"Восстановление"
                   f"\n\n❤️Лечение ─ + ❤️{hp}")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# After death

    if self.health <= 0:

        # Ichigo Kurosaki

        if self.name.startswith('Ichigo Kurosaki') and self.immortal <= 0:
            self.immortal += 1
            self.ability = ['˹🗡Атака˼', "˹☄️Гран Рей Серо˼"]
            im = Passive("💥", immunity, undo_immunity, 5, 1, apply_once=True)
            immortal = Passive("💀Финальный пустой🕳", increase_hp, decrease_hp, 5, 10000, apply_once=True)
            self.add_passive(Passive("💀Финальный пустой🕳", fix_effects, undo_hollow, 5, bot, apply_once=True))
            self.add_passive(immortal)
            self.add_passive(im)

            gif = 'CgACAgIAAx0CfstymgACC1Nl_ISertvi3kRMGCiNOeD1ce9EFgACLFAAAuZv4Uv5LK0AAQPBEzQ0BA'
            caption = (f"💀Финальный пустой🕳 "
                       f"\n\n+ 10000❤️ hp 5⏳"
                       f"\n💥невосприимчивый контроли 5⏳")

            await send_action(bot, self, enemy, chat_id, gif, caption)

        # Aizen Sousuke

        elif self.name.startswith('Aizen Sosuke') and self.immortal <= 0:
            self.immortal += 1
            self.attack += 300
            self.health += 8000
            self.ability = ['˹🗡Атака˼', "˹⬛️Курохицуги˼"]
            im = Passive("🪽", immunity, fix_effects, 5, 1, apply_once=True)
            self.add_passive(im)

            gif = 'CgACAgIAAx0CfstymgACD7tmH6hUhd8QiNsOtxxRNbvK6H9rvgACpEcAAlhE8EgDvFQ_5qQwNDQE'
            caption = (f"🪽Вторая стадия"
                       f"\n\n+ 8000❤️ hp"
                       f"\n+ 300🗡 атаки"
                       f"\n💥невосприимчивый контроли")

            await send_action(bot, self, enemy, chat_id, gif, caption)

        elif self.name.startswith('Aizen Sosuke') and self.immortal == 1:
            self.immortal += 1
            self.ability = ['˹🗡Атака˼', "˹🟣Фрагор˼"]
            im = Passive("👿", immunity, fix_effects, 5, 1, apply_once=True)
            immortal = Passive("👿третья стадия", increase_hp, decrease_hp, 5, 10000, apply_once=True)
            self.add_passive(Passive("👿третья стадия", fix_effects, undo_second, 5, bot, apply_once=True))
            self.add_passive(immortal)
            self.add_passive(im)

            gif = 'CgACAgIAAx0CfstymgACC1Nl_ISertvi3kRMGCiNOeD1ce9EFgACLFAAAuZv4Uv5LK0AAQPBEzQ0BA'
            caption = (f"👿третья стадия"
                       f"\n\n+ 10000❤️ hp 5⏳"
                       f"\n💥невосприимчивый контроли")

            await send_action(bot, self, enemy, chat_id, gif, caption)

# Slaves effect

    if self.slave:
        self.passive_names.append(self.slave)
        result = character_photo.slaves_stats(self.slave)
        clas = result[3]
        if clas == 'heal':
            if self.health > 0:
                self.health += result[2]
        elif clas == 'attack':
            damage = result[2]
            calculate_shield(enemy, damage)

# After action

    if enemy.health <= 0:
        enemy.health = 0

    if enemy.immunity:
        enemy.stun = 0

    self.update_passives()
    self.energy += 5
    enemy.update_passives()
    enemy.energy += 5

    return True, True
