"""
Simple generator to convert shop configurations to .conf files.
"""

import math
import uuid
from pathlib import Path
from typing import List, NamedTuple, Optional, Union

from src.economy.items import Item
from src.economy.recipes import Recipe
from src.economy.shops import Shop, ShopConfig


class ItemRequirement(NamedTuple):
    """Item requirement for crafting"""

    item: Item
    quantity: int


class ShopGenerator:
    """Generate Arma Reforger .conf files from shop configurations"""

    def generate_guid(self) -> str:
        """Generate a GUID for shop merchandise"""
        return str(uuid.uuid4()).replace("-", "").upper()[:16]

    def generate_payment(
        self,
        config: Union[int, ItemRequirement],
        multiplier: float = 1.0,
        indent: int = 2,
        is_buy_payment: bool = True,
    ) -> str:
        """Generate payment method configuration"""
        spaces = "  " * indent
        guid = self.generate_guid()

        if isinstance(config, int):
            # Currency payment - apply multiplier and round accordingly
            if is_buy_payment:
                final_price = math.ceil(config * multiplier)  # Buy prices round up
            else:
                final_price = math.floor(config * multiplier)  # Sell prices round down
            return f"""{spaces}ADM_PaymentMethodCurrency "{{{guid}}}" {{
{spaces} m_Quantity {final_price}
{spaces}}}"""
        else:
            # Item payment - no multiplier for item requirements (must be ItemRequirement)
            lines = [
                f'{spaces}ADM_PaymentMethodItem "{{{guid}}}" {{',
                f'{spaces} m_ItemPrefab "{config.item.prefab_path}"',
            ]
            if config.quantity > 1:
                lines.append(f"{spaces} m_ItemQuantity {config.quantity}")
            lines.append(f"{spaces}}}")
            return "\n".join(lines)

    def generate_shop_item(
        self,
        item: Item,
        buy_config: Optional[Union[int, List[Union[int, ItemRequirement]]]],
        sell_config: Optional[int],
        buy_multiplier: float = 1.0,
        sell_multiplier: float = 1.0,
    ) -> str:
        """Generate single shop item configuration"""
        item_guid = self.generate_guid()
        merch_guid = self.generate_guid()

        lines = [
            f'  ADM_ShopMerchandise "{{{item_guid}}}" {{',
            f'   m_Merchandise ADM_MerchandiseItem "{{{merch_guid}}}" {{',
            f'    m_sPrefab "{item.prefab_path}"',
            "    m_bAllowPurchaseWithFullInventory 1",
            "    m_bAllowSaleWithFullInventory 1",
            "    m_bDropSubStorageItemsOnSell 1",
            "   }",
        ]

        if buy_config is not None:
            lines.append("   m_BuyPayment {")
            if isinstance(buy_config, list):
                # Multiple payment methods (crafting with multiple components)
                for payment in buy_config:
                    lines.append(
                        self.generate_payment(
                            payment, buy_multiplier, 2, is_buy_payment=True
                        )
                    )
            else:
                # Single payment method
                lines.append(
                    self.generate_payment(
                        buy_config, buy_multiplier, 2, is_buy_payment=True
                    )
                )
            lines.append("   }")

        if sell_config is not None:
            lines.append("   m_SellPayment {")
            lines.append(
                self.generate_payment(
                    sell_config, sell_multiplier, 2, is_buy_payment=False
                )
            )
            lines.append("   }")

        lines.append("  }")
        return "\n".join(lines)

    def generate_crafting_config(
        self, recipe: Recipe, crafting_fee: int = 0
    ) -> List[Union[int, ItemRequirement]]:
        """Generate crafting configuration for a recipe - actual item components required"""
        if not recipe.components:
            # Empty recipe, shouldn't happen
            return []

        # Return actual item requirements
        components: List[Union[int, ItemRequirement]] = [
            ItemRequirement(comp_item, quantity)
            for comp_item, quantity in recipe.components
        ]

        # Add crafting fee if specified
        if crafting_fee > 0:
            components.append(crafting_fee)

        return components

    def generate_shop_config(self, shop_config: ShopConfig) -> str:
        """Generate complete shop configuration"""
        lines = ["ADM_ShopConfig {", " m_Merchandise {"]

        # Get all items that appear in the shop, preserving order
        all_items = []
        seen = set()

        # Add buy_items first (preserves order from tuples)
        for item in shop_config.buy_items:
            if item not in seen:
                all_items.append(item)
                seen.add(item)

        # Add sell_items next (preserves order from tuples)
        for item in shop_config.sell_items:
            if item not in seen:
                all_items.append(item)
                seen.add(item)

        # Add recipe result items last (preserves order from tuples)
        for recipe in shop_config.craft_recipes:
            if recipe.result_item not in seen:
                all_items.append(recipe.result_item)
                seen.add(recipe.result_item)

        # Validate that shop has buyable items
        has_buyable_items = bool(shop_config.buy_items or shop_config.craft_recipes)
        if not has_buyable_items:
            raise ValueError(f"Shop '{shop_config.name}' must have at least one buyable item (buy_items) or craft recipe")

        for item in all_items:
            # Check if it's a regular buy/sell item
            buy_config = None
            sell_config = None

            if item in shop_config.buy_items:
                # Direct purchase - use base price with multiplier
                buy_config = item.base_price

            # Check if it's a craftable item (result of a recipe)
            for recipe in shop_config.craft_recipes:
                if recipe.result_item == item:
                    # Craftable item - generate crafting recipe structure using named recipe
                    buy_config = self.generate_crafting_config(
                        recipe, shop_config.crafting_fee
                    )
                    break

            if item in shop_config.sell_items:
                sell_config = item.base_price  # Use base price from enum

            lines.append(
                self.generate_shop_item(
                    item,
                    buy_config,
                    sell_config,
                    shop_config.buy_multiplier,
                    shop_config.sell_multiplier,
                )
            )

        lines.extend([" }", "}"])
        return "\n".join(lines)

    def generate_all_shops(self, output_dir: Path) -> List[Path]:
        """Generate all shop configuration files"""
        output_dir.mkdir(parents=True, exist_ok=True)
        generated_files: List[Path] = []

        for shop in Shop:
            shop_config = shop.value
            config_content = self.generate_shop_config(shop_config)
            file_path = output_dir / f"{shop_config.name}.conf"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(config_content)

            generated_files.append(file_path)
            print(f"Generated: {file_path}")

        return generated_files
