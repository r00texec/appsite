from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from locales import get_text


def admin_menu_kb(lang: str) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("admin_btn_products"), callback_data="adm:products"),
            InlineKeyboardButton(text=t("admin_btn_orders"),   callback_data="adm:orders"),
        ],
        [
            InlineKeyboardButton(text=t("admin_btn_users"),    callback_data="adm:users"),
            InlineKeyboardButton(text=t("admin_btn_stats"),    callback_data="adm:stats"),
        ],
        [
            InlineKeyboardButton(text=t("admin_btn_broadcast"), callback_data="adm:broadcast"),
        ],
        [InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")],
    ])


def admin_products_kb(lang: str, products: list) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    rows = []
    for p in products:
        stock_icon = "✅" if p["stock"] > 0 else "❌"
        rows.append([
            InlineKeyboardButton(
                text=f"{stock_icon} {p['name'][:25]} ({p['price']:,} UZS)",
                callback_data=f"adm:prod_view:{p['id']}",
            )
        ])
    rows.append([InlineKeyboardButton(text=t("admin_btn_add_product"), callback_data="adm:add_product")])
    rows.append([InlineKeyboardButton(text=t("back"), callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_product_actions_kb(lang: str, product_id: int) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("admin_btn_delete_product"), callback_data=f"adm:del_prod:{product_id}"),
        ],
        [InlineKeyboardButton(text=t("back"), callback_data="adm:products")],
    ])


def admin_categories_kb(lang: str, categories: list) -> InlineKeyboardMarkup:
    rows = []
    for cat in categories:
        name = cat["name_ru"] if lang == "ru" else cat["name_uz"]
        rows.append([InlineKeyboardButton(
            text=name,
            callback_data=f"adm:pick_cat:{cat['id']}",
        )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_orders_kb(lang: str, orders: list) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    rows = []
    for o in orders[:20]:
        rows.append([InlineKeyboardButton(
            text=f"#{o['id']} — {o['total']:,} UZS [{o['status']}]",
            callback_data=f"adm:order:{o['id']}",
        )])
    rows.append([InlineKeyboardButton(text=t("back"), callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_order_actions_kb(lang: str, order_id: int) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"adm:confirm_order:{order_id}"),
            InlineKeyboardButton(text="❌ Отменить",    callback_data=f"adm:cancel_order:{order_id}"),
        ],
        [InlineKeyboardButton(text="✅ Завершить",       callback_data=f"adm:complete_order:{order_id}")],
        [InlineKeyboardButton(text=t("back"),            callback_data="adm:orders")],
    ])
