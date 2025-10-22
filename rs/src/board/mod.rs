use crate::*;

pub mod tile;

pub const SIZE_I: usize = 8;
pub const SIZE_J: usize = 8;

pub const RESET_FOCUS: [f32; 3] = [SIZE_I as f32 / 2.0, 0.0, SIZE_J as f32 / 2.0 - 0.5];

#[derive(Resource, Default)]
pub struct Game {
    pub board: Vec<Vec<Cell>>,
    pub player: Beaver,
    pub score: i32,
    pub camera_should_focus: Vec3,
    pub camera_is_focus: Vec3,
}

pub fn spawn_world(
    game: &mut ResMut<Game>,
    commands: &mut Commands,
    asset_server: &Res<AssetServer>,
) {
    // TODO: just load these into a loader or some storage of this
    let ground_grass = board::tile::Tile::GroundGrass.load(asset_server);
    let river_side = board::tile::Tile::GroundRiverSide.load(asset_server);
    let river_open = board::tile::Tile::GroundRiverOpen.load(asset_server);

    game.board = (0..board::SIZE_J)
        .map(|j| {
            (0..board::SIZE_I)
                .map(|i| {
                    let x = board::SIZE_I / 2;
                    if x == i {
                        commands.spawn((
                            DespawnOnExit(GameState::Playing),
                            Transform::from_xyz(i as f32, 0.0 as f32, j as f32),
                            SceneRoot(river_open.clone()),
                        ));
                    } else if x == i.wrapping_sub(1) {
                        commands.spawn((
                            DespawnOnExit(GameState::Playing),
                            Transform::from_translation(Vec3::new(i as f32, 0.0, j as f32))
                                .with_rotation(Quat::from_rotation_y(-std::f32::consts::FRAC_PI_2)),
                            SceneRoot(river_side.clone()),
                        ));
                    } else if x == i + 1 {
                        commands.spawn((
                            DespawnOnExit(GameState::Playing),
                            Transform::from_translation(Vec3::new(i as f32, 0.0, j as f32))
                                .with_rotation(Quat::from_rotation_y(std::f32::consts::FRAC_PI_2)),
                            SceneRoot(river_side.clone()),
                        ));
                    } else {
                        commands.spawn((
                            DespawnOnExit(GameState::Playing),
                            Transform::from_xyz(i as f32, 0.0, j as f32),
                            SceneRoot(ground_grass.clone()),
                        ));
                    }
                    Cell { height: 0.0 }
                })
                .collect()
        })
        .collect();
}
pub fn spawn_beaver(
    game: &mut ResMut<Game>,
    commands: &mut Commands,
    mut graphs: ResMut<Assets<AnimationGraph>>,
    asset_server: &Res<AssetServer>,
) {
    let (graph, _) = AnimationGraph::from_clips((0..=17).map(|i| {
        asset_server
            .load(GltfAssetLabel::Animation(i).from_asset("models/beaver/beaver_animations.glb"))
    }));

    game.player.i = SIZE_I / 2;
    game.player.j = SIZE_J / 2;
    game.player.entity = Some(
        commands
            .spawn((
                DespawnOnExit(GameState::Playing),
                animation::AnimationToPlay {
                    graph_handle: graphs.add(graph),
                },
                CurrentAction {
                    action: BeaverAction::Idle,
                },
                animation::PlayerAnimator {
                    idle_timer: Timer::from_seconds(0.6, TimerMode::Once),
                    action_timer: None,
                },
                PlayerMovement {
                    target_translation: Vec3::new(
                        game.player.i as f32,
                        game.board[game.player.j][game.player.i].height,
                        game.player.j as f32,
                    ),
                    speed: crate::beaver::MOVE_SPEED,
                    rotation: dir_as_quat(BEAVER_DOWN),
                },
                Transform {
                    translation: Vec3::new(
                        game.player.j as f32,
                        game.board[game.player.j][game.player.i].height,
                        game.player.i as f32,
                    ),
                    rotation: dir_as_quat(BEAVER_DOWN),
                    ..default()
                },
                SceneRoot(asset_server.load(
                    GltfAssetLabel::Scene(0).from_asset("models/beaver/beaver_animations.glb"),
                )),
            ))
            .observe(animation::play_animation_when_ready)
            .id(),
    );
}
