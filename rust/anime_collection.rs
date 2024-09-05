use serde::{Deserialize, Serialize};
use std::{
    fs::{self, File},
    path::PathBuf,
};

use crate::anime::{Anime};

#[derive(Debug, Deserialize, Serialize)]
pub struct AnimeCollection {
    #[serde(skip)]
    config: PathBuf,
    pub list: Vec<Anime>,
}

impl AnimeCollection {
    fn load_elo(&mut self) {
        let file = match File::open(&self.config) {
            Ok(file) => file,
            Err(_) => return,
        };
        let data = ron::de::from_reader::<File, AnimeCollection>(file).unwrap();
        for anime in &mut self.list {
            for anime_elo in &data.list {
                if anime.name == anime_elo.name {
                    anime.elo = anime_elo.elo
                }
            }
        }
    }

    pub fn load() -> AnimeCollection {
        let path = dirs::video_dir().unwrap().join("anime");
        let config = path.join("collection.ron").clone();
        let anime_list = fs::read_dir(&path)
            .unwrap()
            .map(|x| x.unwrap())
            .filter(|x| x.path().is_dir())
            .map(|x| Anime::from_path(x.path()))
            .filter(|x| x.name != "Audio");
        let list: Vec<Anime> = Vec::from_iter(anime_list);
        let mut anime_collection = AnimeCollection { config, list };
        anime_collection.load_elo();
        anime_collection.list.sort_by(|a, b| a.elo.cmp(&b.elo));
        anime_collection
    }

    pub fn save(&mut self) {
        let file = File::create(&self.config).unwrap();
        self.list.sort_by(|a, b| a.elo.cmp(&b.elo));
        let _ = ron::ser::to_writer_pretty(file, self, ron::ser::PrettyConfig::default());
    }
}
