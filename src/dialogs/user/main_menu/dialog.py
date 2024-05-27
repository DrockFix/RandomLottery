from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Start
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.user.main_menu.getters import get_main_text
from src.states.user import MenuUser

main_menu_user = Dialog(
    Window(
        Format("{text}"),
        Row(
            SwitchTo("Розыгрыши",
                     id="events",
                     state=MenuUser.events)
        ),
        Row(
            SwitchTo(
                Const("Помощь"),
                id="help",
                state=MenuUser.help,
            ),
            SwitchTo(
                Const("Контакты"),
                id="contact",
                state=MenuUser.contact,
            ),
        ),
        Row(
            SwitchTo(
                Const("Статистика"),
                id="stat",
                on_click=MenuUser.stat
            )
        ),
        state=MenuUser.main,
        getter=get_main_text,
    ),
    Window(
        Format("Events"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=MenuUser.main),
        state=MenuUser.events

    ),
    Window(
        Format("Help"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=MenuUser.main),
        state=MenuUser.help
    ),
    Window(
        Format("Contact"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=MenuUser.main),
        state=MenuUser.contact,
    ),
    Window(
        Format("Stat"),
        SwitchTo(Const("🔙 Назад"),
                 id="back_main_menu",
                 state=MenuUser.main),
        state=MenuUser.stat,
    )
)
