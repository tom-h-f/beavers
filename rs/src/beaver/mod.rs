use crate::*;

pub mod actions;
pub mod animation;

pub const MOVE_SPEED: f32 = 2.0;

#[derive(Default, Debug, Component)]
pub struct Beaver {
    pub entity: Option<Entity>,
    pub i: usize,
    pub j: usize,
    pub move_cooldown: Timer,
}
