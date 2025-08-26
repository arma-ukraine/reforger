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
- Multiple shop configurations for different merchants (Currency.conf, Water.conf, Cooking.conf, Postman.conf)
- Uses ADM_ShopConfig structure with merchandise, buy/sell payments
- Supports both currency and item-based transactions
- Requires ADM_PlayerShopManager component on player controller

**Prefab Cleanup** (`Scripts/Game/AUA_DeletePrefabsOnStart.c`)
- Server-side component for removing specified prefabs at mission start
- Useful for cleaning up unwanted objects in inherited scenarios
- Operates via entity enumeration across the world

### File Structure

**Scripts/Game/** - EnforceScript (.c) source files
**Prefabs/** - Entity definitions (.et files) and associated metadata
**configs/** - Configuration files (.conf) for various systems
- `Factions/` - Faction definitions
- `Shops/` - Shop merchant configurations  
- `Systems/` - Core system settings (garbage collection, etc.)
- `NameTags/` - Name tag display configurations
**Worlds/** - World/mission files and associated layer files
**UI/** - User interface layouts and graphics
**Missions/** - Mission header configuration files

### Key Dependencies

The mod relies heavily on external framework mods:
- **Reforger Shop System** - Third-party shop framework (requires ADM_PlayerShopManager on player controller)
- **EPF (Enfusion Persistence Framework)** - For data persistence and save/load functionality
- Multiple other mods as listed in addon.gproj dependencies

### Configuration System

**Shop Configuration Structure:**
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

**Mission Configuration** - Located in `Missions/ArmAUkraineDeadEveron.conf`
- Defines world reference, player count, time acceleration settings
- Ukrainian description and custom loading screens

### Custom Entities

**Money Items** - Various Russian UAK denominations (1, 5, 10, 50, 100, 500, 1000, 5000 UAK )
**Storage Systems** - PersistentStorageBox for item storage
**Anomaly Triggers** - Custom trigger systems for environmental hazards
**Player Controller** - Modified DefaultPlayerControllerMP_Factions with shop integration

## Development Notes

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
