import asyncio
import inspect
import random

from data import character_photo
# from data.default import caption


async def send_action(bot, self, enemy, chat_id, gif, text, ai=None):
    if self.chat_id == 0:
        if not ai:
            await bot.send_animation(chat_id=self.ident, animation=gif, caption=text)
            if enemy.ident != self.ident * 10:
                await bot.send_animation(chat_id=enemy.ident, animation=gif, caption=text)
        else:
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


def increase_energy(player, points):
    player.energy += points


def decrease_energy(player, points):
    player.energy -= points


# def return_energy(player, points):
#     player.energy = player.initial.energy


def increase_mana(player, points):
    player.mana += points


def decrease_mana(player, points):
    player.mana -= points


# def return_mana(player, points):
#     player.mana = player.initial_mana


def increase_hp(player, points):
    player.health += points


def decrease_hp(player, points):
    player.health -= points


def return_hp(player, _):
    hp = player.pre_hp - player.health
    player.health += hp


def return_half_hp(player, _):
    hp = player.pre_hp - player.health
    player.health += hp // 2


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


def increase_intelligence(player, points):
    player.intelligence += points


def decrease_intelligence(player, points):
    player.intelligence -= points


def return_intelligence(player, _):
    player.intelligence = player.initial_intelligence


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
    text = "<blockquote expandable>⊛ Ичиго заполучил сила Квинси</blockquote>"
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
        self.initial_intelligence = self.intelligence
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


