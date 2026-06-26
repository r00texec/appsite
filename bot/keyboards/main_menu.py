from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from locales import get_text


def main_menu_kb(lang: str) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_catalog"), callback_data="catalog"),
            InlineKeyboardButton(text=t("btn_cabinet"), callback_data="cabinet"),
        ],
        [
            InlineKeyboardButton(text=t("btn_cart"), callback_data="cart"),
            InlineKeyboardButton(text=t("btn_orders"), callback_data="my_orders"),
        ],
        [
            InlineKeyboardButton(text=t("btn_support"), callback_data="support"),
            InlineKeyboardButton(text=t("btn_about"), callback_data="about"),
        ],
        [
            InlineKeyboardButton(text=t("btn_language"), callback_data="language"),
        ],
    ])


def language_kb(lang: str) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru"),
            InlineKeyboardButton(text="🇺🇿 O'zbek",  callback_data="set_lang:uz"),
        ],
        [InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")],
    ])


def back_main_kb(lang: str) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")]
    ])


def support_kb(lang: str, support_url: str) -> InlineKeyboardMarkup:
    t = lambda key: get_text(lang, key)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_write_support"), url=support_url)],
        [InlineKeyboardButton(text=t("back_main"), callback_data="main_menu")],
    ])
