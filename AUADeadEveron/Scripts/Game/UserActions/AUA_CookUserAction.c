class AUA_CookUserAction : ScriptedUserAction
{
	protected SCR_FireplaceComponent m_FireplaceComponent;
	
	//------------------------------------------------------------------------------------------------
	override void Init(IEntity pOwnerEntity, GenericComponent pManagerComponent) 
	{
		super.Init(pOwnerEntity, pManagerComponent);
		m_FireplaceComponent = SCR_FireplaceComponent.Cast(pOwnerEntity.FindComponent(SCR_FireplaceComponent));
	}
	
	//------------------------------------------------------------------------------------------------
	override bool CanBeShownScript(IEntity user)
	{
		if (!super.CanBeShownScript(user))
			return false;
		
		if (!m_FireplaceComponent)
			return false;
		
		return m_FireplaceComponent.IsOn();
	}
	
	//------------------------------------------------------------------------------------------------
	override bool GetActionNameScript(out string outName)
	{
		outName = "Готувати";
		return true;
	}
}
