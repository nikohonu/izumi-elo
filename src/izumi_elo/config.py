from pathlib import Path
from typing import Type

import msgspec
from platformdirs import user_config_dir

config_path = Path(user_config_dir(appname="izumi-elo")) / "config.toml"


def enc_hook(obj: Path) -> str:
    if isinstance(obj, Path):
        return str(obj)
    else:
        raise NotImplementedError(f"Objects of type {type(obj)} are not supported")


def dec_hook(type: Type, obj: str) -> Path:
    if type is Path:
        return Path(obj)
    else:
        raise NotImplementedError(f"Objects of type {type} are not supported")


class Config(msgspec.Struct):
    library_path: Path
    access_token: str

    def get_audio_path(self):
        return self.library_path / "audio"

    @classmethod
    def load(cls):
        if config_path.is_file():
            with config_path.open("rb") as file:
                return msgspec.toml.decode(file.read(), type=cls, dec_hook=dec_hook)
        raise RuntimeError(
            'Unable to load the configuration file. Please run the "init" function first!'
        )

    def save(self):
        config_path.parent.mkdir(exist_ok=True)
        with config_path.open("wb") as file:
            file.write(msgspec.toml.encode(self, enc_hook=enc_hook))
