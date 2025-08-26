"""
Simple shop configuration using NamedTuples.
"""

from enum import Enum
from typing import NamedTuple, Tuple

from src.economy.items import Item
from src.economy.recipes import Recipe


class ShopConfig(NamedTuple):
    """Complete shop configuration"""

    name: str
    buy_items: Tuple[
        Item, ...
    ] = ()  # Items available for direct purchase (uses base_price)
    sell_items: Tuple[Item, ...] = ()  # Items accepted for selling
    craft_recipes: Tuple[Recipe, ...] = ()  # Available crafting recipes at this station
    buy_multiplier: float = 1.0
    sell_multiplier: float = 1.0
    crafting_fee: int = 0  # Additional fee added to crafting recipes


CURRENCY_BUY_SELL = (
    Item.UAK_1,
    Item.UAK_5,
    Item.UAK_10,
    Item.UAK_50,
    Item.UAK_100,
    Item.UAK_500,
    Item.UAK_1000,
    Item.UAK_5000,
)

POSTMAN_BUY_SELL = (
    # Ammo.
    Item.AMMO_12GA_SHELL,
    # Consumnables.
    Item.CANTEEN_EMPTY,
    Item.CONSERVA_THROW,
    # Weapons.
    Item.REMINGTON_870,
    Item.DOUBLE_BARREL_SHOTGUN,
    Item.DOUBLE_BARREL_SAWN_OFF,
    # Apparel.
    Item.GASMASK_GP5,
    Item.GORKA_GREEN,
    Item.GORKA_BROWN,
    Item.GORKA_DARKBROWN,
    Item.GORKA_CAMO_DARK,
    # Equipment.
    Item.COMPASS,
    Item.FLASHLIGHT,
    Item.MAP,
)


class Shop(Enum):
    """Shop configurations with direct ShopConfig instances"""

    CURRENCY = ShopConfig(
        name="Currency",
        buy_items=CURRENCY_BUY_SELL,
        sell_items=CURRENCY_BUY_SELL,
    )

    POSTMAN = ShopConfig(
        name="Postman",
        buy_items=POSTMAN_BUY_SELL + (Item.WALLET,),
        sell_items=POSTMAN_BUY_SELL + (Item.FLOPPY,),
        sell_multiplier=0.3,
    )

    WATER = ShopConfig(
        name="Water",
        craft_recipes=(Recipe.FILL_CANTEEN,),
    )

    COOKING = ShopConfig(
        name="Cooking",
        craft_recipes=(Recipe.PRESERVE_MEAT,),
    )
