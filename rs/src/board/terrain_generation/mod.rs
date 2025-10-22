use std::collections::{HashMap, hash_map};
use std::rc::Rc;

use rand::distr::Distribution;
use rand::distr::weighted::WeightedIndex;
use rand::{Rng, SeedableRng};

use crate::board::terrain_generation::voronoi::{VoronoiPoint, VoronoiSite};

pub mod voronoi;

/// This is used purely for heightmaps
/// for usage in accurate river terrain generation
const MAX_HEIGHTMAP_LEVEL: usize = 8;

pub struct TerrainGenHeightMap {
    pub height_sites: Vec<HeightSite>,
    pub points: Vec<Vec<VoronoiPoint>>,
}

pub struct HeightSite {
    pub height: usize,
    pub site: Rc<VoronoiSite>,
}

pub fn generate_heightmap() -> TerrainGenHeightMap {
    let voronoi_map = voronoi::generate_regions(super::BOARD_WIDTH, super::BOARD_HEIGHT);
    println!("Region Map: {:#?}", voronoi_map);
    let mut rng = rand_chacha::ChaCha8Rng::from_os_rng();
    let weights = [
        (0, 10),
        (1, 9),
        (2, 8),
        (3, 6),
        (4, 4),
        (5, 2),
        (6, 1),
        (7, 1),
        (8, 1),
    ];

    // TODO: use result in this fn and remove this unwrap
    let height_dist = WeightedIndex::new(weights.iter().map(|(_, weight)| weight)).unwrap();

    let mut height_sites = Vec::new();
    let mut max_height = MAX_HEIGHTMAP_LEVEL;
    for site in voronoi_map.sites {
        let mut height = height_dist.sample(&mut rng);
        if height >= max_height {
            height -= 1;
            max_height = height;
        }
        height_sites.push(HeightSite { height, site });
    }
    TerrainGenHeightMap {
        height_sites,
        points: voronoi_map.points,
    }
}
