from .ru import RU
from .uz import UZ

LANGS = {"ru": RU, "uz": UZ}


def get_text(lang: str, key: str, **kwargs) -> str:
    texts = LANGS.get(lang, RU)
    text = texts.get(key, RU.get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text
