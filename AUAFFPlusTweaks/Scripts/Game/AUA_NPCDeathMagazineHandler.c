// Modifies NPC magazine ammo to 0-3 bullets when they die and removes grenades/rockets
[ComponentEditorProps(category: "GameScripted/Custom", description: "Reduces NPC magazine ammo on death and removes explosives")]
class AUA_NPCDeathMagazineHandlerClass : ScriptComponentClass {}

class AUA_NPCDeathMagazineHandler : ScriptComponent
{
	override void OnPostInit(IEntity owner)
	{
		super.OnPostInit(owner);

		// Only run in actual gameplay, not in editor
		if (!GetGame().InPlayMode())
		{
			Print("AUA_NPCDeathMagazineHandler: Not in play mode, skipping", LogLevel.NORMAL);
			return;
		}

		Print(string.Format("AUA_NPCDeathMagazineHandler: OnPostInit called for entity %1", owner), LogLevel.NORMAL);

		// Check if this is a character
		ChimeraCharacter character = ChimeraCharacter.Cast(owner);
		if (!character)
		{
			Print("AUA_NPCDeathMagazineHandler: Entity is not a ChimeraCharacter", LogLevel.NORMAL);
			return;
		}

		// Check if this is NOT a player (skip players)
		PlayerController playerController = GetGame().GetPlayerController();
		if (playerController && playerController.GetControlledEntity() == character)
		{
			Print("AUA_NPCDeathMagazineHandler: Skipping player character", LogLevel.NORMAL);
			return;
		}

		Print("AUA_NPCDeathMagazineHandler: Setting up death monitoring for NPC", LogLevel.NORMAL);

		// Delay setup to allow character to fully initialize
		GetGame().GetCallqueue().CallLater(SetupDeathMonitoring, 1000, false, owner);
	}

	protected void SetupDeathMonitoring(IEntity owner)
	{
		ChimeraCharacter character = ChimeraCharacter.Cast(owner);
		if (!character)
		{
			Print("AUA_NPCDeathMagazineHandler: Character no longer valid", LogLevel.WARNING);
			return;
		}

		// Listen for death events
		SCR_CharacterDamageManagerComponent damageManager = SCR_CharacterDamageManagerComponent.Cast(character.GetDamageManager());
		if (damageManager)
		{
			damageManager.GetOnDamageStateChanged().Insert(OnDamageStateChanged);
			Print("AUA_NPCDeathMagazineHandler: Successfully attached death event listener", LogLevel.NORMAL);
		}
		else
		{
			Print("AUA_NPCDeathMagazineHandler: Could not find damage manager component", LogLevel.WARNING);
		}
	}

	protected void OnDamageStateChanged(EDamageState damageState)
	{
		Print(string.Format("AUA_NPCDeathMagazineHandler: Damage state changed to %1", damageState), LogLevel.NORMAL);

		// Check for death - character dies when reaching destroyed state
		// Based on enum: UNDAMAGED=0, damaged=1, DESTROYED=2
		if (damageState == EDamageState.DESTROYED)
		{
			Print("AUA_NPCDeathMagazineHandler: Character died (reached DESTROYED state)!", LogLevel.NORMAL);
		}
		else
		{
			Print("AUA_NPCDeathMagazineHandler: Not a death state, ignoring", LogLevel.NORMAL);
			return;
		}

		Print("AUA_NPCDeathMagazineHandler: Death detected!", LogLevel.NORMAL);

		// Only run on server
		if (!Replication.IsServer())
		{
			Print("AUA_NPCDeathMagazineHandler: Not on server, skipping", LogLevel.NORMAL);
			return;
		}

		Print("AUA_NPCDeathMagazineHandler: Running on server", LogLevel.NORMAL);

		IEntity owner = GetOwner();
		if (!owner)
		{
			Print("AUA_NPCDeathMagazineHandler: Owner is null", LogLevel.WARNING);
			return;
		}

		ChimeraCharacter character = ChimeraCharacter.Cast(owner);
		if (!character)
		{
			Print("AUA_NPCDeathMagazineHandler: Owner is not a character", LogLevel.WARNING);
			return;
		}

		Print(string.Format("AUA_NPCDeathMagazineHandler: Processing death for %1", owner), LogLevel.NORMAL);

		// Process magazines and remove explosives
		ProcessInventory(character);
	}

	protected bool IsGrenade(IEntity item)
	{
		if (!item)
			return false;

		// Check by prefab name patterns for grenades
		auto prefabData = item.GetPrefabData();
		if (prefabData)
		{
			string prefabName = prefabData.GetPrefabName();
			prefabName.ToLower();
			if (prefabName.Contains("grenade") || prefabName.Contains("40mm"))
				return true;
		}

		return false;
	}