async def turn(self, bot, action, enemy, chat_id, ai=None):

    self.crit_dmg = self.strength + self.attack - (enemy.strength // 4) + (self.intelligence // 4)
    self.crit_ch = self.agility - (enemy.agility + enemy.intelligence // 4) + (self.intelligence // 4)
    enemy.pre_hp = enemy.health

    if action == '˹🗡Атака˼':
        chance = calculate_critical_chance(self.crit_ch)
        damage, msg = calculate_critical_damage(self.attack, self.crit_dmg, chance)

        calculate_shield(enemy, damage)

        if chat_id == 0:
            if not ai:
                await bot.send_message(self.ident, f"˹{self.name} нанес(ла) {damage} {msg} 🗡 урона˼")
                if enemy.ident != self.ident * 10:
                    await bot.send_message(enemy.ident, f"˹{self.name} нанес(ла) {damage} {msg} 🗡 урона˼")
            else:
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
                   f"\n<blockquote expandable>Ичиго нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹◽️Поступь˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.strength
        self.health += self.strength

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC3dl_Vz2TTu7KeI--jvzfvKFElSg9wAC2EgAAv0v8EtdmGJdFwkcUDQE'
        caption = (f"◽️Поступь"
                   f"\n<blockquote expandable>Ичиго нанес {damage} 🗡 урона"
                   f"\n + {self.strength}❤️ hp</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Ичиго нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹◾️Тенса࿖Зангецу˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹🟥Гецуга◼️Теншоу˼", "˹💀Пустой˼"]
        skills_change = Passive("Банкай ࿖", change_skills, undo_change_skills, 8, new_skills)
        attack_up = Passive("⇪🗡", increase_attack, decrease_attack, 8, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)

        gif = 'CgACAgIAAx0CfstymgACCzZl8T9WLPOCuQG34Qcjn4xCiP6KXAACWD8AAvSEkUtsDKXUVPoFeTQE'
        caption = (f"Банкай ࿖: Tensa Zangetsu"
                   f"\n<blockquote expandable>🗡Урон ⇪200 8⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🟥Гецуга◼️Теншоу˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence + self.strength + self.agility

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC29l_VY2zFxjirZIIdOwlfhygw05rwACjEgAAv0v8EuhD_HwUkIBHzQE'
        caption = (f"Гецуга Теншоу"
                   f"\n<blockquote expandable>Ичиго нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>  ✊🏻Сила +100 5⏳"
                   f"\n  👣Лвк +100 5⏳"
                   f"\n🗡Автоатака 100🗡 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🟥Гецуга Теншоу˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACCyxl8SWxVYrXROiEsZDYy1xJ1czIDAACKEkAAvSEiUtyJh4oGxC1tzQE'
        caption = (f"Гецуга Теншоу"
                   f"\n<blockquote expandable>Ичиго нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹◾️Финал⛓Гецуга◾️˼':
        energy = await calculate_energy(self, 55)
        if not energy:
            return True, False

        new_skills = ["˹◾️⛓Мугецу⛓◾️˼"]
        skills_change = Passive("⛓Гецуга◾️", change_skills, undo_change_skills, 3, new_skills, apply_once=True)
        im = Passive("💥", immunity, undo_immunity, 3, 1, apply_once=True)
        over_g = Passive("⛓Гецуга◾️", fix_effects, undo_g, 3, bot, apply_once=True)
        defense_up = Passive("⇪🛡", increase_defense, fix_effects, 3, 900, apply_once=True)
        attack_up = Passive("⇪🗡", increase_attack, fix_effects, 3, 1000, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(over_g)
        self.add_passive(defense_up)
        self.add_passive(attack_up)
        enemy.add_passive(im)

        gif = 'CgACAgIAAx0CfstymgACC4ll_c3Iv9lZgb5gNHy_i9vCDgcs3AACBU8AAv0v8EuVgi04yq7GzjQE'
        caption = (f"Финальная Гецуга Теншоу"
                   f"\n<blockquote expandable>🗡Атака ⇪1000 2⏳"
                   f"\n🛡Защита ⇪900 2⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹◾️⛓Мугецу⛓◾️˼':
        damage = self.attack * 4
        enemy.health -= damage

        gif = 'CgACAgIAAx0CfstymgACC4Bl_WxyumX77FXeGkcaaKF6ZIhWwAACh0kAAv0v8Evl3Ud_DK97oDQE'
        caption = (f"Мугецу"
                   f"\n<blockquote expandable>Ичиго нанес {damage} 🗡 чистого урона"
                   f"\n💥невосприимчивый контроли</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Ичиго нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹☄️Гран Рей Серо˼':
        damage = self.attack * 3 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC7ll_ttMnKMi5xOFBHaZfm9HDyfaVgACzEYAAr96-UuNLgc1LY6fDzQE'
        caption = (f"Гран Рей Серо"
                   f"\n<blockquote expandable>Ичиго нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

# Toshiro Hitsugaya

    elif action == '˹❄️Хёкецу˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack // 2 + self.intelligence + self.strength + self.agility

        stun = Passive("❄️Заморозка", bash, undo_bash, 2, 1, apply_once=True)

        enemy.add_passive(stun)

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACC_lmBPL3pSbME9k2QgfKNG4cpCnxHQACtz0AAu4mKEh95WRm0QiIljQE'
        caption = (f"❄️Хёкецу "
                   f"\n<blockquote expandable>Тоширо нанес {damage} 🗡 урона"
                   f"\n❄️Замарозка 1⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹❄️Рокуи Хёкецу˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        stun = Passive("❄️Заморозка", bash, undo_bash, 3, 1, apply_once=True)

        enemy.add_passive(stun)

        gif = 'CgACAgIAAx0CfstymgACC9VmArOmFW2UktJMe5UVcdw_EVP3ywACIUEAAjWZGEhwP4MJgfBpRjQE'
        caption = (f"❄️Рокуи Хёкецу "
                   f"\n<blockquote expandable>❄️Замарозка 1⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>⇩🛡⇩ -10 защ. противника 20⏳"
                   f"\n⇩👣⇩ -5 лвк. противника 20⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>🐉Ледяной дракон ─ 🗡{self.intelligence * 3} 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹❄️Синку но Кори˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
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
                   f"\n<blockquote expandable>Тоширо нанес {damage} 🗡 урона"
                   f"\n❄️Замарозка 3⏳"
                   f"\n⇩🛡⇩ -25 защ. противника 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>🧊 Ледяная стена ─ +{self.intelligence * 10}🌐 Щит</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
        attack_up = Passive("⇪🗡", increase_attack, decrease_attack, 5, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)

        gif = 'CgACAgIAAx0CfstymgACC9lmArelFbpDJmVZoG6SfaaaQ4yO8gACVUEAAjWZGEgIRJjtP0Il-jQE'
        caption = (f"Банкай ❆: Дайгурен Хёринмару"
                   f"\n<blockquote expandable>🗡Урон ⇪200 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>+{healing}❤️ hp</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Тоширо нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Тоширо нанес {damage} 🗡 урона"
                   f"\n🧊Дизейбл 4⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Тоширо нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>🧊Дизейбл 5⏳"
                   f"\n❄️Хётен Хяккасо {damage}🗡 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Тоширо нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Айзен блокировал {hp} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹⚡️Райхоко˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8JmHz-7RxoM5Cy7osaNS91GlqovVwACoUUAA9zYSEvATkwOWQvwNAQ'
        caption = (f"Хадо #63 ⚡️Райхоко"
                   f"\n<blockquote expandable>Айзен нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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

        calculate_shield(enemy, hp // 2)

        gif = 'CgACAgIAAx0CfstymgACD8BmHz9000pc48CLJIiGlTCTa_WpswACrTcAAkXDAAFJ9MpYhplmZGw0BA'
        caption = (f"🔶Мильон Эскудо"
                   f"\n<blockquote expandable>Айзен блокировал и нанес {hp // 2} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹◼️Курохицуги˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = self.attack * 4 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8NmHz-7x6Zz8uVMrbU2Lvm-IepPRAACEEYAA9zYSBvlrcaxfeYrNAQ'
        caption = (f"Хадо #90 ◼️Курохицуги"
                   f"\n<blockquote expandable>Айзен нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>🐉Вихревые драконы ─ 🗡{self.intelligence * 6} 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹⬛️Курохицуги˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = self.attack * 10 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8RmHz-7pWskknJCngtdfjuWYctsdAACVkYAA9zYSBMfNH3F4RXDNAQ'
        caption = (f"Хадо #90 ⬛️Курохицуги"
                   f"\n<blockquote expandable>Айзен нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🟣Фрагор˼':
        damage = self.attack * 50 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD75mHz8MQpJnkKdAjdvLxphn3gU2sAACqzcAAkXDAAFJ6Prn_DkXPsk0BA'
        caption = (f"🟣Фрагор"
                   f"\n<blockquote expandable>Айзен нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона"
                   f"💫Оглушение 1⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона"
                   f"💫Оглушение 1⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона"
                   f"💫Оглушение 1⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона"
                   f"💫Оглушение 2⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Джугеки Бьякурай˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 5 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9NmH2FzA0xXKiGWNuhQb7soYUfyZQACvDcAAkXDAAFJbF6l8QMxhf80BA'
        caption = (f"Джугеки Бьякурай"
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Окасен˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 6 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9VmH2LkCz4q5Ikf69MreHppyOD02gACvjcAAkXDAAFJS0yJhugsU5M0BA'
        caption = (f"Хадо #32 Окасен"
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Хайхен˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 4 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9tmH2X9To9mil3tn8mvvW3V3cRqgAACxzcAAkXDAAFJzYJxNJjvge80BA'
        caption = (f"Хадо #54 Хайхен"
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>🔥Жжение изнутри ─ 🗡{damage} 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Печать 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Урахара блокировал {hp} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
        attack_up = Passive("⇪🗡", increase_attack, decrease_attack, 10, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)

        gif = 'CgACAgIAAx0CfstymgACEBtmH2kiAyY6VX5-kxc1JDL6ElLxogACyjgAAkXDAAFJCyOIbv_PK7o0BA'
        caption = (f"Шикай: Бенхиме"
                   f"\n<blockquote expandable>🗡Урон ⇪200 10⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Наке Бенхиме˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 3 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD-FmH2nUweMLP1MifHPDGFzHquv8ZgACzTcAAkXDAAFJJOQ8tyUGiCw0BA'
        caption = (f"Наке Бенхиме"
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Урахара блокировал и нанес {hp} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Шинтен Райхо˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 6 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9xmH6qmgOptrihj1rlsclKz6szoiQACyDcAAkXDAAFJYjsNaNiAxD80BA'
        caption = (f"Хадо #88 Хирю Гекузоку Шинтен Райхо"
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Котен Тайхо˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 10 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9lmH2V61lVXDYwf4mxthNn0nozwoAACwjcAAkXDAAFJrw1dl3Vlb3k0BA'
        caption = (f"Хадо #91 Сенджу Котен Тайхо"
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Камисори Бенхиме˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 4 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9hmH2o6yOPXwNlbMlx0HDLW5YDvngACwTcAAkXDAAFJOcUqETV9sX40BA'
        caption = (f"Камисори Бенхиме"
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Шибари Бенхиме˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 5 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD9ZmH2pl3a6dY9UV0agd60h41nLMiAACvzcAAkXDAAFJlkO3COVHqBc0BA'
        caption = (f"Шибари Бенхиме"
                   f"\n<blockquote expandable>Урахара нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>❤️Лечение ─ + ❤️{self.intelligence * 5} 5⏳"
                   f"\n🪡Постоянно шьет раны делая себя неуязвимым 5⏳"
                   f"\n🪡Постоянно перекраиваеть тела противника вскрывая его 5⏳"
                   f"\n💥невосприимчивый контроли 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Унохана нанесла {damage} 🗡 урона"
                   f"💫Оглушение 1⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Унохана нанесла {damage} 🗡 урона"
                   f"💫Оглушение 1⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Унохана нанесла {damage} 🗡 урона"
                   f"💫Оглушение 2⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Унохана блокировала {hp} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>🐋 Лечение ─ ❤️{hp} 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>🧊 ─ {shield}🌐 Щит</blockquote >")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Шинтен Райхо ˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence * 6 + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD-ZmIIRPb0DpjBthdU8MX9nCJ-6oUAAC0jcAAkXDAAFJDJFVxK81rNY0BA'
        caption = (f"Хадо 88 Хирю Гекузоку Шинтен Райхо"
                   f"\n<blockquote expandable>Унохана нанесла {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Миназуки 🩸˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹Лечение🩸˼", "˹Лезвие🩸˼", "˹Защитная сфера🩸˼"]
        skills_change = Passive("🩸", change_skills, undo_minazuki, 20, new_skills)
        attack_up = Passive("⇪🗡", increase_attack, decrease_attack, 20, 400, apply_once=True)
        agility_up = Passive("⇪👣", increase_agility, decrease_agility, 20, 200, apply_once=True)
        strength_up = Passive("⇪✊🏻", increase_strength, decrease_strength, 20, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)
        self.add_passive(agility_up)
        self.add_passive(strength_up)

        gif = 'CgACAgIAAx0CfstymgACD-xmIIezCd3-a2Ek84w5VsAXFGinmwAC2DcAAkXDAAFJ5Zi36HeBGK00BA'
        caption = (f"Миназуки Банкай🩸"
                   f"\n<blockquote expandable>🗡Урон ⇪400 10⏳"
                   f"\n👣Ловкость ⇪200 10⏳"
                   f"\n✊🏻Сила ⇪200 10⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>❤️Лечение ─ + ❤️{hp}</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Унохана нанесла {damage}x3 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Унохана блокировала {hp} 🗡 урона"
                   f"\nИ нанесла {attack} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

# Ulquiorra scifer

    elif action == '˹Серо˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8dmH7whDVX42I55DqsYKAkelDoCSwACrjcAAkXDAAFJtqCbWeaufuA0BA'
        caption = (f"Серо"
                   f"\n<blockquote expandable>Улькиорра нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Мурсьелаго 🦇˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹Гран Рей Серо˼", "˹Луз дэ ла Луна˼", "˹Сэгунда Этапа 🦇˼"]
        skills_change = Passive("🦇", change_skills, undo_change_skills, 10, new_skills)
        attack_up = Passive("⇪🗡", increase_attack, decrease_attack, 10, 200, apply_once=True)
        agility_up = Passive("⇪👣", increase_agility, decrease_agility, 10, 100, apply_once=True)
        strength_up = Passive("⇪✊🏻", increase_strength, decrease_strength, 10, 100, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)
        self.add_passive(agility_up)
        self.add_passive(strength_up)

        gif = 'CgACAgIAAx0CfstymgACD8hmH8rOTwAB4OuK07Jbyh966mMDUnQAAq83AAJFwwABSfYOi7l9klFpNAQ'
        caption = (f"Мурсьелаго 🦇"
                   f"\n<blockquote expandable>🗡Урон ⇪200 10⏳"
                   f"\n👣Ловкость ⇪100 10⏳"
                   f"\n✊🏻Сила ⇪100 10⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Гран Рей Серо˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = self.attack * 2 + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8dmH7whDVX42I55DqsYKAkelDoCSwACrjcAAkXDAAFJtqCbWeaufuA0BA'
        caption = (f"Гран Рей Серо"
                   f"\n<blockquote expandable>Улькиорра нанес {damage} 🗡 урона</blockquote >")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Луз дэ ла Луна˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        damage = (self.attack + self.intelligence + self.strength + self.agility) * 3
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8lmH8bvr11Ul2Hg0S44JxWO9DTBKQACsDcAAkXDAAFJHwpiKkkIM6Y0BA'
        caption = (f"Луз дэ ла Луна"
                   f"\n<blockquote expandable>Улькиорра нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Сэгунда Этапа 🦇˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹Латиго˼", "˹Серо Оскурас˼", "˹Ланза дэль Рэлампаго˼", "˹Лечение ˼"]
        skills_change = Passive("🦇", change_skills, undo_change_skills, 10, new_skills)
        attack_up = Passive("⇪🗡", increase_attack, decrease_attack, 10, 400, apply_once=True)
        agility_up = Passive("⇪👣", increase_agility, decrease_agility, 10, 200, apply_once=True)
        strength_up = Passive("⇪✊🏻", increase_strength, decrease_strength, 10, 200, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(attack_up)
        self.add_passive(agility_up)
        self.add_passive(strength_up)

        gif = 'CgACAgIAAx0CfstymgACEEtmH_ueh2NqxoTZ_KnWCTRHN6LVVQACwkAAAkXDAAFJpRvMV5DKE7Y0BA'
        caption = (f"Сэгунда Этапа 🦇"
                   f"\n<blockquote expandable>🗡Урон ⇪400 10⏳"
                   f"\n👣Ловкость ⇪200 10⏳"
                   f"\n✊🏻Сила ⇪200 10⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Латиго˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        damage = self.attack + self.intelligence + self.strength + self.agility
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD8pmH8E6nQZVWZu9GDPqkFa1P-ZuBAACsjcAAkXDAAFJxhp_ox-JR040BA'
        caption = (f"Латиго"
                   f"\n<blockquote expandable>Улькиорра нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Серо Оскурас˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        damage = (self.attack + self.intelligence + self.strength + self.agility) * 2
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACD81mH8gHfBd1aMZm2MBu6Dmtfj88oAACtzcAAkXDAAFJR62LOrhWBL80BA'
        caption = (f"Серо Оскурас"
                   f"\n<blockquote expandable>Улькиорра нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>Улькиорра нанес {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                   f"\n<blockquote expandable>❤️Лечение ─ + ❤️{hp}</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

# NarutoS

# Naruto Uzumaki

    elif action == '˹💥Расенган˼':
        mana = await calculate_mana(self, 5)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence * 1

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACGx5mywrOWSLSlrCrRScnOmDI6QIAASIAAlVOAALBU1hKA3lbJ-IG2YU1BA'
        caption = (f"💥Расенган"
                   f"\n<blockquote expandable>Наруто использовал Расенган, нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹👥Каге Буншин но дзюцу˼':
        mana = await calculate_mana(self, 10)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 5)
        if not energy:
            return True, False

        dragon = Passive("👥", decrease_hp, fix_effects, 3, (self.agility + self.strength) * 3)

        enemy.add_passive(dragon)

        gif = 'CgACAgIAAx0CfstymgACG0Rmy0aDrxCsRI9ZYixiZLjPMP8rdgACklYAAvXWWEol49jjw9Ps_TUE'
        caption = (f"👥Каге Буншин но дзюцу"
                   f"\n<blockquote expandable>👥Клоны наносят урон ─ 🗡{(self.agility + self.strength) * 3} 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌀Рассен-сурикен˼':
        mana = await calculate_mana(self, 10)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack * 3 + self.intelligence * 2
        bleed_effect = 50  # добавление эффекта кровотечения

        enemy.add_passive(Passive("🩸Кровотечение", decrease_hp, fix_effects, 3, bleed_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACGyRmywyEET6JbeuzgAABFPS42UOwWrQAAtVSAAL11lhKdXYwAfHC6ZA1BA'
        caption = (f"🌀Рассен-сурикен"
                   f"\n<blockquote expandable>Наруто нанес {damage} "
                   f"🗡 урона и применил 🩸кровотечение на 3 хода</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌐Ультра Расенган˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack * 4 + self.intelligence * 3
        stun = Passive("💫", bash, undo_bash, 3, 1, apply_once=True)

        enemy.add_passive(stun)
        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACGThmwCDBT2mh97HUiv45d3XwijAkZAACnVUAAtU0AUpdJ0a3j972njUE'
        caption = (f"🌐Ультра Расенган"
                   f"\n<blockquote expandable>Наруто нанес {damage} 🗡 урона и оглушил врага на 1 ход</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🍃Режим Мудреца˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹👥Каге꙳Буншин но дзюцу˼", "˹🍥Расенган˼",
                      "˹🪐Рассен-сурикен˼", "˹🐸Кучиёсо но дзюцу˼", '˹🦊Кьюби Чакра˼']
        skills_change = Passive("🍃Режим Мудреца", change_skills, undo_change_skills, 15, new_skills)
        sage_boost = Passive("🍃Усиление мудреца", increase_attack, decrease_attack, 15, 300, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(sage_boost)

        gif = 'CgACAgIAAx0CfstymgACG2Vm1fZTWo3A9cvDTBc2kshnlgexrwACMmQAAr3bsEovgO9W46qrMjUE'
        caption = (f"🍃Режим Мудреца"
                   f"\n<blockquote expandable>Наруто активировал Режим Мудреца</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🍥Расенган˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.attack * 3 + self.intelligence * 2

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACG3Fm1fnZFDaMcDFOzanNDEIci3pWOwAC7GQAAr3bsEqRpahLRNGc8zUE'
        caption = (f"🍥Расенган"
                   f"\n<blockquote expandable>Наруто использовал Расенган, "
                   f"нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🪐Рассен-сурикен˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack * 4 + self.intelligence * 3
        bleed_effect = 75  # добавление эффекта кровотечения

        enemy.add_passive(Passive("🩸Кровотечение", decrease_hp, fix_effects, 3, bleed_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACG29m1flF_W4wcYRopNrdrRmQQjE7xAAC3GQAAr3bsEr1_piwhwJ4xzUE'
        caption = (f"🪐Рассен-сурикен"
                   f"\n<blockquote expandable>Наруто нанес {damage} "
                   f"🗡 урона и применил 🩸кровотечение на 3 хода</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹👥Каге꙳Буншин но дзюцу˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        dragon = Passive("👥", decrease_hp, fix_effects, 3, (self.agility + self.strength) * 3)

        enemy.add_passive(dragon)

        gif = 'CgACAgIAAx0CfstymgACG2xm1fincpoW5SJlrpGcHKG2mRMiygACp2QAAr3bsEqZAAFTwS5j6Rc1BA'
        caption = (f"👥Каге Буншин но дзюцу"
                   f"\n<blockquote expandable>👥Клоны наносят урон ─ "
                   f"🗡{(self.agility + self.strength) * 3} 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🐸Кучиёсо но дзюцу˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        damage = (self.agility + self.strength) * 3

        dragon = Passive("🐸🐸🐸", decrease_hp, fix_effects, 3, damage)

        enemy.add_passive(dragon)

        gif = 'CgACAgIAAx0CfstymgACG31m1ftEHS0meSMBPJxHRXrOjvNXoQACfmUAAr3bsEpFmmvIiNPvxzUE'
        caption = (f"🐸Кучиёсо но дзюцу"
                   f"\n<blockquote expandable>🐸🐸🐸 три жабы наносят урон ─ "
                   f"🗡{(self.agility + self.strength)} х3 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🦊Кьюби Чакра˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹⛬Расен Расенган˼", "˹⚡️Усиление˼",
                      "˹🌔Расен Ренган˼", "˹🌘Расен Таренган˼", '˹🦊Биджу модо˼']
        skills_change = Passive("🦊Кьюби Чакра", change_skills, undo_change_skills, 8, new_skills)
        sage_boost = Passive("⇪🗡", increase_attack, decrease_attack, 8, 300, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(sage_boost)

        gif = 'CgACAgIAAx0CfstymgACG3dm1fsXmvbWwHZU3PbESsZcOI-g1wACd2UAAr3bsEraoaALuX9-pzUE'
        caption = (f"🦊Кьюби Чакра"
                   f"\n<blockquote expandable>Наруто активировал усиленный режим, "
                   f"усиливая атаки и получая новые навыки 8⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹⛬Расен Расенган˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.intelligence * 8

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACG4Nm1fzsMYiyQ7B5wu0BKtb6xAXRjgACo2UAAr3bsEqjhPCQREoJKjUE'
        caption = (f"˹⛬Расен Расенган˼"
                   f"\n<blockquote expandable>Наруто использовал множество расенганов, нанося {damage} х6"
                   f"🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹⚡️Усиление˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        sage_boost = Passive("⇪🗡", increase_attack, decrease_attack, 8, 300, apply_once=True)
        a_boost = Passive("⇪👣", increase_agility, decrease_agility, 8, 300, apply_once=True)
        s_boost = Passive("⇪✊🏻", increase_strength, decrease_strength, 8, 300, apply_once=True)

        self.add_passive(sage_boost)
        self.add_passive(a_boost)
        self.add_passive(s_boost)

        gif = 'CgACAgIAAx0CfstymgACG2dm1fZWXWQge4m8MwRQUCrwlQoI4QACM2QAAr3bsEoaoeTckEDm9zUE'
        caption = (f"⚡️Усиление"
                   f"\n<blockquote expandable>+ ⇪300✊🏻 "
                   f"\n+ ⇪300👣  "
                   f"\n+ ⇪300🗡  </blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌔Расен Ренган˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.attack * 3 + self.intelligence * 4

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACGztmyxa201QXRuJNOxN4nroihXKZrQACxlMAAvXWWErAmjO238b8cDUE'
        caption = (f"🌔Расен Ренган"
                   f"\n<blockquote expandable>Наруто использовал Расен Ренган, нанося {damage} "
                   f"🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌘Расен Таренган˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack * 4 + self.intelligence * 4

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAxkBAAKpZWbakfOVD-pZuSHLEC6wgnhykBuSAAJSUwAC8cTQSjy9iesVbo3gNgQ'
        caption = (f"🌘Расен Таренган"
                   f"\n<blockquote expandable>Наруто использовал Расен Таренган, нанося {damage} "
                   f"🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🦊Биджу модо˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹🌀Тайкьёку Расенган˼"]
        skills_change = Passive("🦊", change_skills, undo_change_skills, 3, new_skills)
        sage_boost = Passive("⇪🗡", increase_attack, decrease_attack, 3, 500, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(sage_boost)

        gif = 'CgACAgIAAx0CfstymgACGzFmyxNLivzjGkQoNSoyCKAL4AlDWAACVFMAAvXWWEq9LCwYZqYqmjUE'
        caption = (f"🦊Биджу модо"
                   f"\n<blockquote expandable>Наруто активировал режим курамы, "
                   f"усиливая атаки и получая новые навыки 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌀Тайкьёку Расенган˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack * 4 + self.intelligence * 4 + self.strength * 2 + self.agility * 2
        bleed_effect = 50  # добавление эффекта кровотечения

        enemy.add_passive(Passive("🔥Ожог", decrease_hp, fix_effects, 3, bleed_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACG39m1fypR4h3zUWVPn7A-aRFYxRx_wACnmUAAr3bsErrfqTzmBLM5zUE'
        caption = (f"🌀Тайкьёку Расенган"
                   f"\n<blockquote expandable>Наруто нанес {damage} 🗡 урона и 🔥поджог врага на 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌑Биджу Дама˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.attack * 3 + self.intelligence * 2

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACGy1myxKdF79H1Ctzf_sDnl7U-jz-UAACQFMAAvXWWEoQ2F2vo7bNujUE'
        caption = (f"🌑Биджу Дама"
                   f"\n<blockquote expandable>Наруто использовал Биджу Даму, нанося {damage} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

# Sasuke Uchiha

    elif action == '˹⚡Чидори˼':
        mana = await calculate_mana(self, 10)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence * 2

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHRFm3TQc0IrvhB3NyqXvzt_cjy8MPwAC4lIAAg_z4Eou7YNzwvprfzYE'
        caption = (f"⚡Райтон: Чидори"
                   f"\n<blockquote expandable>Саске использует Райтон: Чидори, нанося {damage} "
                   f"🗡 урона с помощью ⚡ молнии</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹⚡Чидори Нагаши˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack + self.intelligence

        stun = Passive("⚡Паралич", bash, undo_bash, 2, 1, apply_once=True)
        enemy.add_passive(stun)

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHU5m3UsLUKIPsXCxtz9UvUBKrtL7mAACK0wAAg_z6Ep0a7bJoR_DcjYE'
        caption = (f"⚡Райтон: Чидори Нагаши"
                   f"\n<blockquote expandable>Саске использует Райтон: Чидори Нагаши, нанося {damage} "
                   f"🗡 урона с помощью ⚡ молнии и парпализуя врага"
                   f"\n⚡Паралич 💫 на 2⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹⚡Чидори Катана˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = (self.attack + self.intelligence + self.agility * 2) + enemy.defense

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHVFm3V5V27dTe0C7nqCdqyzVntFsdQACHE0AAg_z6EpFbaitX9QCYzYE'
        caption = (f"⚡Райтон: Чидори Катана"
                   f"\n<blockquote expandable>Саске использует Райтон: Чидори Катана, нанося {damage} "
                   f"чистого урона с помощью ⚡молнии и 🗡меча</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹⚡Кирин˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = self.attack + self.intelligence * 12

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHRZm3Wdqp-KhjdtsnFEcjiZGpxHEnAAC5lIAAg_z4Eq1dlieyrX9mDYE'
        caption = (f"⚡Райтон: Кирин"
                   f"\n<blockquote expandable>Саске использует Райтон: Кирин, нанося {damage} "
                   f"🗡 урона с помощью ⚡ молнии</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🔥Хосенка но Дзюцу˼':
        mana = await calculate_mana(self, 10)
        if not mana:
            return False, True

        damage = self.intelligence * 6
        burn_effect = 50  # шанс поджечь врага и нанести урон в течение нескольких ходов

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHUNm3TyYUWFckB2_yltOXpJxTzDPCwACmksAAg_z6ErN4s1A1vQ6PjYE'
        caption = (f"🔥Катон: Хосенка но Дзюцу"
                   f"\n<blockquote expandable>Саске использует Катон: Хосенка но Дзюцу, "
                   f"нанося {self.intelligence} x6 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🔥Гокакью но Дзюцу˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence
        burn_effect = 50  # шанс поджечь врага и нанести урон в течение нескольких ходов

        enemy.add_passive(Passive("🔥Ожог", decrease_hp, fix_effects, 5, burn_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHTtm3Tb_8en4Lxi_1vbt8-0Ss6m1kgAChUsAAg_z6ErC1khQcPAShjYE'
        caption = (f"🔥Катон: Гокакью но Дзюцу"
                   f"\n<blockquote expandable>Саске использует Гокакью но Дзюцу, "
                   f"нанося {damage} 🗡 урона и поджигая врага"
                   f"\n\n🔥Ожог {burn_effect} 💔 на 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🔥Рьюйка но Дзюцу˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.attack * 3 + self.intelligence * 2
        burn_effect = 100  # шанс поджечь врага и нанести урон в течение нескольких ходов

        enemy.add_passive(Passive("🔥Ожог", decrease_hp, fix_effects, 5, burn_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHUFm3Tw-RGK3zGq1OxLX68VKBLzV_wACmUsAAg_z6Eq44H8ZaEpbnzYE'
        caption = (f"🔥Катон: Рьюйка но Дзюцу"
                   f"\n<blockquote expandable>Саске использует Катон: Рьюйка но Дзюцу, нанося {damage} "
                   f"🗡 урона и поджигая врага"
                   f"\n\n🔥Ожог {burn_effect} 💔 на 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹👁Мангекьё❟❛❟Шаринган⚛˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", '˹⚡Чидори Катана˼', '˹🔥Рьюйка но Дзюцу˼',
                      "˹👁Гендзюцу❟❛❟˼", "˹◼️Аматэрасу˼", "˹❛☉❟Риннеган˼", "˹🩻Сусаноо˼"]
        skills_change = Passive("❟❛❟", change_skills, undo_change_skills, 10, new_skills)
        re_hp = Passive("❟❛❟Шаринган", return_half_hp, fix_effects, 6, 0)
        self.add_passive(re_hp)
        self.add_passive(skills_change)

        gif = 'CgACAgIAAx0CfstymgACHVlm3Wk8eo-qgJOqprGm5azXamBa1gACrE0AAg_z6EpEoT5_7NNoIjYE'
        caption = (f"👁Мангекьё❟❛❟Шаринган⚛"
                   f"\n<blockquote expandable>❟❛❟Шаринган - Саске предвидит атаку "
                   f"врага и уклоняается от половины на 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹👁Гендзюцу❟❛❟˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        energy = 15

        new_skills = ["˹🗡Атака˼"]
        skills_change = Passive("❟❛❟Гендзюцу", change_skills, undo_change_skills, 7, new_skills)
        del_defense = Passive("👁", decrease_defense, fix_effects, 100, enemy.defense, apply_once=True)
        dmg = Passive("🪡", decrease_energy, fix_effects, 7, energy)
        enemy.add_passive(skills_change)
        enemy.add_passive(del_defense)
        enemy.add_passive(dmg)

        gif = 'CgACAgIAAx0CfstymgACHVdm3Wk6nVqLDAea0aVZHdb8iSwvCQACq00AAg_z6EoInA4pwLWAWTYE'
        caption = (f"👁Гендзюцу❟❛❟"
                   f"\n<blockquote expandable>❟❛❟Гендзюцу - жертва попала в иллюзию и потеряла возможность "
                   f"использовать своих навыков на 7⏳"
                   f"и получает урон от иллюзии уколотых 🪡 колов. Иллюзия не наноят урон но истощает силу врага"
                   f"\n\n👁 - Саске контролируя органы чувств врага снимает его защиту 🛡</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹◼️Аматэрасу˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack * 3 + self.intelligence * 5
        burn_effect = self.intelligence * 5  # шанс поджечь врага и нанести урон в течение нескольких ходов

        enemy.add_passive(Passive("♨️Ожог", decrease_hp, fix_effects, 99, burn_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHWBm3v3GLp55ClDcKm5YCEMFW1jQewACaVoAAgfJ-Er4iGByVkLFhDYE'
        caption = (f"◼️Аматэрасу"
                   f"\n<blockquote expandable>◼️Чёрная пламя: Саске поджигает врага нанося {damage}"
                   f"🗡 урона и поджигая врага"
                   f"\n\n♨️Ожог {burn_effect}</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹❛☉❟Риннеган˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹❛☉❟Аменотеджикара˼", '˹🌑Чибаку Тенсей˼']
        skills_change = Passive("❟❛❟", change_skills, undo_change_skills, 10, new_skills)
        self.add_passive(skills_change)

        gif = 'CgACAgIAAx0CfstymgACHWtm3xnxyhQbOeV7E0uN5bijt91sNAACKlwAAgfJ-Epo15ism11SnjYE'
        caption = (f"❛☉❟Риннеган"
                   f"\n<blockquote expandable>❛☉❟ - Саске получает новые навыки и возможности на 10⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹❛☉❟Аменотеджикара˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        hp = self.pre_hp - self.health
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACHWlm3xmPzDY5ZBQT8gMc0e4sTapvgQACHVwAAgfJ-Eqh_NhglSbkMjYE'
        caption = (f"❛☉❟Аменотеджикара"
                   f"\n<blockquote expandable>Телепорт - Саске избежал {hp}🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌑Чибаку Тенсей˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False

        damage = self.attack * 10 + self.intelligence * 10 + self.strength * 5 + self.agility * 5

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHTBm3xZwA4UVI1Qb4uGo2XJ3Ty4L9gACB1MAAg_z4EqhD4efLXtZVjYE'
        caption = (f"🌑Чибаку Тенсей"
                   f"\n<blockquote expandable>Саске использовал Чибаку Тенсей, нанося {damage} "
                   f"🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🩻Сусаноо˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 35)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", '˹🗡Кагутсучи но Тсуруги˼', "˹🏹Сусаноо Кагутсучи˼", '˹🌑Ясака🌑но🌑Магатама🌑˼']
        skills_change = Passive("🩻", change_skills, undo_change_skills, 10, new_skills)

        self.shield += self.intelligence * 20
        self.add_passive(skills_change)

        gif = 'CgACAgIAAx0CfstymgACHWRm3xN5B4Gl4j3WL8qOjoIO_qB3HwACzlsAAgfJ-EoI8_8ET1wQFTYE'
        caption = (f"🩻Сусаноо"
                   f"\n<blockquote expandable>🩻Сусаноо - дает Саске {self.intelligence * 20}🌐 щит "
                   f"и навыки Сусаноо на 10⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🗡Кагутсучи но Тсуруги˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack + self.strength * 10

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHXNm30bKYO1wsatNy8EMe9qXG_xa7wACil4AAgfJ-EprnD7hRuwWcDYE'
        caption = (f"🗡Кагутсучи но Тсуруги"
                   f"\n<blockquote expandable>Саске использовал 🗡Кагутсучи но Тсуруги, нанося "
                   f"{damage}🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🏹Сусаноо Кагутсучи˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.attack + self.agility * 10

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHSxnE3vrHPWFEynrZlxRDbOFnYg6qQACBFMAAg_z4Eocrl60txtztjYE'
        caption = (f"🏹Сусаноо Кагутсучи"
                   f"\n<blockquote expandable>Саске использовал 🏹Сусаноо Кагутсучи, нанося "
                   f"{damage}🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌑Ясака🌑но🌑Магатама🌑˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 30)
        if not energy:
            return True, False

        damage = self.intelligence * 100

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACHXVm30ek0l34CPfHivmZjNBy1hPgJwAClV4AAgfJ-EqC4kqVw4K_FDYE'
        caption = (f"🌑Ясака🌑но🌑Магатама🌑"
                   f"\n<blockquote expandable>Саске использовал Ясака но Магатама, нанося {damage}🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

# Jujutsu Kaisen

# Gojo Satoru

    elif action == '˹🔵 Синий˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.intelligence * 5 + self.attack

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQMRoaRZ2I76HTYlQvMtzUB_8BgABUrIAAuB6AAJJl0lLCSXRQ89Z2VY2BA'
        caption = (f"🔵 Синий"
                   f"\n<blockquote expandable>Годзё использует Синий, нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🔴 Красный˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = self.intelligence * 10 + self.attack

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQMNoaRZ2UZmu9z9YuNu33DE8bFgsfAAC33oAAkmXSUsZSV07OYsmqjYE'
        caption = (f"🔴 Красный"
                   f"\n<blockquote expandable>Годзё использует Красный, нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹👁 Rikugan˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        baf_attack = self.intelligence * 5
        self.add_passive(Passive("⇪🗡", increase_attack, decrease_attack, 10, baf_attack, apply_once=True))
        gif = 'CgACAgIAAx0CfstymgACQNhoaoN1ipS8Z_DXJCcq0UMSE9tmYgACLnoAAkmXWUsqiGMd2gIY9zYE'
        caption = (f"👁 Rikugan"
                   f"\n<blockquote expandable>Годзё использует Рикюган, увеличивая атаку на {baf_attack} ⇪🗡⇪ на 10⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌐 Проклятый щит˼':
        mana = await calculate_mana(self, 100)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        damage = self.mana + self.intelligence * 2
        self.shield += damage
        calculate_shield(enemy, damage)
        gif = 'CgACAgIAAx0CfstymgACQMtoaRuK5iPk6lSpSlsc88lDCEk9GAACUXsAAkmXSUv1Csx6qWfs8TYE'
        caption = (f"🌐 Проклятый щит"
                   f"\n<blockquote expandable>Годзё использует Проклятый щит, увеличивая свой щит на {damage} 🌐 "
                   f"и нанося {damage} 🗡 урона противнику</blockquote>")
        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🟣 Фиолетовый˼':
        mana = await calculate_mana(self, 100)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 40)
        if not energy:
            return True, False

        damage = self.intelligence * 15 + self.attack * 5

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQMdoaRfu-5Q1PUBAHMA0V3vtJlBMZAACB3sAAkmXSUtrfyVP_22bNTYE'
        caption = (f"🟣 Фиолетовый"
                   f"\n<blockquote expandable>Годзё использует Фиолетовый, нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🪐 Необъятая бездна˼':
        mana = await calculate_mana(self, 150)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 40)
        if not energy:
            return True, False

        dec_en = Passive("⇩🪫", decrease_energy, fix_effects, 10, 5, apply_once=False)
        dec_mana = Passive("⇩🧪", decrease_mana, fix_effects, 10, 20, apply_once=False)
        dec_int = Passive("⇩🧠", decrease_intelligence, return_intelligence, 10, 100, apply_once=True)
        dec_agl = Passive("⇩👣", decrease_mana, return_agility, 10, 100, apply_once=True)
        inc_int = Passive("⇪🧠", increase_intelligence, return_intelligence, 10, 150, apply_once=True)
        inc_agl = Passive("⇪👣", increase_agility, return_agility, 10, 150, apply_once=True)


        enemy.add_passive(dec_en)
        enemy.add_passive(dec_mana)
        enemy.add_passive(dec_int)
        enemy.add_passive(dec_agl)
        self.add_passive(inc_int)
        self.add_passive(inc_agl)

        gif = 'CgACAgIAAx0CfstymgACQMloaRoqv8KYQ7joZFUulnteetabjwACRHsAAkmXSUue_In4O4j1dzYE'
        caption = (f"Расширение Территории: 🪐 Необъятая бездна"
                   f"\n<blockquote expandable>Годзё использует Необъятую бездну, "
                   f"снижая энергию, ману, интеллект и ловкость противника на ⇩5🪫⇨⏳, ⇩20🧪⇨⏳, ⇩100🧠 и ⇩100👣 соответственно и "
                   f"увеличивая свой интеллект и ловкость на ⇪150🧠 и ⇪150👣 соответственно на 10⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

# Itadori x Sukuna

    elif action == '˹Удар дивергента 💥˼':
        mana = await calculate_mana(self, 10)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 5)
        if not energy:
            return True, False

        damage = self.intelligence * 2 + self.strength + self.attack

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQvVoku0Fl-37WrCGbZ5HGJoUS-d64wACV2AAAi1IIEqIa4b_xoCh_zYE'
        caption = (f"Удар дивергента 💥"
                   f"\n<blockquote expandable>Итадори использует удар дивергента, нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Блок 🤛˼':

        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False
        hp = self.pre_hp - self.health
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACQvdoku0FIS3na20O6jUvwCIn2cLpPQACcmIAArX_KEqVrYn7zTnABjYE'
        caption = (f"Блок 🤛"
                   f"\n<blockquote expandable>Итадори блокировал {hp} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹Чёрная молния ⚡️˼':

        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        damage = self.intelligence * 4 + self.strength * 2 + self.attack

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQvRoku0FKIA6oRj_cK8hIk-TMOQQlAACwV8AAi1IIEpEXGJYzGVJtTYE'
        caption = (f"Чёрная молния ⚡️"
                   f"\n<blockquote expandable>Итадори использует чёрную молнию, нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹😈 Обмен˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        new_skills = ["˹🗡Атака˼", "˹❤️‍🩹 Обратная техника˼", "˹🌑 Рассечение˼", "˹🔥 Mizushi˼",
                      "˹🏹🔥 Божественное пламя˼", "˹⛩🩸 Демоническая гробница˼"]
        skills_change = Passive("😈", change_skills, fix_effects, 8, new_skills)
        strength_up = Passive("⇪💪", increase_strength, fix_effects, 8, 100, apply_once=True)
        agility_up = Passive("⇪👣", increase_agility, fix_effects, 8, 100, apply_once=True)
        intelligence_up = Passive("⇪🧠", increase_intelligence, fix_effects, 8, 100, apply_once=True)

        self.add_passive(skills_change)
        self.add_passive(strength_up)
        self.add_passive(agility_up)
        self.add_passive(intelligence_up)

        gif = 'CgACAgQAAx0CfstymgACQvhoku0FiqNXGqnJzd2LzjqNbF4qvQACAgUAAlo4rVDiQjzhTUyrhDYE'
        caption = (f"😈 Обмен"
                   f"\n<blockquote expandable>Итадори 🔄 обменивается с Сукуной"
                   f"\n💪Сила ⇪100 8⏳"
                   f"\n👣Ловкость ⇪100 8⏳"
                   f"\n🧠Интеллект ⇪100 8⏳"
                   f"</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹❤️‍🩹 Обратная техника˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False
        hp = self.intelligence * 5
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACQvFoku0F-b8TF8AJOE9KFjhkj-K-aQACCmAAAqPDEEp2b8SPPOWyWDYE'
        caption = (f"❤️‍🩹 Обратная техника"
                   f"\n<blockquote expandable>❤️‍🩹Лечение ─ + ❤️{hp}</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🌑 Рассечение˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False

        damage = self.intelligence * 6
        burn_effect = 300  # шанс поджечь врага и нанести урон в течение нескольких ходов

        enemy.add_passive(Passive("️〰️Проколы", decrease_hp, fix_effects, 3, burn_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQvBoku0FlHkyyTHcPPnk4yi02J-GsAACLlwAAqWcAAFKc5svGDgx-GM2BA'
        caption = (f"🌑 Рассечение"
                   f"\n<blockquote expandable>Сукуна использует 🌑 Рассечение нанося {damage} 🗡 урона противнику"
                   f"\n\n〰️Проколы наносят {burn_effect} урона в течении 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🔥 Mizushi˼':
        mana = await calculate_mana(self, 55)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 30)
        if not energy:
            return True, False

        damage = self.intelligence * 12
        burn_effect = 500  # шанс поджечь врага и нанести урон в течение нескольких ходов

        enemy.add_passive(Passive("🔥", decrease_hp, fix_effects, 5, burn_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQwdokzjA3tDH_-085A2JhqK6CTp7EwAC1HkAAqlYmEhp2H4X7IO9cjYE'
        caption = (f"🔥 Mizushi"
                   f"\n<blockquote expandable>Сукуна использует Mizushi, нанося {damage} 🗡 урона противнику"
                   f"\n\n🔥 Поджоги наносят {burn_effect} урона в течении 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🏹🔥 Божественное пламя˼':

        mana = await calculate_mana(self, 75)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 35)
        if not energy:
            return True, False

        damage = self.intelligence * 15
        burn_effect = 650  # шанс поджечь врага и нанести урон в течение нескольких ходов

        enemy.add_passive(Passive("🔥", decrease_hp, fix_effects, 7, burn_effect))

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQwZokziqFGoYDQFa7Wls5Rr8qK-wTwAC0nkAAqlYmEiPN0D3AAECkgI2BA'
        caption = (f"🏹🔥 Божественное пламя"
                   f"\n<blockquote expandable>Сукуна использует Божественное пламя, нанося {damage} 🗡 урона противнику"
                   f"\n\n🔥 Поджоги наносят {burn_effect} урона в течении 7⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹⛩🩸 Демоническая гробница˼':
        mana = await calculate_mana(self, 90)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 45)
        if not energy:
            return True, False

        damage = self.intelligence * 20

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQwNokzcpl4-NogNGahfTE5zlW4Sr7QACunkAAqlYmEjqcIFLQR8w1jYE'
        caption = (f"Расширение Территории: ⛩🩸 Демоническая гробница"
                   f"\n<blockquote expandable>Сукуна использует ⛩🩸 Демоническую гробницу, нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

# Megumi Fushiguro

    elif action == '˹🔥 Проклятая энергия˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 10)
        if not energy:
            return True, False

        inc_int = Passive("⇪💪", increase_strength, return_strength, 10, 100, apply_once=True)
        inc_agl = Passive("⇪👣", increase_agility, return_agility, 10, 100, apply_once=True)

        self.add_passive(inc_int)
        self.add_passive(inc_agl)

        gif = 'CgACAgIAAx0CfstymgACQzhomwQ1oDOyuhL4tIVgyHVBrMaH4wAClX4AArQAAdlIJtVd8Bqqjyg2BA'
        caption = (f"🔥 Проклятая энергия"
                   f"\n<blockquote expandable>"
                   f"💪Сила ⇪100 10⏳"
                   f"\n👣Ловкость ⇪100 10⏳</blockquote>")
        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🐺 Гёкукен˼':
        mana = await calculate_mana(self, 45)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 15)
        if not energy:
            return True, False

        damage = (self.agility + self.strength + self.intelligence) * 3

        dragon = Passive("🐺🐺🗡", decrease_hp, fix_effects, 3, damage)

        enemy.add_passive(dragon)

        gif = 'CgACAgIAAx0CfstymgACQxVomsHiouyIfLH-19MPsJzgRkdKIAACO3sAAinasUjYmI9ogjYUiDYE'
        caption = (f"🐺 Гёкукен"
                   f"\n<blockquote expandable>🐺🐺 два волка наносят 🗡{damage} урона 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🐇🐰 Датто˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False
        stun = Passive("🐇🐰💫", bash, undo_bash, 3, 1, apply_once=True)

        enemy.add_passive(stun)

        gif = 'CgACAgIAAx0CfstymgACQytomd5YJ8BYf38Fdu_argXoQX9YngACFoAAArQAAclIeU85S9fnk842BA'
        caption = (f"🐇🐰 Датто"
                   f"\n<blockquote expandable>🐇🐰 кролики отвлечёт врага"
                   f"\n💫Оглушение 3⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🦅 Нуэ˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 30)
        if not energy:
            return True, False
        hp = self.pre_hp - self.health
        self.health += hp

        gif = 'CgACAgIAAx0CfstymgACQxRomxBaWSTnlOywOgueH8DDDOn0QwACOHsAAinasUhq8czzTHeY4TYE'
        caption = (f"🦅 Нуэ"
                   f"\n<blockquote expandable>🦅 Нуэ дал уклон от {hp} 🗡 урона</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🐸🪽 Гама˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 35)
        if not energy:
            return True, False

        damage = Passive("🐸🪽🗡", decrease_hp, fix_effects, 3, self.intelligence, apply_once=True)
        stun = Passive("🐸🪽💫", bash, undo_bash, 2, 1, apply_once=True)

        enemy.add_passive(damage)
        enemy.add_passive(stun)

        gif = 'CgACAgIAAx0CfstymgACQy1omd5sQVZVYGKXOIkS6Bz53wABQpgAAhmAAAK0AAHJSKuMOHZHTRGuNgQ'
        caption = (f"🐸🪽 Гама"
                   f"\n<blockquote expandable>🐸🪽 летучие жабы оглушают и атакуют врага"
                   f"\n🗡{self.intelligence} Урона 3⏳"
                   f"\n💫Оглушение 2⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🐘💦 Бансё˼':
        mana = await calculate_mana(self, 75)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 40)
        if not energy:
            return True, False

        damage = (self.agility + self.strength + self.intelligence) * 5

        dragon = Passive("🐘💦", decrease_hp, fix_effects, 5, damage)

        enemy.add_passive(dragon)

        gif = 'CgACAgIAAx0CfstymgACQxZomxb3MLEyqn4qWj9QOdJdTSZGfgACPHsAAinasUg9NE70qx2tXDYE'
        caption = (f"🐘💦 Бансё"
                   f"\n<blockquote expandable>🐘 Слон выпускают огромное количество 💦 воды из хобота нанося {damage} 🗡 урона 5⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🐍 Орочи˼':
        mana = await calculate_mana(self, 85)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 40)
        if not energy:
            return True, False

        damage = (self.agility + self.strength + self.intelligence) * 2

        damage = Passive("🐍🗡", decrease_hp, fix_effects, 4, damage, apply_once=True)
        stun = Passive("🐍💫", bash, undo_bash, 4, 1, apply_once=True)

        enemy.add_passive(damage)
        enemy.add_passive(stun)

        gif = 'CgACAgIAAx0CfstymgACQyxomd5iYxETVpR1Xholzz81JKEnjAACF4AAArQAAclIvS1KRECKgWY2BA'
        caption = (f"🐍 Орочи"
                   f"\n<blockquote expandable>🐍 Чудовищная змея оглушаает и атакует врага"
                   f"\n🗡{damage} Урона 4⏳"
                   f"\n💫Оглушение 4⏳</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹🕳 Теневой сад химер˼':
        mana = await calculate_mana(self, 100)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 45)
        if not energy:
            return True, False

        inc_agl = Passive("⇪👣", increase_agility, return_agility, 5, 200, apply_once=True)
        inc_def = Passive("⇪🛡", increase_defense, return_defense, 5, 100, apply_once=True)
        self.mana += 1000

        self.add_passive(inc_agl)
        self.add_passive(inc_def)


        gif = 'CgACAgIAAx0CfstymgACQxJomysysItJk-iQiCYxk81N5NsrYgAC-nEAAjI_oEjVwM5PGhW22zYE'
        caption = (f"Расширение Территории: 🕳 Теневой сад химер"
                   f"\n<blockquote expandable>"
                   f"\n⇪Ловкость ⇪200 5⏳"
                   f"\n⇪Защита ⇪100 5⏳"
                   f"\n⇪Мана ⇪1500</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    elif action == '˹☸️ Колесо адаптации˼':
        damage = self.intelligence * 20

        calculate_shield(enemy, damage)

        gif = 'CgACAgIAAx0CfstymgACQzxomwaK3OSr8bjDklKMaLtq_rhY_AACs34AArQAAdlIcATNBsFE_hM2BA'
        caption = (f"☸️ Колесо адаптации"
                   f"\n<blockquote expandable>Махорага использует ☸️ Колесо адаптации, нанося {damage} 🗡 урона противнику</blockquote>")

        await send_action(bot, self, enemy, chat_id, gif, caption, ai)


    # After death

    if self.health <= 0:

    # Bleach

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
                       f"\n<blockquote expandable>+ 10000❤️ hp 5⏳"
                       f"\n💥невосприимчивый к контроли 5⏳</blockquote>")

            await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                       f"\n<blockquote expandable>+ 8000❤️ hp"
                       f"\n+ 300🗡 атаки"
                       f"\n💥невосприимчивый к контроли</blockquote>")

            await send_action(bot, self, enemy, chat_id, gif, caption, ai)

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
                       f"\n<blockquote expandable>+ 10000❤️ hp 5⏳"
                       f"\n💥невосприимчивый к контроли</blockquote>")

            await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    # Naruto

        # Naruto Udzumaki

        elif self.name.startswith('Naruto') and self.immortal == 0:
            self.immortal += 1
            self.ability = ['˹🗡Атака˼', "˹🌑Биджу Дама˼"]
            im = Passive("👾", immunity, fix_effects, 5, 1, apply_once=True)
            immortal = Passive("👾Бааджен Цуу", increase_hp, decrease_hp, 5, 10000, apply_once=True)
            self.add_passive(immortal)
            self.add_passive(im)

            gif = 'CgACAgIAAx0CfstymgACG3Nm1fsQOgABQ-pLc76a6zIBuDTfy9wAAnRlAAK927BKNR8f5SBhEco1BA'
            caption = (f"👾Бааджен Цуу"
                       f"\n<blockquote expandable>+ 10000❤️ hp 5⏳"
                       f"\n💥невосприимчивый к контроли</blockquote>")

            await send_action(bot, self, enemy, chat_id, gif, caption, ai)

    # Jujutsu Kaisen

        # Megumi Fushiguro

        elif self.name.startswith('Megumi') and self.immortal == 0:
            self.immortal += 1
            self.ability = ["˹☸️ Колесо адаптации˼"]
            im = Passive("💀", immunity, fix_effects, 2, 1, apply_once=True)
            immortal = Passive("💀 Генерал Махорага", increase_hp, decrease_hp, 5, 10000, apply_once=True)
            self.add_passive(immortal)
            self.add_passive(im)

            gif = 'CgACAgIAAx0CfstymgACQy5omd6Ky2jsyKeRxVBFw6xnpMcDyQACHoAAArQAAclICTTzn1zXLFg2BA'
            caption = (f"💀 Генерал Махорага"
                       f"\n<blockquote expandable>Мегуми призывает прирученного генерала Махорагу перед смертью на 1⏳"
                       f"\n💥невосприимчивый к контроли 1⏳</blockquote>")

            await send_action(bot, self, enemy, chat_id, gif, caption, ai)


# Slaves effect
    if self.slave:
        # Проверяем, добавлена ли пассивка
        if self.slave not in self.passive_names:
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
    if enemy.energy <= 0:
        enemy.energy = 0
    if enemy.mana <= 0:
        enemy.mana = 0

    if enemy.immunity:
        enemy.stun = 0

    self.update_passives()
    self.energy += 5
    enemy.update_passives()
    enemy.energy += 5

    return True, True
