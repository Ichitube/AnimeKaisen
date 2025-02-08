@router.message(ChatTypeFilter(chat_type=["private"]), Command("search"))
@router.callback_query(F.data == "search_opponent")
async def search_opponent(callback: CallbackQuery | Message):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    universe = account['universe']

    if account['universe'] in ['Allstars', 'Allstars(old)']:
        await callback.answer(
            text="💢 Пока не доступно в вашой вселеноой!",
            show_alert=True
        )
        return

    if isinstance(callback, CallbackQuery):
        await callback.message.delete()

    if account["battle"]["battle"]["status"] == 0:
        rival = await mongodb.find_opponent()

        await mongodb.update_user(user_id, {"battle.battle.status": 1})

        if rival is None:
            await bot.send_animation(
                user_id, animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                caption=f"\n 💡 <blockquote expandable>{random.choice(character_photo.quotes[universe])}</blockquote>"
                        f"\n── •✧✧• ────────────"
                        f"\n❖ 🔎 Поиск соперника . . . . .",
                reply_markup=reply_builder("✖️ Отмена"))
        else:
            ident = account["_id"]
            name = account["name"]
            character = account['character'][account['universe']]
            avatar = character_photo.get_stats(universe, character, 'avatar')
            avatar_type = character_photo.get_stats(universe, character, 'type')
            rarity = character_photo.get_stats(universe, character, 'rarity')
            strength = character_photo.get_stats(universe, character, 'arena')['strength']
            agility = character_photo.get_stats(universe, character, 'arena')['agility']
            intelligence = character_photo.get_stats(universe, character, 'arena')['intelligence']
            ability = character_photo.get_stats(universe, character, 'arena')['ability']
            power = character_photo.get_stats(universe, character, 'arena')['power']
            slave = None
            if account['inventory']['slaves']:
                slave = account['inventory']['slaves'][0]

            b_character = characters.Character(ident, name, character, strength, agility, intelligence, ability, 1,
                                               False, rival["_id"], slave, 0)

            battle_data[account["_id"]] = b_character

            r_ident = rival["_id"]
            r_name = rival["name"]
            r_universe = rival['universe']
            r_character = rival['character'][rival['universe']]
            r_avatar = character_photo.get_stats(r_universe, r_character, 'avatar')
            r_avatar_type = character_photo.get_stats(r_universe, r_character, 'type')
            r_rarity = character_photo.get_stats(r_universe, r_character, 'rarity')
            r_strength = character_photo.get_stats(r_universe, r_character, 'arena')['strength']
            r_agility = character_photo.get_stats(r_universe, r_character, 'arena')['agility']
            r_intelligence = character_photo.get_stats(r_universe, r_character, 'arena')['intelligence']
            r_ability = character_photo.get_stats(r_universe, r_character, 'arena')['ability']
            r_power = character_photo.get_stats(r_universe, r_character, 'arena')['power']
            r_slave = None
            if rival['inventory']['slaves']:
                r_slave = rival['inventory']['slaves'][0]

            rb_character = characters.Character(r_ident, r_name, r_character, r_strength, r_agility, r_intelligence,
                                                r_ability, 1, False, account["_id"], r_slave, 0)

            battle_data[rival["_id"]] = rb_character

            user_text = (f" ⚔️ Cоперник Найден! "
                         f"\n── •✧✧• ────────────"
                         f"\n<blockquote expandable> 🪪  〢 {rival['name']} "
                         f"\n── •✧✧• ────────────"
                         f"\n❖ ✨ Редкость: {r_rarity}"
                         f"\n❖ 🗺 Вселенная: {r_universe}"
                         f"\n\n   ✊🏻 Сила: {r_strength}"
                         f"\n   👣 Ловкость: {r_agility}"
                         f"\n   🧠 Интелект: {r_intelligence}"
                         f"\n   ⚜️ Мощь: {r_power}</blockquote>"
                         f"\n── •✧✧• ────────────"
                         f"\n<i>🀄️ Опыт: {rival['stats']['exp']} XP </i>")

            rival_text = (f"⚔️ Cоперник Найден! "
                          f"\n── •✧✧• ────────────"
                          f"\n<blockquote expandable> 🪪  〢 {account['name']} "
                          f"\n── •✧✧• ────────────"
                          f"\n❖ ✨ Редкость: {rarity}"
                          f"\n❖ 🗺 Вселенная: {universe}"
                          f"\n\n   ✊🏻 Сила: {strength}"
                          f"\n   👣 Ловкость: {agility}"
                          f"\n   🧠 Интелект: {intelligence}"
                          f"\n   ⚜️ Мощь: {power}</blockquote>"
                          f"\n── •✧✧• ────────────"
                          f"\n<i>🀄️ Опыт: {account['stats']['exp']} XP </i>")

            await mongodb.update_user(account["_id"], {"battle.battle.status": 2, "battle.battle.rid": rival["_id"]})
            await mongodb.update_user(rival["_id"], {"battle.battle.status": 2, "battle.battle.rid": account["_id"]})

            if r_avatar_type == 'photo':
                await bot.send_photo(photo="AgACAgIAAx0CfstymgACNJhnRZTPz9fTnkUVLgH-dSorSmJ6pQAC5OcxG4ISMUqFAsZTkEY1cAEAAwIAA3gAAzYE",
                                     reply_markup=reply_builder("🏴‍☠️ Сдаться"))
            else:
                await bot.send_animation(animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                                         reply_markup=reply_builder("🏴‍☠️ Сдаться"))

            if avatar_type == 'photo':
                await bot.send_photo(photo="AgACAgIAAx0CfstymgACNJhnRZTPz9fTnkUVLgH-dSorSmJ6pQAC5OcxG4ISMUqFAsZTkEY1cAEAAwIAA3gAAzYE",
                                     reply_markup=reply_builder("🏴‍☠️ Сдаться"))
            else:
                await bot.send_animation(animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                                         reply_markup=reply_builder("🏴‍☠️ Сдаться"))

            await bot.send_message(account["_id"], text="⏳ Ход соперника")
            mes = await bot.send_message(rival["_id"], text=f".                    ˗ˋˏ💮 Раунд {rb_character.b_round}ˎˊ˗"
                                                            f"\n✧•───────────────────────•✧"
                                                            f"\n<blockquote expandable>{account_text(rb_character)}"
                                                            f"\n✧•───────────────────────•✧"
                                                            f"\n{account_text(b_character)}</blockquote>"
                                                            f"\n✧•───────────────────────•✧"
                                                            f"\n🔸 Ваш ход:",
                                         reply_markup=inline_builder(r_ability, r_ability, row_width=[2, 2]),
                                         parse_mode=ParseMode.HTML)
            # Инициализируем состояние пользователя
            user_data[rival["_id"]] = {rb_character.b_round: False}
            user_data[user_id] = {b_character.b_round: True}

            # Запускаем таймер
            await surrender_f(rival["_id"], rb_character.b_round, mes)

    elif account["battle"]["battle"]["status"] == 1:
        if isinstance(callback, CallbackQuery):
            await callback.answer(
                text="💢 Вы уже находитесь в поиске соперника!",
                show_alert=True
            )
        else:
            await callback.answer(text="💢 Вы уже находитесь в поиске соперника!")

    elif account["battle"]["battle"]["status"] == 2:
        if isinstance(callback, CallbackQuery):
            await callback.answer(
                text="💢 Вы уже находитесь в битве!",
                show_alert=True
            )
        else:
            await callback.answer(text="💢 Вы уже находитесь в битве!")


