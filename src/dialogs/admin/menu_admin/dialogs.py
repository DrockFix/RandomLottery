from aiogram_dialog import Dialog, Window

from src.states.admin import AdminMenu

admin_menu = Dialog(
    Window(
        state=AdminMenu.main,
    ),
    Window(

        state=AdminMenu.license
    ),
    Window(
        state=AdminMenu.stat
    ),
    Window(
        state=AdminMenu.dict
    )
)