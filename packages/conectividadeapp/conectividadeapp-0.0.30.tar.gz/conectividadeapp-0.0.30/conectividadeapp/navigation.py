from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices


# Declare a list of menu items to be added to NetBox's built-in naivgation menu
menu_items = (

    # Each PluginMenuItem instance renders a custom menu item. Each item may have zero or more buttons.
    PluginMenuItem(
        link='plugins:conectividadeapp:list',
        link_text='ConectividadePLUG',
        permissions=[],

    ),
    PluginMenuItem(
        link='plugins:conectividadeapp:actor_list',
        link_text='Actors',
        permissions=[],
        buttons=(
            PluginMenuButton(
                link='plugins:conectividadeapp:addactor',
                title='Add a new actor',
                icon_class='fa fa-plus',
                color=ButtonColorChoices.GREEN,
                permissions=[]
            ),
        )
    ),
    PluginMenuItem(
        link='plugins:conectividadeapp:list',
        link_text='Activities',
        permissions=[],
        buttons=(
            PluginMenuButton(
                link='plugins:conectividadeapp:searchdevice',
                title='Assign an activity to a device',
                icon_class='fa fa-plus',
                color=ButtonColorChoices.GREEN,
                permissions=[]
            ),
        )
    ),
)
