class AUA_FillCanteenUserAction : ScriptedUserAction
{
	protected SCR_FireplaceComponent m_FireplaceComponent;
	
	//------------------------------------------------------------------------------------------------
	override void Init(IEntity pOwnerEntity, GenericComponent pManagerComponent)
	{
		m_FireplaceComponent = SCR_FireplaceComponent.Cast(pOwnerEntity.FindComponent(SCR_FireplaceComponent));
	}

	//------------------------------------------------------------------------------------------------	
	override bool CanBeShownScript(IEntity user)
	{
		if (!user)
			return false;
		
		if (!m_FireplaceComponent)
			return false;
		
		return m_FireplaceComponent.IsOn();
	}
	
	//------------------------------------------------------------------------------------------------
	override void PerformAction(IEntity pOwnerEntity, IEntity pUserEntity)
	{
		ChimeraCharacter userCharacter = ChimeraCharacter.Cast(pUserEntity);
		if (!userCharacter)
			return;
		
		SCR_CharacterDamageManagerComponent damageComponent = SCR_CharacterDamageManagerComponent.Cast(userCharacter.GetDamageManager());
		if (!damageComponent)
			return;
		
		damageComponent.FullHeal();
	}
};
