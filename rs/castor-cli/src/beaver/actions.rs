use crate::*;

pub type BeaverDirection = f32;
pub const BEAVER_UP: BeaverDirection = PI / 2.;
pub const BEAVER_DOWN: BeaverDirection = -PI / 2.;
pub const BEAVER_LEFT: BeaverDirection = PI;
pub const BEAVER_RIGHT: BeaverDirection = 0.;

pub fn dir_as_quat(dir: BeaverDirection) -> Quat {
    Quat::from_rotation_y(dir)
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum BeaverAction {
    Idle,
    Walk,
    Jump,
    Eat,
}

impl BeaverAction {
    pub fn animation_index(&self) -> usize {
        match self {
            Self::Idle => 9,
            Self::Walk => 18,
            Self::Jump => 12,
            Self::Eat => 5,
        }
    }

    pub fn should_repeat(&self) -> bool {
        matches!(self, Self::Walk | Self::Idle)
    }

    pub fn duration(&self) -> Option<f32> {
        match self {
            Self::Jump => Some(1.0), // Adjust based on your animation length
            Self::Eat => Some(1.5),  // Adjust based on your animation length
            _ => None,
        }
    }
}

#[derive(Debug, Component, PartialEq, Clone, Copy)]
pub struct CurrentAction {
    pub action: BeaverAction,
}

#[derive(Debug, Component)]
pub struct PlayerMovement {
    pub rotation: Quat,
    pub target_translation: Vec3,
    pub speed: f32,
}
