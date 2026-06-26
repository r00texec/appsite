from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from locales import get_text
from keyboards.admin import (
    admin_menu_kb, admin_products_kb, admin_categories_kb,
    admin_orders_kb, admin_order_actions_kb, admin_product_actions_kb,
)
from keyboards.main_menu import back_main_kb
from database import (
    get_stats, get_all_orders, get_all_user_ids, get_categories,
    add_product, get_all_products, get_product, delete_product,
    update_order_status,
)
from utils.helpers import format_price
from config import ADMIN_IDS

router = Router()


class AddProductFSM(StatesGroup):
    name = State()
    description = State()
    price = State()
    stock = State()
    category = State()


class BroadcastFSM(StatesGroup):
    text = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ── Admin panel ───────────────────────────────────────────────────────────────

@router.callback_query(F.data == "adm:stats")
async def cb_adm_stats(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    stats = await get_stats()
    text = get_text(
        lang, "admin_stats",
        users=stats["users"],
        orders=stats["orders"],
        completed=stats["completed"],
        revenue=format_price(stats["revenue"]),
        today_users=stats["today_users"],
    )
    from keyboards.admin import admin_menu_kb
    await callback.message.edit_text(text, reply_markup=admin_menu_kb(lang), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "adm:orders")
async def cb_adm_orders(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    orders = await get_all_orders()
    await callback.message.edit_text(
        get_text(lang, "admin_orders_list"),
        reply_markup=admin_orders_kb(lang, orders),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:order:"))
async def cb_adm_order_view(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    order_id = int(callback.data.split(":")[2])
    orders = await get_all_orders()
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        await callback.answer(get_text(lang, "not_found"))
        return
    text = (
        f"📋 <b>Заказ #{order['id']}</b>\n"
        f"👤 Пользователь: {order.get('full_name')} (@{order.get('username')})\n"
        f"💰 Сумма: <code>{format_price(order['total'])}</code> UZS\n"
        f"💳 Способ: {order.get('payment_method', '—')}\n"
        f"📊 Статус: {order['status']}\n"
        f"📅 Дата: {order['created_at']}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=admin_order_actions_kb(lang, order_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:confirm_order:"))
async def cb_adm_confirm_order(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    order_id = int(callback.data.split(":")[2])
    await update_order_status(order_id, "paid")
    await callback.answer(get_text(lang, "admin_order_confirmed", order_id=order_id), show_alert=True)
    orders = await get_all_orders()
    await callback.message.edit_text(
        get_text(lang, "admin_orders_list"),
        reply_markup=admin_orders_kb(lang, orders),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("adm:cancel_order:"))
async def cb_adm_cancel_order(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    order_id = int(callback.data.split(":")[2])
    await update_order_status(order_id, "cancelled")
    await callback.answer(get_text(lang, "admin_order_cancelled", order_id=order_id), show_alert=True)
    orders = await get_all_orders()
    await callback.message.edit_text(
        get_text(lang, "admin_orders_list"),
        reply_markup=admin_orders_kb(lang, orders),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("adm:complete_order:"))
async def cb_adm_complete_order(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    order_id = int(callback.data.split(":")[2])
    await update_order_status(order_id, "completed")
    await callback.answer("✅ Заказ завершён!", show_alert=True)
    orders = await get_all_orders()
    await callback.message.edit_text(
        get_text(lang, "admin_orders_list"),
        reply_markup=admin_orders_kb(lang, orders),
        parse_mode="HTML",
    )


# ── Products management ───────────────────────────────────────────────────────

@router.callback_query(F.data == "adm:products")
async def cb_adm_products(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    products = await get_all_products()
    await callback.message.edit_text(
        get_text(lang, "admin_products_list"),
        reply_markup=admin_products_kb(lang, products),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:prod_view:"))
async def cb_adm_prod_view(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    product_id = int(callback.data.split(":")[2])
    product = await get_product(product_id)
    if not product:
        await callback.answer(get_text(lang, "not_found"))
        return
    text = (
        f"📦 <b>{product['name']}</b>\n"
        f"📋 {product['description']}\n"
        f"💰 <code>{format_price(product['price'])}</code> UZS\n"
        f"📦 Склад: {product['stock']} шт."
    )
    await callback.message.edit_text(
        text,
        reply_markup=admin_product_actions_kb(lang, product_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:del_prod:"))
async def cb_adm_del_prod(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    product_id = int(callback.data.split(":")[2])
    await delete_product(product_id)
    await callback.answer(get_text(lang, "product_deleted"), show_alert=True)
    products = await get_all_products()
    await callback.message.edit_text(
        get_text(lang, "admin_products_list"),
        reply_markup=admin_products_kb(lang, products),
        parse_mode="HTML",
    )


# ── Add product FSM ───────────────────────────────────────────────────────────

@router.callback_query(F.data == "adm:add_product")
async def cb_adm_add_product(callback: CallbackQuery, lang: str, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    await state.set_state(AddProductFSM.name)
    await callback.message.answer(get_text(lang, "admin_ask_product_name"))
    await callback.answer()


@router.message(AddProductFSM.name)
async def fsm_product_name(message: Message, lang: str, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProductFSM.description)
    await message.answer(get_text(lang, "admin_ask_product_desc"))


@router.message(AddProductFSM.description)
async def fsm_product_desc(message: Message, lang: str, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProductFSM.price)
    await message.answer(get_text(lang, "admin_ask_product_price"))


@router.message(AddProductFSM.price)
async def fsm_product_price(message: Message, lang: str, state: FSMContext):
    try:
        price = int(message.text.replace(" ", "").replace(",", ""))
    except ValueError:
        await message.answer("❌ Введите число!")
        return
    await state.update_data(price=price)
    await state.set_state(AddProductFSM.stock)
    await message.answer(get_text(lang, "admin_ask_product_stock"))


@router.message(AddProductFSM.stock)
async def fsm_product_stock(message: Message, lang: str, state: FSMContext):
    try:
        stock = int(message.text)
    except ValueError:
        await message.answer("❌ Введите число!")
        return
    await state.update_data(stock=stock)
    await state.set_state(AddProductFSM.category)
    cats = await get_categories()
    await message.answer(
        get_text(lang, "admin_ask_product_cat"),
        reply_markup=admin_categories_kb(lang, cats),
    )


@router.callback_query(AddProductFSM.category, F.data.startswith("adm:pick_cat:"))
async def fsm_product_cat(callback: CallbackQuery, lang: str, state: FSMContext):
    cat_id = int(callback.data.split(":")[2])
    data = await state.get_data()
    await state.clear()
    product_id = await add_product(cat_id, data["name"], data["description"], data["price"], data["stock"])
    await callback.message.edit_text(
        get_text(lang, "admin_product_added", name=data["name"]),
        parse_mode="HTML",
    )
    await callback.answer()


# ── Users ─────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "adm:users")
async def cb_adm_users(callback: CallbackQuery, lang: str):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    user_ids = await get_all_user_ids()
    await callback.message.edit_text(
        get_text(lang, "admin_users_list", count=len(user_ids)),
        reply_markup=admin_menu_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ── Broadcast ─────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "adm:broadcast")
async def cb_adm_broadcast(callback: CallbackQuery, lang: str, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    await state.set_state(BroadcastFSM.text)
    await callback.message.answer(get_text(lang, "admin_broadcast_ask"))
    await callback.answer()


@router.message(BroadcastFSM.text)
async def fsm_broadcast_text(message: Message, lang: str, state: FSMContext):
    await state.clear()
    user_ids = await get_all_user_ids()
    success = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(uid, message.text, parse_mode="HTML")
            success += 1
        except Exception:
            pass
    await message.answer(
        get_text(lang, "admin_broadcast_done", count=success),
        parse_mode="HTML",
    )
