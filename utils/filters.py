from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.config import admin_id

class IsAdmin(BaseFilter):
    def __init__(self):
        self.user_id = admin_id
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self.user_id
