

mod anime;
mod anime_collection;
mod play;
mod elo;

use clap::{CommandFactory, Parser, Subcommand};

#[derive(Parser, Debug)]
#[command(author("Niko Honu"), version("0.1.0"), about("A cli app for manage anime collection."), long_about = None)]
struct Cli {
    // #[arg(short, long, default_value_t = false)]
    // full: bool,
    // #[arg(short, long, default_value_t = false)]
    // random: bool,
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand, Debug)]
enum Commands {
    Play(play::PlayArgs),
    Elo(elo::EloArgs),
    // Completion(completion::CompletionArgs),
    // List(list::ListArgs),
    // Now(now::NowArgs),
    // Do(r#do::DoArgs),
    // Remove(remove::RemoveArgs),
    // RegenerateIds(regenerate_ids::RegenerateIdsArgs),
}

fn main() {
    let cli = Cli::parse();
    let _command = Cli::command();
    match &cli.command {
        Some(Commands::Play(cmd)) => cmd.run(),
        Some(Commands::Elo(cmd)) => cmd.run(),
        // Some(Commands::Completion(cmd)) => cmd.run(&mut Cli::command()),
        // Some(Commands::List(cmd)) => cmd.run(),
        // Some(Commands::Now(cmd)) => cmd.run(),
        // Some(Commands::RegenerateIds(cmd)) => cmd.run(),
        // Some(Commands::Do(cmd)) => cmd.run(),
        // Some(Commands::Remove(cmd)) => cmd.run(),
        // _ => now::NowArgs {
        //     full: cli.full,
        //     random: cli.random,
        // }
        _ => {}
    }
}
