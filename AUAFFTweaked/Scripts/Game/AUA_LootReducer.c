// Reduces NPC loot quality when they die - limits magazine ammo and removes explosives
[ComponentEditorProps(category: "GameScripted/Custom", description: "Reduces NPC loot quality on death")]
class AUA_LootReducerClass : ScriptComponentClass {}

class AUA_LootReducer : ScriptComponent
{
	// ==============================================
	// CONFIGURATION CONSTANTS - MODIFY THESE TO ADJUST BEHAVIOR
	// ==============================================

	// Probability settings
	protected static const float PRISTINE_LOOT_CHANCE = 0.2; // Chance to keep loot pristine (no processing)

	// Magazine processing probabilities (for standalone magazines only)
	protected static const float MAGAZINE_EMPTY_CHANCE = 0.8; // Chance for standalone magazines to be completely empty
	protected static const float MAGAZINE_MIN_PERCENTAGE = 0.1; // Minimum ammo when standalone magazine is not empty
	protected static const float MAGAZINE_MAX_PERCENTAGE = 0.5; // Maximum ammo when standalone magazine is not empty

	// Loaded magazine ammo limits (magazines in weapons)
	protected static const int LOADED_MAG_MIN_AMMO = 0; // Minimum ammo for loaded magazines (goes to full capacity)

	// Item deletion configuration - easily extensible
	// Format: {patterns_array, probability_as_string}
	protected static ref array<ref array<ref array<string>>> DELETION_CONFIG = {
		{{"items/medicine", "items/equipment"}, {"0.95"}}, // medical items, maps, etc.
		{{"weapons/grenades","weapons/ammo"}, {"0.8"}}, // grenades, rockets, etc.
	};

	protected static const ref array<string> LAUNCHER_PATTERNS = {"weapons/launchers"};

	// Items exempt from all processing (neither magazine processing nor deletion)
	protected static const ref array<string> EXEMPT_ITEM_PATTERNS = {
		"items/equipment/accessories/dogtags"
	};
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
		// Use SCR_CharacterHelper to check if this is a player
		if (SCR_CharacterHelper.IsAPlayer(character))
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
			Print("AUA_LootReducer: Could not find damage manager component", LogLevel.WARNING);
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

		// Double-check if this is NOT a player (skip players)
		// Player might have taken control after initialization
		if (SCR_CharacterHelper.IsAPlayer(character))
			return;

		// Process magazines and remove explosives
		ProcessInventory(character);
	}

	protected bool IsItemExempt(IEntity item)
	{
		if (!item)
			return false;

		auto prefabData = item.GetPrefabData();
		if (!prefabData)
			return false;

		string prefabName = prefabData.GetPrefabName();
		prefabName.ToLower();

		// Check if item matches any exempt pattern
		foreach (string pattern : EXEMPT_ITEM_PATTERNS)
		{
			if (prefabName.Contains(pattern))
				return true;
		}

		return false;
	}

	protected bool ShouldDeleteItem(IEntity item)
	{
		if (!item)
			return false;

		// Check by prefab name patterns for items to delete
		auto prefabData = item.GetPrefabData();
		if (!prefabData)
			return false;

		string prefabName = prefabData.GetPrefabName();
		prefabName.ToLower();

		// Check each deletion config entry
		foreach (auto configEntry : DELETION_CONFIG)
		{
			if (configEntry.Count() < 2)
				continue;

			// Get patterns array and probability
			auto patterns = configEntry[0];
			float deletionChance = configEntry[1][0].ToFloat();

			// Check if item matches any pattern in this config entry
			foreach (string pattern : patterns)
			{
				if (prefabName.Contains(pattern))
				{
					// Roll for deletion based on probability
					float randomRoll = Math.RandomFloat01();
					return randomRoll < deletionChance;
				}
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
			// Check if item is exempt from all processing
			if (IsItemExempt(item))
				continue;

			// Chance to keep this item completely pristine
			float randomChance = Math.RandomFloat01();
			if (randomChance < PRISTINE_LOOT_CHANCE)
				continue; // Skip processing this item entirely

			if (ProcessMagazineItem(item))
				processedMagazines++;

			if (ShouldDeleteItem(item))
			{
				inventoryManager.TryRemoveItemFromInventory(item);
				SCR_EntityHelper.DeleteEntityAndChildren(item);
				removedItems++;
			}
		}

		Print(string.Format("AUA_LootReducer: Processed %1 magazines, removed %2 items", processedMagazines, removedItems), LogLevel.NORMAL);
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
						magazine.SetAmmoCount(LOADED_MAG_MIN_AMMO);
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
				if (magazine && ProcessMagazineComponent(magazine, true)) // true = loaded magazine
					processedAny = true;
			}
			return processedAny;
		}

		// Check if item is a standalone magazine
		BaseMagazineComponent magazineComponent = BaseMagazineComponent.Cast(item.FindComponent(BaseMagazineComponent));
		if (magazineComponent)
		{
			return ProcessMagazineComponent(magazineComponent, false); // false = standalone magazine
		}

		return false;
	}

	protected bool ProcessMagazineComponent(BaseMagazineComponent magazine, bool isLoadedInWeapon = false)
	{
		if (!magazine)
			return false;

		int currentAmmo = magazine.GetAmmoCount();
		int newAmmo;

		if (isLoadedInWeapon)
		{
			// Loaded magazines: random ammo from 0 to full capacity
			int maxCapacity = magazine.GetMaxAmmoCount();
			newAmmo = Math.RandomInt(LOADED_MAG_MIN_AMMO, maxCapacity + 1); // +1 because RandomInt is exclusive on upper bound
		}
		else
		{
			// Standalone magazines: new weighted system
			float emptyChance = Math.RandomFloat01();
			if (emptyChance < MAGAZINE_EMPTY_CHANCE)
			{
				// Empty magazine
				newAmmo = 0;
			}
			else
			{
				// Partially filled magazine based on percentage of capacity
				int maxCapacity = magazine.GetMaxAmmoCount();
				int minAmmo = Math.Max(1, Math.Round(maxCapacity * MAGAZINE_MIN_PERCENTAGE)); // At least 1 bullet
				int maxAmmo = Math.Max(minAmmo, Math.Round(maxCapacity * MAGAZINE_MAX_PERCENTAGE));
				newAmmo = Math.RandomInt(minAmmo, maxAmmo + 1); // +1 because RandomInt is exclusive on upper bound
			}
		}

		magazine.SetAmmoCount(newAmmo);
		return true;
	}
}