@router.callback_query(CallbackChatTypeFilter(chat_type=["private"]), F.data.startswith("˹"))
async def battle(callback: CallbackQuery):
    user_id = callback.from_user.id
    account = await mongodb.get_user(user_id)
    try:
        action = callback.data
        character = battle_data.get(account["_id"])
        r_character = battle_data.get(character.rid)

        if account["battle"]["battle"]["status"] == 2:
            if character.b_turn:
                return await bot.send_message(user_id, "✖️ Вы уже сделали ход!")

            mana, energy = await characters.turn(character, bot, action, r_character, 0)

            if not mana:
                await callback.answer("✖️ Недостаточно маны 🧪", show_alert=True)
                return

            if not energy:
                await callback.answer("✖️ Недостаточно энергии 🪫", show_alert=True)
                return

            await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)

            battle_data[character.ident] = character
            battle_data[r_character.ident] = r_character

            async def send_round_photo():
                if r_character.stun == 0:
                    character.b_round += 1
                    battle_data[r_character.ident].b_turn = False
                    battle_data[character.ident].b_turn = True
                    if r_character.ident != character.ident * 10:
                        mes = await bot.send_message(r_character.ident,
                                                     text=f".                    ˗ˋˏ💮 Раунд {r_character.b_round}ˎˊ˗"
                                                          f"\n✧•───────────────────────•✧"
                                                          f"\n<blockquote expandable>{account_text(r_character)}"
                                                          f"\n✧•───────────────────────•✧"
                                                          f"\n{account_text(character)}</blockquote>"
                                                          f"\n✧•───────────────────────•✧"
                                                          f"\n🔸 Ваш ход:",
                                                     reply_markup=inline_builder(r_character.ability, r_character.ability,
                                                                                 row_width=[2, 2]),
                                                     parse_mode=ParseMode.HTML)
                    else:
                        await ai(r_character)
                    user_data[user_id][character.b_round - 1] = True  # Обновляем состояние
                    # Инициализируем состояние пользователя
                    user_data[r_character.ident][r_character.b_round] = False
                    # Запускаем таймер
                    if r_character.ident != character.ident * 10:
                        await surrender_f(r_character.ident, r_character.b_round, mes)
                else:
                    character.b_round += 1
                    r_character.b_round += 1
                    battle_data[character.rid].b_turn = True
                    battle_data[character.ident].b_turn = False
                    if r_character.ident != character.ident * 10:
                        await bot.send_message(r_character.ident,
                                               text=f".                    ˗ˋˏ💮 Раунд {r_character.b_round - 1}ˎˊ˗"
                                                    f"\n✧•───────────────────────•✧"
                                                    f"\n<blockquote expandable>{account_text(r_character)}"
                                                    f"\n✧•───────────────────────•✧"
                                                    f"\n{account_text(character)}"
                                                    f"\n✧•───────────────────────•✧</blockquote>"
                                                    f"\n💫 Вы под действием оглушения",
                                               parse_mode=ParseMode.HTML)
                    mes = await bot.send_message(user_id,
                                                 text=f".                    ˗ˋˏ💮 Раунд {character.b_round}ˎˊ˗"
                                                      f"\n✧•───────────────────────•✧"
                                                      f"\n<blockquote expandable>{account_text(character)}"
                                                      f"\n✧•───────────────────────•✧"
                                                      f"\n{account_text(r_character)}</blockquote>"
                                                      f"\n✧•───────────────────────•✧"
                                                      f"\n🔸 Ваш ход:",
                                                 reply_markup=inline_builder(character.ability, character.ability,
                                                                             row_width=[2, 2]),
                                                 parse_mode=ParseMode.HTML)
                    user_data[r_character.ident][r_character.b_round - 1] = True  # Обновляем состояние
                    user_data[character.ident][character.b_round - 1] = True  # Обновляем состояние
                    # Инициализируем состояние пользователя
                    user_data[user_id][character.b_round] = False
                    # Запускаем таймер
                    if r_character.ident != character.ident * 10:
                        await bot.send_message(chat_id=r_character.ident, text="⏳ Ход соперника")
                        await surrender_f(character.ident, character.b_round, mes)

            if character.health <= 0 and r_character.health <= 0:
                await bot.send_animation(chat_id=user_id, animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                                         caption=draw_text, reply_markup=menu_button())
                if r_character.ident != character.ident * 10:
                    await bot.send_animation(chat_id=r_character, animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                                             caption=draw_text, reply_markup=menu_button())

                # await mongodb.update_many(
                #     {"_id": {"$in": [account["_id"], character.rid]}},
                #     {"$set": {"battle.battle.status": 0, "battle.battle.rid": ""}}
                # )
                #
                # await mongodb.update_many(
                #     {"_id": {"$in": [account["_id"], character.rid]}},
                #     {"$inc": {"stats.exp": 80, "battle.stats.ties": 1, "account.money": 150}}
                # )

                await mongodb.update_value(account["_id"], {"battle.stats.ties": 1})
                await mongodb.update_value(account["_id"], {"stats.exp": 80})
                await mongodb.update_value(account["_id"], {"account.money": 150})
                current_date = datetime.today().date()
                current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
                await mongodb.update_user(account["_id"], {"tasks.last_arena_fight": current_datetime})
                await mongodb.update_user(account["_id"], {"battle.battle.status": 0})
                await mongodb.update_user(account["_id"], {"battle.battle.rid": ""})
                await mongodb.update_value(account["_id"], {"inventory.items.halloween": 4})
                if r_character.ident != character.ident * 10:
                    await mongodb.update_value(character.rid, {"battle.stats.ties": 1})
                    await mongodb.update_value(character.rid, {"stats.exp": 80})
                    await mongodb.update_value(character.rid, {"account.money": 150})
                    await mongodb.update_user(character.rid, {"tasks.last_arena_fight": current_datetime})
                    await mongodb.update_user(character.rid, {"battle.battle.status": 0})
                    await mongodb.update_user(character.rid, {"battle.battle.rid": ""})
                    await mongodb.update_value(character.rid, {"inventory.items.halloween": 4})

            elif character.health <= 0:
                if character.b_round != r_character.b_round:
                    await bot.send_animation(chat_id=user_id, animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                                             caption=lose_text, reply_markup=menu_button())
                    if r_character.ident != character.ident * 10:
                        await bot.send_animation(chat_id=character.rid, animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                                                 caption=win_text, reply_markup=menu_button())

                    await mongodb.update_value(account["_id"], {"battle.stats.loses": 1})
                    await mongodb.update_value(account["_id"], {"stats.exp": 55})
                    await mongodb.update_value(account["_id"], {"account.money": 100})
                    current_date = datetime.today().date()
                    current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
                    await mongodb.update_user(account["_id"], {"tasks.last_arena_fight": current_datetime})
                    await mongodb.update_user(account["_id"], {"battle.battle.status": 0})
                    await mongodb.update_user(account["_id"], {"battle.battle.rid": ""})
                    await mongodb.update_value(account["_id"], {"inventory.items.halloween": 2})
                    if r_character.ident != character.ident * 10:
                        await mongodb.update_value(character.rid, {"battle.stats.wins": 1})
                        await mongodb.update_value(character.rid, {"stats.exp": 100})
                        await mongodb.update_value(character.rid, {"account.money": 200})
                        await mongodb.update_user(character.rid, {"tasks.last_arena_fight": current_datetime})
                        await mongodb.update_user(character.rid, {"battle.battle.status": 0})
                        await mongodb.update_user(character.rid, {"battle.battle.rid": ""})
                        await mongodb.update_value(character.rid, {"inventory.items.halloween": 5})

                else:
                    await send_round_photo()

            elif r_character.health <= 0:
                if character.b_round != r_character.b_round:
                    await bot.send_animation(chat_id=user_id, animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                                             caption=win_text, reply_markup=menu_button())
                    if r_character.ident != character.ident * 10:
                        await bot.send_animation(chat_id=character.rid, animation="CgACAgIAAx0CfstymgACNKRnRZTGyuTCHjBKHMGXvnUr-6YSLwACZGMAAoISMUpp-usAASvF56w2BA",
                                                 caption=lose_text, reply_markup=menu_button())

                    current_date = datetime.today().date()
                    current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
                    if r_character.ident != character.ident * 10:
                        await mongodb.update_value(character.rid, {"battle.stats.loses": 1})
                        await mongodb.update_value(character.rid, {"stats.exp": 55})
                        await mongodb.update_value(character.rid, {"account.money": 100})
                        await mongodb.update_user(character.rid, {"tasks.last_arena_fight": current_datetime})
                        await mongodb.update_user(character.rid, {"battle.battle.status": 0})
                        await mongodb.update_user(character.rid, {"battle.battle.rid": ""})
                        await mongodb.update_value(character.rid, {"inventory.items.halloween": 2})
                    await mongodb.update_user(account["_id"], {"battle.battle.status": 0})
                    await mongodb.update_user(account["_id"], {"battle.battle.rid": ""})
                    await mongodb.update_user(account["_id"], {"tasks.last_arena_fight": current_datetime})
                    await mongodb.update_value(account["_id"], {"battle.stats.wins": 1})
                    await mongodb.update_value(account["_id"], {"stats.exp": 100})
                    await mongodb.update_value(account["_id"], {"account.money": 200})
                    await mongodb.update_value(account["_id"], {"inventory.items.halloween": 5})

                else:
                    await send_round_photo()
            else:
                await send_round_photo()

