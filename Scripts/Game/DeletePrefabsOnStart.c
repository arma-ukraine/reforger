// Deletes specified prefabs once at mission start (server-side).
// Attach to a server-authoritative entity (e.g. `SCR_BaseGameMode`).
[ComponentEditorProps(category: "GameScripted/Custom", description: "Delete selected prefabs on mission start (server-only)")]
class DeletePrefabOnStartClass : ScriptComponentClass {}

class DeletePrefabOnStart : ScriptComponent
{
    [Attribute("", UIWidgets.ResourceNamePicker, "Prefabs (.et) to delete on mission start", "et")]
    protected ref array<ResourceName> m_PrefabsToDelete;
    protected int m_DeletedCount = 0;
    protected ref array<string> m_ConfiguredPathsNoGuid;
    protected ref array<string> m_ConfiguredBaseNames;

    override void OnPostInit(IEntity owner)
    {
        super.OnPostInit(owner);
        SetEventMask(owner, EntityEvent.INIT);
        Print("DeletePrefabOnStart: Requested INIT event", LogLevel.NORMAL);
        Print("DeletePrefabOnStart: OnPostInit", LogLevel.NORMAL);
    }

    override void EOnInit(IEntity owner)
    {
        Print("DeletePrefabOnStart: EOnInit", LogLevel.NORMAL);
        // Ensure server authority (multiplayer safe)
        if (!Replication.IsServer())
        {
            Print("DeletePrefabOnStart: Not server - skipping", LogLevel.NORMAL);
            return;
        }

        // Ensure running gameplay, not just editor load
        if (!GetGame().InPlayMode())
        {
            Print("DeletePrefabOnStart: Not in play mode - skipping", LogLevel.NORMAL);
            return;
        }

        if (!m_PrefabsToDelete || m_PrefabsToDelete.IsEmpty())
        {
            Print("DeletePrefabOnStart: No prefabs specified to delete.", LogLevel.WARNING);
            return;
        }

        m_DeletedCount = 0;

        // Prepare diagnostics: configured full, path-only, and base names
        Print("DeletePrefabOnStart: Configured prefabs (full) begin", LogLevel.NORMAL);
        foreach (ResourceName rnFull : m_PrefabsToDelete)
        {
            Print(string.Format("DeletePrefabOnStart: Configured full: %1", rnFull), LogLevel.NORMAL);
        }
        Print("DeletePrefabOnStart: Configured prefabs (full) end", LogLevel.NORMAL);

        m_ConfiguredPathsNoGuid = new array<string>();
        m_ConfiguredBaseNames = new array<string>();
        Print("DeletePrefabOnStart: Configured prefabs (path-only) begin", LogLevel.NORMAL);
        foreach (ResourceName rn2 : m_PrefabsToDelete)
        {
            string withoutGuid = StripGuid(rn2);
            m_ConfiguredPathsNoGuid.Insert(withoutGuid);
            Print(string.Format("DeletePrefabOnStart: Configured path: %1", withoutGuid), LogLevel.NORMAL);
            string baseName = GetBaseName(withoutGuid);
            if (!baseName.IsEmpty())
                m_ConfiguredBaseNames.Insert(baseName);
        }
        Print("DeletePrefabOnStart: Configured prefabs (path-only) end", LogLevel.NORMAL);

        // Run a single scan at init
        ScanWorld();
    }

    protected bool OnVisitEntity(IEntity entity)
    {
        if (!entity)
            return true;

        auto pd = entity.GetPrefabData();
        if (!pd)
            return true;

        ResourceName prefabName = pd.GetPrefabName();
        string pathOnly = StripGuid(prefabName);
        string entityBase = GetBaseName(pathOnly);

        if (m_PrefabsToDelete && m_PrefabsToDelete.Contains(prefabName))
        {
            Print(string.Format("DeletePrefabOnStart: Match full, deleting: %1", prefabName), LogLevel.NORMAL);
            SCR_EntityHelper.DeleteEntityAndChildren(entity);
            m_DeletedCount++;
            Print("DeletePrefabOnStart: Deleted entity", LogLevel.NORMAL);
        }

        return true; // continue enumeration
    }

    protected void ScanWorld()
    {
        auto world = GetGame().GetWorld();
        if (!world)
        {
            Print("DeletePrefabOnStart: World is null - skipping", LogLevel.ERROR);
            return;
        }
        vector center = "0 0 0";
        float radius = 1000000.0;
        Print("DeletePrefabOnStart: Scanning world", LogLevel.NORMAL);
        world.QueryEntitiesBySphere(center, radius, OnVisitEntity);
        Print("DeletePrefabOnStart: Done", LogLevel.NORMAL);
    }

    protected string StripGuid(ResourceName res)
    {
        string s = res;
        int idx = s.IndexOf("}");
        if (idx >= 0)
        {
            int len = s.Length();
            int start = idx + 1;
            if (start < len)
                return s.Substring(start, len - start);
            return "";
        }
        return s;
    }

    protected string GetBaseName(string path)
    {
        int slash = path.LastIndexOf("/");
        if (slash == -1)
            return path;
        int len = path.Length();
        int start = slash + 1;
        if (start < len)
            return path.Substring(start, len - start);
        return "";
    }
}
