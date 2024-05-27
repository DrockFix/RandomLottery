from aiogram import Router, types, Bot
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION, PROMOTED_TRANSITION
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession


from ..filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))

admins = set()


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins = await bot.get_chat_administrators(chat_id)
    admins = [
        member.user.id
        for member in admins
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins
    if message.from_user.id in admins:
        await message.delete()

