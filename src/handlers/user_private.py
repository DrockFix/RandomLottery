from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram_dialog import StartMode, DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from ..filters.chat_types import ChatTypeFilter
from ..states.user import MenuUser

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(MenuUser.main, mode=StartMode.RESET_STACK)
