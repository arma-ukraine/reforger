"""
Simple enums for shops and items.
"""

from enum import Enum
from typing import NamedTuple

# Recipes are now defined in recipes.py module


class ItemDefinition(NamedTuple):
    prefab_path: str
    base_price: int  # Base price in UAK for direct purchase


class Item(Enum):
    # MARK: Currency
    UAK_1 = ItemDefinition(
        "{1475B3B154A8441C}Prefabs/Items/Moneys/armst_itm_money_1rub.et", 1
    )
    UAK_5 = ItemDefinition(
        "{CC56D3FA7BCF1399}Prefabs/Items/Moneys/armst_itm_money_5rub.et", 5
    )
    UAK_10 = ItemDefinition(
        "{9233C3DE9EB24257}Prefabs/Items/Moneys/armst_itm_money_10rub.et", 10
    )
    UAK_50 = ItemDefinition(
        "{69F7DB51E2DFCEE4}Prefabs/Items/Moneys/armst_itm_money_50rub.et", 50
    )
    UAK_100 = ItemDefinition(
        "{2BFAE99AC771DF8E}Prefabs/Items/Moneys/armst_itm_money_100rub.et", 100
    )
    UAK_500 = ItemDefinition(
        "{F9BCE359095B16BB}Prefabs/Items/Moneys/armst_itm_money_500rub.et", 500
    )
    UAK_1000 = ItemDefinition(
        "{1D5355A64F27521C}Prefabs/Items/Moneys/armst_itm_money_1000rub.et", 1000
    )
    UAK_5000 = ItemDefinition(
        "{2243768D6050B899}Prefabs/Items/Moneys/armst_itm_money_5000rub.et", 5000
    )

    # MARK: Mutant parts
    MUT_BOAR = ItemDefinition(
        "{5DDC31EAA3B77A02}Prefabs/Items/Mut_parts/armst_itm_mut_boar.et", 100
    )

    # MARK: Containers
    CANTEEN_EMPTY = ItemDefinition(
        "{654D80AC7C1E0F80}Prefabs/Items/Food/armst_itm_food_canteen_empty.et", 500
    )
    CONSERVA_THROW = ItemDefinition(
        "{16230D52F5022FAC}Prefabs/Items/bolts/armst_throw_conserva.et", 250
    )

    # MARK: Food
    CANTEEN_WATER = ItemDefinition(
        "{52D3FE1E430900D3}Prefabs/Items/Food/armst_itm_food_canteen_water.et",
        100,
    )
    TUSHONKA_1 = ItemDefinition(
        "{1472B9856B26B931}Prefabs/Items/Food/armst_itm_food_tushonka_1.et",
        200,
    )

    # MARK: Weapons
    REMINGTON_870 = ItemDefinition(
        "{458A4E8CD3590D92}Prefabs/Weapons/Shotguns/Remington 870/BC_Shotgun_Remington_870.et",
        20000,
    )
    DOUBLE_BARREL_SHOTGUN = ItemDefinition(
        "{3C4FB3D9D54B46DF}Prefabs/Weapons/Shotguns/Double Barrel/BC_Shotgun_Double_Barrel_760mm.et",
        3000,
    )
    DOUBLE_BARREL_SAWN_OFF = ItemDefinition(
        "{E7A3BA1F06C057FF}Prefabs/Weapons/Shotguns/Double Barrel/BC_Shotgun_Double_Barrel_Sawn_Off.et",
        1500,
    )

    # MARK: Ammo
    AMMO_12GA_SHELL = ItemDefinition(
        "{B0DFDF7AAA9C5D39}Prefabs/Weapons/Magazines/BC_Shell_12ga_Buckshot.et", 25
    )

    # MARK: Armor
    SOVIET_JACKET = ItemDefinition(
        "{F5C7F3A66723915A}Prefabs/New_Equipment/Jackets/armst_jacket_soviet_army.et",
        3500,
    )
    GORKA_GREEN = ItemDefinition(
        "{20491CABD61C4846}Prefabs/New_Equipment/Jackets/gorka/armst_jacket_gorka_green.et",
        8000,
    )
    GORKA_BROWN = ItemDefinition(
        "{21D031F8E0C0A646}Prefabs/New_Equipment/Jackets/gorka/armst_jacket_gorka_brown.et",
        8000,
    )
    GORKA_DARKBROWN = ItemDefinition(
        "{924D262DBDCB4950}Prefabs/New_Equipment/Jackets/gorka/armst_jacket_gorka_darkbrown.et",
        8000,
    )
    GORKA_CAMO_DARK = ItemDefinition(
        "{7F934FAC7B4676A5}Prefabs/New_Equipment/Jackets/gorka/camo/armst_jacket_gorka_camo_dark.et",
        8000,
    )

    # MARK: GasMasks
    GASMASK_GP5 = ItemDefinition(
        "{D7B25AAE6F51908A}Prefabs/New_Equipment/Gasmasks/armst_gasmask_gp5.et",
        2000,
    )

    # MARK: Equipment
    WALLET = ItemDefinition("{B0E67230AEEE2DF3}Prefabs/Items/Wallet.et", 0)  # Free
    COMPASS = ItemDefinition(
        "{61D4F80E49BF9B12}Prefabs/Items/Equipment/Compass/Compass_SY183.et", 500
    )
    FLASHLIGHT = ItemDefinition(
        "{3A421547BC29F679}Prefabs/Items/Equipment/Flashlights/Flashlight_MX991/Flashlight_MX991.et",
        500,
    )
    MAP = ItemDefinition(
        "{922F95F91943F69A}Prefabs/Items/Equipment/Maps/PaperMap_01_folded_US.et", 500
    )

    # MARK: Misc
    FLOPPY = ItemDefinition(
        "{866D3B6301B1AA4E}Prefabs/Items/Electronics/armst_itm_floppy.et", 3000
    )

    @property
    def prefab_path(self) -> str:
        return self.value.prefab_path

    @property
    def base_price(self) -> int:
        return self.value.base_price


# Recipes are now defined in recipes.py module
