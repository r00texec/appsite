from aiogram import Router, F
from aiogram.types import CallbackQuery
from locales import get_text
from keyboards.catalog import cabinet_kb, orders_kb
from keyboards.main_menu import back_main_kb
from database import get_user_orders, get_ref_count, get_user_stats
from utils.helpers import format_price, format_date, ORDER_STATUS_MAP

router = Router()


@router.callback_query(F.data == "cabinet")
async def cb_cabinet(callback: CallbackQuery, lang: str, user: dict):
    stats = await get_user_stats(callback.from_user.id)
    ref_count = await get_ref_count(callback.from_user.id)
    name = user.get("full_name") or callback.from_user.full_name
    reg_date = format_date(user.get("created_at", ""))
    text = get_text(
        lang, "cabinet_title",
        user_id=callback.from_user.id,
        name=name,
        reg_date=reg_date,
        orders_count=stats["orders_count"],
        spent=format_price(stats["spent"]),
        ref_code=user.get("ref_code", "—"),
        ref_count=ref_count,
    )
    balance_line = "\n" + get_text(lang, "balance", balance=format_price(user.get("balance", 0)))
    await callback.message.edit_text(
        text + balance_line,
        reply_markup=cabinet_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "my_orders")
async def cb_my_orders(callback: CallbackQuery, lang: str):
    orders = await get_user_orders(callback.from_user.id)
    if not orders:
        await callback.message.edit_text(
            get_text(lang, "orders_title") + "\n\n" + get_text(lang, "orders_empty"),
            reply_markup=orders_kb(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return
    text = get_text(lang, "orders_title")
    for o in orders[:10]:
        status_key, status_icon = ORDER_STATUS_MAP.get(o["status"], ("order_status_pending", "🕐"))
        status_text = status_icon + " " + get_text(lang, status_key)
        text += get_text(
            lang, "order_item",
            order_id=o["id"],
            date=format_date(o["created_at"]),
            total=format_price(o["total"]),
            status=status_text,
        )
    await callback.message.edit_text(
        text,
        reply_markup=orders_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "ref_link")
async def cb_ref_link(callback: CallbackQuery, lang: str, user: dict):
    ref_count = await get_ref_count(callback.from_user.id)
    bot_info = await callback.bot.get_me()
    link = f"https://t.me/{bot_info.username}?start=ref_{user.get('ref_code', '')}"
    text = get_text(lang, "ref_link_text", link=link, count=ref_count)
    await callback.message.edit_text(
        text,
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "top_up")
async def cb_top_up(callback: CallbackQuery, lang: str):
    await callback.answer(get_text(lang, "coming_soon"), show_alert=True)
