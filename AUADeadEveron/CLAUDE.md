# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Arma Reforger mod** called "ArmAUkraine Dead Everon" - a post-apocalyptic survival scenario set on Everon island with S.T.A.L.K.E.R.-inspired elements including anomalies, radiation zones, and a currency-based economy system. The mod is built using Bohemia Interactive's Enfusion engine.

## Development Environment

**Arma Reforger Workbench** - This project uses Arma Reforger Workbench for development, not traditional command-line build tools. Work should be done through the Workbench IDE.

**No Build Commands** - Unlike traditional software projects, Arma Reforger mods are primarily developed and tested through the Workbench GUI. There are no npm, gradle, or similar build commands.

**Testing** - Testing is performed by running the mission in Arma Reforger Workbench's preview mode or on a dedicated server.

## Architecture

### Core Systems

**Currency System** (`Scripts/Game/Currency/`)
- `AdmCurrencySaveData.c` - Persistence layer for currency using EPF (Enfusion Persistence Framework)
- Integrates with ADM_CurrencyComponent for player currency management
- Uses EPF_ComponentSaveData for save/load operations

**Shop System** (`configs/Shops/`)
- Multiple shop configurations for different merchants (Currency.conf, Water.conf, Cooking.conf, Postman.conf, PostmanIntel.conf)
- Uses ADM_ShopConfig structure with merchandise, buy/sell payments, and crafting recipes
- Supports both currency-based transactions and crafting stations
- Requires ADM_PlayerShopManager component on player controller
- PostmanIntel shop specializes in intelligence items with higher prices

**Prefab Cleanup** (`Scripts/Game/AUA_DeletePrefabsOnStart.c`)
- Server-side component for removing specified prefabs at mission start
- Useful for cleaning up unwanted objects in inherited scenarios
- Operates via entity enumeration across the world

### File Structure

