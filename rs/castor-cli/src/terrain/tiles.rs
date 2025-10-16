use bevy::prelude::*;
use bevy_ecs_tilemap::prelude::*;
use serde::Deserialize;

#[derive(Asset, TypePath, Deserialize)]
pub struct TileConfig {
    tiles: Vec<String>,
}

#[derive(Resource)]
pub struct TileAssets {
    config: Handle<TileConfig>,
    handles: Option<Vec<Handle<Image>>>,
}

pub fn load_tiles(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.insert_resource(TileAssets {
        config: asset_server.load("tiles.ron"),
        handles: None,
    });
}

// TODO: review how we can make this NOT get called all the time.
pub fn tilemap_loader(
    mut tile_assets: ResMut<TileAssets>,
    tile_configs: Res<Assets<TileConfig>>,
    asset_server: Res<AssetServer>,
    mut commands: Commands,
) {
    if tile_assets.handles.is_some() {
        return;
    }

    if let Some(config) = tile_configs.get(&tile_assets.config) {
        let handles: Vec<Handle<Image>> = config
            .tiles
            .iter()
            .map(|path| asset_server.load(path))
            .collect();

        create_tilemap(&mut commands, handles.clone());
        tile_assets.handles = Some(handles);
    }
}

fn create_tilemap(commands: &mut Commands, tile_handles: Vec<Handle<Image>>) {
    let tilemap_bundles = super::generation::gen_terrain_map(commands, tile_handles);

    for (entity, bundle) in tilemap_bundles {
        commands.entity(entity).insert(bundle);
    }
}

// TODO: try to codegen this from the `tiles.ron` file
// instead of writing this mapping twice.
#[allow(dead_code)]
#[derive(Debug, Clone, Copy)]
pub enum Tile {
    GrassLarge = 0,
    Frog = 1,
}

impl Tile {
    pub fn idx(self) -> TileTextureIndex {
        TileTextureIndex(self as u32)
    }
}
