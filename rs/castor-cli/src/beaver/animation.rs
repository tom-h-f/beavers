use super::actions::{BeaverAction, CurrentAction};
use crate::*;

#[derive(Debug, Component)]
pub struct AnimationToPlay {
    pub graph_handle: Handle<AnimationGraph>,
}

#[derive(Message)]
pub struct TriggerAnimation {
    pub entity: Entity,
    pub action: BeaverAction,
    pub force_replay: bool,
}

#[derive(Debug, Component)]
pub struct PlayerAnimator {
    pub idle_timer: Timer,
    pub action_timer: Option<Timer>, // for one-shot animations
}

pub fn handle_animation_events(
    mut events: MessageReader<TriggerAnimation>,
    mut query: Query<(&mut CurrentAction, &mut PlayerAnimator)>,
) {
    for event in events.read() {
        if let Ok((mut action, mut animator)) = query.get_mut(event.entity) {
            if event.force_replay || action.action != event.action {
                action.action = event.action;

                if let Some(duration) = event.action.duration() {
                    animator.action_timer = Some(Timer::from_seconds(duration, TimerMode::Once));
                } else {
                    animator.action_timer = None;
                }
            }
        }
    }
}

pub fn check_idle_state(
    query: Query<(Entity, &CurrentAction, &PlayerAnimator)>,
    mut anim_events: MessageWriter<TriggerAnimation>,
) {
    for (entity, current_action, anim_state) in query.iter() {
        match current_action.action {
            BeaverAction::Walk => {
                if anim_state.idle_timer.is_finished() {
                    anim_events.write(TriggerAnimation {
                        entity,
                        action: BeaverAction::Idle,
                        force_replay: false,
                    });
                }
            }
            BeaverAction::Jump | BeaverAction::Eat => {
                if let Some(ref timer) = anim_state.action_timer {
                    if timer.is_finished() {
                        anim_events.write(TriggerAnimation {
                            entity,
                            action: BeaverAction::Idle,
                            force_replay: false,
                        });
                    }
                }
            }
            BeaverAction::Idle => {}
        }
    }
}

pub fn smooth_player_movement(
    time: Res<Time>,
    mut query: Query<(&mut Transform, &PlayerMovement)>,
) {
    for (mut transform, movement) in query.iter_mut() {
        transform.rotation = movement.rotation;

        let direction = movement.target_translation - transform.translation;
        let distance = direction.length();

        if distance > 0.01 {
            let move_distance = movement.speed * time.delta_secs();
            if move_distance >= distance {
                transform.translation = movement.target_translation;
            } else {
                transform.translation += direction.normalize() * move_distance;
            }
        }
    }
}

pub fn control_player_animation(
    query: Query<(Entity, &CurrentAction), Changed<CurrentAction>>,
    children: Query<&Children>,
    mut players: Query<&mut AnimationPlayer>,
) {
    for (entity, current_action) in query.iter() {
        for child in children.iter_descendants(entity) {
            if let Ok(mut player) = players.get_mut(child) {
                let target_index = AnimationNodeIndex::new(current_action.action.animation_index());

                player.stop_all();
                let anim = player.play(target_index);

                if current_action.action.should_repeat() {
                    anim.repeat();
                }
            }
        }
    }
}

pub fn tick_timers(time: Res<Time>, mut query: Query<&mut beaver::animation::PlayerAnimator>) {
    for mut animator in query.iter_mut() {
        animator.idle_timer.tick(time.delta());
        if let Some(ref mut timer) = animator.action_timer {
            timer.tick(time.delta());
        }
    }
}

pub fn play_animation_when_ready(
    scene_ready: On<SceneInstanceReady>,
    mut commands: Commands,
    children: Query<&Children>,
    animations_to_play: Query<&AnimationToPlay>,
    players: Query<&AnimationPlayer>,
    mut anim_events: MessageWriter<TriggerAnimation>,
) {
    if let Ok(animation_to_play) = animations_to_play.get(scene_ready.entity) {
        for child in children.iter_descendants(scene_ready.entity) {
            if let Ok(_player) = players.get(child) {
                commands
                    .entity(child)
                    .insert(AnimationGraphHandle(animation_to_play.graph_handle.clone()));

                anim_events.write(TriggerAnimation {
                    entity: scene_ready.entity,
                    action: BeaverAction::Idle,
                    force_replay: true,
                });
            }
        }
    }
}
