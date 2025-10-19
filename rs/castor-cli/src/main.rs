use std::f32::consts::PI;

use beaver::Beaver;
pub use bevy::prelude::*;
use bevy::scene::SceneInstanceReady;
use rand::{Rng, SeedableRng};
use rand_chacha::ChaCha8Rng;

mod beaver;
mod board;
use beaver::actions::*;
use beaver::animation;
use board::Game;

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug, Default, States)]
enum GameState {
    #[default]
    Playing,
    GameOver,
}

#[derive(Resource)]
struct BonusSpawnTimer(Timer);

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .init_resource::<board::Game>()
        .insert_resource(BonusSpawnTimer(Timer::from_seconds(
            5.0,
            TimerMode::Repeating,
        )))
        .add_message::<beaver::animation::TriggerAnimation>()
        .init_state::<GameState>()
        .add_systems(Startup, setup_cameras)
        .add_systems(OnEnter(GameState::Playing), setup)
        .add_systems(
            Update,
            (
                move_player,
                animation::handle_animation_events,
                animation::tick_timers,
                animation::check_idle_state,
                animation::control_player_animation,
                animation::smooth_player_movement,
                focus_camera,
                rotate_bonus,
                scoreboard_system,
                spawn_bonus,
            )
                .chain()
                .run_if(in_state(GameState::Playing)),
        )
        .add_systems(OnEnter(GameState::GameOver), display_score)
        .add_systems(
            Update,
            game_over_keyboard.run_if(in_state(GameState::GameOver)),
        )
        .run();
}

struct Cell {
    height: f32,
}

#[derive(Default)]
struct Bonus {
    entity: Option<Entity>,
    i: usize,
    j: usize,
    handle: Handle<Scene>,
}

#[derive(Resource, Deref, DerefMut)]
struct Random(ChaCha8Rng);

fn setup_cameras(mut commands: Commands, mut game: ResMut<Game>) {
    game.camera_should_focus = Vec3::from(board::RESET_FOCUS);
    game.camera_is_focus = game.camera_should_focus;
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(
            -(board::SIZE_I as f32 / 2.0),
            2.0 * board::SIZE_J as f32 / 3.0,
            board::SIZE_J as f32 / 2.0 - 0.5,
        )
        .looking_at(game.camera_is_focus, Vec3::Y),
    ));
}

fn setup(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut graphs: ResMut<Assets<AnimationGraph>>,
    mut game: ResMut<Game>,
) {
    let rng = ChaCha8Rng::from_os_rng();

    // reset the game state
    game.cake_eaten = 0;
    game.score = 0;

    commands.spawn((
        DespawnOnExit(GameState::Playing),
        PointLight {
            intensity: 2_000_000.0,
            shadows_enabled: true,
            range: 30.0,
            ..default()
        },
        Transform::from_xyz(4.0, 10.0, 4.0),
    ));

    // spawn the flat board
    let cell_scene =
        asset_server.load(GltfAssetLabel::Scene(0).from_asset("models/ground_grass.glb"));

    let big_block =
        asset_server.load(GltfAssetLabel::Scene(0).from_asset("models/ground_riverStraight.glb"));
    game.board = (0..board::SIZE_J)
        .map(|j| {
            (0..board::SIZE_I)
                .map(|i| {
                    if j % 16 == 0 {
                        commands.spawn((
                            DespawnOnExit(GameState::Playing),
                            Transform::from_xyz(i as f32, 0.0, j as f32),
                            SceneRoot(big_block.clone()),
                        ));
                    } else {
                        commands.spawn((
                            DespawnOnExit(GameState::Playing),
                            Transform::from_xyz(i as f32, 0.0, j as f32),
                            SceneRoot(cell_scene.clone()),
                        ));
                    }
                    Cell { height: 0.0 }
                })
                .collect()
        })
        .collect();

    board::spawn_beaver(&mut game, &mut commands, &mut graphs, &asset_server);
    game.bonus.handle =
        asset_server.load(GltfAssetLabel::Scene(0).from_asset("models/tree_oak.glb"));

    commands.spawn((
        DespawnOnExit(GameState::Playing),
        Text::new("Score:"),
        TextFont {
            font_size: 33.0,
            ..default()
        },
        TextColor(Color::srgb(0.5, 0.5, 1.0)),
        Node {
            position_type: PositionType::Absolute,
            top: px(5),
            left: px(5),
            ..default()
        },
    ));

    commands.insert_resource(Random(rng));
}

