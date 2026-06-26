from aiogram import Router, F
from aiogram.types import CallbackQuery
from locales import get_text
from keyboards.catalog import (
    categories_kb, products_kb, product_detail_kb,
)
from database import get_categories, get_products_by_category, get_product, add_to_cart
from utils.helpers import format_price

router = Router()


@router.callback_query(F.data == "catalog")
async def cb_catalog(callback: CallbackQuery, lang: str):
    cats = await get_categories()
    await callback.message.edit_text(
        get_text(lang, "catalog_title"),
        reply_markup=categories_kb(lang, cats),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cat:"))
async def cb_category(callback: CallbackQuery, lang: str):
    cat_id = int(callback.data.split(":")[1])
    cats = await get_categories()
    cat = next((c for c in cats if c["id"] == cat_id), None)
    if not cat:
        await callback.answer(get_text(lang, "not_found"))
        return
    products = await get_products_by_category(cat_id)
    cat_name = cat["name_ru"] if lang == "ru" else cat["name_uz"]
    text = get_text(lang, "products_in_cat", category=cat_name, count=len(products))
    if not products:
        from keyboards.main_menu import back_main_kb
        await callback.message.edit_text(
            get_text(lang, "no_products"),
            reply_markup=back_main_kb(lang),
            parse_mode="HTML",
        )
    else:
        await callback.message.edit_text(
            text,
            reply_markup=products_kb(lang, products, cat_id),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(F.data.startswith("product:"))
async def cb_product(callback: CallbackQuery, lang: str):
    product_id = int(callback.data.split(":")[1])
    product = await get_product(product_id)
    if not product:
        await callback.answer(get_text(lang, "not_found"))
        return
    text = get_text(
        lang, "product_card",
        name=product["name"],
        description=product["description"] or "—",
        price=format_price(product["price"]),
        stock=product["stock"],
    )
    await callback.message.edit_text(
        text,
        reply_markup=product_detail_kb(lang, product),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("add_cart:"))
async def cb_add_cart(callback: CallbackQuery, lang: str, user: dict):
    product_id = int(callback.data.split(":")[1])
    product = await get_product(product_id)
    if not product:
        await callback.answer(get_text(lang, "not_found"))
        return
    added = await add_to_cart(callback.from_user.id, product_id)
    if added:
        await callback.answer(
            get_text(lang, "added_to_cart", name=product["name"]),
            show_alert=True,
        )
    else:
        await callback.answer(get_text(lang, "already_in_cart"), show_alert=True)
