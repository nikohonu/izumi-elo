use inquire::Confirm;
use serde::{Deserialize, Serialize};
use std::{
    fs::{self, read_dir},
    path::PathBuf,
};

#[derive(Debug, Deserialize, Serialize)]
pub struct Anime {
    pub name: String,
    #[serde(skip)]
    pub path: PathBuf,
    pub elo: i32,
}

impl Anime {
    pub fn from_path(path: PathBuf) -> Anime {
        Anime {
            name: path.file_name().unwrap().to_str().unwrap().to_string(),
            path,
            elo: 1000,
        }
    }
    pub fn play(&self) {
        let files = match read_dir(&self.path) {
            Ok(result) => result,
            Err(message) => {
                println!("{}", message);
                return;
            }
        };
        let mut ok_files: Vec<PathBuf> = vec![];
        for file in files {
            match file {
                Ok(file) => ok_files.push(file.path()),
                Err(message) => {
                    println!("{}", message);
                    return;
                }
            }
        }
        let files = ok_files;
        let mut ok_files: Vec<PathBuf> = vec![];
        for file in files {
            match file.extension() {
                Some(extension) => {
                    if extension == "mkv" {
                        ok_files.push(file)
                    }
                }
                None => {}
            }
        }
        ok_files.sort();
        let file = &ok_files[0];
        println!("{:?}", file);
        std::process::Command::new("mpv")
            .arg(file)
            .output()
            .expect("Can't run mpv");
        if Confirm::new("Move file to Audio?").prompt().unwrap() {
            let new_path = self
                .path
                .parent()
                .unwrap()
                .join("Audio")
                .join(file.file_name().unwrap());
            fs::rename(file, &new_path).unwrap();
            println!("from {:?} to {:?}", file, new_path);
        }
    }

    pub fn play_match(&mut self, other: &mut Anime, result: f64) {
        let k_factor = 32.0;
        println!(
            "Before {} ({}) - {} ({})",
            self.name, self.elo, other.name, other.elo
        );
        let p_self_elo = 1.0 / (1.0 + 10.0_f64.powf((other.elo - self.elo) as f64 / 400.0));
        let p_other_elo = 1.0 - p_self_elo;

        self.elo = (self.elo as f64 + k_factor * (result - p_self_elo)).round() as i32;
        other.elo = (other.elo as f64 + k_factor * ((1.0 - result) - p_other_elo)).round() as i32;
        println!(
            "After {} ({}) - {} ({})",
            self.name, self.elo, other.name, other.elo
        );
    }
}
