#!/usr/bin/env python3
"""
Price Validation and Auto-Fix Script for AUA Freedom Fighters Tweaks

This script:
1. Validates that m_iMoneyPrice is exactly 5 times m_iSuppliesPrice
2. Automatically adds missing m_iMoneyPrice entries (calculated as 5x supplies price)
3. Shows errors for incorrect ratios in the FreedomFighters.conf configuration file
"""

import argparse
import re
import sys
from pathlib import Path


class PriceValidator:
    def __init__(self, config_path: str, auto_fix: bool = False):
        self.config_path = Path(config_path)
        self.auto_fix = auto_fix
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.fixes_applied: list[str] = []
        self.content_modified = False

    def validate_file(self) -> bool:
        """Validate the configuration file and return True if all validations pass."""
        if not self.config_path.exists():
            self.errors.append(f"Configuration file not found: {self.config_path}")
            return False

        try:
            content = self.config_path.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(f"Failed to read file: {e}")
            return False

        validation_passed = self._validate_and_fix_prices(content)

        # Write back modified content if auto-fix is enabled and changes were made
        if self.auto_fix and self.content_modified:
            try:
                self.config_path.write_text(self.modified_content, encoding="utf-8")
                print(f"\nConfiguration file updated: {self.config_path}")
            except Exception as e:
                self.errors.append(f"Failed to write updated file: {e}")
                return False

        return validation_passed

    def _validate_and_fix_prices(self, content: str) -> bool:
        """Extract, validate, and optionally fix price ratios from config content."""
        self.modified_content = content
        validation_passed = True

        # First, find rules with both money and supplies prices
        complete_rule_pattern = (
            r'(JWK_ItemAttributesConfigRule\s+"([^"]+)"\s*\{.*?'
            r"m_iMoneyPrice\s+(\d+).*?m_iSuppliesPrice\s+(\d+).*?"
            r"\n\s*\}\s*\n\s*\})"
        )
        complete_matches = re.findall(complete_rule_pattern, content, re.DOTALL)

        for (
            _full_match,
            rule_id,
            money_price_str,
            supplies_price_str,
        ) in complete_matches:
            try:
                money_price = int(money_price_str)
                supplies_price = int(supplies_price_str)
                expected_money_price = supplies_price * 5

                if money_price != expected_money_price:
                    if self.auto_fix:
                        # Fix the money price
                        old_money_line = f"m_iMoneyPrice {money_price}"
                        new_money_line = f"m_iMoneyPrice {expected_money_price}"
                        self.modified_content = self.modified_content.replace(
                            old_money_line, new_money_line
                        )
                        self.content_modified = True
                        self.fixes_applied.append(
                            f"Rule {rule_id}: Fixed m_iMoneyPrice from "
                            f"{money_price} to {expected_money_price}"
                        )
                    else:
                        self.errors.append(
                            f"Rule {rule_id}: Invalid price ratio! "
                            f"m_iMoneyPrice={money_price}, "
                            f"m_iSuppliesPrice={supplies_price}. "
                            f"Expected m_iMoneyPrice={expected_money_price} "
                            f"(5x supplies price)"
                        )
                        validation_passed = False
                else:
                    print(
                        f"OK Rule {rule_id}: Price ratio correct "
                        f"(Money: {money_price}, Supplies: {supplies_price})"
                    )

            except ValueError as e:
                self.errors.append(f"Rule {rule_id}: Failed to parse prices - {e}")
                validation_passed = False

        # Now find rules with only supplies prices (missing money prices)
        supplies_only_pattern = (
            r'(JWK_ItemAttributesConfigRule\s+"([^"]+)"\s*\{'
            r"(?:(?!m_iMoneyPrice).)*?m_iSuppliesPrice\s+(\d+)"
            r"(?:(?!m_iMoneyPrice).)*?\n\s*\}\s*\n\s*\})"
        )
        supplies_only_matches = re.findall(supplies_only_pattern, content, re.DOTALL)

        for _full_match, rule_id, supplies_price_str in supplies_only_matches:
            try:
                supplies_price = int(supplies_price_str)
                money_price = supplies_price * 5

                if self.auto_fix:
                    # Add the missing money price line before supplies price
                    supplies_line = f"m_iSuppliesPrice {supplies_price}"
                    new_block = f"m_iMoneyPrice {money_price}\n    {supplies_line}"
                    self.modified_content = self.modified_content.replace(
                        supplies_line, new_block
                    )
                    self.content_modified = True
                    self.fixes_applied.append(
                        f"Rule {rule_id}: Added missing m_iMoneyPrice={money_price} "
                        f"(5x supplies price {supplies_price})"
                    )
                    print(
                        f"FIXED Rule {rule_id}: Added missing money price "
                        f"(Money: {money_price}, Supplies: {supplies_price})"
                    )
                else:
                    self.errors.append(
                        f"Rule {rule_id}: Missing m_iMoneyPrice! "
                        f"Found m_iSuppliesPrice={supplies_price}. "
                        f"Should add m_iMoneyPrice={money_price} (5x supplies price)"
                    )
                    validation_passed = False

            except ValueError as e:
                self.errors.append(
                    f"Rule {rule_id}: Failed to parse supplies price - {e}"
                )
                validation_passed = False

        # Check if we found any rules at all
        if not complete_matches and not supplies_only_matches:
            self.errors.append("No price configuration rules found in the file")
            return False

        return validation_passed

    def print_results(self):
        """Print validation results."""
        if self.fixes_applied:
            print("\nFIXES APPLIED:")
            for fix in self.fixes_applied:
                print(f"  + {fix}")

        if self.errors:
            print("\nVALIDATION ERRORS:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            if self.fixes_applied:
                print("\nAll price validations passed after applying fixes!")
            else:
                print("\nAll price validations passed!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate and optionally fix price ratios in FreedomFighters.conf"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix missing money prices and incorrect ratios",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file (default: Configs/Items/FreedomFighters.conf)",
    )

    args = parser.parse_args()

    if args.config:
        config_file = Path(args.config)
    else:
        script_dir = Path(__file__).parent
        config_file = script_dir / "Configs" / "Items" / "FreedomFighters.conf"

    print(f"Validating prices in: {config_file}")
    if args.fix:
        print("Auto-fix mode: ON - Will automatically fix issues")
    else:
        print("Auto-fix mode: OFF - Will only report issues (use --fix to auto-fix)")
    print("=" * 60)

    validator = PriceValidator(str(config_file), auto_fix=args.fix)
    validation_passed = validator.validate_file()

    validator.print_results()

    if validation_passed:
        print("\nValidation completed successfully!")
        return 0
    else:
        print("\nValidation failed! Use --fix to automatically resolve issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
