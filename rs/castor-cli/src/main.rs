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
            )
                .chain()
                .run_if(in_state(GameState::Playing)),
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
        Transform::from_xyz(-10.0, 10.0, 0.0).looking_at(game.camera_is_focus, Vec3::Y),
    ));
}

fn setup(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    graphs: ResMut<Assets<AnimationGraph>>,
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
            range: 300.0,
            ..default()
        },
        Transform::from_xyz(4.0, 10.0, 4.0),
    ));

    board::spawn_world(&mut game, &mut commands, &asset_server);
    board::spawn_beaver(&mut game, &mut commands, graphs, &asset_server);
}

fn move_player(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    mut game: ResMut<Game>,
    mut query: Query<(&Transform, &mut PlayerMovement)>,
    mut anim_state_query: Query<&mut animation::PlayerAnimator>,
    mut anim_events: MessageWriter<animation::TriggerAnimation>,
) {
    if let Ok((transform, movement)) = query.get(game.player.entity.unwrap()) {
        let distance = transform.translation.distance(movement.target_translation);
        if distance > 0.01 {
            return;
        }

        let mut moved = false;
        let mut rotation = 0.0;
        let mut action = BeaverAction::Idle;

        if keyboard_input.just_pressed(KeyCode::Space) {
            action = BeaverAction::Jump;
            anim_events.write(animation::TriggerAnimation {
                entity: game.player.entity.unwrap(),
                action,
                force_replay: true,
            });
            return;
        }

        if keyboard_input.pressed(KeyCode::ArrowUp) || keyboard_input.pressed(KeyCode::KeyW) {
            if game.player.i < board::SIZE_I - 1 {
                game.player.i += 1;
            }
            rotation = BEAVER_UP;
            action = BeaverAction::Walk;
            moved = true;
        } else if keyboard_input.pressed(KeyCode::ArrowDown)
            || keyboard_input.pressed(KeyCode::KeyS)
        {
            if game.player.i > 0 {
                game.player.i -= 1;
            }
            rotation = BEAVER_DOWN;
            action = BeaverAction::Walk;
            moved = true;
        } else if keyboard_input.pressed(KeyCode::ArrowRight)
            || keyboard_input.pressed(KeyCode::KeyD)
        {
            if game.player.j < board::SIZE_J - 1 {
                game.player.j += 1;
            }
            rotation = BEAVER_RIGHT;
            action = BeaverAction::Walk;
            moved = true;
        } else if keyboard_input.pressed(KeyCode::ArrowLeft)
            || keyboard_input.pressed(KeyCode::KeyA)
        {
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
