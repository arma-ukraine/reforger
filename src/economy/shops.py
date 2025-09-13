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
    # Weapons.
    Item.BAYONET,
    Item.PM,
    Item.DOUBLE_BARREL_SAWN_OFF,
    Item.DOUBLE_BARREL_SHOTGUN,
    Item.REMINGTON_870,
    # Ammo.
    Item.AMMO_PM_9x18,
    Item.AMMO_12GA_SHELL,
    # Medicine.
    Item.MEDKIT_AI2,
    Item.MORPHINE,
    Item.BANDAGE,
    Item.TOURNIQUET,
    Item.SALINE_BAG,
    # Equipment
    Item.MAP,
    Item.FLASHLIGHT,
    Item.COMPASS,
    Item.PDA,
    Item.ATMOS,
)

POSTMAN_INTEL_BUY_SELL = (
    Item.FLOPPY,
    Item.DOCS_1,
    Item.DOCS_2,
    Item.DOCS_3,
    Item.DOCS_4,
    Item.DOCS_5,
    Item.DOCS_SECRETS,
    Item.HDD,
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
        buy_items=POSTMAN_BUY_SELL
        + (
            # Containers.
            Item.CANTEEN_EMPTY,
            Item.CONSERVA_THROW,
            # Gasmasks.
            Item.GASMASK_GP5,
            # Backpacks.
            Item.BACKPACK_RUKZAK,
            Item.BACKPACK_KOLOBOK,
            # Equipment.
            Item.COMPASS,
            Item.FLASHLIGHT,
            Item.MAP,
        ),
        sell_items=POSTMAN_BUY_SELL,
        sell_multiplier=0.2,
    )

    POSTMAN_INTEL = ShopConfig(
        name="PostmanIntel",
        buy_items=POSTMAN_INTEL_BUY_SELL,
        sell_items=POSTMAN_INTEL_BUY_SELL,
        buy_multiplier=5,
    )

    WATER = ShopConfig(
        name="Water",
        craft_recipes=(Recipe.FILL_CANTEEN,),
    )

    COOKING = ShopConfig(
        name="Cooking",
        craft_recipes=(Recipe.PRESERVE_MEAT,),
    )
