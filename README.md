# GamersPaperData

Community-maintained board game rule data for [GamersPaper](https://gamerspaper.com).

This repository contains structured JSON files describing board game rules, components, setup instructions, and card data. The GamersPaper app fetches this data to display game references.

## Repository Structure

```
files/                        # Game data (one folder per game)
└── <game_id>/
    ├── <game_id>_rules.json  # Main rules file
    ├── <game_id>_cards.json  # Card data (optional)
    └── ...
icons/                        # SVG icons for game components
registry.json                 # Game index consumed by the app
```

## Contributing

We welcome contributions! To add a new game or improve existing data, see the **[Contributing Guide](CONTRIBUTING.md)** for:

- Full JSON schema reference for rules, cards, components, and more
- Step-by-step instructions for adding a game
- Available icons for components (see [icons/README.md](icons/README.md))
- Validation checklist and PR process

## Quick Start

1. Fork this repo
2. Create `files/<game_id>/<game_id>_rules.json` following the [schema](CONTRIBUTING.md#rules-file-game_id_rulesjson)
3. Add an entry to `registry.json`
4. Open a pull request

## License

Game data is contributed by the community for use with the GamersPaper app.
