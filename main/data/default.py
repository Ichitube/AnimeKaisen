




# Minato Namikaze

    elif action == '˹⚡Расенган˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = self.attack * 2 + self.intelligence * 0.5
        knockback_chance = 50  # шанс отбросить врага, снижая его скорость

        if random.randint(1, 100) <= knockback_chance:
            enemy.reduce_speed(2)

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"⚡Расенган"
                   f"\n\nМинато создал Расенган, нанося {damage} 🗡 урона и уменьшая скорость врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹⚡Летящий Гром Бог˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = self.attack * 1.8 + self.intelligence * 0.7
        teleport_effect = True  # телепортируется за спину врага, усиливая следующую атаку

        self.add_passive(Passive("⚡Летящий Гром Бог", increase_attack, decrease_attack, 3, damage))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"⚡Летящий Гром Бог"
                   f"\n\nМинато использует Летящий Гром Бог, нанося {damage} 🗡 урона и телепортируясь за спину врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹⚡Барьер Летящего Грома˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        defense_boost = 40  # усиление защиты на 3 хода
        reflect_damage = self.intelligence * 1.5  # отражение урона обратно врагу

        self.add_passive(Passive("⚡Барьер Летящего Грома", increase_defense, decrease_defense, 3, defense_boost))

        calculate_shield(enemy, reflect_damage)

        gif = '1111111111111111'
        caption = (f"⚡Барьер Летящего Грома"
                   f"\n\nМинато создал барьер, усиливая свою защиту на {defense_boost} и отражая {reflect_damage} урона врагу")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹⚡Режим Отшельника˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        sage_mode_boost = self.intelligence * 2 + self.agility * 1.5  # Усиление после активации режима
        damage = self.attack * 2.5 + sage_mode_boost

        self.add_passive(Passive("⚡Режим Отшельника", increase_attack, decrease_attack, 5, sage_mode_boost))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"⚡Режим Отшельника"
                   f"\n\nМинато активирует Режим Отшельника, нанося {damage} 🗡 урона и усиливая свои способности")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹⚡Хирайшин: Шики Фуджин˼':
        mana = await calculate_mana(self, 60)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 30)
        if not energy:
            return True, False

        instant_kill_chance = 10  # шанс на мгновенное уничтожение врага
        damage = self.attack * 3 + self.intelligence * 2

        if random.randint(1, 100) <= instant_kill_chance:
            enemy.instant_kill()

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"⚡Хирайшин: Шики Фуджин"
                   f"\n\nМинато использует Хирайшин: Шики Фуджин, нанося {damage} 🗡 урона и с шансом мгновенно уничтожить врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Hotake Kakashi

    elif action == '˹⚡️Чидори˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = 100  # Урон от Чидори

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"⚡️Чидори"
                   f"\n\nКакаши использовал Чидори, нанося {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌀Камуи˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        damage = 150  # Урон от Камуи
        duration = 2  # Длительность способности

        self.add_passive(Passive("🌀Камуи", remove_enemy, return_enemy, duration))

        gif = '1111111111111111'
        caption = (f"🌀Камуи"
                   f"\n\nКакаши использовал Камуи, нанося {damage} 🗡 урона и выводя врага из боя на {duration} хода")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🔥Катон: Гоенко˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = 120  # Урон от Гоенко
        burn_duration = 3  # Длительность ожога

        self.add_passive(Passive("🔥Ожог", apply_burn, remove_burn, burn_duration, damage_per_turn=30))

        gif = '1111111111111111'
        caption = (f"🔥Катон: Гоенко"
                   f"\n\nКакаши использовал Катон: Гоенко, нанося {damage} 🗡 урона и накладывая ожог на {burn_duration} ходов")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹⚡️Райкири˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = 130  # Урон от Райкири

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"⚡️Райкири"
                   f"\n\nКакаши использовал Райкири, нанося {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹👁Шаринган˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True

        duration = 3  # Длительность Шарингана

        self.add_passive(Passive("👁Шаринган", increase_critical, decrease_critical, duration, critical_chance=50))

        gif = '1111111111111111'
        caption = (f"👁Шаринган"
                   f"\n\nКакаши активировал Шаринган, увеличивая шанс критического удара на {duration} ходов")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Madara Uchiha

    elif action == '˹🔥Катон: Гокакью но Дзюцу˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = self.attack * 1.8 + self.intelligence * 0.7
        burn_effect = 45  # шанс поджечь врага и нанести урон в течение нескольких ходов

        self.add_passive(Passive("🔥Ожог", burn_effect, decrease_defense, 5, burn_effect))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🔥Катон: Гокакью но Дзюцу"
                   f"\n\nМадара использует Гокакью но Дзюцу, нанося {damage} 🗡 урона и поджигая врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌪Сусаноо˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        defense_boost = 50  # увеличение защиты после использования способности
        damage = self.attack * 2 + self.intelligence * 1.3

        self.add_passive(Passive("🌪Сусаноо", increase_defense, decrease_defense, 6, defense_boost))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🌪Сусаноо"
                   f"\n\nМадара активировал Сусаноо, нанося {damage} 🗡 урона и усиливая свою защиту на {defense_boost} единиц")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌌Вечный Мангекё Шаринган˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 25)
        if not energy:
            return True, False

        genjutsu_damage = self.intelligence * 2 + self.agility * 1.5

        calculate_shield(enemy, genjutsu_damage)

        gif = '1111111111111111'
        caption = (f"🌌Вечный Мангекё Шаринган"
                   f"\n\nМадара использует Вечный Мангекё Шаринган, нанося {genjutsu_damage} 🗡 урона с помощью гендзюцу")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌑Инфинити Цукуёми˼':
        mana = await calculate_mana(self, 60)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 30)
        if not energy:
            return True, False

        stun_chance = 40  # шанс оглушить всех врагов на 1 ход
        genjutsu_damage = self.intelligence * 3 + self.attack * 1.5

        if random.randint(1, 100) <= stun_chance:
            enemy.stun(1)

        calculate_shield(enemy, genjutsu_damage)

        gif = '1111111111111111'
        caption = (f"🌑Инфинити Цукуёми"
                   f"\n\nМадара использует Инфинити Цукуёми, нанося {genjutsu_damage} 🗡 урона и оглушая всех врагов на 1 ход")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌪Мокутон: Дзюкай Котан˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        damage = self.attack * 2.2 + self.intelligence * 1.1
        entangle_chance = 30  # шанс запутать врага, снижая его скорость

        if random.randint(1, 100) <= entangle_chance:
            enemy.reduce_speed(2)

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🌪Мокутон: Дзюкай Котан"
                   f"\n\nМадара использует Мокутон: Дзюкай Котан, нанося {damage} 🗡 урона и снижая скорость врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌑Мудреца Шесть Путей˼':
        mana = await calculate_mana(self, 70)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 40)
        if not energy:
            return True, False

        sage_boost = self.intelligence * 2.5 + self.agility * 1.5
        damage = self.attack * 3 + sage_boost

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🌑Мудреца Шесть Путей"
                   f"\n\nМадара использует силу Мудреца Шести Путей, нанося {damage} 🗡 урона и усиливая свои способности")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Konan

    elif action == '˹📜Шикигами но Май˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = 80
        duration = 2  # Длительность способности

        self.add_passive(Passive("📜Шикигами но Май", increase_damage, decrease_damage, duration, damage))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"📜Шикигами но Май"
                   f"\n\nКонан активировала Шикигами но Май, нанося {damage} 🗡 урона в течение {duration} ходов")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹💠Ками Буншин˼':
        mana = await calculate_mana(self, 15)
        if not mana:
            return False, True

        damage = 60
        duration = 1  # Длительность способности

        self.add_passive(Passive("💠Ками Буншин", absorb_damage, remove_absorb_damage, duration))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"💠Ками Буншин"
                   f"\n\nКонан использовала Ками Буншин, нанося {damage} 🗡 урона и поглощая урон в течение {duration} хода")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌸Ками но Шиша но Дзюцу˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = 100
        duration = 3  # Длительность способности

        self.add_passive(Passive("🌸Ками но Шиша но Дзюцу", gradual_damage, remove_gradual_damage, duration, damage))

        gif = '1111111111111111'
        caption = (f"🌸Ками но Шиша но Дзюцу"
                   f"\n\nКонан активировала Ками но Шиша но Дзюцу, нанося {damage} 🗡 урона в течение {duration} ходов")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹💀Бумажный Океан˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        damage = 150

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"💀Бумажный Океан"
                   f"\n\nКонан использовала Бумажный Океан, нанося {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌸Бумажные Крылья˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        duration = 1  # Длительность способности

        self.add_passive(Passive("🌸Бумажные Крылья", apply_evasion, remove_evasion, duration))

        gif = '1111111111111111'
        caption = (f"🌸Бумажные Крылья"
                   f"\n\nКонан активировала Бумажные Крылья, давая себе уклонение на {duration} ход")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Itachi Uchiha

    elif action == '˹🔥Аматерасу˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = self.intelligence * 2 + self.attack * 0.5
        burn_duration = 3  # продолжительность горения (ходы)

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🔥Аматерасу"
                   f"\n\nИтачи использует Аматерасу, нанося {damage} 🗡 урона и вызывая горение на {burn_duration} ходов")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🛡Сусаноо˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        defense_boost = 50  # увеличение защиты после использования способности
        shield_duration = 5  # продолжительность усиления защиты (ходы)

        self.add_passive(Passive("🛡Защита Сусаноо", increase_defense, decrease_defense, shield_duration, defense_boost))

        gif = '1111111111111111'
        caption = (f"🛡Сусаноо"
                   f"\n\nИтачи использует Сусаноо, увеличивая свою защиту на {defense_boost} на {shield_duration} ходов")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹👁Цукуёми˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True

        stun_duration = 2  # продолжительность оглушения (ходы)

        if random.randint(1, 100) <= 100:  # Цукуёми всегда оглушает противника
            enemy.stun(stun_duration)

        gif = '1111111111111111'
        caption = (f"👁Цукуёми"
                   f"\n\nИтачи использует Цукуёми, мгновенно оглушая противника на {stun_duration} ходов")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🔥Катон: Гоуюка˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = self.intelligence * 1.5 + self.attack * 1.2

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🔥Катон: Гоуюка"
                   f"\n\nИтачи использует Катон: Гоуюка, нанося {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Нагато (Пейн)

    elif action == '˹🌀Шинра Тенсей˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = 120  # Урон от Шинра Тенсей

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🌀Шинра Тенсей"
                   f"\n\nНагато использовал Шинра Тенсей, нанося {damage} 🗡 урона и отталкивая врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🔴Чибаку Тенсей˼':
        mana = await calculate_mana(self, 40)
        if not mana:
            return False, True

        damage = 150  # Урон от Чибаку Тенсей
        duration = 3  # Длительность эффекта

        self.add_passive(Passive("🔴Чибаку Тенсей", trap_enemy, release_enemy, duration))

        gif = '1111111111111111'
        caption = (f"🔴Чибаку Тенсей"
                   f"\n\nНагато использовал Чибаку Тенсей, нанося {damage} 🗡 урона и запечатывая врага на {duration} хода")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹👁Баншо Тенин˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = 90  # Урон от Баншо Тенин
        pull_chance = 50  # Шанс притянуть врага

        if random.randint(1, 100) <= pull_chance:
            enemy.pull_towards(self)

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"👁Баншо Тенин"
                   f"\n\nНагато использовал Баншо Тенин, нанося {damage} 🗡 урона и притягивая врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹⚡️Риннеган: Чакра Поглощение˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        drain_amount = 50  # Количество чакры, которое поглощается у врага

        enemy.mana -= drain_amount
        self.mana += drain_amount

        gif = '1111111111111111'
        caption = (f"⚡️Риннеган: Чакра Поглощение"
                   f"\n\nНагато использовал Риннеган для поглощения {drain_amount} чакры у врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🔵Наруками˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        damage = 140  # Урон от Наруками

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🔵Наруками"
                   f"\n\nНагато использовал Наруками, нанося {damage} 🗡 урона и создавая мощный удар молнии")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Sasori

    elif action == '˹🎭Красная армия кукол˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True

        damage = 100  # Урон от Красной армии кукол
        puppet_count = 100  # Количество кукол

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🎭Красная армия кукол"
                   f"\n\nСасори использовал свою Красную армию кукол, атакуя врага с помощью {puppet_count} кукол и нанося {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🦂Ядовитая игла˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = 80  # Урон от Ядовитой иглы
        poison_duration = 3  # Длительность яда (в ходах)

        self.add_passive(Passive("🦂Яд", apply_poison, remove_poison, poison_duration, damage // 2))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🦂Ядовитая игла"
                   f"\n\nСасори выстрелил ядовитой иглой, нанося {damage} 🗡 урона и отравляя врага на {poison_duration} хода")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹💀Железный песок˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        damage = 120  # Урон от Железного песка

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"💀Железный песок"
                   f"\n\nСасори использовал Железный песок, нанося {damage} 🗡 урона врагу")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌀Техника секретного красного песка: Сотня кукол˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True

        damage = 150  # Урон от Секретной техники
        puppet_count = 100  # Количество кукол, использованных в атаке

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🌀Техника секретного красного песка: Сотня кукол"
                   f"\n\nСасори использовал Секретную технику, управляя {puppet_count} куклами и нанося {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🔥Техника огненного дыхания˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = 90  # Урон от Техники огненного дыхания

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🔥Техника огненного дыхания"
                   f"\n\nСасори использовал Технику огненного дыхания, нанося {damage} 🗡 урона и поджигая врага")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Rok Li

    elif action == '˹🥋Первый Врата Открытия˼':
        mana = await calculate_mana(self, 10)
        if not mana:
            return False, True

        damage = 50  # Урон от атаки после открытия Первого Врата
        agility_boost = 20  # Увеличение ловкости на 3 хода

        self.add_passive(Passive("🥋Увеличение ловкости", increase_agility, decrease_agility, 3, agility_boost))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🥋Первый Врата Открытия"
                   f"\n\nРок Ли открыл Первые Врата, нанося {damage} 🗡 урона и увеличивая свою ловкость на {agility_boost} на 3 хода")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹💥Первичный Лотос˼':
        mana = await calculate_mana(self, 30)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 20)
        if not energy:
            return True, False

        damage = 120  # Урон от Лотоса

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"💥Первичный Лотос"
                   f"\n\nРок Ли использовал Лотос, нанося {damage} 🗡 урона врагу")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🥊Удар Листа˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        damage = 80  # Урон от Удара Листа
        stun_chance = 25  # Шанс оглушить врага на 1 ход

        if random.randint(1, 100) <= stun_chance:
            enemy.stun(1)

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🥊Удар Листа"
                   f"\n\nРок Ли нанес Удар Листа, нанося {damage} 🗡 урона и с шансом {stun_chance}% оглушить врага на 1 ход")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🔥Удар ножницами˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = 90  # Урон от Удара ножницами

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🔥Удар ножницами"
                   f"\n\nРок Ли нанес {damage} 🗡 урона Ударом ножницами")

        await send_action(bot, self, enemy, chat_id, gif, caption)

