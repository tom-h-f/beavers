use bevy::prelude::*;
use bevy_common_assets::ron::RonAssetPlugin;
use bevy_ecs_tilemap::prelude::*;
use terrain::tiles;

mod camera;
mod terrain;

fn startup(mut commands: Commands, _asset_server: Res<AssetServer>) {
    commands.spawn(Camera2d);
}

fn main() {
    App::new()
        .add_plugins(
            DefaultPlugins
                .set(WindowPlugin {
                    primary_window: Some(Window {
                        title: String::from("Beav.rs"),
                        ..Default::default()
                    }),
                    ..default()
                })
                .set(ImagePlugin::default_nearest()),
        )
        .add_plugins(RonAssetPlugin::<tiles::TileConfig>::new(&["tiles.ron"]))
        .add_plugins(TilemapPlugin)
        .add_systems(Startup, (tiles::load_tiles, startup).chain())
        .add_systems(Update, (tiles::tilemap_loader, camera::movement))
        .run();
}
