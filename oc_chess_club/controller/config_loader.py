import yaml

from pathlib import Path


class ConfigLoader:
    """Loader for YAML configuration file.

    Attributes:
        config (dict): Configuration settings loaded from file."""

    def __init__(self):
        """Constructor for ConfigLoader."""

        self.load_settings()

    def load_settings(self):
        package_dir = Path(__file__).parent.parent
        config_path = package_dir.joinpath("config.yaml").resolve()

        with open(config_path) as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

    def save_settings(self):
        package_dir = Path(__file__).parent.parent
        config_path = package_dir.joinpath("config.yaml").resolve()

        with open(config_path, "w") as config_file:
            yaml.dump(self.config, config_file)

    def database_path_exists(self):
        return Path(self.config["database_file"]).parent.is_dir()

    def database_exists(self):
        return Path(self.config["database_file"]).is_file()

    def database_is_json(self):
        return Path(self.config["database_file"]).suffix == ".json"

    def report_save_path_exists(self):
        return Path(self.config["report_save_path"]).is_dir()


_CONFIG = ConfigLoader()