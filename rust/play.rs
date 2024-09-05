use std::cmp::min;

use rand::Rng;

use crate::anime_collection::AnimeCollection;

#[derive(clap::Args, Debug)]
pub struct PlayArgs {
    // #[arg(short, long, default_value_t = false)]
    // pub full: bool,
    // #[arg(short, long, default_value_t = false)]
    // pub random: bool,
}

impl PlayArgs {
    pub fn run(&self) {
        let anime_collection = AnimeCollection::load();
        let mut rng = rand::thread_rng();
        let size = anime_collection.list.len();
        let mut index = size - 1;
        let max = min(size, 4);
        for _ in 0..max {
            if rng.gen_bool(0.5) {
                break;
            } else {
                index -= 1;
            }
        }
        if size - max - 1 == index {
            index = rng.gen_range(0..=index);
        }
        anime_collection.list[index].play()
    }
}