fn move_player(
    mut commands: Commands,
    keyboard_input: Res<ButtonInput<KeyCode>>,
    mut game: ResMut<Game>,
    mut query: Query<(&Transform, &mut PlayerMovement)>,
    mut anim_state_query: Query<&mut animation::PlayerAnimator>,
    mut anim_events: MessageWriter<animation::TriggerAnimation>,
    time: Res<Time>,
) {
    if game.player.move_cooldown.tick(time.delta()).is_finished() {
        if let Ok((transform, movement)) = query.get(game.player.entity.unwrap()) {
            let distance = transform.translation.distance(movement.target_translation);
            if distance > 0.01 {
                return;
            }
        }

        let mut moved = false;
        let mut rotation = 0.0;
        let mut action = BeaverAction::Idle;

        // Jump with spacebar
        if keyboard_input.just_pressed(KeyCode::Space) {
            action = BeaverAction::Jump;
            anim_events.write(animation::TriggerAnimation {
                entity: game.player.entity.unwrap(),
                action,
                force_replay: true,
            });
            return;
        }

        if keyboard_input.pressed(KeyCode::ArrowUp) {
            if game.player.i < board::SIZE_I - 1 {
                game.player.i += 1;
            }
            rotation = BEAVER_UP;
            action = BeaverAction::Walk;
            moved = true;
        } else if keyboard_input.pressed(KeyCode::ArrowDown) {
            if game.player.i > 0 {
                game.player.i -= 1;
            }
            rotation = BEAVER_DOWN;
            action = BeaverAction::Walk;
            moved = true;
        } else if keyboard_input.pressed(KeyCode::ArrowRight) {
            if game.player.j < board::SIZE_J - 1 {
                game.player.j += 1;
            }
            rotation = BEAVER_RIGHT;
            action = BeaverAction::Walk;
            moved = true;
        } else if keyboard_input.pressed(KeyCode::ArrowLeft) {
            if game.player.j > 0 {
                game.player.j -= 1;
            }
            rotation = BEAVER_LEFT;
            action = BeaverAction::Walk;
            moved = true;
        }

        if moved {
            game.player.move_cooldown.reset();

            if let Ok((_, mut movement)) = query.get_mut(game.player.entity.unwrap()) {
                movement.target_translation = Vec3::new(
                    game.player.i as f32,
                    game.board[game.player.j][game.player.i].height,
                    game.player.j as f32,
                );
                movement.rotation = Quat::from_rotation_y(rotation);
            }

            if let Ok(mut anim_state) = anim_state_query.get_mut(game.player.entity.unwrap()) {
                anim_state.idle_timer.reset();
            }

            anim_events.write(animation::TriggerAnimation {
                entity: game.player.entity.unwrap(),
                action,
                force_replay: false,
            });
        }
    }

    // eat the cake!
    if let Some(entity) = game.bonus.entity
        && game.player.i == game.bonus.i
        && game.player.j == game.bonus.j
    {
        game.score += 2;
        game.cake_eaten += 1;
        commands.entity(entity).despawn();
        game.bonus.entity = None;

        // Trigger eat animation
        anim_events.write(animation::TriggerAnimation {
            entity: game.player.entity.unwrap(),
            action: BeaverAction::Eat,
            force_replay: true,
        });
    }
}

