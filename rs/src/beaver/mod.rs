use crate::{
    beaver::movement::{BEAVER_DOWN, BEAVER_UP, dir_as_quat},
    board::{BOARD_HEIGHT, BOARD_WIDTH, Board},
    *,
};

pub mod actions;
pub mod animation;
pub mod movement;

pub const MOVE_SPEED: f32 = 2.0;

#[allow(dead_code)]
#[derive(Default, Debug, Component)]
pub struct Beaver {
    pub name: String,
    pub action: actions::BeaverAction,
}

pub fn beaver_plugin(app: &mut App) {
    app.add_systems(
        Startup,
        beaver::create_the_beavers.after(crate::board::render_world),
    );
    app.add_systems(FixedUpdate, movement::advance_physics);
    app.add_systems(
        // The `RunFixedMainLoop` schedule allows us to schedule systems to run before and after the fixed timestep loop.
        RunFixedMainLoop,
        (
            (
                // Accumulate our input before the fixed timestep loop to tell the physics simulation what it should do during the fixed timestep.
                movement::accumulate_input,
            )
                .chain()
                .in_set(RunFixedMainLoopSystems::BeforeFixedMainLoop),
            (
                // The player's visual representation needs to be updated after the physics simulation has been advanced.
                // This could be run in `Update`, but if we run it here instead, the systems in `Update`
                // will be working with the `Transform` that will actually be shown on screen.
                movement::interpolate_rendered_transform,
            )
                .chain()
                .in_set(RunFixedMainLoopSystems::AfterFixedMainLoop),
        ),
    );
}

pub fn create_the_beavers(
    mut commands: Commands,
    board: Res<Board>,
    mut graphs: ResMut<Assets<AnimationGraph>>,
    asset_server: Res<AssetServer>,
) {
    // TODO: Remove this code once we have a proper
    // animation system working.
    let (graph, _) = AnimationGraph::from_clips((0..=17).map(|i| {
        asset_server
            .load(GltfAssetLabel::Animation(i).from_asset("models/beaver/beaver_animations.glb"))
    }));

    // TODO make a smarter system to work out
    // where to spawn the beaver(s)

    let spawn_loc_i = BOARD_WIDTH / 2;
    let spawn_loc_j = BOARD_HEIGHT / 2;

    let beaver_id =
        commands
            .spawn((
                Beaver {
                    name: "Blossom".to_string(),
                    action: actions::BeaverAction::Idle,
                },
                DespawnOnExit(SimState::Playing),
                Transform {
                    // TODO make the y match the level its actually at
                    translation: Vec3::new(
                        spawn_loc_i as f32,
                        //board.board[0][spawn_loc_j][spawn_loc_j],
                        0.0,
                        spawn_loc_j as f32,
                    ),
                    rotation: dir_as_quat(BEAVER_UP),
                    ..default()
                },
                movement::AccumulatedInput::default(),
                movement::Velocity::default(),
                movement::PhysicalTranslation::default(),
                movement::PreviousPhysicalTranslation::default(),
                SceneRoot(asset_server.load(
                    GltfAssetLabel::Scene(0).from_asset("models/beaver/beaver_animations.glb"),
                )),
            ))
            .id();
}
