from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from locales import get_text


def categories_kb(lang: str, categories: list) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    rows = []
    for i in range(0, len(categories), 2):
        row = []
        for cat in categories[i:i+2]:
            name = cat["name_ru"] if lang == "ru" else cat["name_uz"]
            row.append(InlineKeyboardButton(
                text=name,
                callback_data=f"cat:{cat['id']}",
            ))
        rows.append(row)
    rows.append([InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def products_kb(lang: str, products: list, category_id: int) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    rows = []
    for p in products:
        label = f"{p['name']} — {p['price']:,} UZS"
        rows.append([InlineKeyboardButton(
            text=label[:50],
            callback_data=f"product:{p['id']}",
        )])
    rows.append([InlineKeyboardButton(text=t("back"), callback_data="catalog")])
    rows.append([InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_detail_kb(lang: str, product: dict) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    rows = []
    if product["stock"] > 0:
        rows.append([
            InlineKeyboardButton(text=t("add_to_cart"), callback_data=f"add_cart:{product['id']}"),
            InlineKeyboardButton(text=t("buy_now"),     callback_data=f"buy_now:{product['id']}"),
        ])
    else:
        rows.append([InlineKeyboardButton(text=t("out_of_stock"), callback_data="noop")])
    rows.append([InlineKeyboardButton(text=t("back"), callback_data=f"cat:{product['category_id']}")])
    rows.append([InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def cart_kb(lang: str, items: list) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    rows = []
    for item in items:
        rows.append([InlineKeyboardButton(
            text=f"🗑 {item['name'][:30]}",
            callback_data=f"rm_cart:{item['product_id']}",
        )])
    rows.append([
        InlineKeyboardButton(text=t("cart_checkout"), callback_data="checkout"),
        InlineKeyboardButton(text=t("cart_clear"),    callback_data="clear_cart"),
    ])
    rows.append([InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def payment_kb(lang: str) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("pay_click"), callback_data="pay:click"),
            InlineKeyboardButton(text=t("pay_payme"), callback_data="pay:payme"),
        ],
        [
            InlineKeyboardButton(text=t("pay_uzcard"), callback_data="pay:uzcard"),
            InlineKeyboardButton(text=t("pay_humo"),   callback_data="pay:humo"),
        ],
        [InlineKeyboardButton(text=t("pay_crypto"), callback_data="pay:crypto")],
        [InlineKeyboardButton(text=t("back_main"),  callback_data="main_menu")],
    ])


def cabinet_kb(lang: str) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_my_orders"), callback_data="my_orders"),
            InlineKeyboardButton(text=t("btn_ref_link"),  callback_data="ref_link"),
        ],
        [InlineKeyboardButton(text=t("btn_top_up"), callback_data="top_up")],
        [InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")],
    ])


def orders_kb(lang: str) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("back"), callback_data="cabinet")],
        [InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")],
    ])
