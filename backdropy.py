"""Backdrop is a supplement to wallpaper managers like swaybg, nitrogen, etc.
License: GPLv3
"""
from typing import Dict, Union
import logging
import argparse
import json
import os

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
    def info(msg: str) -> int:
        Log.logger.info(msg)
        return 0

    @staticmethod
    def warning(msg: str) -> int:
        Log.logger.warning(msg)
        return 0

    @staticmethod
    def error(msg: str, errc: str = None) -> int:
        if errc:
            Log.logger.error(f"{msg} - {errc}")
        else:
            Log.logger.error(msg)
        return 0

    @staticmethod
    def success(msg: str) -> int:
        Log.logger.info(f"[SUCCESS] {msg}")
        return 0

    @staticmethod
    def debug(msg: str) -> int:
        Log.logger.debug(msg)
        return 0

class Config:
    """Holds attributes and methods for the config."""
    path: str = "bdy.json"
    debug: bool = True

    @staticmethod
    def set_default_config() -> int:
        """Writes the default config file."""
        default: Dict = {
            "wallpaper": {
                "dir": "/home/$USER/Pictures/Wallpapers",  # Directory to search for wallpapers
                "current": "/home/$USER/Pictures/Wallpapers/current",  # Current wallpaper
                "ext": ".jpg",  # File extension of wallpapers
                "cmd": "swaybg -i",  # Command to set the wallpaper
                "auto_change": {
                    "toggle": False,  # Changes whether or not the wallpaper is changed automatically
                    "interval": 300,  # The interval of changing the wallpaper
                    "list": [],  # A list of wallpapers to change to
                    "random": True,  # Changes whether or not the wallpaper is chosen randomly
                },
                "fzf": {
                    "toggle": False,  # Changes whether or not fzf is used to select the wallpaper
                    "cmd": "fzf",  # The command to use to select the wallpaper
                },
                "wofi": {
                    "toggle": False,  # Changes whether or not wofi is used to select the wallpaper
                },
                "rofi": {
                    "toggle": False,  # Changes whether or not rofi is used to select the wallpaper
                },
                "dmenu": {
                    "toggle": False,  # Changes whether or not dmenu is used to select the wallpaper
                },
            },
            "notifications": {
                "toggle": True,  # Changes whether notifications are shown at all
                "interval": 300,  # The interval of showing the notification
                "cmd": "notify-send",  # The command to show the notification
                "wallpaper_change": True,  # Notify when the wallpaper is changed
                "wallpaper_error": True,  # Notify when the wallpaper is not found
                "wallpaper_add": True,  # Notify when a wallpaper is added
                "wallpaper_remove": True,  # Notify when a wallpaper is removed
            },
            "logging": {
                "enable": True,  # Changes whether logging is enabled
                "file": "log/backdropy.log",  # The file to log to
                "level": "INFO",  # The level of logging
            }
        }

        # Writing the config in JSON format
        try:
            JSONParser.write_file(Config.path, default)
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
    def edit_key(data: Dict, key: str, new_value: str) -> Dict:
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
    def add_key(file_path: str, key: str, value: str) -> Dict:
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
            self.name: str = None
            self.tags: list[str] = None
            self.dir: str = None
            self.ext: str = None

            self.cmd: str = None

        def set_wallpaper(self) -> int:
            """Set the wallpaper."""
            # Very simple implementation
            Backdrop.run_process(f"{self.cmd} {self.dir}")
            return 0

    class Notifications:
        """Holds attributes and methods for the notifications."""
        def __init__(self):
            self.toggle: bool = None
            self.interval: int = None
            self.cmd: str = None

        def notify(self, message: str) -> int:
            """Send a notification."""
            Backdrop.run_process(f"{self.cmd} {message}")
            return 0

    class FuzzySearch:
        """Holds attributes and methods for the fuzzy search."""
        def __init__(self):
            self.toggle: bool = None
            self.cmd: str = None

    @staticmethod
    def run_process(cmd: str) -> int:
        """Run a process."""
        try:
            os.system(cmd)
            return 0
        except Exception as e:
            Log.error(f"Error running process: {cmd}", str(e))
            return 1

    def set_default_config(self) -> int:
        """Writes the default config file."""
        default: Dict = {
            "wallpaper": {
                "dir": "/home/$USER/Pictures/Wallpapers",  # Directory to search for wallpapers
                "current": "/home/$USER/Pictures/Wallpapers/current",  # Current wallpaper
                "ext": ".jpg",  # File extension of wallpapers
                "cmd": "swaybg -i",  # Command to set the wallpaper
                "auto_change": {
                    "toggle": False,  # Changes whether or not the wallpaper is changed automatically
                    "interval": 300,  # The interval of changing the wallpaper
                    "list": [],  # A list of wallpapers to change to
                    "random": True,  # Changes whether or not the wallpaper is chosen randomly
                },
                "fzf": {
                    "toggle": False,  # Changes whether or not fzf is used to select the wallpaper
                    "cmd": "fzf",  # The command to use to select the wallpaper
                },
                "wofi": {
                    "toggle": False,  # Changes whether or not wofi is used to select the wallpaper
                },
                "rofi": {
                    "toggle": False,  # Changes whether or not rofi is used to select the wallpaper
                },
                "dmenu": {
                    "toggle": False,  # Changes whether or not dmenu is used to select the wallpaper
                },
            },
            "notifications": {
                "toggle": True,  # Changes whether notifications are shown at all
                "interval": 300,  # The interval of showing the notification
                "cmd": "notify-send",  # The command to show the notification
                "wallpaper_change": True,  # Notify when the wallpaper is changed
                "wallpaper_error": True,  # Notify when the wallpaper is not found
                "wallpaper_add": True,  # Notify when a wallpaper is added
                "wallpaper_remove": True,  # Notify when a wallpaper is removed
            },
            "logging": {
                "enable": True,  # Changes whether logging is enabled
                "file": "log/backdropy.log",  # The file to log to
                "level": "INFO",  # The level of logging
            }
        }

        # Writing the config in JSON format
        try:
            JSONParser.write_file(self.config_path, default)
        except Exception as e:
            Log.error(f"Error writing to file: {self.config_path}", str(e))
            return 1

        return 0

    def set_arguments(self) -> argparse.Namespace:
        """Set the arguments."""
        parser = argparse.ArgumentParser(description="Backdrop is a supplement to wallpaper managers like swaybg, nitrogen, etc.")

        parser.add_argument(
            "-s",
            "--set",
            type=str,
            nargs=1,
            action="store",
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
            "-a",
            "--add",
            type=str,
            nargs="+", # Allows for multiple wallpapers to be added
            action="store",
            help="Add wallpaper(s) to the list"
        )

        parser.add_argument(
            "-r",
            "--remove",
            type=str,
            nargs="+", # Allows for multiple wallpapers to be removed
            action="store",
            help="Remove wallpaper(s) from the list"
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

    # Setting up the wallpaper attributes
    wallpaper = Backdrop.Wallpaper()
    wallpaper.dir = config["wallpaper"]["dir"]
    wallpaper.cmd = config["wallpaper"]["cmd"]

    # Setting up the notifications attributes
    notifications = Backdrop.Notifications()
    notifications.toggle = config["notifications"]["toggle"]
    notifications.interval = config["notifications"]["interval"]
    notifications.cmd = config["notifications"]["cmd"]

    # Setting up the logging attributes and initializing the logging
    logging = Backdrop.Logging()
    logging.enable = config["logging"]["enable"]
    logging.file = config["logging"]["file"]
    logging.level = config["logging"]["level"].upper() # Converting the level to uppercase
    # 'cause logging requires it
    logging.init_logging()

    # Testing
    logging.write("Testing logging", "DEBUG")
    logging.write("Testing logging", "INFO")
    logging.write("Testing logging", "WARNING")
    logging.write("Testing logging", "ERROR")

    # Setting up the fuzzy search attributes
    fuzzy_search = Backdrop.FuzzySearch()
    fuzzy_search.toggle = config["wallpaper"]["fzf"]["toggle"]
    fuzzy_search.cmd = config["wallpaper"]["fzf"]["cmd"]

    # Initializing the arguments
    # args = Backdrop.set_arguments()

    # Initial setup done

    # Checking if the set argument is present
    #if args.set:
    #    Status.Messages.Log.debug(f"Setting wallpaper to: {args.set}")
    #    logging.write(f"Wallpaper set to: {args.set}", "DEBUG")

if __name__ == "__main__":
    main()

