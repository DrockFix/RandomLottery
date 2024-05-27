import os

from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from src.filters.chat_types import IsAdmin, ChatTypeFilter
from src.states.admin import AdminMenu

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminMenu.menu, mode=StartMode.RESET_STACK)
    # await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