**Scripts/Game/** - EnforceScript (.c) source files
- `Currency/` - Currency system and save data components
- `AUA_DeletePrefabsOnStart.c` - Prefab cleanup component

**Prefabs/** - Entity definitions (.et files) and associated metadata
- `Anomals/TRIGGERS/` - Anomaly trigger systems 
- `Characters/Core/` - Player controller with shop integration
- `Compositions/Misc/CustomEntities/InteractionPoints/` - Storage and interaction systems
- `Items/Moneys/` - UAK currency denominations
- `Items/Wallet.et` - Currency storage item
- `Props/` - Environmental objects
- `Sounds/Environment/` - Ambient audio systems

**configs/** - Configuration files (.conf) for various systems
- `EntityCatalog/` - Item catalog configurations
- `Factions/` - Faction definitions (ARMY, STALKER, US)
- `Shops/` - Shop merchant configurations (Currency, Water, Cooking, Postman, PostmanIntel)
- `Systems/` - Core system settings (garbage collection, etc.)
- `NameTags/` - Name tag display configurations

**Worlds/** - World/mission files and associated layer files
- Multiple world configurations (ArmAUkraineDeadEveron.ent, GMTest.ent, ShopTest.ent)
- Layer system for organized content placement (Environment/, Base/, SF/)

**UI/** - User interface layouts and graphics
- `PDA/` - PDA interface layouts
- `layouts/Menus/` - Loading screens and main menu customization
- Generated loading screen images and screenshots

**Missions/** - Mission header configuration files
**src/economy/** - Python-based shop configuration system
- `items.py` - Item definitions with prefab paths and prices
- `shops.py` - Shop configurations 
- `recipes.py` - Crafting recipes
- `generator.py` - Configuration file generator

### Key Dependencies

The mod relies heavily on external framework mods:
- **Reforger Shop System** - Third-party shop framework (requires ADM_PlayerShopManager on player controller)
- **EPF (Enfusion Persistence Framework)** - For data persistence and save/load functionality
- Multiple other mods as listed in addon.gproj dependencies

### Configuration System

**Shop Configuration Generation:**
Shop configurations are generated from Python code in `src/economy/` using a simple, declarative system.

**Python Shop Generation System:**
- `src/economy/items.py` - Item definitions with prefab paths and base prices using ItemDefinition NamedTuples
- `src/economy/shops.py` - Shop configurations using ShopConfig NamedTuples with buy/sell items and crafting recipes
- `src/economy/recipes.py` - Crafting recipe definitions using RecipeData NamedTuples
- `src/economy/generator.py` - Generates .conf files from Python configuration
- `generate_shop_configs.py` - Main script to regenerate all shop files

**Shop Configuration Structure (Generated):**
```
ADM_ShopConfig {
  m_Merchandise {
    ADM_ShopMerchandise {
      m_Merchandise ADM_MerchandiseItem { m_sPrefab "path/to/item.et" }
      m_BuyPayment { ADM_PaymentMethodCurrency { m_Quantity 100 } }
      m_SellPayment { ADM_PaymentMethodCurrency { m_Quantity 80 } }
    }
  }
}
```

**Current Python Configuration Format:**

**Item Definition:**
```python
class Item(Enum):
    WALLET = ItemDefinition("{B0E67230AEEE2DF3}Prefabs/Items/Wallet.et", 0)  # Free
    MEDKIT_AI2 = ItemDefinition("{CB67A30D05AA4F29}Prefabs/Items/Medicine/armst_itm_medkit_ai2.et", 2000)
```

**Shop Configuration:**
```python
class Shop(Enum):
    POSTMAN = ShopConfig(
        name="Postman",
        buy_items=(Item.WALLET, Item.MEDKIT_AI2),  # Items available for purchase
        sell_items=(Item.MEDKIT_AI2,),  # Items accepted for selling
        buy_multiplier=1.0,   # Normal buy prices
        sell_multiplier=0.3,  # Sell for 30% of buy price
    )
```

**Recipe Definition:**
```python
class Recipe(Enum):
    FILL_CANTEEN = RecipeData(Item.CANTEEN_WATER, ((Item.CANTEEN_EMPTY, 1),))
```

**Supported Payment Types:**
- `int` - Currency payment (e.g., `500` UAK)
- `ItemTrade(item, count)` - Item-for-item trade (e.g., `ItemTrade(Item.CANTEEN_EMPTY, 1)`)
- `None` - Item cannot be bought/sold

**Multipliers:**
- `buy_multiplier` - Affects currency prices when buying (default: 1.0)
- `sell_multiplier` - Affects currency prices when selling (default: 1.0)
- ItemTrade quantities are NOT affected by multipliers
- Final prices are rounded up using `math.ceil()`

**Mission Configuration** - Located in `Missions/ArmAUkraineDeadEveron.conf`
- Defines world reference, player count, time acceleration settings
- Ukrainian description and custom loading screens

### Custom Entities

**Money Items** - Various UAK denominations (1, 5, 10, 50, 100, 500, 1000, 5000 UAK) with custom prefabs
**Storage Systems** - PersistentStorageBox for item storage with persistence
**Anomaly Triggers** - Custom trigger systems for environmental hazards (ARMST_TRIGGER_ANOMAL, ARMST_TRIGGER_GROUPS)
**Player Controller** - Modified DefaultPlayerControllerMP_Factions with shop integration and currency support
**Intelligence Items** - Floppy disks, flash drives, and classified documents for trading
**Mutant Parts** - Boar parts and other mutant materials for crafting
**Medical Supplies** - AI-2 medkits, morphine, bandages, tourniquets, saline bags
**Food & Water** - Canteens (empty/filled), tushonka canned food, throwable cans
**Weapons & Ammo** - PM handgun, various shotguns (double barrel, Remington 870), ammunition
**Equipment** - Gas masks (GP5), tactical clothing (Gorka suits), compasses, flashlights, maps
**Ambient Audio** - Custom ambient sound prefab for Everon atmosphere

## Development Notes

**Shop Configuration Workflow:**
1. Add new items to `src/economy/items.py` with correct prefab paths and base prices using ItemDefinition
2. Add crafting recipes to `src/economy/recipes.py` if needed using RecipeData
3. Update shop configurations in `src/economy/shops.py` using ShopConfig format
4. Run `python generate_shop_configs.py` to regenerate all .conf files
5. Import updated .conf files into Arma Reforger Workbench

**Python Code Conventions:**
- Use absolute imports: `from src.economy.items import Item` and `from src.economy.shops import Shop`
- Keep NamedTuple structures simple and declarative
- Avoid magic strings - use enums for all item and shop references
- Each item has a base_price used for currency calculations with multipliers
- Crafting recipes define components needed and result item produced
- Price multipliers affect final currency costs but not item quantities in recipes

**Persistence Requirements:**
- Custom components require EPF_ComponentSaveData implementation for persistence
- Save data classes must be added to prefab's EPF_PersistanceComponent->SaveData->Components

**Shop Integration Issues:**
- "Purchase button does nothing" - Ensure ADM_PlayerShopManager is on player controller
- "Shop not found" errors - Verify shop prefab has replication component enabled

**Script Debugging:**
- Use `Print()` statements with LogLevel for debugging (NORMAL, WARNING, ERROR)
- Server-only operations should check `Replication.IsServer()`
- Gameplay mode checks with `GetGame().InPlayMode()`

## File Naming Conventions

- Scripts: PascalCase with descriptive prefixes (e.g., `AUA_DeletePrefabsOnStart.c`)
- Prefabs: Lowercase with underscores (e.g., `armst_itm_money_1000rub.et`)
- Configurations: PascalCase matching their system (e.g., `Currency.conf`)
- All files include .meta counterparts for Workbench metadata

## Mission Context

The mod recreates Everon island as a post-Soviet experimental zone with:
- 16-player multiplayer support
- Accelerated day/night cycles (8x speed)
- Random weather and time systems
- Faction-based gameplay (STALKER, ARMY, CIV factions)
- Economics-driven survival gameplay
