# GamePaperData

Community-maintained board game rule models for [GamePaper](https://github.com/nibuen/GamePaper).

## Structure

```
files/
└── <game_id>/
    ├── <game_id>_rules.json      # Main rules file
    ├── <game_id>_<cards>.json    # Card data files (referenced by rules)
    └── ...
registry.json                      # Game index consumed by the app
```

## Registry

The `registry.json` file lists all available games. The GamePaper app fetches this file to discover remotely-hosted games.

## Contributing

To add a new game:

1. Create a directory under `files/` named with the game's snake_case ID
2. Add the rules JSON and any card data files
3. Add an entry to `registry.json`
4. Open a pull request

See the [GamePaper model documentation](https://github.com/nibuen/GamePaper/blob/main/model.md) for the JSON schema.
