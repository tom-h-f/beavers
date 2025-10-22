#![allow(dead_code)]

use bevy::{
    asset::{AssetServer, Handle},
    ecs::system::Res,
    scene::Scene,
};

use crate::board::assets::{TileAsset, get_asset};

#[derive(Debug, Default, Clone, Copy)]
pub struct Tile {
    pub typ: TileType,
}

impl Tile {
    pub fn new(typ: TileType) -> Self {
        Self { typ }
    }
}

#[derive(Debug, Default, Clone, Copy)]
pub enum TileType {
    #[default]
    Empty,
    GrassFlat,
    RiverStraight,
    RiverBank,
    RiverWater,
}
impl TileType {
    pub fn get_tile_asset(&self) -> TileAsset {
        match self {
            Self::GrassFlat => TileAsset::GroundGrass,
            Self::RiverStraight => TileAsset::GroundRiverStraight,
            Self::Empty => unreachable!("a tile type should have been set! It was empty"),
            _ => unreachable!("Match arm for this tile type not created yet"),
        }
    }
    pub fn get_model(&self, asset_server: &Res<AssetServer>) -> Handle<Scene> {
        get_asset(self.get_tile_asset(), asset_server)
    }
}
