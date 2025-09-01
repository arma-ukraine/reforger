"""
Simple enums for shops and items.
"""

from enum import Enum
from typing import NamedTuple

BASE_AMMO_PRICE = 2
BASE_ARMOR_PRICE = 3500
BASE_BACKPACK_PRICE = 5000
BASE_EQUIPMENT_PRICE = 1000
BASE_FILLED_CONTAINER_PROFIT = 100
BASE_FOOD_WATER_CONTAINER_PRICE = 300
BASE_GASMASK_PRICE = 2000
BASE_INTEL_PRICE = 1000
BASE_MEDKIT_PRICE = 2000
BASE_MUTANT_PART_PRICE = 200
BASE_WEAPON_PRICE = 800


class ItemDefinition(NamedTuple):
    prefab_path: str
    base_price: int  # Base price in UAK for direct purchase


class Item(Enum):
    # MARK: Currency
    WALLET = ItemDefinition("{B0E67230AEEE2DF3}Prefabs/Items/Wallet.et", 0)  # Free
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
        "{5DDC31EAA3B77A02}Prefabs/Items/Mut_parts/armst_itm_mut_boar.et",
        BASE_MUTANT_PART_PRICE,
    )

    # MARK: Containers
    CANTEEN_EMPTY = ItemDefinition(
        "{654D80AC7C1E0F80}Prefabs/Items/Food/armst_itm_food_canteen_empty.et",
        BASE_FOOD_WATER_CONTAINER_PRICE,
    )
    CONSERVA_THROW = ItemDefinition(
        "{16230D52F5022FAC}Prefabs/Items/bolts/armst_throw_conserva.et",
        int(CANTEEN_EMPTY.base_price / 2),
    )

    # MARK: Consumnables.
    CANTEEN_WATER = ItemDefinition(
        "{52D3FE1E430900D3}Prefabs/Items/Food/armst_itm_food_canteen_water.et",
        CANTEEN_EMPTY.base_price + BASE_FILLED_CONTAINER_PROFIT,
    )
    TUSHONKA = ItemDefinition(
        "{1472B9856B26B931}Prefabs/Items/Food/armst_itm_food_tushonka_1.et",
        CONSERVA_THROW.base_price
        + (MUT_BOAR.base_price * 2)
        + BASE_FILLED_CONTAINER_PROFIT,
    )
    MEDKIT_AI2 = ItemDefinition(
        "{CB67A30D05AA4F29}Prefabs/Items/Medicine/armst_itm_medkit_ai2.et",
        BASE_MEDKIT_PRICE,
    )
    MORPHINE = ItemDefinition(
        "{0D9A5DCF89AE7AA9}Prefabs/Items/Medicine/MorphineInjection_01/MorphineInjection_01.et",
        int(MEDKIT_AI2.base_price * 0.75),
    )
    BANDAGE = ItemDefinition(
        "{A81F501D3EF6F38E}Prefabs/Items/Medicine/FieldDressing_01/FieldDressing_US_01.et",
        int(MEDKIT_AI2.base_price / 2),
    )
    TOURNIQUET = ItemDefinition(
        "{D70216B1B2889129}Prefabs/Items/Medicine/Tourniquet_01/Tourniquet_US_01.et",
        int(MEDKIT_AI2.base_price / 2),
    )
    SALINE_BAG = ItemDefinition(
        "{00E36F41CA310E2A}Prefabs/Items/Medicine/SalineBag_01/SalineBag_US_01.et",
        MEDKIT_AI2.base_price,
    )

    # MARK: Weapons
    BAYONET = ItemDefinition(
        "{558117556F3880A8}Prefabs/Weapons/Attachments/Bayonets/Bayonet_M9.et",
        BASE_WEAPON_PRICE,
    )
    PM = ItemDefinition(
        "{C0F7DD85A86B2900}Prefabs/Weapons/Handguns/armst_PM.et", BASE_WEAPON_PRICE
    )
    DOUBLE_BARREL_SAWN_OFF = ItemDefinition(
        "{E7A3BA1F06C057FF}Prefabs/Weapons/Shotguns/Double Barrel/BC_Shotgun_Double_Barrel_Sawn_Off.et",
        PM.base_price * 2,
    )
    DOUBLE_BARREL_SHOTGUN = ItemDefinition(
        "{3C4FB3D9D54B46DF}Prefabs/Weapons/Shotguns/Double Barrel/BC_Shotgun_Double_Barrel_760mm.et",
        DOUBLE_BARREL_SAWN_OFF.base_price * 2,
    )
    REMINGTON_870 = ItemDefinition(
        "{458A4E8CD3590D92}Prefabs/Weapons/Shotguns/Remington 870/BC_Shotgun_Remington_870.et",
        DOUBLE_BARREL_SHOTGUN.base_price * 5,
    )

    # MARK: Ammo
    AMMO_12GA_SHELL = ItemDefinition(
        "{B0DFDF7AAA9C5D39}Prefabs/Weapons/Magazines/BC_Shell_12ga_Buckshot.et",
        12 * BASE_AMMO_PRICE,
    )
    AMMO_PM_9x18 = ItemDefinition(
        "{8B853CDD11BA916E}Prefabs/Weapons/Magazines/Magazine_9x18_PM_8rnd_Ball.et",
        8 * BASE_AMMO_PRICE,
    )

    # MARK: GasMasks
    GASMASK_GP5 = ItemDefinition(
        "{D7B25AAE6F51908A}Prefabs/New_Equipment/Gasmasks/armst_gasmask_gp5.et",
        BASE_GASMASK_PRICE,
    )

    # MARK: Backpacks
    BACKPACK_RUKZAK = ItemDefinition(
        "{DF7ECE4FEB0F0B69}Prefabs/New_Equipment/backpack/armst_backpack_rukzak.et",
        BASE_BACKPACK_PRICE,
    )
    BACKPACK_KOLOBOK = ItemDefinition(
        "{FA1A1C2700C3306D}Prefabs/New_Equipment/backpack/armst_backpack_kolobok.et",
        BASE_BACKPACK_PRICE * 3,
    )

    # MARK: Equipment
    COMPASS = ItemDefinition(
        "{61D4F80E49BF9B12}Prefabs/Items/Equipment/Compass/Compass_SY183.et",
        BASE_EQUIPMENT_PRICE,
    )
    FLASHLIGHT = ItemDefinition(
        "{3A421547BC29F679}Prefabs/Items/Equipment/Flashlights/Flashlight_MX991/Flashlight_MX991.et",
        BASE_EQUIPMENT_PRICE,
    )
    MAP = ItemDefinition(
        "{922F95F91943F69A}Prefabs/Items/Equipment/Maps/PaperMap_01_folded_US.et",
        int(BASE_EQUIPMENT_PRICE / 2),
    )
    PDA = ItemDefinition(
        "{6E2790C4C516701B}Prefabs/Items/devices/armst_itm_pda.et",
        BASE_EQUIPMENT_PRICE * 2,
    )
    ATMOS = ItemDefinition(
        "{33C169417F310F0D}Prefabs/Items/devices/armst_itm_atmos.et",
        BASE_EQUIPMENT_PRICE * 2,
    )

    # MARK: Misc
    PAPERS_PERSONAL_US = ItemDefinition(
        "{A735A93A8AD4077A}Prefabs/Props/PersonalBelongings/Papers/Papers_Personal_US.et",
        1000,
    )
    FLOPPY = ItemDefinition(
        "{866D3B6301B1AA4E}Prefabs/Items/Electronics/armst_itm_floppy.et",
        BASE_INTEL_PRICE,
    )
    FLASH_EMPTY = ItemDefinition(
        "{A93E6BD6C9A7F748}Prefabs/Items/Electronics/armst_itm_flash.et",
        int(FLOPPY.base_price * 1.2),
    )
    DOCS_1 = ItemDefinition(
        "{BAFDB21966A26568}Prefabs/Items/Others/Documents/armst_itm_docs.et",
        int(FLASH_EMPTY.base_price * 1.5),
    )
    DOCS_2 = ItemDefinition(
        "{AFB860AD776F046E}Prefabs/Items/Others/Documents/armst_itm_docs_2.et",
        DOCS_1.base_price,
    )
    DOCS_3 = ItemDefinition(
        "{1369209D87219FEC}Prefabs/Items/Others/Documents/armst_itm_docs_3.et",
        DOCS_1.base_price,
    )
    DOCS_4 = ItemDefinition(
        "{2E5D05A5F24D16DB}Prefabs/Items/Others/Documents/armst_itm_docs_4.et",
        DOCS_1.base_price,
    )
    DOCS_5 = ItemDefinition(
        "{CBC1495CFEA881B0}Prefabs/Items/Others/Documents/armst_itm_docs_5.et",
        DOCS_1.base_price,
    )
    DOCS_SECRETS = ItemDefinition(
        "{F91FDAD0027E732D}Prefabs/Items/Others/Documents/armst_itm_docs_secrets.et",
        DOCS_1.base_price * 2,
    )
    HDD = ItemDefinition(
        "{CB5DFD80DA966328}Prefabs/Items/Electronics/armst_itm_hdd.et",
        BASE_INTEL_PRICE * 2,
    )

    @property
    def prefab_path(self) -> str:
        return self.value.prefab_path

    @property
    def base_price(self) -> int:
        return self.value.base_price
