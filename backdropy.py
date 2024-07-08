"""Backdrop is a supplement to wallpaper managers like swaybg, nitrogen, etc.
License: GPLv3
"""
from typing import Dict, Union, List
import logging
import argparse
import random
import json
import os

DEFAULT_CONFIG = {
    "wallpaper": {
        "dir": "/home/$USER/Pictures/Wallpapers",
        "current": "/home/$USER/Pictures/Wallpapers/current",
        "ext": ".jpg",
        "cmd": "swaybg -i",
        "auto_change": {
            "toggle": False,
            "interval": 300,
            "list": [],
            "random": True,
        },
        "fzf": {
            "toggle": False,
            "cmd": "fzf",
        },
        "wofi": {
            "toggle": False,
        },
        "rofi": {
            "toggle": False,
        },
        "dmenu": {
            "toggle": False,
        },
    },
    "notifications": {
        "toggle": True,
        "interval": 300,
        "cmd": "notify-send",
        "wallpaper_change": True,
        "wallpaper_error": True,
        "wallpaper_add": True,
        "wallpaper_remove": True,
    },
    "logging": {
        "enable": True,
        "file": "log/backdropy.log",
        "level": "INFO",
    }
}

class Log:
    logger = logging.getLogger(__name__)

    @staticmethod
    def configure_logging(enable: bool, file: str, level: str):
        if enable:
            logging.basicConfig(
                level=level,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(file),
                    logging.StreamHandler()
                ]
            )

    @staticmethod
    def info(msg: str) -> None:
        Log.logger.info(msg)

    @staticmethod
    def warning(msg: str) -> None:
        Log.logger.warning(msg)

    @staticmethod
    def error(msg: str, errc: str = None) -> None:
        if errc:
            Log.logger.error(f"{msg} - {errc}")
        else:
            Log.logger.error(msg)

    @staticmethod
    def success(msg: str) -> None:
        Log.logger.info(f"[SUCCESS] {msg}")

    @staticmethod
    def debug(msg: str) -> None:
        Log.logger.debug(msg)

class Config:
    """Holds attributes and methods for the config."""
    path: str = "bdy.json"
    debug: bool = True

    @staticmethod
    def set_default_config() -> int:
        """Writes the default config file."""
        try:
            JSONParser.write_file(Config.path, DEFAULT_CONFIG)
        except Exception as e:
            Log.error(f"Error writing to file: {Config.path}", str(e))
            return 1
        return 0

