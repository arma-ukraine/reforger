#!/usr/bin/env python3
"""
Price Auto-Fix Script for AUA Freedom Fighters Tweaks

This script automatically sets m_iMoneyPrice to 5x m_iSuppliesPrice
in the FreedomFighters.conf configuration file.
"""

import argparse
import re
import sys
from pathlib import Path
from re import Match


class PriceValidator:
    def __init__(self, config_path: str, auto_fix: bool = False):
        self.config_path = Path(config_path)
        self.auto_fix = auto_fix
        self.fixes_applied: list[str] = []

    def validate_file(self) -> bool:
        """Process the configuration file and auto-fix prices."""
        if not self.config_path.exists():
            print(f"Configuration file not found: {self.config_path}")
            return False

        try:
            content = self.config_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Failed to read file: {e}")
            return False

        modified_content = self._fix_prices(content)

        if self.auto_fix and modified_content != content:
            try:
                self.config_path.write_text(modified_content, encoding="utf-8")
            except Exception as e:
                print(f"Failed to write updated file: {e}")
                return False

        return True

    def _fix_prices(self, content: str) -> str:
        """Auto-set money prices to 5x supplies prices."""
        # Find all rules with supplies prices
        pattern = (
            r'(JWK_ItemAttributesConfigRule\s+"([^"]+)"\s*\{.*?'
            r"m_iSuppliesPrice\s+(\d+).*?\n\s*\}\s*\n\s*\})"
        )

        def replace_prices(match: Match[str]) -> str:
            full_block, rule_id, supplies_price = match.groups()
            supplies_price = int(supplies_price)
            money_price = supplies_price * 5

            # Remove existing money price but preserve structure
            block_without_money = re.sub(r"\s*m_iMoneyPrice\s+\d+\n", "", full_block)

            # Add new money price before supplies price with proper indentation
            supplies_line = f"m_iSuppliesPrice {supplies_price}"
            supplies_match = re.search(
                rf"(\s*){re.escape(supplies_line)}", block_without_money
            )
            assert supplies_match is not None
            indent = supplies_match.group(1)
            replacement = (
                f"\n{indent}m_iMoneyPrice {money_price}"
                f"\n{indent}m_iSuppliesPrice {supplies_price}"
            )
            new_block = block_without_money.replace(supplies_line, replacement)

            self.fixes_applied.append(
                f"Rule {rule_id}: Set m_iMoneyPrice={money_price} "
                f"(5x supplies price {supplies_price})"
            )

            return new_block

        modified_content = re.sub(pattern, replace_prices, content, flags=re.DOTALL)

        return modified_content


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Auto-fix price ratios in FreedomFighters.conf"
    )
    parser.add_argument("--fix", action="store_true", help="Apply fixes to the file")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to config file (default: Configs/Items/FreedomFighters.conf)",
    )

    args = parser.parse_args()

    if args.config:
        config_file = Path(args.config)
    else:
        script_dir = Path(__file__).parent
        config_file = script_dir / "Configs" / "Items" / "FreedomFighters.conf"

    validator = PriceValidator(str(config_file), auto_fix=args.fix)
    success = validator.validate_file()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
