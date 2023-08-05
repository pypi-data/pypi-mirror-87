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

)
