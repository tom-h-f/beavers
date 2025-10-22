# Castor CLI - Beaver Simulation

## TODOs

- ACTUALLY read through bevy docs in-depth. Work out what systems, entities, messages, components, resources DO and where and WHY we should use them.

- Play audio when doing actions

- Generate semi-good terrain, procgen with some kind of river situation. - implement this perhaps: https://rtouti.github.io/graphics/perlin-noise-algorithm

- Create an actual terrain management structure.

- Split each tile into  9 sub-tiles. So beavers can navigate the world or they will be very outscaled of it

- Add beaver state - inventory etc

- World State - Tree/dam/other health/data

- Actually blend beaver animations https://bevy.org/examples/animation/animation-graph/





## Resources

## Code

Good code to read from: https://bevy.org/examples/games/alien-cake-addict/

proced. code to copy for terrain gen?
https://github.com/bones-ai/rust-procedural-world/blob/main/src/terrain.rs

Fantastic physics code: https://bevy.org/examples/movement/physics-in-fixed-timestep/

## UI
- Sounds:  https://kenney.nl/assets/interface-sounds
- Emotes: https://kenney.nl/assets/emotes-pack (Good for showing action of a beaver?)
- Interface: https://kenney.nl/assets/ui-pack-adventure


## Models
Potentially buy this pack for nicer ambience
https://assetstore.unity.com/packages/3d/characters/animals/quirky-series-river-animals-vol-1-183279

### Tiles

#### General

The ground may look better if we use it from this kit https://kenney.nl/assets/tower-defense-kit

#### Dams
To make the Dams, we could use a combination of some of the assets from the other kenney.nl packs
like https://kenney.nl/assets/platformer-kit and https://kenney.nl/assets/graveyard-kit and https://kenney.nl/assets/pirate-kit

I think we ideally want like a incomplete version and various complete versions that show differently

### Sounds

Free Sounds:  https://directory.audio/ 
Could use the foley section for walking sounds, eating sounds can be found too!

## WASM

Optimize wasm files with:
```bash
wasm-opt -Os --output output.wasm input.wasm
```
https://bevy.org/learn/quick-start/getting-started/setup/ go to 'Advanced wasm optimizations'

## Future Planned Features

### AI Interop

I should be able to perform the observation retreival and action instruction via the bevy remote plugin which
they natively provide: https://docs.rs/bevy/latest/bevy/remote/index.html

### Interaction

While we *do* intend for this to be a non-interactive simulation, it might be fun to add a feature where a user can interact with the world and watch the agents interact, such as a meteor strike, giving them a huge cake to eat, or other silly things.
