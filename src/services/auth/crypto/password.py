import asyncio
from concurrent.futures import ProcessPoolExecutor

from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()
_executor = ProcessPoolExecutor()


def _hash_sync(password: str) -> str:
    return _password_hash.hash(password)


def _verify_sync(plain_password: str, hashed_password: str) -> bool:
    return _password_hash.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, _hash_sync, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, _verify_sync, plain_password, hashed_password)
