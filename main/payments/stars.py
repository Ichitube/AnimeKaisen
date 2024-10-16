from os import getenv
from dotenv import load_dotenv

from aiogram import Router, F, Bot

from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from aiogram.enums import ParseMode

from keyboards.builders import inline_builder
from data import mongodb

router = Router()


# @router.callback_query(F.data == "buy_keys")
# async def buy_keys(callback: CallbackQuery):
#     await callback.message.delete()
#
#     pattern = dict(caption=f"\n<blockquote expandable>❖ 🧧 Вы можете купить священный билет за 20 🌟</blockquote>"
#                            f"\n── •✧✧• ────────────",
#                    parse_mode=ParseMode.HTML,
#                    reply_markup=inline_builder(["🧧 Купить", "✖️ Отмена"], ["stars", "store"], row_width=[2, 1]))
#
#     media_id = "CgACAgIAAx0CfstymgACBQVluXo_n-FnFfBB1XW8zCIU7_Ed0QAC6TsAAtfz0Enh8jW0yBuKgzQE"
#
#     await callback.message.answer_animation(animation=media_id, **pattern)

@router.message(F.text.lower().in_(['донат', 'купить']))
@router.callback_query(F.data == "buy_keys")
async def buy_keys(message: Message | CallbackQuery):
    if isinstance(message, CallbackQuery):
        await message.message.answer_invoice(
            title="🌟 Покупка билет 🧧",
            description="❖ 🧧 Священный билет имеет высокий шанс выпадения редких персонажей"
                        "\n\n\n\n • Цена: 25 🌟",
            payload="buy_ticket",
            currency="XTR",
            prices=[LabeledPrice(label="XTR", amount=25)],
        )
    else:
        await message.answer_invoice(
            title="🌟 Покупка билет 🧧",
            description="❖ 🧧 Священный билет имеет высокий шанс выпадения редких персонажей",
                       # f"\n\n • Цена: 25 🌟",
            payload="buy_ticket",
            currency="XTR",
            prices=[LabeledPrice(label="XTR", amount=25)]
        )


@router.pre_checkout_query()
async def process_pre_checkout_query(event: PreCheckoutQuery):
    await event.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):
    payload = message.successful_payment.invoice_payload

    if payload == "buy_slave":
        # Обработка покупки рабыни
        data = await state.get_data()
        result = character_photo.slaves_stats(data['slave'])
        await mongodb.push_slave(message.from_user.id, data.get('slave'))
        current_date = datetime.today().date()
        current_datetime = datetime.combine(current_date, datetime.time(datetime.now()))
        await mongodb.update_user(message.from_user.id, {"tasks.last_shop_purchase": current_datetime})
        await message.answer(f"❖ 🔖 Вы успешно приобрели {result[1]}")

    elif payload == "buy_ticket":
        # Обработка покупки билета
        # await bot.refund_star_payment(message.from_user.id, message.successful_payment.telegram_payment_charge_id)
        await mongodb.update_value(message.from_user.id, {'inventory.items.tickets.keys': 1})
        await message.answer("❖ Вы успешно приобрели 🧧 священный билет")

    # await bot.refund_star_payment(message.from_user.id, message.successful_payment.telegram_payment_charge_id)
    # await mongodb.update_value(message.from_user.id, {'inventory.items.tickets.keys': 1})
    # await message.answer("❖ Вы успешно приобрели 🧧 священный билет")

# @router.callback_query(F.data == "buy_keys")
# async def buy_keys(callback: CallbackQuery):
#     await callback.message.delete()
#
#     billing = crystalpayAPI.Invoice.create(100, InvoiceType.purchase, 15)
#     billing_id = billing['id']
#     tasks[callback.from_user.id] = billing_id
#     pattern = dict(caption=f"\n── •✧✧• ────────────"
#                            f"\n❖  💮 Если вы из следющих стран:\n🇺🇸 $  🇺🇦 ₴  🇰🇿 ₸ (или другие страны) оплатите через "
#                            f"  <b>💳 Paysend</b>"
#                            f"\n── •✧✧• ────────────"
#                            f"\n❖  💮 Если вы из РФ 🇷🇺 ₽ оплатите через <b>💎 CrystalPay либо</b> "
#                            f"свяжитесь с\n<a href='https://t.me/falcon_blackhawk'><b>👤 Админом</b></a> и купите лично."
#                            f"\n── •✧✧• ────────────",
#                    parse_mode=ParseMode.HTML,
#                    reply_markup=inline_builder(["💳 Paysend", "💎 CrystalPay", "✖️ Отмена"],
#                                                ["paysend", "buy_crypt", "store"], row_width=[2, 1])
#                    )
#
#     media_id = "CgACAgIAAx0CfstymgACBQVluXo_n-FnFfBB1XW8zCIU7_Ed0QAC6TsAAtfz0Enh8jW0yBuKgzQE"
#
#     await callback.message.answer_animation(animation=media_id, **pattern)
#
#
# @router.callback_query(F.data == "paysend")
# async def buy_keys(callback: CallbackQuery):
#     inline_id = callback.inline_message_id
#     pattern = dict(caption=f"❖  💳 Для оплаты через Paysend:"
#                            f"\n── •✧✧• ────────────"
#                            f"\n 1. <a href='https://paysend.com/login?from_page=send'>"
#                            f"<b>Перейдите в Paysend</b></a>\n 2. Переведите 🇺🇸 1$ = 🇺🇦 35₴ = 🇰🇿 390₸ \n "
#                            f"3. Отправьте <a href='https://t.me/falcon_blackhawk'><b>👤 Админу</b></a> скриншот с "
#                            f"\n🧾 чеком и id: "
#                            f"<a href='tg://user?id={callback.from_user.id}'>{callback.from_user.id}</a>",
#                    parse_mode=ParseMode.HTML,
#                    reply_markup=inline_builder(["✖️ Отмена"], ["buy_keys"], row_width=[1])
#                    )
#
#     await callback.message.edit_caption(inline_id, **pattern)
#
#
# @router.callback_query(F.data == "buy_crypt")
# async def buy_keys(callback: CallbackQuery):
#     inline_id = callback.inline_message_id
#
#     billing = crystalpayAPI.Invoice.create(100, InvoiceType.purchase, 15)
#     billing_id = billing['id']
#     tasks[callback.from_user.id] = billing_id
#     pattern = dict(caption=f"\n── •✧✧• ────────────"
#                    f"\n❖  🪙 Для оплаты <a href='{billing['url']}'><b> перейдите сюда</b></a>",
#                    parse_mode=ParseMode.HTML,
#                    reply_markup=inline_builder(["✔️ Оплатил", "✖️ Отмена"], ["check", "buy_keys"], row_width=[1])
#                    )
#
#     await callback.message.edit_caption(inline_id, **pattern)
#
#
# @router.callback_query(F.data == "check")
# async def buy_keys(callback: CallbackQuery):
#     billing_id = tasks[callback.from_user.id]
#     billing = crystalpayAPI.Invoice.getinfo(billing_id)
#     if billing['state'] == 'notpayed':
#         await callback.answer("❖  💎 Вы ещё не оплатили", show_alert=True)
#     else:
#         await callback.answer("❖  💎 Вы успешно приобрели 🧧 священный билет", show_alert=True)
#         tasks.pop(callback.from_user.id)
#         await mongodb.update_value(callback.from_user.id, {'inventory.items.tickets.keys': 1})
#         await store(callback)
