class AUA_FillCanteenWithWaterUserAction : ScriptedUserAction
{
	protected const string EMPTY_CANTEEN_PREFAB = "{654D80AC7C1E0F80}Prefabs/Items/Food/armst_itm_food_canteen_empty.et";
	protected const string FILLED_CANTEEN_PREFAB = "{52D3FE1E430900D3}Prefabs/Items/Food/armst_itm_food_canteen_water.et";

	//------------------------------------------------------------------------------------------------
	override bool CanBeShownScript(IEntity user)
	{
		if (!user)
			return false;

		ChimeraCharacter userCharacter = ChimeraCharacter.Cast(user);
		if (!userCharacter)
			return false;

		SCR_InventoryStorageManagerComponent inventoryManager = SCR_InventoryStorageManagerComponent.Cast(userCharacter.GetCharacterController().GetInventoryStorageManager());
		if (!inventoryManager)
			return false;

		return HasEmptyCanteenInInventory(inventoryManager);
	}

	//------------------------------------------------------------------------------------------------
	override void PerformAction(IEntity pOwnerEntity, IEntity pUserEntity)
	{
		ChimeraCharacter userCharacter = ChimeraCharacter.Cast(pUserEntity);
		if (!userCharacter)
			return;

		SCR_InventoryStorageManagerComponent inventoryManager = SCR_InventoryStorageManagerComponent.Cast(userCharacter.GetCharacterController().GetInventoryStorageManager());
		if (!inventoryManager)
			return;

		IEntity emptyCanteen = FindEmptyCanteenInInventory(inventoryManager);
		if (!emptyCanteen)
			return;

		if (!inventoryManager.TrySpawnPrefabToStorage(FILLED_CANTEEN_PREFAB))
			return;

		inventoryManager.TryDeleteItem(emptyCanteen);
	}

	//------------------------------------------------------------------------------------------------
	protected bool HasEmptyCanteenInInventory(SCR_InventoryStorageManagerComponent inventoryManager)
	{
		return FindEmptyCanteenInInventory(inventoryManager) != null;
	}

	//------------------------------------------------------------------------------------------------
	protected IEntity FindEmptyCanteenInInventory(SCR_InventoryStorageManagerComponent inventoryManager)
	{
		array<IEntity> items = {};
		inventoryManager.GetItems(items);

		foreach (IEntity item : items)
		{
			if (!item)
				continue;

			EntityPrefabData prefabData = item.GetPrefabData();
			if (!prefabData)
				continue;

			string prefabName = prefabData.GetPrefabName();
			if (prefabName == EMPTY_CANTEEN_PREFAB)
				return item;
		}

		return null;
	}
};
