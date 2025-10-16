use crate::terrain::{GRID_HEIGHT, GRID_WIDTH};

use super::{tiles::Tile, GRID_SZ};
use bevy::prelude::*;
use bevy_ecs_tilemap::prelude::*;
use bevy_ecs_tilemap::{
    map::{TilemapId, TilemapSize},
    tiles::TileStorage,
};
use rand::Rng;

#[derive(Debug, Copy, Clone)]
pub struct HeightMap([usize; GRID_SZ]);

pub fn gen_terrain_map(
    mut tile_storage: &mut TileStorage,
    mut commands: &mut Commands,
    tilemap_id: TilemapId,
) {
    let heightmap = generate_heightmap();
    // Iterate through each x position in the heightmap
    for x in 0..GRID_WIDTH {
        for y in 0..GRID_HEIGHT {
            let tile_pos = TilePos {
                x: x as u32,
                y: y as u32,
            };
            let height = heightmap.0[(x + y) as usize];
            println!("{} {} {}", x, y, height);

            let tile_entity = commands
                .spawn(TileBundle {
                    position: tile_pos,
                    tilemap_id,
                    texture_index: Tile::Frog.idx(),
                    ..Default::default()
                })
                .id();

            let z = (y as f32 * 0.1) + (height as f32);

            commands
                .entity(tile_entity)
                .insert(Transform::from_xyz(0.0, 0.0, z));

            tile_storage.set(&tile_pos, tile_entity);
        }
    }
}

fn generate_heightmap() -> HeightMap {
    let mut rng = rand::thread_rng();
    return HeightMap(std::array::from_fn(|_| rng.gen_range(0..4)));
}
