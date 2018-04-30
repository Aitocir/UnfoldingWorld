# UnfoldingWorld
Unfolding World is a text-based, multi-player RPG with a procedurally-generated world. This is my entry into the [Enter the Multi-User Dungeon Game Jam](https://itch.io/jam/enterthemud). It's built with [pymug](https://github.com/Aitocir/Pymug) and lots and lots of derping.

## features
Unfolding World is named so because the game generates new locations on the fly as players visit them for the first time. The starting location is the Origin Tree, and the game measures other locations in the node distance from the Origin Tree. The farther the player gets, the more difficult survival becomes. If a player dies, they resurrect at the Origin Tree without their inventory but with all of their character XP. 

## game commands

### go
```go <location>```

This will cause your character to move to <location>

### say
```say <stuff to say>```

This will cause your character to speak to the area at large (everyone in the general area will hear you)

### whisper
```whisper <character> <stuff to whisper>```

This will cause your character to whisper quietly to another character in the same area (nobody but the other character will hear you)
