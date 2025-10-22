use rand::{Rng, SeedableRng};
use std::rc::Rc;

#[allow(dead_code)]
#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct VoronoiRegionMap {
    pub points: Vec<Vec<VoronoiPoint>>,
    pub sites: Vec<Rc<VoronoiSite>>,
}

fn nearest_site(sites: &[Rc<VoronoiSite>], x: usize, y: usize) -> Rc<VoronoiSite> {
    let mut nearest_index = 0;
    let mut min_dist =
        ((sites[0].x as i32 - x as i32).pow(2) + (sites[0].y as i32 - y as i32).pow(2)) as f32;
    for i in 1..sites.len() {
        let dist =
            ((sites[i].x as i32 - x as i32).pow(2) + (sites[i].y as i32 - y as i32).pow(2)) as f32;
        if dist < min_dist {
            min_dist = dist;
            nearest_index = i;
        }
    }
    sites[nearest_index].clone()
}

#[allow(dead_code)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct VoronoiSite {
    pub x: usize,
    pub y: usize,
}

#[allow(dead_code)]
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct VoronoiPoint {
    pub x: usize,
    pub y: usize,
    pub nearest_site: Rc<VoronoiSite>,
}

pub fn generate_regions(width: usize, height: usize) -> VoronoiRegionMap {
    let mut rng = rand_chacha::ChaCha8Rng::seed_from_u64(
        std::time::SystemTime::now().elapsed().unwrap().as_nanos() as u64,
    );

    let number_of_sites = rng.random_range(0..(width * height) / 4);

    let mut sites = Vec::new();
    for _ in 0..number_of_sites {
        let x = rng.random_range(0..width);
        let y = rng.random_range(0..height);
        sites.push(Rc::new(VoronoiSite { x, y }));
    }

    let points: Vec<Vec<VoronoiPoint>> = (0..height)
        .map(|y| {
            (0..width)
                .map(|x| {
                    let nearest_site = nearest_site(&sites, x, y);
                    VoronoiPoint { x, y, nearest_site }
                })
                .collect()
        })
        .collect();

    VoronoiRegionMap { points, sites }
}
