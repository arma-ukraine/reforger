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
    output_dir = Path("configs/Shops")
    
    generated_files = generator.generate_all_shops(output_dir)
    
    print(f"\nGenerated {len(generated_files)} shop files:")
    for file_path in generated_files:
        print(f"  - {file_path}")

if __name__ == "__main__":
    main()