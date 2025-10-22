use crate::*;

pub mod assets;
pub mod decor;
pub mod terrain_generation;
pub mod tiles;
use tiles::{Tile, TileType};

pub const BOARD_WIDTH: usize = 16;
pub const BOARD_HEIGHT: usize = 16;

pub const RESET_FOCUS: [f32; 3] = [
    BOARD_WIDTH as f32 / 2.0,
    0.0,
    BOARD_HEIGHT as f32 / 2.0 - 0.5,
];

pub fn board_plugin(app: &mut App) {
    let mut b = Board::default();
    b.generate_world();
    app.insert_resource(b);
    app.add_systems(Startup, render_world);
}

#[derive(Resource, Default, Debug)]
pub struct Board {
    pub board: Vec<Vec<Cell>>,
}

#[derive(Debug, Default, Clone)]
struct Cell {
    /// The type of tile it is and any contextual information
    /// in relation to that.
    tile: Tile,
    /// Any models, trees, other animals (maybe?) that
    /// are on top of this cell.
    decor: Vec<decor::Decor>,
}

impl Board {
    pub fn new() -> Self {
        Self {
            board: (0..BOARD_HEIGHT).map(|_| Vec::new()).collect(),
        }
    }
    pub fn generate_world(&mut self) {
        let heightmap = terrain_generation::generate_heightmap();
        let mut new_board = vec![vec![Cell::default(); BOARD_WIDTH]; BOARD_HEIGHT];
        for layer in heightmap.points {
            for element in layer {
                // TODO: use the heightmap to determine where rivers
                // tiles should be, ideally via the height, and the proximity to the site.
                // So at 'higher' levels, there will be more river tiles/points as the
                // river is wider and narrows as it travels downwards.
                let is_river = false;
                let tile = if is_river {
                    // would have to be more complex so being a bank
                    // when on edge of the layer's river width etc.
                    Tile::new(TileType::RiverStraight)
                } else {
                    Tile::new(TileType::GrassFlat)
                };
                let tile = match heightmap
                    .height_sites
                    .iter()
                    .find(|x| x.site == element.nearest_site)
                    .unwrap()
                    .height
                {
                    4.. => Tile::new(TileType::RiverStraight),
                    _ => Tile::new(TileType::GrassFlat),
                };
                new_board[element.y][element.x] = Cell {
                    tile,
                    decor: Vec::new(),
                }
            }
        }
        println!("{:#?}", new_board);
        self.board = new_board;
    }
}

pub fn render_world(board: ResMut<Board>, mut commands: Commands, asset_server: Res<AssetServer>) {
    for layer_i in 0..board.board.len() {
        for cell_i in 0..board.board[layer_i].len() {
            let cell = &board.board[layer_i][cell_i];
            commands.spawn((
                DespawnOnExit(SimState::Playing),
                Transform::from_xyz(cell_i as f32, 0.0 as f32, layer_i as f32),
                SceneRoot(cell.tile.typ.get_model(&asset_server).clone()),
            ));
        }
    }
}
