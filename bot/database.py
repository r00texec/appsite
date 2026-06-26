import aiosqlite
import asyncio
from datetime import datetime, date
from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY,
                tg_id       INTEGER UNIQUE NOT NULL,
                username    TEXT,
                full_name   TEXT,
                lang        TEXT DEFAULT 'ru',
                balance     INTEGER DEFAULT 0,
                ref_code    TEXT UNIQUE,
                referred_by INTEGER,
                created_at  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS categories (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                slug  TEXT UNIQUE NOT NULL,
                name_ru TEXT NOT NULL,
                name_uz TEXT NOT NULL,
                emoji TEXT DEFAULT '📦',
                sort  INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name        TEXT NOT NULL,
                description TEXT,
                price       INTEGER NOT NULL,
                stock       INTEGER DEFAULT 0,
                is_active   INTEGER DEFAULT 1,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            );

            CREATE TABLE IF NOT EXISTS cart (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity   INTEGER DEFAULT 1,
                UNIQUE(user_id, product_id)
            );

            CREATE TABLE IF NOT EXISTS orders (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id        INTEGER NOT NULL,
                total          INTEGER NOT NULL,
                payment_method TEXT,
                status         TEXT DEFAULT 'pending',
                created_at     TEXT DEFAULT (datetime('now')),
                updated_at     TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id   INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                name       TEXT NOT NULL,
                price      INTEGER NOT NULL,
                quantity   INTEGER DEFAULT 1,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            );
        """)
        await db.commit()
        await _seed_categories(db)
        await _seed_products(db)


async def _seed_categories(db):
    cats = [
        ("premium", "💎 Premium аккаунты", "💎 Premium akkauntlar", "💎", 1),
        ("og",      "✨ OG аккаунты",      "✨ OG akkauntlar",      "✨", 2),
        ("fresh",   "🆕 Свежие аккаунты",  "🆕 Yangi akkauntlar",   "🆕", 3),
        ("aged",    "📅 Старые аккаунты",   "📅 Eski akkauntlar",    "📅", 4),
        ("subs",    "👥 С подписчиками",    "👥 Obunachili",          "👥", 5),
    ]
    for slug, name_ru, name_uz, emoji, sort in cats:
        await db.execute(
            "INSERT OR IGNORE INTO categories (slug, name_ru, name_uz, emoji, sort) VALUES (?,?,?,?,?)",
            (slug, name_ru, name_uz, emoji, sort),
        )
    await db.commit()


async def _seed_products(db):
    cursor = await db.execute("SELECT COUNT(*) FROM products")
    row = await cursor.fetchone()
    if row[0] > 0:
        return
    products = [
        (1, "Premium аккаунт #1", "Telegram Premium 12 месяцев, 2FA отключена, +7 номер", 150_000, 5),
        (1, "Premium аккаунт #2", "Telegram Premium 6 месяцев, отлежанный, UZ номер",      90_000, 3),
        (2, "OG @username аккаунт", "Редкий короткий юзернейм 4 символа, 2018 года",       500_000, 1),
        (2, "OG аккаунт 5 симв.",   "Красивый @username 5 символов, 2019 года",            250_000, 2),
        (3, "Свежий аккаунт",      "Новый аккаунт, +998 номер, без ограничений",            25_000, 10),
        (3, "Свежий EU аккаунт",   "Новый аккаунт, европейский номер",                     30_000, 8),
        (4, "Аккаунт 2020 года",   "Отлежанный аккаунт 4 года, есть история",              60_000, 4),
        (4, "Аккаунт 2019 года",   "Старый аккаунт 5 лет, много групп",                    80_000, 3),
        (5, "Аккаунт 1000 подп.",  "1000 реальных подписчиков, канал активен",             120_000, 2),
        (5, "Аккаунт 500 подп.",   "500 реальных подписчиков",                              70_000, 3),
    ]
    await db.executemany(
        "INSERT INTO products (category_id, name, description, price, stock) VALUES (?,?,?,?,?)",
        products,
    )
    await db.commit()


# ── Users ─────────────────────────────────────────────────────────────────────

async def get_or_create_user(tg_id: int, username: str, full_name: str, ref_code_used: str = None):
    import hashlib, random, string
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
        user = await cursor.fetchone()
        if user:
            await db.execute(
                "UPDATE users SET username=?, full_name=? WHERE tg_id=?",
                (username, full_name, tg_id),
            )
            await db.commit()
            return dict(user)
        ref = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        referred_by = None
        if ref_code_used:
            cursor2 = await db.execute(
                "SELECT tg_id FROM users WHERE ref_code=?", (ref_code_used,)
            )
            row = await cursor2.fetchone()
            if row:
                referred_by = row[0]
                await db.execute(
                    "UPDATE users SET balance=balance+5000 WHERE tg_id=?", (row[0],)
                )
        await db.execute(
            "INSERT INTO users (tg_id, username, full_name, ref_code, referred_by) VALUES (?,?,?,?,?)",
            (tg_id, username, full_name, ref, referred_by),
        )
        await db.commit()
        cursor3 = await db.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
        return dict(await cursor3.fetchone())


async def get_user(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def set_user_lang(tg_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET lang=? WHERE tg_id=?", (lang, tg_id))
        await db.commit()


async def get_all_user_ids():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT tg_id FROM users")
        rows = await cursor.fetchall()
        return [r[0] for r in rows]


# ── Categories & Products ─────────────────────────────────────────────────────

async def get_categories():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM categories ORDER BY sort")
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_products_by_category(category_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM products WHERE category_id=? AND is_active=1 ORDER BY id",
            (category_id,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_product(product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM products WHERE id=?", (product_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def add_product(category_id, name, description, price, stock):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO products (category_id, name, description, price, stock) VALUES (?,?,?,?,?)",
            (category_id, name, description, price, stock),
        )
        await db.commit()
        return cursor.lastrowid


async def delete_product(product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM products WHERE id=?", (product_id,))
        await db.commit()


async def get_all_products():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT p.*, c.name_ru as cat_name FROM products p "
            "JOIN categories c ON p.category_id=c.id ORDER BY p.id"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


# ── Cart ──────────────────────────────────────────────────────────────────────

async def get_cart(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT c.*, p.name, p.price, p.stock FROM cart c "
            "JOIN products p ON c.product_id=p.id WHERE c.user_id=?",
            (user_id,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def add_to_cart(user_id: int, product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id FROM cart WHERE user_id=? AND product_id=?", (user_id, product_id)
        )
        exists = await cursor.fetchone()
        if exists:
            return False
        await db.execute(
            "INSERT INTO cart (user_id, product_id) VALUES (?,?)", (user_id, product_id)
        )
        await db.commit()
        return True


async def remove_from_cart(user_id: int, product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM cart WHERE user_id=? AND product_id=?", (user_id, product_id)
        )
        await db.commit()


async def clear_cart(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM cart WHERE user_id=?", (user_id,))
        await db.commit()


# ── Orders ────────────────────────────────────────────────────────────────────

async def create_order(user_id: int, cart_items: list, total: int, payment_method: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO orders (user_id, total, payment_method, status) VALUES (?,?,?,'pending')",
            (user_id, total, payment_method),
        )
        order_id = cursor.lastrowid
        for item in cart_items:
            await db.execute(
                "INSERT INTO order_items (order_id, product_id, name, price, quantity) VALUES (?,?,?,?,?)",
                (order_id, item["product_id"], item["name"], item["price"], item["quantity"]),
            )
            await db.execute(
                "UPDATE products SET stock=MAX(0, stock-1) WHERE id=?", (item["product_id"],)
            )
        await db.execute("DELETE FROM cart WHERE user_id=?", (user_id,))
        await db.commit()
        return order_id


async def get_user_orders(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM orders WHERE user_id=? ORDER BY id DESC", (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_all_orders():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT o.*, u.username, u.full_name FROM orders o "
            "JOIN users u ON o.user_id=u.tg_id ORDER BY o.id DESC LIMIT 50"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def update_order_status(order_id: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET status=?, updated_at=datetime('now') WHERE id=?",
            (status, order_id),
        )
        await db.commit()


# ── Statistics ────────────────────────────────────────────────────────────────

async def get_stats():
    today = date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        users = (await (await db.execute("SELECT COUNT(*) FROM users")).fetchone())[0]
        orders = (await (await db.execute("SELECT COUNT(*) FROM orders")).fetchone())[0]
        completed = (await (await db.execute(
            "SELECT COUNT(*) FROM orders WHERE status='completed'"
        )).fetchone())[0]
        revenue_row = await (await db.execute(
            "SELECT COALESCE(SUM(total),0) FROM orders WHERE status='completed'"
        )).fetchone()
        revenue = revenue_row[0]
        today_users = (await (await db.execute(
            "SELECT COUNT(*) FROM users WHERE created_at>=?", (today,)
        )).fetchone())[0]
        return {
            "users": users,
            "orders": orders,
            "completed": completed,
            "revenue": revenue,
            "today_users": today_users,
        }


async def get_ref_count(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users WHERE referred_by=?", (tg_id,)
        )
        row = await cursor.fetchone()
        return row[0]


async def get_user_stats(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        orders_count = (await (await db.execute(
            "SELECT COUNT(*) FROM orders WHERE user_id=?", (tg_id,)
        )).fetchone())[0]
        spent_row = await (await db.execute(
            "SELECT COALESCE(SUM(total),0) FROM orders WHERE user_id=? AND status='completed'",
            (tg_id,),
        )).fetchone()
        return {"orders_count": orders_count, "spent": spent_row[0]}
