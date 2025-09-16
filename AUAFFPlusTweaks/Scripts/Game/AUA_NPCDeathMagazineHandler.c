// Modifies NPC magazine ammo to 0-3 bullets when they die and removes grenades/rockets
[ComponentEditorProps(category: "GameScripted/Custom", description: "Reduces NPC magazine ammo on death and removes explosives")]
class AUA_NPCDeathMagazineHandlerClass : ScriptComponentClass {}

class AUA_NPCDeathMagazineHandler : ScriptComponent
{
	// Configurable patterns for items to delete from NPC inventory
	protected static ref array<string> ITEMS_TO_DELETE_PATTERNS = {"grenade", "40mm", "ammo_rocket"};
	protected static ref array<string> LAUNCHER_PATTERNS = {"rpg", "rocket", "launcher"};

	// Magazine ammo reduction constants
	protected static const int MIN_AMMO_COUNT = 0;
	protected static const int MAX_AMMO_COUNT = 3;
	override void OnPostInit(IEntity owner)
	{
		super.OnPostInit(owner);
		SetEventMask(owner, EntityEvent.INIT);
	}

	override void EOnInit(IEntity owner)
	{
		// Only run in actual gameplay, not in editor
		if (!GetGame().InPlayMode())
			return;

		// Check if this is a character
		ChimeraCharacter character = ChimeraCharacter.Cast(owner);
		if (!character)
			return;

		// Check if this is NOT a player (skip players)
		PlayerController playerController = GetGame().GetPlayerController();
		if (playerController && playerController.GetControlledEntity() == character)
			return;

		// Setup death monitoring - damage manager should be ready now
		SetupDeathMonitoring(character);
	}

	protected void SetupDeathMonitoring(ChimeraCharacter character)
	{
		if (!character)
			return;

		// Listen for death events
		SCR_CharacterDamageManagerComponent damageManager = SCR_CharacterDamageManagerComponent.Cast(character.GetDamageManager());
		if (damageManager)
		{
			damageManager.GetOnDamageStateChanged().Insert(OnDamageStateChanged);
		}
		else
		{
			Print("AUA_NPCDeathMagazineHandler: Could not find damage manager component", LogLevel.WARNING);
		}
	}

	protected void OnDamageStateChanged(EDamageState damageState)
	{
		// Check for death - character dies when reaching destroyed state
		// Based on enum: UNDAMAGED=0, damaged=1, DESTROYED=2
		if (damageState != EDamageState.DESTROYED)
			return;

		// Only run on server
		if (!Replication.IsServer())
			return;

		IEntity owner = GetOwner();
		if (!owner)
			return;

		ChimeraCharacter character = ChimeraCharacter.Cast(owner);
		if (!character)
			return;

		// Process magazines and remove explosives
		ProcessInventory(character);
	}

	protected bool ShouldDeleteItem(IEntity item)
	{
		if (!item)
			return false;

		// Check by prefab name patterns for items to delete
		auto prefabData = item.GetPrefabData();
		if (prefabData)
		{
			string prefabName = prefabData.GetPrefabName();
			prefabName.ToLower();

			foreach (string pattern : ITEMS_TO_DELETE_PATTERNS)
			{
				if (prefabName.Contains(pattern))
					return true;
			}
		}

		return false;
	}

	protected bool IsLauncher(IEntity item)
	{
		if (!item)
			return false;

		// Check by prefab name patterns for rocket launchers
		auto prefabData = item.GetPrefabData();
		if (prefabData)
		{
			string prefabName = prefabData.GetPrefabName();
			prefabName.ToLower();

			foreach (string pattern : LAUNCHER_PATTERNS)
			{
				if (prefabName.Contains(pattern))
					return true;
			}
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
		int removedItems = 0;

		foreach (IEntity item : allItems)
		{
			if (ProcessMagazineItem(item))
				processedMagazines++;

			if (ShouldDeleteItem(item))
			{
				inventoryManager.TryRemoveItemFromInventory(item);
				SCR_EntityHelper.DeleteEntityAndChildren(item);
				removedItems++;
			}
		}

		Print(string.Format("AUA_NPCDeathMagazineHandler: Processed %1 magazines, removed %2 items", processedMagazines, removedItems), LogLevel.NORMAL);
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
			if (IsLauncher(item))
			{
				// Remove loaded rockets from RPG
				array<BaseMuzzleComponent> muzzles = {};
				weaponComponent.GetMuzzlesList(muzzles);

				foreach (BaseMuzzleComponent muzzle : muzzles)
				{
					BaseMagazineComponent magazine = muzzle.GetMagazine();
					if (magazine)
					{
						// Set ammo to minimum count to empty the launcher
						magazine.SetAmmoCount(MIN_AMMO_COUNT);
						// Try to delete the rocket entity if it exists
						IEntity magazineEntity = magazine.GetOwner();
						if (magazineEntity)
						{
							SCR_EntityHelper.DeleteEntityAndChildren(magazineEntity);
						}
					}
				}
				return true;
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
		if (currentAmmo <= MAX_AMMO_COUNT)
			return false; // Already low enough

		// Set random ammo count between MIN_AMMO_COUNT and MAX_AMMO_COUNT
		int newAmmo = Math.RandomInt(MIN_AMMO_COUNT, MAX_AMMO_COUNT + 1); // +1 because RandomInt is exclusive on upper bound
		magazine.SetAmmoCount(newAmmo);
		return true;
	}
}
