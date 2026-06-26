from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from database import get_or_create_user, get_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user = None
        ref_code = None

        if isinstance(event, Message):
            tg_user = event.from_user
            text = event.text or ""
            if text.startswith("/start "):
                parts = text.split()
                if len(parts) > 1 and parts[1].startswith("ref_"):
                    ref_code = parts[1][4:]
        elif isinstance(event, CallbackQuery):
            tg_user = event.from_user

        if tg_user:
            user = await get_or_create_user(
                tg_id=tg_user.id,
                username=tg_user.username or "",
                full_name=tg_user.full_name or "",
                ref_code_used=ref_code,
            )
            data["user"] = user
            data["lang"] = user.get("lang", "ru")
        else:
            data["user"] = None
            data["lang"] = "ru"

        return await handler(event, data)
