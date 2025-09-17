# AUA NPC Death Magazine Handler

## Overview
This component reduces NPC magazine ammunition to 0-3 bullets when NPCs die. It processes both weapons with attached magazines and standalone magazines in the NPC's inventory.

## Usage

### Adding to NPCs

1. Open an AI character prefab in Workbench
2. Add the `AUA_NPCDeathMagazineHandler` component to the character entity
3. The component will automatically:
   - Detect when the NPC dies
   - Find all magazines in their inventory
   - Reduce each magazine's ammo count to 0-3 bullets randomly

### Technical Details

- **Server-side only**: Only runs on the server to prevent desync
- **AI characters only**: Automatically detects and only affects AI agents
- **Death event**: Triggers when damage state changes to DESTROYED
- **Magazine types**: Handles both attached weapon magazines and standalone magazines

### Files Created
- `Scripts/Game/AUA_NPCDeathMagazineHandler.c` - The main component

### Integration
The component should be added to AI character prefabs that spawn with weapons/magazines. It will automatically handle the rest once attached.

### Debugging
The component includes Print statements with LogLevel.NORMAL to track:
- When processing begins for a dead NPC
- How many magazines were processed
- Individual magazine ammo reductions

### Testing
Test in Workbench by:
1. Adding component to an AI character prefab
2. Spawning the character with weapons/magazines
3. Killing the character
4. Checking their inventory to verify reduced ammo counts