	protected bool IsRocket(IEntity item)
	{
		if (!item)
			return false;

		// Check by prefab name patterns for rockets/AT weapons
		auto prefabData = item.GetPrefabData();
		if (prefabData)
		{
			string prefabName = prefabData.GetPrefabName();
			prefabName.ToLower();
			if (prefabName.Contains("ammo_rocket"))
				return true;
		}

		return false;
	}

	protected void ProcessInventory(ChimeraCharacter character)
	{
		SCR_InventoryStorageManagerComponent inventoryManager = SCR_InventoryStorageManagerComponent.Cast(character.GetCharacterController().GetInventoryStorageManager());
		if (!inventoryManager)
			return;

		array<IEntity> allItems = {};
		inventoryManager.GetAllRootItems(allItems);

		int processedMagazines = 0;
		int removedGrenades = 0;
		int removedRockets = 0;

		foreach (IEntity item : allItems)
		{
			if (ProcessMagazineItem(item))
				processedMagazines++;

			if (IsGrenade(item))
			{
				Print(string.Format("AUA_NPCDeathMagazineHandler: Removing grenade: %1", item), LogLevel.NORMAL);
				inventoryManager.TryRemoveItemFromInventory(item);
				SCR_EntityHelper.DeleteEntityAndChildren(item);
				removedGrenades++;
			}
			else if (IsRocket(item))
			{
				Print(string.Format("AUA_NPCDeathMagazineHandler: Removing rocket: %1", item), LogLevel.NORMAL);
				inventoryManager.TryRemoveItemFromInventory(item);
				SCR_EntityHelper.DeleteEntityAndChildren(item);
				removedRockets++;
			}
		}

		Print(string.Format("AUA_NPCDeathMagazineHandler: Processed %1 magazines, removed %2 grenades, removed %3 rockets", processedMagazines, removedGrenades, removedRockets), LogLevel.NORMAL);
	}

	protected bool ProcessMagazineItem(IEntity item)
	{
		if (!item)
			return false;

		// Check if item is a weapon with magazines/rockets
		WeaponComponent weaponComponent = WeaponComponent.Cast(item.FindComponent(WeaponComponent));
		if (weaponComponent)
		{
			// Check if this is an RPG or rocket launcher
			auto prefabData = item.GetPrefabData();
			if (prefabData)
			{
				string weaponName = prefabData.GetPrefabName();
				weaponName.ToLower();
				if (weaponName.Contains("rpg") || weaponName.Contains("rocket") || weaponName.Contains("launcher"))
				{
					// Remove loaded rockets from RPG
					array<BaseMuzzleComponent> muzzles = {};
					weaponComponent.GetMuzzlesList(muzzles);

					foreach (BaseMuzzleComponent muzzle : muzzles)
					{
						BaseMagazineComponent magazine = muzzle.GetMagazine();
						if (magazine)
						{
							Print(string.Format("AUA_NPCDeathMagazineHandler: Removing loaded rocket from launcher: %1", magazine), LogLevel.NORMAL);
							// Set ammo to 0 to empty the launcher
							magazine.SetAmmoCount(0);
							// Try to delete the rocket entity if it exists
							IEntity magazineEntity = magazine.GetOwner();
							if (magazineEntity)
							{
								SCR_EntityHelper.DeleteEntityAndChildren(magazineEntity);
								Print("AUA_NPCDeathMagazineHandler: Deleted rocket entity from launcher", LogLevel.NORMAL);
							}
						}
					}
					return true;
				}
			}

			// This is a regular weapon, check for attached magazines
			array<BaseMuzzleComponent> muzzles = {};
			weaponComponent.GetMuzzlesList(muzzles);

			bool processedAny = false;
			foreach (BaseMuzzleComponent muzzle : muzzles)
			{
				BaseMagazineComponent magazine = muzzle.GetMagazine();
				if (magazine && ProcessMagazineComponent(magazine))
					processedAny = true;
			}
			return processedAny;
		}

		// Check if item is a standalone magazine
		BaseMagazineComponent magazineComponent = BaseMagazineComponent.Cast(item.FindComponent(BaseMagazineComponent));
		if (magazineComponent)
		{
			return ProcessMagazineComponent(magazineComponent);
		}

		return false;
	}

	protected bool ProcessMagazineComponent(BaseMagazineComponent magazine)
	{
		if (!magazine)
			return false;

		int currentAmmo = magazine.GetAmmoCount();
		if (currentAmmo <= 3)
			return false; // Already low enough

		// Set random ammo count between 0 and 3
		int newAmmo = Math.RandomInt(0, 4); // 0-3 inclusive
		magazine.SetAmmoCount(newAmmo);

		Print(string.Format("AUA_NPCDeathMagazineHandler: Reduced magazine ammo from %1 to %2", currentAmmo, newAmmo), LogLevel.NORMAL);
		return true;
	}
}
