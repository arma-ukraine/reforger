"""
Crafting recipes definitions.
"""

from enum import Enum
from typing import NamedTuple, Tuple

from src.economy.items import Item


class RecipeData(NamedTuple):
    """Recipe definition with result and components"""

    result_item: Item  # What this recipe produces (always quantity 1)
    components: Tuple[Tuple[Item, int], ...]  # (Item, quantity) pairs needed


class Recipe(Enum):
    """Named crafting recipes with results and component requirements"""

    FILL_CANTEEN = RecipeData(Item.CANTEEN_WATER, ((Item.CANTEEN_EMPTY, 1),))
    PRESERVE_MEAT = RecipeData(
        Item.TUSHONKA_1, ((Item.MUT_BOAR, 2), (Item.CONSERVA_THROW, 1))
    )

    @property
    def result_item(self) -> Item:
        return self.value.result_item

    @property
    def components(self) -> Tuple[Tuple[Item, int], ...]:
        return self.value.components