fn focus_camera(
    time: Res<Time>,
    mut game: ResMut<Game>,
    mut transforms: ParamSet<(Query<&mut Transform, With<Camera3d>>, Query<&Transform>)>,
) {
    const SPEED: f32 = 2.0;
    if let (Some(player_entity), Some(bonus_entity)) = (game.player.entity, game.bonus.entity) {
        let transform_query = transforms.p1();
        if let (Ok(player_transform), Ok(bonus_transform)) = (
            transform_query.get(player_entity),
            transform_query.get(bonus_entity),
        ) {
            game.camera_should_focus = player_transform
                .translation
                .lerp(bonus_transform.translation, 0.5);
        }
    } else if let Some(player_entity) = game.player.entity {
        if let Ok(player_transform) = transforms.p1().get(player_entity) {
            game.camera_should_focus = player_transform.translation;
        }
    } else {
        game.camera_should_focus = Vec3::from(board::RESET_FOCUS);
    }

    let mut camera_motion = game.camera_should_focus - game.camera_is_focus;
    if camera_motion.length() > 0.2 {
        camera_motion *= SPEED * time.delta_secs();
        game.camera_is_focus += camera_motion;
    }

    for mut transform in transforms.p0().iter_mut() {
        *transform = transform.looking_at(game.camera_is_focus, Vec3::Y);
    }
}

fn spawn_bonus(
    time: Res<Time>,
    mut timer: ResMut<BonusSpawnTimer>,
    mut next_state: ResMut<NextState<GameState>>,
    mut commands: Commands,
    mut game: ResMut<Game>,
    mut rng: ResMut<Random>,
) {
    if !timer.0.tick(time.delta()).is_finished() {
        return;
    }

    if let Some(entity) = game.bonus.entity {
        game.score -= 3;
        commands.entity(entity).despawn();
        game.bonus.entity = None;
        if game.score <= -5 {
            next_state.set(GameState::GameOver);
            return;
        }
    }

    loop {
        game.bonus.i = rng.random_range(0..board::SIZE_I);
        game.bonus.j = rng.random_range(0..board::SIZE_J);
        if game.bonus.i != game.player.i || game.bonus.j != game.player.j {
            break;
        }
    }

    game.bonus.entity = Some(
        commands
            .spawn((
                DespawnOnExit(GameState::Playing),
                Transform::from_xyz(
                    game.bonus.i as f32,
                    game.board[game.bonus.j][game.bonus.i].height + 0.2,
                    game.bonus.j as f32,
                ),
                SceneRoot(game.bonus.handle.clone()),
                children![(
                    PointLight {
                        color: Color::srgb(1.0, 1.0, 0.0),
                        intensity: 500_000.0,
                        range: 10.0,
                        ..default()
                    },
                    Transform::from_xyz(0.0, 2.0, 0.0),
                )],
            ))
            .id(),
    );
}

fn rotate_bonus(game: Res<Game>, time: Res<Time>, mut transforms: Query<&mut Transform>) {
    if let Some(entity) = game.bonus.entity
        && let Ok(mut cake_transform) = transforms.get_mut(entity)
    {
        cake_transform.rotate_y(time.delta_secs());
        cake_transform.scale =
            Vec3::splat(1.0 + (game.score as f32 / 10.0 * ops::sin(time.elapsed_secs())).abs());
    }
}

fn scoreboard_system(game: Res<Game>, mut display: Single<&mut Text>) {
    display.0 = format!("Sugar Rush: {}", game.score);
}

fn game_over_keyboard(
    mut next_state: ResMut<NextState<GameState>>,
    keyboard_input: Res<ButtonInput<KeyCode>>,
) {
    if keyboard_input.just_pressed(KeyCode::Space) {
        next_state.set(GameState::Playing);
    }
}

fn display_score(mut commands: Commands, game: Res<Game>) {
    commands.spawn((
        DespawnOnExit(GameState::GameOver),
        Node {
            width: percent(100),
            align_items: AlignItems::Center,
            justify_content: JustifyContent::Center,
            ..default()
        },
        children![(
            Text::new(format!("Cake eaten: {}", game.cake_eaten)),
            TextFont {
                font_size: 67.0,
                ..default()
            },
            TextColor(Color::srgb(0.5, 0.5, 1.0)),
        )],
    ));
}
