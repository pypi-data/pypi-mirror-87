import contextlib
import hashlib
import logging
from functools import wraps
from typing import Callable, Iterable, Mapping, Optional

from django.core.cache import cache
from django.utils.encoding import force_bytes
from django_redis import get_redis_connection
from redis.exceptions import LockError


logger = logging.getLogger(__name__)

NO_CACHE = object()
DEFAULT_LOCK_TIMEOUT = 10
KeyMakerType = Callable[[Iterable, Mapping], str]


def redis_client(write=True):
    return get_redis_connection(write=write)


def _make_key_id(*args, **kwargs):
    return ':'.join((
        *(str(value) for value in args),
        *(f'{key}={value}' for key, value in kwargs.items())
    ))


def _hash(key):
    return hashlib.md5(force_bytes(key)).hexdigest()  # noqa: S303


@contextlib.contextmanager
def use_lock(key, timeout=DEFAULT_LOCK_TIMEOUT, blocking_timeout=None):
    """
    If blocking_timeout is specified, will proceed after
    blocking_timeout even without the lock obtained.
    Check the return value and abort if needed.
    """

    if timeout is None:  # Prevent locks without timeout set - it is too dangerous if the process dies
        timeout = DEFAULT_LOCK_TIMEOUT

    lock = redis_client().lock(f'use_lock:{key}', timeout=timeout, blocking_timeout=blocking_timeout)
    acquired = lock.acquire(blocking=True)
    try:
        yield acquired
    finally:
        if not acquired:
            return

        # Don't want failed lock release to break the whole application
        try:
            lock.release()
        except LockError as exc:
            logger.exception(str(exc))


def with_lock(
    key,
    timeout,
    blocking_timeout=None,
    proceed_without_lock=False,
):
    """
    If blocking_timeout is specified, and the lock is not obtained after blocking_timeout,
    behavior will depend on the proceed_without_lock.
    """

    def factory(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            with use_lock(key, timeout, blocking_timeout) as acquired:
                if not (acquired or proceed_without_lock):
                    return None
                return func(*args, **kwargs)

        return decorator

    return factory


def ensure_single(key, timeout):
    """Ensure function executes only single time simultaneously, other executions are aborted immediately"""
    return with_lock(key, timeout, blocking_timeout=0, proceed_without_lock=False)


def cache_memoize(
    timeout: Optional[int],
    fresh_after: Optional[int] = 0,
    prefix: Optional[int] = None,
    key_maker: Optional[KeyMakerType] = _make_key_id,
    calculation_time=DEFAULT_LOCK_TIMEOUT,
):
    if timeout is None and fresh_after:
        raise ValueError('fresh_after can only be specified when timeout is set')

    if fresh_after < 0:
        raise ValueError('fresh_after must be positive number')

    def factory(func):
        key_prefix = f'cache_memoize:{prefix or func.__name__}'

        def _make_cache_key(*args, **kwargs):  # noqa: WPS430
            # Allow to provide full key via key_prefix
            if key_maker is None:
                return key_prefix

            cache_key = _hash(key_maker(*args, **kwargs))
            return f'{key_prefix}:{cache_key}'

        @wraps(func)
        def decorator(*args, **kwargs):
            cache_key = _make_cache_key(*args, **kwargs)
            result = cache.get(cache_key, NO_CACHE)

            semi_fresh = False
            if result is not NO_CACHE:
                semi_fresh = fresh_after and (cache.ttl(cache_key) < fresh_after)
                if not semi_fresh:
                    # Still absolutely fresh
                    return result

            # Let one process to recalculate and others to return semi-fresh value (if exists),
            # else wait for calculation
            blocking_timeout = 0 if semi_fresh else None
            with use_lock(cache_key, timeout=calculation_time, blocking_timeout=blocking_timeout) as acquired:
                if not acquired:
                    # Only possible with semi_fresh = True (blocking_timeout = 0, no waiting for the lock)
                    return result

                if not semi_fresh:
                    # Check value wasn't calculated while we were waiting for the lock
                    result = cache.get(cache_key, NO_CACHE)

                # This process was selected for value calculation
                if semi_fresh or result is NO_CACHE:
                    result = func(*args, **kwargs)
                    cache.set(cache_key, result, timeout + fresh_after)
            return result

        def set_cache(value, *args, **kwargs):  # noqa: WPS430
            cache_key = _make_cache_key(*args, **kwargs)
            return cache.set(cache_key, value, timeout + fresh_after)

        def invalidate(*args, **kwargs):  # noqa: WPS430
            cache_key = _make_cache_key(*args, **kwargs)
            return cache.delete(cache_key)

        decorator.set_cache = set_cache
        decorator.invalidate = invalidate
        return decorator

    return factory
