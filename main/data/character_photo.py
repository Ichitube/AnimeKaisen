from aiogram import Router, F

from aiogram.types import CallbackQuery
from keyboards.builders import inline_builder, Ability

router = Router()
user_data = {}


def get_stats(universe, name, key):
    characters = {
        'Bleach': {
                   'Toshiro Hitsuyaga 🌠': {'avatar': 'CgACAgIAAx0CfstymgACCvtl4fr3kR30xtesKEMVVwkQ5CNbQAACZUQAAr-XEUv73A0u5KLPsjQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 65, 'agility': 87, 'intelligence': 80, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Toshiro Hitsuyaga🌠': {'avatar': 'CgACAgIAAx0CfstymgACEPFmILbzqmjSBPn2jGXku2tvw8BigwAC5EcAAkXDCElu9plEyYLYczQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 65, 'agility': 87, 'intelligence': 80, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Ulquiorra Cifer 🌠': {'avatar': 'CgACAgIAAx0CfstymgACETJmIOSrwqCNT4xrWpS3Pp2rpm642wACxUkAAkXDCEneExC8UwABmJY0BA', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Ulquiorra', 'ability': ['˹🗡Атака˼', '˹Серо˼', '˹Мурсьелаго 🦇˼'], 'strength': 70, 'agility': 85, 'intelligence': 77, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Urahara Kisuke🌠': {'avatar': 'CgACAgIAAx0CfstymgACEUZmIPXU3Ur_DoL0BHp83eEqXekIUgACY0oAAkXDCEnMHghjaPLXazQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Urahara', 'ability': ['˹🗡Атака˼', '˹Джугеки Бьякурай˼', '˹Окасен˼', '˹Хайхен˼', '˹Фусатсу Какеи˼', '˹Какафумецу˼', '˹Данку ˼', '˹Бенхиме˼'], 'strength': 65, 'agility': 80, 'intelligence': 87, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Unohana Retsu 🌠': {'avatar': 'CgACAgIAAx0CfstymgACEVdmIWc9AzMoyBj8SJx1Vxnn-QGYOwACuEAAAvmiEEmabu73--tOTDQE', 'type': 'animation', 'gender': 'girl', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Unohana', 'ability': ['˹🗡Атака˼', '˹Гочью Теккан ˼', '˹Фусатсу Какеи˼', '˹ Данку ˼', '˹🐋 Миназуки˼', '˹🧊 Щит ˼', '˹Шинтен Райхо ˼', '˹Миназуки 🩸˼'], 'strength': 78, 'agility': 77, 'intelligence': 77, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke🌠': {'avatar': 'CgACAgIAAx0CfstymgACERhmINzY2DuLAAHGNlT5l1lPFCQu868AAn9JAAJFwwhJg5GwrXHegcM0BA', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 65, 'agility': 87, 'intelligence': 80, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke 🌠': {'avatar': 'CgACAgIAAx0CfstymgACERlmINzdwHb4cfStV3IzsMzjj9BSogACgEkAAkXDCEl5C9F0XKQqeTQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 65, 'agility': 87, 'intelligence': 80, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke 🌠 ': {'avatar': 'CgACAgIAAx0CfstymgACERpmINzxiKRXM_HaKoJK51PLCj-f2AACgUkAAkXDCEkvYwfez_INczQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 65, 'agility': 87, 'intelligence': 80, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke  🌠': {'avatar': 'CgACAgIAAx0CfstymgACERtmINzzuVeZP72dpcrKYd-owb1whgACgkkAAkXDCElwfWFpCNT8JDQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 65, 'agility': 87, 'intelligence': 80, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🌠': {'avatar': 'CgACAgIAAx0CfstymgACCvpl4fr3iHPoeQeOgUYLxvZnKMHNpgACV0QAAr-XEUsJRaXM45JZnjQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼', '˹◾️Финал⛓Гецуга◾️˼'], 'strength': 82, 'agility': 90, 'intelligence': 60, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki  🌠': {'avatar': 'CgACAgIAAx0CfstymgACEMZmIK_B2OvWqHXlyYUYKU88s89fHAACqUcAAkXDCEnJtChfbdWoLDQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼', '˹◾️Финал⛓Гецуга◾️˼'], 'strength': 82, 'agility': 90, 'intelligence': 60, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🌠 ': {'avatar': 'CgACAgIAAx0CfstymgACEMhmIK_BwxJbSsVCjvvPTRQjkYHmpQACqkcAAkXDCEmbkKhuGuJRnzQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼', '˹◾️Финал⛓Гецуга◾️˼'], 'strength': 82, 'agility': 90, 'intelligence': 60, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki🌠 ': {'avatar': 'CgACAgIAAx0CfstymgACEMVmIK_AHUSSv-TA-B_lAoF0XlKlyQACp0cAAkXDCEkyb-5jXS7RbTQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼', '˹◾️Финал⛓Гецуга◾️˼'], 'strength': 82, 'agility': 90, 'intelligence': 60, 'power': 232, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki🌠': {'avatar': 'CgACAgIAAx0CfstymgACEMRmIK_Af6pCCzCOP45mlkuY3mmuWAACpkcAAkXDCElF8yJ4VaCIaTQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Божественная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼', '˹◾️Финал⛓Гецуга◾️˼'], 'strength': 82, 'agility': 90, 'intelligence': 60, 'power': 232, 'shield': 0, 'stun': 0}},

                   'Toshiro Hitsuyaga 🌌': {'avatar': 'CgACAgIAAx0CfstymgACCvll4fr3ojfi_rBBsmfzR7wOkM5g3wACR0QAAr-XEUs5ZXN9zuXt8zQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 59, 'agility': 81, 'intelligence': 74, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Ulquiorra Cifer 🌌': {'avatar': 'CgACAgIAAx0CfstymgACETNmIOSvai5W2pr33USlXraNqYmcRAACxkkAAkXDCEkQkk0sOGt9BzQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Ulquiorra', 'ability': ['˹🗡Атака˼', '˹Серо˼', '˹Мурсьелаго 🦇˼'], 'strength': 64, 'agility': 80, 'intelligence': 70, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Ulquiorra Cifer🌌': {'avatar': 'CgACAgIAAx0CfstymgACETRmIOS0_dA_0zPsR8YYJcM5KwJKEwACyEkAAkXDCEm9Sov_fQHIjjQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Ulquiorra', 'ability': ['˹🗡Атака˼', '˹Серо˼', '˹Мурсьелаго 🦇˼'], 'strength': 64, 'agility': 80, 'intelligence': 70, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Urahara Kisuke🌌': {'avatar': 'CgACAgIAAx0CfstymgACEUVmIWRLFyiq9IoeLy8L57gEeONIWQACYkoAAkXDCElMrLqK60xV7TQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Urahara', 'ability': ['˹🗡Атака˼', '˹Джугеки Бьякурай˼', '˹Окасен˼', '˹Хайхен˼', '˹Фусатсу Какеи˼', '˹Какафумецу˼', '˹Данку ˼', '˹Бенхиме˼'], 'strength': 52, 'agility': 75, 'intelligence': 87, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Urahara Kisuke 🌌': {'avatar': 'CgACAgIAAx0CfstymgACEURmIWRTOj3VtrxVSv6umDiT8TK-2AACYUoAAkXDCElCeIvVjDbi6TQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Urahara', 'ability': ['˹🗡Атака˼', '˹Джугеки Бьякурай˼', '˹Окасен˼', '˹Хайхен˼', '˹Фусатсу Какеи˼', '˹Какафумецу˼', '˹Данку ˼', '˹Бенхиме˼'], 'strength': 52, 'agility': 75, 'intelligence': 87, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Urahara Kisuke 🌌 ': {'avatar': 'CgACAgIAAx0CfstymgACEUNmIWRZuIlcC-8UfA_HtfuBzmO-KgACYEoAAkXDCEk2CiJfIM5kIjQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Urahara', 'ability': ['˹🗡Атака˼', '˹Джугеки Бьякурай˼', '˹Окасен˼', '˹Хайхен˼', '˹Фусатсу Какеи˼', '˹Какафумецу˼', '˹Данку ˼', '˹Бенхиме˼'], 'strength': 52, 'agility': 75, 'intelligence': 87, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Urahara Kisuke  🌌': {'avatar': 'CgACAgIAAx0CfstymgACEUJmIWRgmtuPhIZjKI5-Bc_JnftbqwACX0oAAkXDCEnV2VYgklu7DTQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Urahara', 'ability': ['˹🗡Атака˼', '˹Джугеки Бьякурай˼', '˹Окасен˼', '˹Хайхен˼', '˹Фусатсу Какеи˼', '˹Какафумецу˼', '˹Данку ˼', '˹Бенхиме˼'], 'strength': 52, 'agility': 75, 'intelligence': 87, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Unohana Retsu 🌌': {'avatar': 'CgACAgIAAx0CfstymgACEVlmIWdCOOocxQ39A1tBtTXMd8irIwACuUAAAvmiEEnRXbfoAvruhDQE', 'type': 'animation', 'gender': 'girl', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Unohana', 'ability': ['˹🗡Атака˼', '˹Гочью Теккан ˼', '˹Фусатсу Какеи˼', '˹ Данку ˼', '˹🐋 Миназуки˼', '˹🧊 Щит ˼', '˹Шинтен Райхо ˼', '˹Миназуки 🩸˼'], 'strength': 72, 'agility': 71, 'intelligence': 71, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke 🌌': {'avatar': 'CgACAgIAAx0CfstymgACERdmINzTrWVjChcFMwZ1sEgxd0G7XwACfkkAAkXDCEmzHou_nYuHuzQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 54, 'agility': 76, 'intelligence': 84, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke🌌': {'avatar': 'CgACAgIAAx0CfstymgACERZmINzGYyL7HC5rnpgzNRvkf7XWXwACfEkAAkXDCEnJ_Bd4QW1CQTQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 54, 'agility': 76, 'intelligence': 84, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke 🌌 ': {'avatar': 'CgACAgIAAx0CfstymgACERVmINzC5KVz5pmRv6FFjiZOIkj7vwACe0kAAkXDCEmlYoLsqob-VDQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 54, 'agility': 76, 'intelligence': 84, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🌌': {'avatar': 'CgACAgIAAx0CfstymgACEMNmIK-_trORK2ltCBNlONBHPWalKwACpUcAAkXDCEl2_kD5iERtuTQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 76, 'agility': 84, 'intelligence': 54, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki  🌌': {'avatar': 'CgACAgIAAx0CfstymgACEMJmIK-_vzoUw2rQg56i-7Nyx0uSGQACpEcAAkXDCElR6GZYQjIPkTQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 76, 'agility': 84, 'intelligence': 54, 'power': 214, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🌌 ': {'avatar': 'CgACAgIAAx0CfstymgACEMFmIK-zHiux496uXKC8nJrpShsuRQACo0cAAkXDCEnqr3YF6ErPyDQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Мифическая', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 76, 'agility': 84, 'intelligence': 54, 'power': 214, 'shield': 0, 'stun': 0}},

                   'Ichigo Kurosaki 🌅': {'avatar': 'CgACAgIAAx0CfstymgACCvdl4fr37OoIqdXbSGLnKjK50b_j8QACPEQAAr-XEUudGmaRhnDFwzQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Легендарная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 70, 'agility': 78, 'intelligence': 48, 'power': 196, 'shield': 0, 'stun': 0}},

                   'Toshiro Hitsuyaga 🎆': {'avatar': 'CgACAgIAAx0CfstymgACCvZl4fr3bM2AG281IrnIo9DrZXWU8QACMkQAAr-XEUvmgv2R8SoTCzQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Эпическая', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 47, 'agility': 69, 'intelligence': 62, 'power': 178, 'shield': 0, 'stun': 0}},
                   'Toshiro Hitsuyaga🎆': {'avatar': 'CgACAgIAAx0CfstymgACEO9mIMyUVxgyiY4NB8ZwDs0WvYsz_wAC4kcAAkXDCEngsGVAJEzrpjQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Эпическая', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 47, 'agility': 69, 'intelligence': 62, 'power': 178, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke 🎆': {'avatar': 'CgACAgIAAx0CfstymgACERRmINyyX-alniOsyAtaIjw5yiLQYgACekkAAkXDCEk7NlBmqy5GsjQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Эпическая', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 42, 'agility': 64, 'intelligence': 72, 'power': 178, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🎆': {'avatar': 'CgACAgIAAx0CfstymgACEL9mIK98KdcFrLySXNU7Xp6JIP2i_AACoEcAAkXDCEn-ZMYSzjHHSDQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Эпическая', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 64, 'agility': 72, 'intelligence': 42, 'power': 178, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki🎆': {'avatar': 'CgACAgIAAx0CfstymgACEMBmIK-XtuOpu95l5W9yGnVz3SxE6AACokcAAkXDCEnJkuN4Ncr1BTQE', 'type': 'animation', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Эпическая', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 64, 'agility': 72, 'intelligence': 42, 'power': 178, 'shield': 0, 'stun': 0}},

                   'Toshiro Hitsuyaga 🎇': {'avatar': 'AgACAgIAAx0CfstymgACEOpmIMzuJlnbmIGZxCv80-yehDHATAAC0NsxG0XDCEmX0_jIwoJUJQEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Редкая', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 41, 'agility': 63, 'intelligence': 56, 'power': 160, 'shield': 0, 'stun': 0}},
                   'Toshiro Hitsuyaga🎇': {'avatar': 'AgACAgIAAx0CfstymgACEOlmIMz37CTGirrboDd_-sxIuhXhFgACz9sxG0XDCEmUt5S1DfgMzQEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Редкая', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 41, 'agility': 63, 'intelligence': 56, 'power': 160, 'shield': 0, 'stun': 0}},
                   'Urahara Kisuke 🎇': {'avatar': 'AgACAgIAAx0CfstymgACEUFmIWS2UOZBoXwH-o5lRh4oA_9OhwACZd0xG0XDCEnu_wagdQVvzAEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Редкая', 'arena': {'class': 'Urahara', 'ability': ['˹🗡Атака˼', '˹Джугеки Бьякурай˼', '˹Окасен˼', '˹Хайхен˼', '˹Фусатсу Какеи˼', '˹Какафумецу˼', '˹Данку ˼', '˹Бенхиме˼'], 'strength': 41, 'agility': 56, 'intelligence': 63, 'power': 160, 'shield': 0, 'stun': 0}},
                   'Unohana Retsu 🎇': {'avatar': 'AgACAgIAAx0CfstymgACEVhmIWdBpIW_vz9vVIpteCfijWI7vwACMuAxG_miEEkSm4s9pL2LQQEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'girl', 'universe': 'Bleach', 'rarity': 'Редкая', 'arena': {'class': 'Unohana', 'ability': ['˹🗡Атака˼', '˹Гочью Теккан ˼', '˹Фусатсу Какеи˼', '˹ Данку ˼', '˹🐋 Миназуки˼', '˹🧊 Щит ˼', '˹Шинтен Райхо ˼', '˹Миназуки 🩸˼'], 'strength': 54, 'agility': 53, 'intelligence': 53, 'power': 160, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🎇': {'avatar': 'AgACAgIAAx0CfstymgACELhmIK38jZ9bUqZU6R8iYv0fZBeD_AACadsxG0XDCEnX-3DjblSJ1QEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Редкая', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 58, 'agility': 66, 'intelligence': 36, 'power': 160, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki🎇': {'avatar': 'AgACAgIAAx0CfstymgACELdmIK31XIPQSJkaw3wSLPpW7y4ShgACaNsxG0XDCEkYGdRkYUG0NgEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Редкая', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 58, 'agility': 66, 'intelligence': 36, 'power': 160, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🎇 ': {'avatar': 'AgACAgIAAx0CfstymgACELVmIK2_rBgONZIciwTz_DBn58e33gACZtsxG0XDCEmoTQHa42dDBQEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Редкая', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 58, 'agility': 66, 'intelligence': 36, 'power': 160, 'shield': 0, 'stun': 0}},

                   'Toshiro Hitsuyaga 🌁': {'avatar': 'AgACAgIAAx0CfstymgACEOtmIM1MTyw-riyYbsrptN8VeOC1RQAC0dsxG0XDCEn8cJI_SWSg0AEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 35, 'agility': 57, 'intelligence': 50, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Toshiro Hitsuyaga🌁': {'avatar': 'AgACAgIAAx0CfstymgACEOxmIM1WvTeb_VX8Ddu1b1wdHTOFSAAC0tsxG0XDCEkeQ3KYuZzYzwEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 35, 'agility': 57, 'intelligence': 50, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Toshiro Hitsuyaga 🌁 ': {'avatar': 'AgACAgIAAx0CfstymgACEO1mIM1fQ0a0MksIfNIgFzMQmGQMuAAC09sxG0XDCEn73GXRI0lmegEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 35, 'agility': 57, 'intelligence': 50, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Toshiro Hitsuyaga  🌁': {'avatar': 'AgACAgIAAx0CfstymgACEO5mIM1ni73zRtyFkoyzRTta0fMr6AAC1NsxG0XDCEk1VlOesA-cTwEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Toshiro', 'ability': ['˹🗡Атака˼', '˹❄️Хёкецу˼', '˹❄️Рокуи Хёкецу˼', '˹🌫Тенсо Джурин˼', '˹🐉Хёринмару˼', '˹❄️Синку но Кори˼', '˹🧊Рёджин Хёхеки˼', '˹❆Дайгурен🪽Хёринмару˼'], 'strength': 35, 'agility': 57, 'intelligence': 50, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Urahara Kisuke 🌁': {'avatar': 'AgACAgIAAx0CfstymgACEUBmIWXqRlIqjZp7R3crP_xWq0XhCAACZN0xG0XDCEnjKPIZJDolPQEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Urahara', 'ability': ['˹🗡Атака˼', '˹Джугеки Бьякурай˼', '˹Окасен˼', '˹Хайхен˼', '˹Фусатсу Какеи˼', '˹Какафумецу˼', '˹Данку ˼', '˹Бенхиме˼'], 'strength': 35, 'agility': 49, 'intelligence': 58, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Urahara Kisuke🌁': {'avatar': 'AgACAgIAAx0CfstymgACET9mIWXzN4ed2c2C6Zkq9EJu0EdH_AACY90xG0XDCEmP-TXK-DPn3QEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Urahara', 'ability': ['˹🗡Атака˼', '˹Джугеки Бьякурай˼', '˹Окасен˼', '˹Хайхен˼', '˹Фусатсу Какеи˼', '˹Какафумецу˼', '˹Данку ˼', '˹Бенхиме˼'], 'strength': 35, 'agility': 49, 'intelligence': 58, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Unohana Retsu 🌁': {'avatar': 'AgACAgIAAx0CfstymgACEVpmIW-umttpOcKOZTYd1Adu_jWGDQACM-AxG_miEEkiZv_qfdy1ngEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'girl', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Unohana', 'ability': ['˹🗡Атака˼', '˹Гочью Теккан ˼', '˹Фусатсу Какеи˼', '˹ Данку ˼', '˹🐋 Миназуки˼', '˹🧊 Щит ˼', '˹Шинтен Райхо ˼', '˹Миназуки 🩸˼'], 'strength': 48, 'agility': 47, 'intelligence': 47, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Unohana Retsu🌁': {'avatar': 'AgACAgIAAx0CfstymgACEVtmIW-10MVq0LUfnCLrP-hmlLe6IAACNOAxG_miEEkBVw-0ZLnO2wEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'girl', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Unohana', 'ability': ['˹🗡Атака˼', '˹Гочью Теккан ˼', '˹Фусатсу Какеи˼', '˹ Данку ˼', '˹🐋 Миназуки˼', '˹🧊 Щит ˼', '˹Шинтен Райхо ˼', '˹Миназуки 🩸˼'], 'strength': 48, 'agility': 47, 'intelligence': 47, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Unohana Retsu 🌁 ': {'avatar': 'AgACAgIAAx0CfstymgACEVxmIW-8PrQXIHdJBGMssXnqC60J2gACNeAxG_miEEmk8UsaV0dR3gEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'girl', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Unohana', 'ability': ['˹🗡Атака˼', '˹Гочью Теккан ˼', '˹Фусатсу Какеи˼', '˹ Данку ˼', '˹🐋 Миназуки˼', '˹🧊 Щит ˼', '˹Шинтен Райхо ˼', '˹Миназуки 🩸˼'], 'strength': 48, 'agility': 47, 'intelligence': 47, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Ulquiorra Cifer 🌁': {'avatar': 'AgACAgIAAx0CfstymgACETFmIOSpb8SdkGrGwJNyu62nfrEAAW0AAtLcMRtFwwhJH7VV_WSvp8wBAAMCAAN5AAM0BA', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Ulquiorra', 'ability': ['˹🗡Атака˼', '˹Серо˼', '˹Мурсьелаго 🦇˼'], 'strength': 35, 'agility': 50, 'intelligence': 57, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Ulquiorra Cifer🌁': {'avatar': 'AgACAgIAAx0CfstymgACETBmIOShjUGM5ZgBmHcO0sED1ClCKQACz9wxG0XDCEnwx7OA74B8XwEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Ulquiorra', 'ability': ['˹🗡Атака˼', '˹Серо˼', '˹Мурсьелаго 🦇˼'], 'strength': 35, 'agility': 50, 'intelligence': 57, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke 🌁': {'avatar': 'AgACAgIAAx0CfstymgACERNmINyvG6iUp11ljNbmwtyMmDP6ZgACrNwxG0XDCEmP2pkzUrYvxQEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 32, 'agility': 50, 'intelligence': 60, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Aizen Sosuke🌁': {'avatar': 'AgACAgIAAx0CfstymgACERJmINynXI59EXCJsyhOUynb2ZbmfQACq9wxG0XDCEl5BwVfIDI9IwEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Aizen', 'ability': ['˹🗡Атака˼', '˹Данку˼', '˹⚡️Райхоко˼', '˹🔶Мильон Эскудо˼', '˹◼️Курохицуги˼', '˹🐉Горьюу Теммецу˼'], 'strength': 32, 'agility': 50, 'intelligence': 60, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🌁': {'avatar': 'AgACAgIAAx0CfstymgACELJmIK2WnI3avtMwF6OW_nD0qCYQ3AACVtsxG0XDCEnMtyCfhVDqZgEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 52, 'agility': 60, 'intelligence': 30, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki🌁': {'avatar': 'AgACAgIAAx0CfstymgACELNmIK2hmWxTO5XWArqxprXUl1bzqgACXtsxG0XDCEmLfD-RQbBaggEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 52, 'agility': 60, 'intelligence': 30, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki 🌁 ': {'avatar': 'AgACAgIAAx0CfstymgACELRmIK2wOjJWYl4d-Wp6NdhFgRYiCQACX9sxG0XDCElpt5NF4WSaswEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 52, 'agility': 60, 'intelligence': 30, 'power': 142, 'shield': 0, 'stun': 0}},
                   'Ichigo Kurosaki  🌁': {'avatar': 'AgACAgIAAx0CfstymgACELZmIK3b80QWSIHXfnF-2XL8FlS91wACYNsxG0XDCEmEPt5pwueMfAEAAwIAA3kAAzQE', 'type': 'photo', 'gender': 'boy', 'universe': 'Bleach', 'rarity': 'Обычная', 'arena': {'class': 'Ichigo', 'ability': ['˹🗡Атака˼', '˹▫️Слэш˼', '˹◽️Поступь˼', '˹◻️Гецуга Теншоу˼', '˹◾️Тенса࿖Зангецу˼'], 'strength': 52, 'agility': 60, 'intelligence': 30, 'power': 142, 'shield': 0, 'stun': 0}}
                   }}
    return characters.get(universe).get(name).get(key)


def ability_stats(name):
    stats = {
        'Toshiro Hitsuyaga 🌠': ['˹❄️Хёкецу ─ наносить 🗡:2 + ✊🏻 + 👣 + 🧠 урона, замараживает врага на 1⏳, стоимость 25🧪˼',
                                '˹❄️Рокуи Хёкецу˼ ─ техника позволяет Тоширо создать ледяной дракон. Наносит урон врагу на 2 хода',
                                '˹❄️Реджин˼ ─ техника позволяет Тоширо создать ледяной щит. Защищает от урона на 1 ход',
                                '˹❄️Дайгурен⁂Хёринмару❄️˼ ─ техника позволяет Тоширо создать ледяной дракон. Наносит урон врагу на 3 хода'],
        'Ichigo Kurosaki 🌠': ['˹▫️Слэш ─ небольшая волна энергии, наносить 🗡х2 Урона, стоимость 10🧪˼',
                              '˹◽️Поступь ─ волна энергии, наносить 🗡х2 + ✊🏻 Урона, +✊🏻 ❤️hp стоимость 15🧪˼',
                              '˹◻️Гецуга Теншоу ─ волна энергии, наносить 🗡х2 + ✊🏻 Урона, стоимость 20🧪 10🪫˼',
                              '˹◾️Тенса࿖Зангецу ─ Банкай ࿖, +200🗡 на 5⏳, стоимость 25🧪 15🪫˼ \n  Навыки:'
                              '\n     ˹🟥Гецуга◼️Теншоу ─ сильнейшая волна энергии, наносить 🗡х2 + ✊🏻 + 👣 + 🧠 Урона, стоимость 30🧪˼'
                              '\n   ˹💀Пустой ─ Сила пустого, +100✊🏻, +100👣, наносить 100🗡 урона каждый ход, стоимость 45🧪 15🪫˼'
                              '\n       Навыки:'
                              '\n          ˹🟥Гецуга Теншоу ─ сильнейшая волна энергии, наносить 🗡х2 + ✊🏻 + 👣 + 🧠 Урона, стоимость 35🧪˼',
                              '˹◾️Финал⛓Гецуга◾️ ─ Завершенная Гецуга Теншоу, +1000🗡 на 3⏳, стоимость 70🪫˼ \n   Навыки:'
                              '\n     ˹◾️⛓Мугецу⛓◾️ ─ Чёрная вольна очень мощной энергии, наносить 🗡х4 чистейшего урона игнорируя защиту противника˼\nПобочные эффекты:'
                              ' После выхода из формы Гецуга Теншоу, Ичиго теряет все силы, атаки и защиты на 5⏳',
                              '⊛Квинси - Ичиго заполучить силу квинси после окончании побочного эффекта Гецуга Теншоу˼ \n   Навыки:'
                              '\n     ˹🌙Гецуга⊛Теншоу ─ сильнейшая волна энергии, наносить 🗡х4 + ✊🏻 + 👣 + 🧠 Урона, стоимость 20🧪 15🪫˼',
                              'Особенности: После смерти воскреснет и входят в форму Финального пустого ─ +10000 ❤️hp на 5⏳ \n  Навыки:'
                              '\n     ˹☄️Гран Рей Серо ─ Серо арранкар, наносить 🗡х3 + ✊🏻 + 👣 + 🧠 Урона˼ \nПобочные эффекты:'
                              ' После выхода из формы Финального пустого, Ичиго умрёт',
                              ]
    }
    if name in stats:
        return stats.get(name)
    else:
        return 'Нет данных'


async def ability(callback, universe, character, back):
    abilities = ability_stats(character)
    skills = ''
    for skill in abilities:
        skills += skill + '\n\n'

    strength = get_stats(universe, character, 'arena')['strength']
    agility = get_stats(universe, character, 'arena')['agility']
    intelligence = get_stats(universe, character, 'arena')['intelligence']

    await callback.message.answer(f"❖ 🎴 {character}"
                                  f"\n── •✧✧• ────────────"
                                  f"\n✊🏻Сл: {strength}"
                                  f" 👣Лов: {agility}"
                                  f" 🧠Инт: {intelligence}"
                                  f"\n\n{skills}", reply_markup=inline_builder(["☑️"], ["delete"], row_width=[1]))


@router.callback_query(Ability.filter(F.action == "ability"))
async def answer_ability(callback: CallbackQuery, callback_data: Ability):
    user_data[callback.from_user.id] = [callback_data.universe, callback_data.character, callback_data.back]
    await ability(callback, callback_data.universe, callback_data.character, callback_data.back)
    await callback.answer()


@router.callback_query(F.data == "delete")
async def delete(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()


h_stats = {
        '🏠 home_1': ('CgACAgIAAx0CfstymgACBSdlxMKCT9RgJMzJipEu1JSGiKBMjwACkT4AAgrXEEqHUaLCIEJOpDQE', 5000),
        '🏠 home_2': ('CgACAgIAAx0CfstymgACBSVlxMJsufpVxh33vCBQxQKpJCYP8AACI0IAAoHCEUpzwQdzGCsF7DQE', 7000),
        '🏠 home_3': ('CgACAgIAAx0CfstymgACBSNlxMJ4LQ-8mCz7sCBC5WamzSx4LAAC_kEAAoHCEUqwNPS5JomlgTQE', 9000),
        '🏠 home_4': ('CgACAgIAAx0CfstymgACBSZlxMJQZb7FFLh9iPFdSpXOklwDqQACaD4AAgrXEEpTmie8hGfs1zQE', 12000),
        '🏠 home_5': ('CgACAgIAAx0CfstymgACBdtlzO0rWNF9QoR6R4_5ZaHZDVb37wACakkAAsywaUpFT0CPnQYM5TQE', 15000),
    }


def home_stats(name: str):
    return h_stats.get(name)


s_stats = {
        'Алекси': ('CgACAgIAAx0CfstymgACD0ZmGQuj-TUH0EaHzCE01UdHdiqcGgACTkcAAoofyEiCZ9PYwk9VxzQE', 'Алекси', 50, 'heal', 10000),
        'Вилли': ('CgACAgIAAx0CfstymgACD0hmGQutT-LRIY1_8NfBQqzakjj3SAACUUcAAoofyEgNOObyJvd72TQE', 'Вилли',  70, 'attack', 10000),
        'Пушистик': ('CgACAgIAAx0CfstymgACD0dmGQutNdjmwtt7uPxRDNw8n_Mt_gACUEcAAoofyEhgSwrVi03r0TQE', 'Пушистик', 50, 'heal', 10000),
        'Лера': ('CgACAgIAAx0CfstymgACD1JmGQ5HuGtNegOJ18XNrW3nFECTFAACaEcAAoofyEgRJnqIGb9B0DQE', 'Лера', 70, 'attack', 10000),
        'Беата': ('CgACAgIAAx0CfstymgACD1hmGVnuoE1Vh_qLRX9YhwjjvNaNtgACMkYAAqk6yUiLbHT72gGuszQE', 'Беата', 70, 'attack', 10000),
    }


def slaves_stats(name: str):
    return s_stats.get(name)


quotes = {
    'Bleach': [
        'Все, что я хочу, это стать сильнее ── Ичиго Куросаки',
        'Жизнь - это не просто веселая прогулка ── Киске Урахара',
        'Я не могу позволить себе проиграть ── Тосиро Хицугая',
        'Ты не можешь понять чужую боль, если сам не испытал ее ── Киске Урахара',
        'Это оскорбительно солдату — думать о своей жизни на поле боя ── Абараи Ренджи',
        'Убьёшь ты — или убьют тебя, какая разница? В любом случае мы просто убиваем время ── Зараки Кенпачи',
        'Каково не было бы твое развлечение, если ты один, то это не весело ── Орихиме Иноуэ',
        'Жизнь не всегда справедлива, но это не значит, что ты должен сдаваться. Ты можешь сделать свою жизнь лучше, '
        'если будешь верить в себя и свои мечты ── Ичиго Куросаки',
        'Совсем не ужасно постоянно опасаться предательства. Гораздо страшнее когда предательства не ожидаешь… '
        '── Айзен Соскэ',
        'Владеть клинком только ради исполнения долга — вот что значит быть капитаном ── Тосиро Хицугая',
        'Владение клинком из ненависти — не что иное, как мелкое насилие. Это не то, что мы считаем битвой'
        ' ── Тосиро Хицугая',
    ]
}
