import asyncio

from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()
# argon2-cffi is a C extension — GIL is released during hashing, so threads are sufficient


async def get_password_hash(password: str) -> str:
    return await asyncio.to_thread(_password_hash.hash, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(_password_hash.verify, plain_password, hashed_password)
