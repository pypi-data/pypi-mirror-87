import asyncio
from functools import wraps

from ..backends.interface import Backend
from ..key import get_cache_key, get_cache_key_template, register_template


def auto(
    backend: Backend, prefix: str = "auto",
):
    def decorator(func):
        _key_template = get_cache_key_template(func, key=None, prefix=prefix)
        _key_template_all = get_cache_key_template(func, key="all", prefix=prefix)
        register_template(func, _key_template)

        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            _cache_key = get_cache_key(func, _key_template, args, kwargs)
            _cache_key_all = get_cache_key(func, _key_template_all, args, kwargs)
            count, all_count = asyncio.gather(backend.incr(_cache_key), backend.incr(_cache_key_all),)
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                raise e

        return wrapped_func

    return decorator
