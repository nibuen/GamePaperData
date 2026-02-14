# Board Game Icons

This directory contains 259 SVG icons for use in game JSON files. Icons represent common board game components like cards, dice, tokens, pawns, resources, and structures.

## How to Use Icons in Game JSON

Reference an icon by its filename (without the `.svg` extension) in the `"icon"` field of a component:

```json
{
  "name": "Wheat Tokens",
  "type": "Resource",
  "description": "12 wheat resource tokens",
  "icon": "resource_wheat"
}
```

The app resolves the icon name to the corresponding SVG file automatically.

## Available Icons

### Arrows & Direction
`arrow_clockwise`, `arrow_counterclockwise`, `arrow_cross`, `arrow_cross_divided`, `arrow_diagonal`, `arrow_diagonal_cross`, `arrow_diagonal_cross_divided`, `arrow_horizontal`, `arrow_reserve`, `arrow_right`, `arrow_right_curve`, `arrow_rotate`, `direction_e`, `direction_n`, `direction_s`, `direction_w`

### Cards
`card`, `card_add`, `card_diagonal`, `card_down`, `card_down_outline`, `card_flip`, `card_flipdouble`, `card_lift`, `card_outline`, `card_outline_lift`, `card_outline_place`, `card_outline_remove`, `card_place`, `card_remove`, `card_rotate`, `card_subtract`, `card_tap`, `card_tap_down`, `card_tap_outline`, `card_tap_outline_down`, `card_tap_outline_up`, `card_tap_up`, `card_target`, `cards_collection`, `cards_collection_outline`, `cards_diagonal`, `cards_fan`, `cards_fan_outline`, `cards_flip`, `cards_order`, `cards_return`, `cards_seek`, `cards_seek_top`, `cards_shift`, `cards_shuffle`, `cards_skull`, `cards_stack`, `cards_stack_cross`, `cards_stack_high`, `cards_take`, `cards_under`

### Characters & Pawns
`character`, `character_lift`, `character_place`, `character_remove`, `pawn`, `pawn_clockwise`, `pawn_counterclockwise`, `pawn_down`, `pawn_flip`, `pawn_left`, `pawn_reverse`, `pawn_right`, `pawn_skip`, `pawn_table`, `pawn_up`, `pawns`

### Chess Pieces
`chess_bishop`, `chess_king`, `chess_knight`, `chess_pawn`, `chess_queen`, `chess_rook`

### Dice
`d2`, `d2_number`, `d2_outline`, `d2_outline_number`, `d3`, `d3_number`, `d3_outline`, `d3_outline_number`, `d4`, `d4_number`, `d4_outline`, `d4_outline_number`, `d6`, `d6_number`, `d6_outline`, `d6_outline_number`, `d8`, `d8_number`, `d8_outline`, `d8_outline_number`, `d10`, `d10_number`, `d10_outline`, `d10_outline_number`, `d12`, `d12_number`, `d12_outline`, `d12_outline_number`, `d20`, `d20_number`, `d20_outline`, `d20_outline_number`, `dice`, `dice_1`, `dice_2`, `dice_3`, `dice_3D`, `dice_3D_detailed`, `dice_4`, `dice_5`, `dice_6`, `dice_close`, `dice_detailed`, `dice_empty`, `dice_out`, `dice_question`, `dice_shield`, `dice_skull`, `dice_sword`

### Flasks
`flask_empty`, `flask_full`, `flask_half`

### Flips (Coins)
`flip_empty`, `flip_full`, `flip_half`, `flip_head`, `flip_tails`

### Flags
`flag_square`, `flag_triangle`

### Hands
`hand`, `hand_card`, `hand_cross`, `hand_cube`, `hand_hexagon`, `hand_token`, `hand_token_open`

### Hexagons & Shapes
`hexagon`, `hexagon_in`, `hexagon_out`, `hexagon_outline`, `hexagon_question`, `hexagon_switch`, `hexagon_tile`, `pentagon`, `pentagon_outline`, `pentagon_question`, `rhombus`, `rhombus_outline`, `rhombus_question`

### Pouches
`pouch`, `pouch_add`, `pouch_remove`

### Resources
`resource_apple`, `resource_fish`, `resource_grapes`, `resource_iron`, `resource_lumber`, `resource_planks`, `resource_rose`, `resource_stone`, `resource_wheat`, `resource_wood`

### Structures
`structure_church`, `structure_farm`, `structure_gate`, `structure_house`, `structure_tower`, `structure_wall`, `structure_watchtower`

### Suit (Card Suits)
`suit_clubs`, `suit_diamonds`, `suit_hearts`, `suit_hearts_broken`, `suit_spades`

### Tags (Numbered Labels)
`tag_1`, `tag_2`, `tag_3`, `tag_4`, `tag_5`, `tag_6`, `tag_7`, `tag_8`, `tag_9`, `tag_10`, `tag_d6`, `tag_d6_1`, `tag_d6_2`, `tag_d6_3`, `tag_d6_4`, `tag_d6_5`, `tag_d6_6`, `tag_d6_check`, `tag_d6_cross`, `tag_d6_infinte`, `tag_empty`, `tag_infinite`, `tag_shield`, `tag_shield_1`, `tag_shield_2`, `tag_shield_3`, `tag_shield_4`, `tag_shield_5`, `tag_shield_6`, `tag_shield_7`, `tag_shield_8`, `tag_shield_9`, `tag_shield_10`, `tag_shield_infinite`

### Timers & Hourglasses
`hourglass`, `hourglass_bottom`, `hourglass_top`, `timer_0`, `timer_100`, `timer_CCW_25`, `timer_CCW_50`, `timer_CCW_75`, `timer_CW_25`, `timer_CW_50`, `timer_CW_75`

### Tokens
`token`, `token_add`, `token_give`, `token_in`, `token_out`, `token_remove`, `token_subtract`, `tokens`, `tokens_shadow`, `tokens_stack`

### Miscellaneous
`award`, `book_closed`, `book_open`, `bow`, `campfire`, `crown_a`, `crown_b`, `dollar`, `exploding`, `exploding_6`, `fire`, `lock_closed`, `lock_open`, `notepad`, `notepad_write`, `puzzle`, `shield`, `skull`, `spinner`, `spinner_segment`, `sword`

## Adding New Icons

To contribute a new icon:

1. Create an SVG file following these conventions:
   - **Size**: 24x24 viewport (`viewBox="0 0 24 24"`)
   - **Style**: Single-color, monochrome (the app applies color via tint)
   - **Naming**: Use `snake_case` (e.g., `resource_gold.svg`)
   - **No embedded styles or fonts** — use pure path data
2. Place the SVG file in this `icons/` directory
3. Reference it in your game JSON by filename (without `.svg`)
4. Open a pull request
