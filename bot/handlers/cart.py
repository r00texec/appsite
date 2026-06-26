from aiogram import Router, F
from aiogram.types import CallbackQuery
from locales import get_text
from keyboards.catalog import cart_kb, payment_kb
from keyboards.main_menu import back_main_kb
from database import get_cart, remove_from_cart, clear_cart, create_order, get_product, add_to_cart
from utils.helpers import format_price, PAYMENT_DETAILS
from config import SUPPORT_USERNAME

router = Router()


@router.callback_query(F.data == "cart")
async def cb_cart(callback: CallbackQuery, lang: str):
    items = await get_cart(callback.from_user.id)
    if not items:
        await callback.message.edit_text(
            get_text(lang, "cart_empty"),
            reply_markup=back_main_kb(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return
    text = get_text(lang, "cart_title")
    total = 0
    for item in items:
        text += get_text(lang, "cart_item", name=item["name"], price=format_price(item["price"]))
        total += item["price"] * item["quantity"]
    text += get_text(lang, "cart_total", total=format_price(total))
    await callback.message.edit_text(
        text,
        reply_markup=cart_kb(lang, items),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("rm_cart:"))
async def cb_rm_cart(callback: CallbackQuery, lang: str):
    product_id = int(callback.data.split(":")[1])
    await remove_from_cart(callback.from_user.id, product_id)
    items = await get_cart(callback.from_user.id)
    if not items:
        await callback.message.edit_text(
            get_text(lang, "cart_empty"),
            reply_markup=back_main_kb(lang),
            parse_mode="HTML",
        )
    else:
        text = get_text(lang, "cart_title")
        total = 0
        for item in items:
            text += get_text(lang, "cart_item", name=item["name"], price=format_price(item["price"]))
            total += item["price"] * item["quantity"]
        text += get_text(lang, "cart_total", total=format_price(total))
        await callback.message.edit_text(
            text,
            reply_markup=cart_kb(lang, items),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(F.data == "clear_cart")
async def cb_clear_cart(callback: CallbackQuery, lang: str):
    await clear_cart(callback.from_user.id)
    await callback.message.edit_text(
        get_text(lang, "cart_cleared"),
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "checkout")
async def cb_checkout(callback: CallbackQuery, lang: str):
    items = await get_cart(callback.from_user.id)
    if not items:
        await callback.answer(get_text(lang, "cart_empty"), show_alert=True)
        return
    total = sum(item["price"] * item["quantity"] for item in items)
    await callback.message.edit_text(
        get_text(lang, "choose_payment", total=format_price(total)),
        reply_markup=payment_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pay:"))
async def cb_pay(callback: CallbackQuery, lang: str):
    method = callback.data.split(":")[1]
    items = await get_cart(callback.from_user.id)
    if not items:
        await callback.answer(get_text(lang, "cart_empty"), show_alert=True)
        return
    total = sum(item["price"] * item["quantity"] for item in items)
    order_id = await create_order(callback.from_user.id, items, total, method)
    details = PAYMENT_DETAILS.get(method, "—")
    await callback.message.edit_text(
        get_text(lang, "payment_pending", total=format_price(total), details=details),
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()
    await callback.message.answer(
        get_text(lang, "order_created", order_id=order_id, support=SUPPORT_USERNAME),
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("buy_now:"))
async def cb_buy_now(callback: CallbackQuery, lang: str):
    product_id = int(callback.data.split(":")[1])
    product = await get_product(product_id)
    if not product or product["stock"] == 0:
        await callback.answer(get_text(lang, "out_of_stock"), show_alert=True)
        return
    await add_to_cart(callback.from_user.id, product_id)
    total = product["price"]
    await callback.message.edit_text(
        get_text(lang, "choose_payment", total=format_price(total)),
        reply_markup=payment_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()
