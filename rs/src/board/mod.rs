use crate::*;

pub mod tile;

pub const SIZE_I: usize = 8;
pub const SIZE_J: usize = 8;

pub const RESET_FOCUS: [f32; 3] = [SIZE_I as f32 / 2.0, 0.0, SIZE_J as f32 / 2.0 - 0.5];

#[derive(Component)]
pub struct Position {
    pub x: usize,
    pub y: usize,
}

#[derive(Resource, Default)]
pub struct Board {
    pub board: Vec<Vec<Cell>>,
    pub score: i32,
}

pub fn generate_terrain(
    board: &mut ResMut<Board>,
    commands: &mut Commands,
    asset_server: &Res<AssetServer>,
) {
    // TODO: just load these into a loader or some storage of this
    let ground_grass = board::tile::Tile::GroundGrass.load(asset_server);
    let river_side = board::tile::Tile::GroundRiverSide.load(asset_server);
    let river_open = board::tile::Tile::GroundRiverOpen.load(asset_server);

    board.board = (0..board::SIZE_J)
        .map(|j| {
            (0..board::SIZE_I)
                .map(|i| {
                    let x = board::SIZE_I / 2;
                    if x == i {
                        commands.spawn((
                            DespawnOnExit(SimState::Playing),
                            Transform::from_xyz(i as f32, 0.0 as f32, j as f32),
                            SceneRoot(river_open.clone()),
                        ));
                    } else if x == i.wrapping_sub(1) {
                        commands.spawn((
                            DespawnOnExit(SimState::Playing),
                            Transform::from_translation(Vec3::new(i as f32, 0.0, j as f32))
                                .with_rotation(Quat::from_rotation_y(-std::f32::consts::FRAC_PI_2)),
                            SceneRoot(river_side.clone()),
                        ));
                    } else if x == i + 1 {
                        commands.spawn((
                            DespawnOnExit(SimState::Playing),
                            Transform::from_translation(Vec3::new(i as f32, 0.0, j as f32))
                                .with_rotation(Quat::from_rotation_y(std::f32::consts::FRAC_PI_2)),
                            SceneRoot(river_side.clone()),
                        ));
                    } else {
                        commands.spawn((
                            DespawnOnExit(SimState::Playing),
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
