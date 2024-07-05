"""Backdrop is a supplement to wallpaper managers like swaybg, nitrogen and jadda jadda.
License: GPLv3
"""
from typing import Dict, Union
import json

global config_path
global debug
config_path:str = "bdy.config"
debug:bool = True

class status:
    # Methods related to status messages
    class colors:
        # Color ANSI codes
        red:str     = "\033[91m"
        green:str   = "\033[92m"
        yellow:str  = "\033[93m"
        blue:str    = "\033[94m"
        purple:str  = "\033[95m"
        reset:str   = "\033[0m"

    class messages:
        @staticmethod
        def info(msg:str) -> int:
            """Print an info message."""
            print(f"{status.colors.blue}[INFO]{status.colors.reset} {msg}")
            return 0

        @staticmethod
        def warning(msg:str) -> int:
            """Print a warning message."""
            print(f"{status.colors.yellow}[WARNING]{status.colors.reset} {msg}")
            return 0

        @staticmethod
        def error(msg:str, errc:str=None) -> int:
            """Print an error message."""
            print(f"{status.colors.red}[ERROR]{status.colors.reset} {msg}")
            if errc:
                print(f"{status.colors.yellow}[ERRC]{status.colors.reset} {errc}")
            return 0

        @staticmethod
        def success(msg:str) -> int:
            """Print a success message."""
            print(f"{status.colors.green}[SUCCESS]{status.colors.reset} {msg}")
            return 0

        @staticmethod
        def debug(msg:str) -> int:
            """Print a debug message."""
            if debug:
                print(f"{status.colors.purple}[DEBUG]{status.colors.reset} {msg}")
            return 0

    class prompt:
        @staticmethod
        def input(msg:str, exp:str=any) -> Union[any, int]:
            """Print a prompt and return the input.
            args:
                msg:str - The message to print
                exp:str - The expected input type
            """
            return input(f"{status.colors.blue}[PROMPT]{status.colors.reset} {msg}{status.colors.green}")

class jsonParser:
    """Functions related to parsing JSON files."""

    @staticmethod
    def readFile(filePath: str) -> Union[Dict, int]:
        """Read the file."""
        try:
            with open(filePath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {filePath}")
            return 1
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {filePath}")
            return 1

    @staticmethod
    def writeFile(filePath: str, data: Dict) -> int:
        """Write the file."""
        try:
            with open(filePath, "w") as file:
                json.dump(data, file, indent=4)
            return 0
        except Exception as e:
            print(f"Error writing to file: {filePath}")
            return 1

    @staticmethod
    def editKey(data: str, key: str, newValue: str) -> Dict:
        """Edit a key in a JSON file."""
        data[key] = newValue
        return data

    @staticmethod
    def getKey(filePath: str, key: str) -> str:
        """Get a key from a JSON file."""
        data = JsonParser.readFile(filePath)
        return data.get(key)

    @staticmethod
    def deleteKey(filePath: str, key: str) -> Union[Dict, int]:
        """Delete a key from a JSON file."""
        data = JsonParser.readFile(filePath)
        if key in data:
            del data[key]
            return data
        else:
            print(f"Key '{key}' not found in the file.")
            return 1

    @staticmethod
    def addKey(filePath: str, key: str, value: str) -> Dict:
        """Add a key to a JSON file."""
        data = JsonParser.readFile(filePath)
        data[key] = value
        JsonParser.writeFile(filePath, data)
        return data

def config_set_default() -> int:
    """Writes the default config file."""
    default: Dict = {
        "wallpaper": {
            "dir": "/home/$USER/Pictures/Wallpapers", # Directory to search for wallpapers
            "current": "/home/$USER/Pictures/Wallpapers/current", # Current wallpaper
            "ext": ".jpg", # File extension of wallpapers
            "cmd": "swaybg -i", # Command to set the wallpaper
            "auto_change": {
                "toggle": False, # Changes whether or not the wallpaper is changed automatically
                "interval": 300, # The interval of changing the wallpaper
                "list": [], # A list of wallpapers to change to
                "random": True, # Changes whether or not the wallpaper is chosen randomly
            },
            "fzf": {
                "toggle": False, # Changes whether or not fzf is used to select the wallpaper
                "cmd": "fzf", # The command to use to select the wallpaper
            },
            "wofi": {
                "toggle": False, # Changes whether or not wofi is used to select the wallpaper
            },
            "rofi": {
                "toggle": False, # Changes whether or not rofi is used to select the wallpaper
            },
            "dmenu": {
                "toggle": False, # Changes whether or not dmenu is used to select the wallpaper
            },
        },
        "notifications": {
            "toggle": True, # Changes whether or are shown at all
            "interval": 300, # The interval of showing the notification
            "cmd": "notify-send", # The command to show the notification
            "wallpaper_change": True, # Notify when the wallpaper is changed
            "wallpaper_error": True, # Notify when the wallpaper is not found
            "wallpaper_add": True, # Notify when a wallpaper is added
            "wallpaper_remove": True, # Notify when a wallpaper is removed
        },
        "logging": {
            "enable": True, # Changes whether or not logging is enabled
            "file": "/var/log/backdropy.log", # The file to log to
            "level": "info", # The level of logging
        }
    }

    # Writing the config in Json format
    try:
        JsonParser.writeFile(config_path, default)
    except Exception as e:
        print(f"Error writing to file: {config_path}") # Catch all case
        return 1

    return 0

def main() -> int:
    """Main function."""
    return 0

if __name__ == "__main__":
    main()
