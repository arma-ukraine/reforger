// ADM_CurrencySaveData.c
[EPF_ComponentSaveDataType(ADM_CurrencyComponent), BaseContainerProps()]
class ADM_CurrencySaveDataClass : EPF_ComponentSaveDataClass
{
    // You can add more properties or settings if needed
};

[EDF_DbName.Automatic()]
class ADM_CurrencySaveData : EPF_ComponentSaveData
{
    int m_iCurrencyValue;  // The currency value we want to persist

    // Read the currency value from the component and save it
    override EPF_EReadResult ReadFrom(IEntity owner, GenericComponent component, EPF_ComponentSaveDataClass attributes)
    {
        ADM_CurrencyComponent currencyComp = ADM_CurrencyComponent.Cast(component);
        m_iCurrencyValue = currencyComp.GetValue();  // Get the currency value from the component
        return EPF_EReadResult.OK;
    }

    // Apply the saved currency value to the component when loading
    override EPF_EApplyResult ApplyTo(IEntity owner, GenericComponent component, EPF_ComponentSaveDataClass attributes)
    {
        ADM_CurrencyComponent currencyComp = ADM_CurrencyComponent.Cast(component);
        currencyComp.SetValue(m_iCurrencyValue);  // Set the saved currency value to the component
        return EPF_EApplyResult.OK;
    }

    // Compare if the save data is the same (useful for checking if the value has changed)
    override bool Equals(notnull EPF_ComponentSaveData other)
    {
        ADM_CurrencySaveData otherData = ADM_CurrencySaveData.Cast(other);
        return m_iCurrencyValue == otherData.m_iCurrencyValue;
    }
};
