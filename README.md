# Notes

* [Reforger Shop System](https://github.com/ekudmada/Reforger-Shop-System) "Purchase" button does nothing:
 - If you have your own player controller prefab you must add the ADM_PlayerShopManager component to it. This controls communicating to the server to request purchasing. The project overrides the DefaultPlayerControllerMP prefab to achieve this.

* In order to save data for the custom component on a prefab you need to:
 - https://github.com/Arkensor/EnfusionPersistenceFramework/blob/armareforger/docs/custom-component.md
 - Add the class you just wrote into the respective components section of your prefab's EPF_PersistanceComponent SaveData->Components.

* "Shop not found" error in logs and interface closes but nothing happening on purchase.
 - Make sure prefab shop is tied to replicated. So replication component exists and is enabled.
