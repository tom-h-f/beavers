#[derive(Debug, Clone, Copy, PartialEq, Default)]
pub enum BeaverAction {
    #[default]
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
            Self::Jump => Some(0.4),
            Self::Eat => Some(0.1),
            _ => None,
        }
    }
}
