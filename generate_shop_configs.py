#!/usr/bin/env python3
"""
Simple Shop Generator for ArmAUkraine Dead Everon

Usage:
    python generate_shops_simple.py

Generates .conf files from the simple configuration in src/economy/prices.py
"""

from pathlib import Path
from src.economy.generator import ShopGenerator

def main():
    print("=== Simple Shop Generator ===\n")
    
    generator = ShopGenerator()
    shop_output_dir = Path("configs/Shops")
    
    # Generate shop configurations
    generated_shop_files = generator.generate_all_shops(shop_output_dir)
    
    print(f"\nGenerated {len(generated_shop_files)} shop files:")
    for file_path in generated_shop_files:
        print(f"  - {file_path}")
    
    # Generate EntityCatalog
    print("\n=== Generating EntityCatalog ===")
    entity_catalog_file = Path("configs/EntityCatalog/VIDSICH/InventoryItems_EntityCatalog_VIDSICH.conf")
    generated_catalog_file = generator.generate_entity_catalog_file(entity_catalog_file)
    
    print(f"\nGenerated EntityCatalog file:")
    print(f"  - {generated_catalog_file}")
    
    # Generate ArsenalShops
    print("\n=== Generating ArsenalShops ===")
    arsenal_output_dir = Path("configs/ArsenalShops")
    generated_arsenal_files = generator.generate_all_arsenal_shops(arsenal_output_dir)
    
    print(f"\nGenerated {len(generated_arsenal_files)} ArsenalShop files:")
    for file_path in generated_arsenal_files:
        print(f"  - {file_path}")
    
    print(f"\nTotal files generated: {len(generated_shop_files) + len(generated_arsenal_files) + 1}")

if __name__ == "__main__":
    main()