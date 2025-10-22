use rand_chacha::ChaCha8Rng;
use std::f32::consts::PI;
use std::time::Duration;

pub use bevy::{
    dev_tools::fps_overlay::{FpsOverlayConfig, FpsOverlayPlugin, FrameTimeGraphConfig},
    prelude::*,
    scene::SceneInstanceReady,
    text::FontSmoothing,
};

use board::Board;

mod beaver;
mod board;
mod diag;

#[derive(States, Clone, Copy, Default, Eq, PartialEq, Hash, Debug)]
enum SimState {
    #[default]
    Playing,
    Paused,
}

#[derive(Resource, Default)]
pub struct BeaverWorld {
    // TODO add stuff here
    pub is_running: bool,
}

fn main() {
    App::new()
        .add_plugins((
            DefaultPlugins,
            FpsOverlayPlugin {
                config: FpsOverlayConfig {
                    text_config: TextFont {
                        font_size: 21.0,
                        ..default()
                    },
                    refresh_interval: Duration::from_millis(100),
                    text_color: Color::srgb(0.0, 1.0, 0.0),
                    enabled: true,
                    frame_time_graph_config: FrameTimeGraphConfig {
                        enabled: true,
                        // The minimum acceptable fps
                        min_fps: 30.0,
                        // The target fps
                        target_fps: 144.0,
                    },
                },
            },
        ))
        .init_resource::<BeaverWorld>()
        .init_resource::<Board>()
        .add_plugins(beaver::beaver_plugin)
        .init_state::<SimState>()
        .add_systems(Startup, (setup_cameras, setup))
        .run();
}

struct Cell {
    height: f32,
}

#[derive(Resource, Deref, DerefMut)]
struct Random(ChaCha8Rng);

fn setup_cameras(mut commands: Commands) {
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(-10.0, 10.0, 0.0).looking_at(Vec3::from(board::RESET_FOCUS), Dir3::Y),
    ));
}

pub fn setup(mut commands: Commands, asset_server: Res<AssetServer>, mut board: ResMut<Board>) {
    commands.spawn((
        DespawnOnExit(SimState::Playing),
        PointLight {
            intensity: 2_000_000.0,
            shadows_enabled: true,
            range: 300.0,
            ..default()
        },
        Transform::from_xyz(4.0, 10.0, 4.0),
    ));

    board::generate_terrain(&mut board, &mut commands, &asset_server);
}
