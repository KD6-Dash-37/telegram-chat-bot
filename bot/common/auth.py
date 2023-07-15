#auth.py
from telegram import Update


async def verify_user(update: Update, auth_users: list[int]) -> bool:

    if update.effective_user.id in auth_users:

        return True

    return False
