from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from locales import get_text
from keyboards.main_menu import main_menu_kb, language_kb, back_main_kb, support_kb
from database import set_user_lang
from config import SUPPORT_USERNAME, CHANNEL_ID, ADMIN_IDS
from keyboards.admin import admin_menu_kb

router = Router()


async def send_main_menu(target, lang: str, user=None):
    t = lambda key, **kw: get_text(lang, key, **kw)
    text = t("welcome") + "\n\n" + t("choose_action")
    kb = main_menu_kb(lang)
    if isinstance(target, Message):
        await target.answer(text, reply_markup=kb, parse_mode="HTML")
    elif isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        await target.answer()


@router.message(CommandStart())
async def cmd_start(message: Message, user: dict, lang: str):
    await send_main_menu(message, lang, user)


@router.message(Command("admin"))
async def cmd_admin(message: Message, user: dict, lang: str):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(get_text(lang, "not_admin"))
        return
    await message.answer(
        get_text(lang, "admin_panel"),
        reply_markup=admin_menu_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery, user: dict, lang: str):
    await send_main_menu(callback, lang, user)


@router.callback_query(F.data == "language")
async def cb_language(callback: CallbackQuery, lang: str):
    await callback.message.edit_text(
        get_text(lang, "select_language"),
        reply_markup=language_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_lang:"))
async def cb_set_lang(callback: CallbackQuery, user: dict):
    new_lang = callback.data.split(":")[1]
    await set_user_lang(callback.from_user.id, new_lang)
    text = get_text(new_lang, "lang_set") + "\n\n" + get_text(new_lang, "choose_action")
    await callback.message.edit_text(
        text,
        reply_markup=main_menu_kb(new_lang),
        parse_mode="HTML",
    )
    await callback.answer(get_text(new_lang, "success"))


@router.callback_query(F.data == "support")
async def cb_support(callback: CallbackQuery, lang: str):
    channel = CHANNEL_ID if CHANNEL_ID else "—"
    text = get_text(lang, "support_text", support=SUPPORT_USERNAME, channel=channel)
    url = f"https://t.me/{SUPPORT_USERNAME}"
    await callback.message.edit_text(
        text,
        reply_markup=support_kb(lang, url),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "about")
async def cb_about(callback: CallbackQuery, lang: str):
    await callback.message.edit_text(
        get_text(lang, "about_text"),
        reply_markup=back_main_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin")
async def cb_admin(callback: CallbackQuery, lang: str):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(get_text(lang, "not_admin"), show_alert=True)
        return
    await callback.message.edit_text(
        get_text(lang, "admin_panel"),
        reply_markup=admin_menu_kb(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer()
