# UnfoldingWorld
Unfolding World is a text-based, multi-player RPG with a procedurally-generated world. This is my entry into the [Enter the Multi-User Dungeon Game Jam](https://itch.io/jam/enterthemud). It's built with [pymug](https://github.com/Aitocir/Pymug) and lots and lots of derping.

## features
Unfolding World is named so because the game generates new locations on a repeating timer. Currently, the world is very boring (though wonderful, as 100% of all tiles have huckleberry bushes on them).

## game commands

### go
```go <location>```

This will cause your character to move to <location>

### say
```say <stuff to say>```

This will cause your character to speak to the area at large (everyone in the general area will hear you)

### search
```search plants```

This wil cause your character to search the immediate area for interactable objects. For now, the only supported parameter is "plants".

### whisper
```whisper <character> <stuff to whisper>```

This will cause your character to whisper quietly to another character in the same area (nobody but the other character will hear you)
