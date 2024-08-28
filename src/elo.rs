use std::cmp::min;

use crate::anime_collection::AnimeCollection;
use inquire::Select;
use rand::seq::SliceRandom;
use rand::thread_rng;

#[derive(clap::Args, Debug)]
pub struct EloArgs {
    // #[arg(short, long, default_value_t = false)]
    // pub full: bool,
    // #[arg(short, long, default_value_t = false)]
    // pub random: bool,
}

impl EloArgs {
    pub fn run(&self) {
        let mut anime_collection = AnimeCollection::load();
        let mut matches: Vec<(usize, usize)> = Vec::new();
        let size = anime_collection.list.len();
        for i in 0..size {
            for j in i + 1..size {
                matches.push((i, j));
            }
        }
        let max = min(size, 32);
        matches.shuffle(&mut thread_rng());
        let matches = &matches[0..max];
        for m in matches {
            let options = vec![
                &anime_collection.list[m.0].name,
                &anime_collection.list[m.1].name,
                "Tie",
                "Exit",
            ];
            match Select::new("Who win?", options).prompt_skippable() {
                Ok(Some(choice)) => {
                    if choice == "Exit" {
                        break;
                    }
                    let result = if choice == "Tie" {
                        0.5
                    } else if choice == anime_collection.list[m.0].name.clone() {
                        1.0
                    } else {
                        0.0
                    };
                    let (a, b) = anime_collection.list.split_at_mut(m.1);
                    a[m.0].play_match(&mut b[0], result);
                }
                Ok(None) => {}
                Err(_) => {}
            }
        }
        anime_collection.save();
    }
}
