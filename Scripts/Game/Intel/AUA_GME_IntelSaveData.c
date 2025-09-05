// AUA_GME_IntelSaveData.c
[EPF_ComponentSaveDataType(GME_IntelComponent), BaseContainerProps()]
class AUA_GME_IntelSaveDataClass : EPF_ComponentSaveDataClass
{
    // You can add more properties or settings if needed
};

[EDF_DbName.Automatic()]
class AUA_GME_IntelSaveData : EPF_ComponentSaveData
{
    string m_sTitle;   // The intel title to persist
    string m_sContent; // The intel content to persist

    // Read the intel data from the component and save it
    override EPF_EReadResult ReadFrom(IEntity owner, GenericComponent component, EPF_ComponentSaveDataClass attributes)
    {
        GME_IntelComponent intelComp = GME_IntelComponent.Cast(component);
        m_sTitle = intelComp.GetTitle();
        m_sContent = intelComp.GetContent();
        return EPF_EReadResult.OK;
    }

    // Apply the saved intel data to the component when loading
    override EPF_EApplyResult ApplyTo(IEntity owner, GenericComponent component, EPF_ComponentSaveDataClass attributes)
    {
        GME_IntelComponent intelComp = GME_IntelComponent.Cast(component);
        intelComp.SetTitle(m_sTitle);
        intelComp.SetContent(m_sContent);
        return EPF_EApplyResult.OK;
    }

    // Compare if the save data is the same (useful for checking if the value has changed)
    override bool Equals(notnull EPF_ComponentSaveData other)
    {
        AUA_GME_IntelSaveData otherData = AUA_GME_IntelSaveData.Cast(other);
        return m_sTitle == otherData.m_sTitle && m_sContent == otherData.m_sContent;
    }
};
