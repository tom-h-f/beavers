use crate::*;

pub const MOVE_SPEED: f32 = 2.0;
pub const MOVE_DURATION: f32 = MOVE_SPEED * 0.3;
pub const MOVE_COOLDOWN: f32 = 0.01;

pub const SIZE_I: usize = 5;
pub const SIZE_J: usize = 5;

pub const RESET_FOCUS: [f32; 3] = [SIZE_I as f32 / 2.0, 0.0, SIZE_J as f32 / 2.0 - 0.5];

#[derive(Resource, Default)]
pub struct Game {
    pub board: Vec<Vec<Cell>>,
    pub player: Beaver,
    pub bonus: Bonus,
    pub score: i32,
    pub cake_eaten: u32,
    pub camera_should_focus: Vec3,
    pub camera_is_focus: Vec3,
}

pub fn spawn_beaver(
    game: &mut ResMut<Game>,
    commands: &mut Commands,
    mut graphs: &mut ResMut<Assets<AnimationGraph>>,
    asset_server: &Res<AssetServer>,
) {
    let (graph, _) = AnimationGraph::from_clips((0..=17).map(|i| {
        asset_server
            .load(GltfAssetLabel::Animation(i).from_asset("models/beaver/beaver_animations.glb"))
    }));

    game.player.move_cooldown = Timer::from_seconds(MOVE_DURATION, TimerMode::Once);
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
                    idle_timer: Timer::from_seconds(MOVE_DURATION, TimerMode::Once),
                    action_timer: None,
                },
                PlayerMovement {
                    target_translation: Vec3::new(
                        game.player.i as f32,
                        game.board[game.player.j][game.player.i].height,
                        game.player.j as f32,
                    ),
                    speed: MOVE_SPEED,
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
