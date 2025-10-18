# Castor CLI - Beaver Simulation

## TODOs

- Generate semi-good terrain, procgen with some kind of river situation. - implement this perhaps: https://rtouti.github.io/graphics/perlin-noise-algorithm

- Beaver Animations: Implement this from scratch using bevy guides and use the gltf animations
- Add beaver state - inventory etc

- World State - Tree/dam/other health/data

- General Animations for misc stuff

- Menu


## Resources

Good code to read from: https://bevy.org/examples/games/alien-cake-addict/

proced. code to copy for terrain gen?
https://github.com/bones-ai/rust-procedural-world/blob/main/src/terrain.rs

Potentially buy this pack for nicer ambience

## WASM

Optimize wasm files with:
```bash
wasm-opt -Os --output output.wasm input.wasm
```
https://bevy.org/learn/quick-start/getting-started/setup/ go to 'Advanced wasm optimizations'

