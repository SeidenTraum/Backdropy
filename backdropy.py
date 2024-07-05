"""Backdrop is a supplement to wallpaper managers like swaybg, nitrogen, etc.
License: GPLv3
"""
from typing import Dict, Union
import json
import os

class Status:
    # Color ANSI codes
    class Colors:
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        PURPLE = "\033[95m"
        RESET = "\033[0m"

    class Messages:
        @staticmethod
        def info(msg: str) -> int:
            """Print an info message."""
            print(f"{Status.Colors.BLUE}[INFO]{Status.Colors.RESET} {msg}")
            return 0

        @staticmethod
        def warning(msg: str) -> int:
            """Print a warning message."""
            print(f"{Status.Colors.YELLOW}[WARNING]{Status.Colors.RESET} {msg}")
            return 0

        @staticmethod
        def error(msg: str, errc: str = None) -> int:
            """Print an error message."""
            print(f"{Status.Colors.RED}[ERROR]{Status.Colors.RESET} {msg}")
            if errc:
                print(f"{Status.Colors.YELLOW}[ERRC]{Status.Colors.RESET} {errc}")
            return 0

        @staticmethod
        def success(msg: str) -> int:
            """Print a success message."""
            print(f"{Status.Colors.GREEN}[SUCCESS]{Status.Colors.RESET} {msg}")
            return 0

        @staticmethod
        def debug(msg: str, debug: bool) -> int:
            """Print a debug message."""
            if debug:
                print(f"{Status.Colors.PURPLE}[DEBUG]{Status.Colors.RESET} {msg}")
            return 0

    class Prompt:
        @staticmethod
        def input(msg: str) -> str:
            """Print a prompt and return the input."""
            return input(f"{Status.Colors.BLUE}[PROMPT]{Status.Colors.RESET} {msg}{Status.Colors.GREEN}")

class JSONParser:
    """Functions related to parsing JSON files."""

    @staticmethod
    def read_file(file_path: str) -> Union[Dict, int]:
        """Read the file."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            Status.Messages.error(f"File not found: {file_path}")
            return 1
        except json.JSONDecodeError:
            Status.Messages.error(f"Error decoding JSON from file: {file_path}")
            return 1

    @staticmethod
    def write_file(file_path: str, data: Dict) -> int:
        """Write the file."""
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
            return 0
        except Exception as e:
            Status.Messages.error(f"Error writing to file: {file_path}", str(e))
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
        Status.Messages.error(f"Key '{key}' not found in the file.")
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
    def __init__(self):
        self.config_path: str = "bdy.json"
        self.debug: bool = True

    class Wallpaper:
        """Holds attributes for the wallpaper."""
        def __init__(self):
            self.name: str = None
            self.tags: list[str] = None
            self.dir: str = None
            self.ext: str = None

    class Notifications:
        """Holds attributes and methods for the notifications."""
        def __init__(self):
            self.toggle: bool = None
            self.interval: int = None
            self.cmd: str = None

    class Logging:
        """Holds attributes and methods for the logging."""
        def __init__(self):
            self.enable: bool = None
            self.file: str = None
            self.level: str = None

    class FuzzySearch:
        """Holds attributes and methods for the fuzzy search."""
        def __init__(self):
            self.toggle: bool = None
            self.cmd: str = None

    def run_process(self, cmd: str) -> int:
        """Run a process."""
        try:
            os.system(cmd)
            return 0
        except Exception as e:
            Status.Messages.error(f"Error running process: {cmd}", str(e))
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
                "file": "/var/log/backdropy.log",  # The file to log to
                "level": "info",  # The level of logging
            }
        }

        # Writing the config in JSON format
        try:
            JSONParser.write_file(self.config_path, default)
        except Exception as e:
            Status.Messages.error(f"Error writing to file: {self.config_path}", str(e))
            return 1

        return 0

def main() -> int:
    """Main function."""
    backdrop = Backdrop()

    # Checking if bdy.json exists
    if not os.path.exists(backdrop.config_path):
        tmp = Status.Prompt.input(f"Config file not found at {backdrop.config_path}, create it? (y/n): ")
        if tmp.lower() in ["y", "yes", "s", "sim", "si", "j", "ja"]:
            Status.Messages.info("Creating config file...")
            backdrop.set_default_config()
            Status.Messages.success("Config file created successfully.")
        elif tmp.lower() in ["n", "no", "não", "nao", "nein"]:
            Status.Messages.error(f"Config file not found at {backdrop.config_path}, exiting...")
            return 1
        else:
            Status.Messages.error("Invalid input, exiting...")
            return 1
    # Checking if the file is empty
    elif os.stat(backdrop.config_path).st_size == 0:
        tmp = Status.Prompt.input("Config file is empty, create it? (y/n): ")
        if tmp.lower() in ["y", "yes", "s", "sim", "si", "j", "ja"]:
            Status.Messages.info("Creating config file...")
            backdrop.set_default_config()
            Status.Messages.success("Config file created successfully.")
        elif tmp.lower() in ["n", "no", "não", "nao", "nein"]:
            Status.Messages.error("Config file not found, exiting...")
            return 1
    else:
        Status.Messages.debug("Config file found.", backdrop.debug)
    return 0

if __name__ == "__main__":
    main()