class JSONParser:
    """Functions related to parsing JSON files."""

    @staticmethod
    def read_file(file_path: str) -> Union[Dict, int]:
        """Read the file."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            Log.error(f"File not found: {file_path}")
            return 1
        except json.JSONDecodeError:
            Log.error(f"Error decoding JSON from file: {file_path}")
            return 1

    @staticmethod
    def write_file(file_path: str, data: Dict) -> int:
        """Write the file."""
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
            return 0
        except Exception as e:
            Log.error(f"Error writing to file: {file_path}", str(e))
            return 1

    @staticmethod
    def edit_key(data: Dict, key: str, new_value: Union[str, bool, int]) -> Dict:
        """Edit a key in a JSON file."""
        data[key] = new_value
        return data

    @staticmethod
    def get_key(file_path: str, key: str) -> Union[str, None]:
        """Get a key from a JSON file."""
        data = JSONParser.read_file(file_path)
        if isinstance(data, Dict):
            return data.get(key)
        return None

    @staticmethod
    def delete_key(file_path: str, key: str) -> Union[Dict, int]:
        """Delete a key from a JSON file."""
        data = JSONParser.read_file(file_path)
        if isinstance(data, Dict) and key in data:
            del data[key]
            return data
        Log.error(f"Key '{key}' not found in the file.")
        return 1

    @staticmethod
    def add_key(file_path: str, key: str, value: Union[str, bool, int]) -> Dict:
        """Add a key to a JSON file."""
        data = JSONParser.read_file(file_path)
        if isinstance(data, Dict):
            data[key] = value
            JSONParser.write_file(file_path, data)
            return data
        return {}

class Backdrop:
    """Holds methods for the backdrop script"""
    class Wallpaper:
        """Holds attributes for the wallpaper."""
        def __init__(self):
            self.name: str = ""
            self.tags: List[str] = []
            self.dir: str = ""
            self.ext: str = ""
            self.cmd: str = ""

        def set_wallpaper(self, wallpaper: str) -> int:
            """Set the wallpaper."""
            Backdrop.run_process(f"{self.cmd} {self.dir}/{wallpaper}")
            return 0

        def get_wallpaper_list(self) -> List[str]:
            """Get the wallpaper list."""
            return os.listdir(self.dir)

        class Dynamic:
            """Holds attributes and methods for the dynamic wallpaper change."""
            def __init__(self):
                self.toggle: bool = False
                self.interval: int = 0
                self.list: List[str] = []
                self.type: str = "random" # Or linear (TBI)

            def set_list(self, *args) -> List[str]:
                """Just appends the arguments to the list, very much WIP
                Plans:
                    Support sorting
                """
                if not args:
                    raise ValueError("No arguments provided")
                for arg in args:
                    self.list.append(arg)

            def get_random_wallpaper(self) -> str:
                """Get a random wallpaper."""
                if not self.list:
                    self.list = self.get_wallpaper_list()
                return random.choice(self.list)

    class Notifications:
        """Holds attributes and methods for the notifications."""
        def __init__(self):
            self.toggle: bool = False
            self.interval: int = 0
            self.cmd: str = ""

        def notify(self, message: str) -> int:
            """Send a notification."""
            Backdrop.run_process(f"{self.cmd} {message}")
            return 0

    class FuzzySearch:
        """Holds attributes and methods for the fuzzy search."""
        def __init__(self):
            self.toggle: bool = False
            self.cmd: str = ""

    @staticmethod
    def run_process(cmd: str) -> int:
        """Run a process."""
        try:
            os.system(cmd)
            return 0
        except Exception as e:
            Log.error(f"Error running process: {cmd}", str(e))
            return 1

    @staticmethod
    def set_arguments() -> argparse.Namespace:
        """Set the arguments."""
        parser = argparse.ArgumentParser(description="Backdrop is a supplement to wallpaper managers like swaybg, nitrogen, etc.")

        parser.add_argument(
            "-s",
            "--set",
            type=str,
            nargs='?', # Takes any ammount of args and outputs them as a single str
            help="Set the wallpaper"
        )

        parser.add_argument(
            "-r",
            "--random",
            action="store_true",
            help="Randomly select a wallpaper"
        )

        parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="List all wallpapers"
        )

        parser.add_argument(
            "--add", # Yes, it is verbose
            type=str,
            nargs="+",
            help="Add wallpaper(s) to the list"
        )

        parser.add_argument(
            "--remove",
            type=str,
            nargs="+",
            help="Remove wallpaper(s) from the list"
        )

        parser.add_argument(
            "-srl", # Note: I've no fuckin' clue how to accept it in any order
            # and I'm not about to hard code every single permutation.
            "--set-random-list",
            type=str,
            nargs="+",
            help="Set the wallpaper list"
        )

        return parser.parse_args()

def prompt(msg: str) -> str:
    """Prompt the user for input."""
    BLUE: str = "\033[94m"
    NC: str = "\033[0m"
    return input(f"{BLUE}{msg}{NC}")

def main() -> int:
    """Main function."""

    # Initialization
    # Checking if bdy.json exists
    if not os.path.exists(Config.path):
        tmp = prompt(f"Config file not found at {Config.path}, create it? (y/n): ")
        if tmp.lower() in ["y", "yes", "s", "sim", "si", "j", "ja"]:
            Log.info("Creating config file...")
            Backdrop.set_default_config()
            Log.success("Config file created successfully.")
        elif tmp.lower() in ["n", "no", "não", "nao", "nein"]:
            Log.error(f"Config file not found at {Config.path}, exiting...")
            return 1
        else:
            Log.error("Invalid input, exiting...")
            return 1
    # Checking if the file is empty
    elif os.stat(Config.path).st_size == 0:
        tmp = prompt("Config file is empty, create it? (y/n): ")
        if tmp.lower() in ["y", "yes", "s", "sim", "si", "j", "ja"]:
            Log.info("Creating config file...")
            Backdrop.set_default_config()
            Log.success("Config file created successfully.")
        elif tmp.lower() in ["n", "no", "não", "nao", "nein"]:
            Log.error("Config file not found, exiting...")
            return 1
    else:
        Log.debug("Config file found.")

    # Parsing config and setting up variables
    config = JSONParser.read_file(Config.path)

    # Setting up the logging attributes and initializing the logging
    Log.configure_logging(
        config["logging"]["enable"],
        config["logging"]["file"],
        config["logging"]["level"].upper()
    )

    # Initializing the arguments
    args = Backdrop.set_arguments()

    wallpaper = Backdrop.Wallpaper()
    wallpaper.dir = os.path.expanduser(config["wallpaper"]["dir"])
    wallpaper.ext = config["wallpaper"]["ext"]
    wallpaper.cmd = config["wallpaper"]["cmd"]

    aest = Backdrop.Aesthetic

    if args.set:
        wallpaper.set_wallpaper(args.set)
    elif args.random:
        wallpaper.set_wallpaper(wallpaper.get_random_wallpaper())
    elif args.set_random_list:
        wallpaper.Dynamic.set_list(args.set_random_list)
        wallpaper.set_wallpaper(wallpaper.Dynamic.get_random_wallpaper())
    elif args.list:
        color: int = 0
        list: List[str] = wallpaper.get_wallpaper_list()
        for wallpaper in list:
            match color:
                case 1:
                    print(f"{aest.colors['RED']}{wallpaper}{aest.NC}")
                case 2:
                    print(f"{aest.colors['GREEN']}{wallpaper}{aest.NC}")
                case 3:
                    print(f"{aest.colors['BLUE']}{wallpaper}{aest.NC}")
                case 4:
                    print(f"{aest.colors['MAGENTA']}{wallpaper}{aest.NC}")
                case 5:
                    aest.print_color(aest.colors["CYAN"], wallpaper)
                    color = 0 # Resets iterator
            color += 1
    elif args.add:
        # Add wallpapers to path
        # WIP
        ...
    elif args.remove:
        ...

if __name__ == "__main__":
    main()
