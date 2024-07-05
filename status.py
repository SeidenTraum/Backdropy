class Status:
    debug: bool = True

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
        def debug(msg: str) -> int:
            """Print a debug message."""
            if debug:
                print(f"{Status.Colors.PURPLE}[DEBUG]{Status.Colors.RESET} {msg}")
            return 0

    class Prompt:
        @staticmethod
        def input(msg: str) -> str:
            """Print a prompt and return the input."""
            return input(f"{Status.Colors.BLUE}[PROMPT]{Status.Colors.RESET} {msg}{Status.Colors.GREEN}")