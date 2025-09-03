from data import character_photo


class CardCharacters:
    def __init__(self, ident, p_name, universe, cb, name, slave, rid, data,
                 status="🎴", avatar=None, avatar_type=None, rarity=None, strength=None,
                 agility=None, intelligence=None, clas=None, shield=0, stun=0, health=None,
                 attack=None, defense=None, mana=None, crit_dmg=None, crit_ch=None,
                 b_round=1, b_turn=True, c_status="🎴", is_active=False):

        # Если переданы None, получаем данные из character_photo
        if avatar is None:
            avatar = character_photo.get_stats(universe, name, 'avatar')
        if avatar_type is None:
            avatar_type = character_photo.get_stats(universe, name, 'type')
        if rarity is None:
            rarity = character_photo.get_stats(universe, name, 'rarity')
        if strength is None:
            strength = character_photo.get_stats(universe, name, 'arena')['strength']
        if agility is None:
            agility = character_photo.get_stats(universe, name, 'arena')['agility']
        if intelligence is None:
            intelligence = character_photo.get_stats(universe, name, 'arena')['intelligence']
        if clas is None:
            clas = character_photo.get_stats(universe, name, 'arena')['class']

        # Устанавливаем параметры объекта
        self.status = status
        self.avatar = avatar
        self.avatar_type = avatar_type
        self.ident = ident
        self.p_name = p_name
        self.universe = universe
        self.cb = cb
        self.rarity = rarity
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.shield = shield
        self.stun = stun
        self.health = health if health is not None else strength * 75
        self.attack = attack if attack is not None else strength * 5 + agility * 5 + intelligence * 5
        self.defense = defense if defense is not None else (strength + agility + (intelligence // 2)) // 4
        self.mana = mana if mana is not None else intelligence * 10
        self.crit_dmg = crit_dmg if crit_dmg is not None else strength + (agility // 2) + (intelligence // 4)
        self.crit_ch = crit_ch if crit_ch is not None else agility + (strength // 2) + (intelligence // 4)
        self.clas = clas
        self.b_round = b_round
        self.b_turn = b_turn
        self.rid = rid
        self.slave = slave
        self.c_status = c_status
        self.data = data
        self.is_active = is_active

    # Метод для сериализации объекта в словарь
    # def to_dict(self):
    #     return {
    #         "status": self.status,
    #         "avatar": self.avatar,
    #         "avatar_type": self.avatar_type,
    #         "ident": self.ident,
    #         "p_name": self.p_name,
    #         "universe": self.universe,
    #         "cb": self.cb,
    #         "rarity": self.rarity,
    #         "name": self.name,
    #         "strength": self.strength,
    #         "agility": self.agility,
    #         "intelligence": self.intelligence,
    #         "shield": self.shield,
    #         "stun": self.stun,
    #         "health": self.health,
    #         "attack": self.attack,
    #         "defense": self.defense,
    #         "mana": self.mana,
    #         "crit_dmg": self.crit_dmg,
    #         "crit_ch": self.crit_ch,
    #         "clas": self.clas,
    #         "b_round": self.b_round,
    #         "b_turn": self.b_turn,
    #         "rid": self.rid,
    #         "slave": self.slave,
    #         "c_status": self.c_status,
    #         "data": self.data,
    #         "is_active": self.is_active
    #     }
    #
    # # Метод для восстановления объекта из словаря
    # @classmethod
    # def from_dict(cls, data):
    #     return cls(
    #         ident=data["ident"],
    #         p_name=data["p_name"],
    #         universe=data["universe"],
    #         cb=data["cb"],
    #         name=data["name"],
    #         slave=data["slave"],
    #         rid=data["rid"],
    #         data=data["data"],
    #         status=data.get("status", "🗡"),
    #         avatar=data.get("avatar"),
    #         avatar_type=data.get("avatar_type"),
    #         rarity=data.get("rarity"),
    #         strength=data.get("strength"),
    #         agility=data.get("agility"),
    #         intelligence=data.get("intelligence"),
    #         shield=data.get("shield", 0),
    #         stun=data.get("stun", 0),
    #         health=data.get("health"),
    #         attack=data.get("attack"),
    #         defense=data.get("defense"),
    #         mana=data.get("mana"),
    #         crit_dmg=data.get("crit_dmg"),
    #         crit_ch=data.get("crit_ch"),
    #         clas=data.get("clas"),
    #         b_round=data.get("b_round", 1),
    #         b_turn=data.get("b_turn", True),
    #         c_status=data.get("c_status", "🎴"),
    #         is_active=data.get("is_active", False)
    #     )
