use super::{tiles::Tile, GRID_HEIGHT, GRID_WIDTH};
use bevy::prelude::*;
use bevy_ecs_tilemap::prelude::*;
use bevy_ecs_tilemap::{
    map::{TilemapId, TilemapSize},
    tiles::TileStorage,
};
use rand::Rng;

#[derive(Debug, Copy, Clone)]
pub struct HeightMap {
    data: [[usize; GRID_WIDTH as usize]; GRID_HEIGHT as usize],
}

impl HeightMap {
    fn new() -> Self {
        let mut rng = rand::thread_rng();
        let data = std::array::from_fn(|_| std::array::from_fn(|_| rng.gen_range(0..2)));
        Self { data }
    }

    fn get(&self, x: u32, y: u32) -> usize {
        self.data[y as usize][x as usize]
    }
}

pub fn gen_terrain_map(
    commands: &mut Commands,
    tile_handles: Vec<Handle<Image>>,
) -> Vec<(Entity, TilemapBundle)> {
    let heightmap = HeightMap::new();
    let map_size = TilemapSize {
        x: GRID_WIDTH as u32,
        y: GRID_HEIGHT as u32,
    };
    let tile_size = TilemapTileSize { x: 256.0, y: 256.0 };
    let grid_size = TilemapGridSize { x: 200.0, y: 116.0 };
    let map_type = TilemapType::Isometric(IsoCoordSystem::Diamond);

    let mut bundles = Vec::new();

    for height_level in 0..4 {
        let tilemap_entity = commands.spawn_empty().id();
        let tilemap_id = TilemapId(tilemap_entity);
        let mut tile_storage = TileStorage::empty(map_size);

        // Only place tiles at positions matching this height level
        for x in 0..GRID_WIDTH {
            for y in 0..GRID_HEIGHT {
                let tile_height = heightmap.get(x, y);

                if tile_height == height_level {
                    let tile_pos = TilePos {
                        x: x as u32,
                        y: y as u32,
                    };

                    let tile_entity = commands
                        .spawn(TileBundle {
                            position: tile_pos,
                            tilemap_id,
                            texture_index: Tile::GrassLarge.idx(),
                            ..Default::default()
                        })
                        .id();

                    tile_storage.set(&tile_pos, tile_entity);
                }
            }
        }

        let bundle = TilemapBundle {
            grid_size,
            size: map_size,
            storage: tile_storage,
            texture: TilemapTexture::Vector(tile_handles.clone()),
            tile_size,
            map_type,
            anchor: TilemapAnchor::Center,
            transform: Transform::from_xyz(0.0, height_level as f32 * -10.0, height_level as f32),
            render_settings: TilemapRenderSettings {
                render_chunk_size: UVec2::new(2, 1),
                y_sort: true,
            },
            ..Default::default()
        };

        bundles.push((tilemap_entity, bundle));
    }

    bundles
}