# Obito Uchiha

    elif action == '˹🌪Камуи˼':
        mana = await calculate_mana(self, 35)
        if not mana:
            return False, True

        damage = 100  # Урон от использования Камуи
        dodge_chance = 40  # Шанс увернуться от атаки на 2 хода

        self.add_passive(Passive("🌪Неуязвимость Камуи", increase_dodge, decrease_dodge, 2, dodge_chance))

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🌪Камуи"
                   f"\n\nОбито использует Камуи, нанося {damage} 🗡 урона и увеличивая шанс уклонения на {dodge_chance}% на 2 хода")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🔥Катон: Гоенка˼':
        mana = await calculate_mana(self, 25)
        if not mana:
            return False, True

        damage = 90  # Урон от огненной атаки

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"🔥Катон: Гоенка"
                   f"\n\nОбито использует технику Катон: Гоенка, нанося {damage} 🗡 урона огненной атакой")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹🌀Шаринган˼':
        mana = await calculate_mana(self, 20)
        if not mana:
            return False, True

        intelligence_boost = 30  # Увеличение интеллекта на 3 хода
        damage_reduction = 20  # Снижение получаемого урона на 3 хода

        self.add_passive(Passive("🌀Интеллект Шарингана", increase_intelligence, decrease_intelligence, 3, intelligence_boost))
        self.add_passive(Passive("🌀Щит Шарингана", reduce_damage, undo_reduce_damage, 3, damage_reduction))

        gif = '1111111111111111'
        caption = (f"🌀Шаринган"
                   f"\n\nОбито активирует Шаринган, увеличивая интеллект на {intelligence_boost} и снижая получаемый урон на {damage_reduction}% на 3 хода")

        await send_action(bot, self, enemy, chat_id, gif, caption)

    elif action == '˹💀Вторжение Дзюби˼':
        mana = await calculate_mana(self, 50)
        if not mana:
            return False, True
        energy = await calculate_energy(self, 30)
        if not energy:
            return True, False

        damage = 150  # Мощная атака Дзюби

        calculate_shield(enemy, damage)

        gif = '1111111111111111'
        caption = (f"💀Вторжение Дзюби"
                   f"\n\nОбито использует силу Дзюби, нанося {damage} 🗡 урона")

        await send_action(bot, self, enemy, chat_id, gif, caption)